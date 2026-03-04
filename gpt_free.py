# ==============================
# 고객사 업무 보고서 자동 생성 시스템
# Windows + Outlook + Streamlit + OpenAI
# ==============================

import streamlit as st
import pandas as pd
import win32com.client
import pythoncom
import datetime
import calendar
import json
from openai import OpenAI

# ==============================
# 🔐 OpenAI API KEY 설정
# ==============================

OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)

# ==============================
# 📅 기간 계산 함수
# ==============================
def get_week_range():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())  # 월요일
    end = start + datetime.timedelta(days=6)  # 일요일
    return start, end

def get_month_range():
    today = datetime.date.today()
    start = today.replace(day=1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    end = today.replace(day=last_day)
    return start, end

# ==============================
# 📧 Outlook 메일 수집 함수
# ==============================
def collect_outlook_emails(start_date, end_date, user_email):
    pythoncom.CoInitialize()
    emails_data = []

    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

        # 받은 편지함(6), 보낸 편지함(5)
        folders = [
            outlook.GetDefaultFolder(6),
            outlook.GetDefaultFolder(5)
        ]

        for folder in folders:
            messages = folder.Items
            messages.Sort("[ReceivedTime]", True)

            for msg in messages:
                try:
                    received_time = msg.ReceivedTime.date()
                except:
                    continue

                if start_date <= received_time <= end_date:

                    sender = str(msg.SenderEmailAddress)
                    to = str(msg.To)
                    cc = str(msg.CC)

                    if user_email.lower() in (sender + to + cc).lower():

                        body_text = str(msg.Body)
                        body_text = body_text[:1000]  # 토큰 절약용 1000자 제한

                        emails_data.append({
                            "date": received_time.strftime("%Y-%m-%d"),
                            "subject": str(msg.Subject),
                            "sender": sender,
                            "to": to,
                            "cc": cc,
                            "body": body_text
                        })

        return emails_data

    finally:
        pythoncom.CoUninitialize()

# ==============================
# 🤖 OpenAI 분석 함수
# ==============================
def analyze_with_openai(email_list, worker_name):
    if not email_list:
        return []

    prompt = f"""
아래는 작업자 {worker_name}의 업무 관련 이메일 데이터이다.
이를 분석하여 반드시 JSON 배열 형태로 출력하라.

[출력 JSON 구조]
[
  {{
    "날짜": "2026-03-03, 2026-03-04",
    "고객사명": "고객사명",
    "수행내용": "1. 수행 내용 (03/03)\\n2. 수행 내용 (03/04)",
    "특이사항": "없음"
  }}
]

[분석 및 출력 규칙]
1. 동일 고객사는 반드시 1개의 JSON 객체로만 생성.
2. 날짜는 모두 나열.
3. 수행내용은 능동형으로 작성 (~진행, ~완료, ~요청, ~확인 등).
4. 수행내용 끝에는 반드시 메일 날짜를 (MM/DD) 형태로 기재.
5. 여러 수행내용은 반드시 숫자번호(1.,2.,3.) + \\n 로 구분.
6. 특이사항이 없으면 반드시 '없음'으로 기재.
7. 절대 설명문을 출력하지 말고 JSON만 출력.

이메일 데이터:
{json.dumps(email_list, ensure_ascii=False)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 기업 업무 보고서 자동 작성 전문가이다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    # JSON 안전 파싱
    try:
        return json.loads(content)
    except:
        # 혹시 코드블록 감싸짐 제거
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)

# ==============================
# 🌐 Streamlit UI 구성
# ==============================
st.set_page_config(page_title="고객사 업무 보고 자동 생성기", layout="wide")
st.title("📊 고객사 업무 보고 자동 생성기")

# 1️⃣ 기간 선택
report_type = st.radio("보고 유형 선택", ["주간 보고", "월간 보고"])

if report_type == "주간 보고":
    start_date, end_date = get_week_range()
else:
    start_date, end_date = get_month_range()

st.info(f"📅 보고 기간: {start_date} ~ {end_date}")

# 2️⃣ 작업자 정보 입력
col1, col2 = st.columns(2)
with col1:
    worker_name = st.text_input("작업자 이름")
with col2:
    worker_email = st.text_input("작업자 이메일 주소")

# 3️⃣ 실행 버튼
if st.button("📨 메일 분석 및 보고서 생성"):

    if not worker_name or not worker_email:
        st.warning("작업자 이름과 이메일을 모두 입력하세요.")
        st.stop()

    with st.spinner("Outlook 메일 수집 중..."):
        emails = collect_outlook_emails(start_date, end_date, worker_email)

    if not emails:
        st.warning("해당 기간 내 조건에 맞는 메일이 없습니다.")
        st.stop()

    with st.spinner("AI 분석 중..."):
        result_json = analyze_with_openai(emails, worker_name)

    # DataFrame 변환
    df = pd.DataFrame(result_json)

    if "수행내용" in df.columns:
        df["수행내용"] = df["수행내용"].astype(str).str.replace(r"\\n", "\n", regex=True)

    st.success("✅ 보고서 생성 완료")

    # 🔥 줄바꿈 잘림 방지 출력
    st.table(df)

    # CSV 다운로드
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name=f"업무보고_{start_date}_{end_date}.csv",
        mime="text/csv"
    )