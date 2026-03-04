import streamlit as st
import win32com.client
import pythoncom
import pandas as pd
from openai import OpenAI
from datetime import datetime, timedelta
import calendar
import json

# ==========================================
# [설정] OpenAI API 키 입력
# ==========================================
OPENAI_API_KEY = "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"


# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

# ==========================================
# 1. 날짜 계산 함수
# ==========================================
def get_date_range(report_type):
    today = datetime.now()
    if report_type == "주간 보고":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    else:
        start_date = datetime(today.year, today.month, 1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end_date = datetime(today.year, today.month, last_day)
    
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start_date, end_date

# ==========================================
# 2. Outlook 메일 추출 함수
# ==========================================
def fetch_outlook_emails(start_date, end_date, target_email):
    pythoncom.CoInitialize()
    extracted_emails = []
    
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        folders = [outlook.GetDefaultFolder(6), outlook.GetDefaultFolder(5)]
        
        for folder in folders:
            items = folder.Items
            items.Sort("[ReceivedTime]", True)
            
            for item in items:
                try:
                    if item.Class != 43:
                        continue
                    
                    dt = item.ReceivedTime
                    mail_date = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
                    
                    if mail_date < start_date:
                        break
                    
                    if start_date <= mail_date <= end_date:
                        sender = item.SenderEmailAddress if hasattr(item, 'SenderEmailAddress') else ""
                        to_addr = item.To if hasattr(item, 'To') else ""
                        cc_addr = item.CC if hasattr(item, 'CC') else ""
                        
                        target_lower = target_email.lower()
                        if (target_lower in sender.lower() or 
                            target_lower in to_addr.lower() or 
                            target_lower in cc_addr.lower()):
                            
                            extracted_emails.append({
                                "Date": mail_date.strftime("%Y-%m-%d"),
                                "ShortDate": mail_date.strftime("%m/%d"), # AI가 괄호 안에 넣기 쉽도록 추가
                                "Subject": item.Subject,
                                "Body": item.Body[:1000] # 토큰 절약을 위해 1000자로 조정
                            })
                except Exception:
                    continue
    finally:
        pythoncom.CoUninitialize()
        
    return extracted_emails

# ==========================================
# 3. OpenAI 요약 분석 함수 (수정됨)
# ==========================================
def analyze_emails_with_ai(emails_data):
    if not emails_data:
        return []

    prompt = f"""
    당신은 업무 보고서를 전문적으로 작성하는 AI 어시스턴트입니다.
    아래 제공된 이메일 데이터를 분석하여 다음 규칙에 따라 고객사별 업무 보고서 데이터를 JSON 형식으로 생성하세요.
    
    [분석 및 출력 규칙]
    1. 동일한 '고객사'의 메일은 하나로 묶어(Grouping) **고객사 1곳당 1개의 행(Row)**만 생성할 것.
    2. '날짜'는 해당 고객사와 업무를 진행한 날짜들을 모두 표기 (예: 2026-03-02, 2026-03-04).
    3. '수행내용'은 다음 규칙을 엄격히 따를 것:
       - 단순 메일 제목이나 안내 문구가 아닌, **작업자가 직접 수행한 업무 내역**으로 능동형으로 변환 (예: ~안내 -> ~진행, ~완료, ~요청, ~확인 등).
       - 각 수행내용의 맨 끝에는 해당 메일의 날짜를 괄호로 추가할 것 (예: `(03/04)`).
       - 한 고객사에 여러 수행내용이 있다면 번호를 붙여 줄바꿈(\\n)으로 구분할 것.
       - <예시 변환> "기술자 특급 교육의 취소 및 재신청 안내" -> "기술자 특급 교육의 취소 및 재신청 진행. (03/04)"
    4. '특이사항'은 특별한 이슈가 없다면 무조건 '없음'으로 표기.
    
    [출력 JSON 포맷 예시]
    {{
      "reports": [
        {{
          "날짜": "2026-03-04",
          "고객사명": "ICT폴리텍대학",
          "수행내용": "1. 기술자 특급 교육의 취소 및 재신청 진행. (03/04)\\n2. 교육비 환불 계좌 정보 전달 완료. (03/04)",
          "특이사항": "없음"
        }}
      ]
    }}

    [이메일 데이터]
    {json.dumps(emails_data, ensure_ascii=False)}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs strictly in JSON format matching the provided example."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        result_text = response.choices[0].message.content
        parsed_json = json.loads(result_text)
        
        # 'reports' 키로 배열을 가져오거나, 없으면 값들 중 리스트를 찾음
        if "reports" in parsed_json:
            return parsed_json["reports"]
        else:
            for val in parsed_json.values():
                if isinstance(val, list):
                    return val
            return [parsed_json]

    except Exception as e:
        st.error(f"AI 분석 중 오류가 발생했습니다: {e}")
        return []

# ==========================================
# 4. Streamlit UI 구성
# ==========================================
st.set_page_config(page_title="고객사 업무 보고서 자동 생성기", layout="wide")

st.title("✉️ 고객사 업무 보고서 자동 생성기")
st.markdown("로컬 Outlook 메일을 분석하여 주간/월간 고객사 업무 보고서를 자동으로 작성합니다.")

with st.form("report_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.radio("보고서 유형 선택", ["주간 보고", "월간 보고"])
    
    with col2:
        worker_name = st.text_input("작업자 이름", placeholder="예: 홍길동")
        worker_email = st.text_input("필터링할 이메일 주소 (송/수신자 기준)", placeholder="예: user@company.com")
        
    submit_button = st.form_submit_button("보고서 생성 시작")

if submit_button:
    if not OPENAI_API_KEY.startswith("sk-"):
        st.warning("코드 상단에 올바른 OpenAI API 키를 입력해주세요.")
    elif not worker_name or not worker_email:
        st.warning("작업자 이름과 이메일 주소를 모두 입력해주세요.")
    else:
        start_dt, end_dt = get_date_range(report_type)
        st.info(f"📅 검색 기간: {start_dt.strftime('%Y-%m-%d')} ~ {end_dt.strftime('%Y-%m-%d')}")
        
        with st.spinner("Outlook 메일 수집 중..."):
            emails = fetch_outlook_emails(start_dt, end_dt, worker_email)
            
        if not emails:
            st.warning("해당 기간 내에 조건에 맞는 메일이 없습니다.")
        else:
            st.success(f"총 {len(emails)}건의 관련 메일 발견! AI 분석(고객사별 그룹화)을 시작합니다...")
            
            with st.spinner("AI가 업무 내역을 정리하고 있습니다..."):
                report_data = analyze_emails_with_ai(emails)
                
            if report_data:
                df = pd.DataFrame(report_data)
                
                expected_cols = ["날짜", "고객사명", "수행내용", "특이사항"]
                for col in expected_cols:
                    if col not in df.columns:
                        df[col] = "데이터 없음"
                df = df[expected_cols]
                
                # [핵심 수정 1] AI가 텍스트로 보낸 이스케이프 문자(\\n)를 실제 줄바꿈(\n)으로 확실하게 변환
                df["수행내용"] = df["수행내용"].astype(str).str.replace(r"\\n", "\n", regex=True)
                
                st.subheader(f"📊 {worker_name}님의 {report_type} 결과")
                
                # [핵심 수정 2] st.dataframe 대신 st.table 사용
                # st.table은 HTML 표 형태로 렌더링되어 줄바꿈과 행 높이 자동 조절이 완벽하게 지원됩니다.
                st.table(df)
                
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 CSV 파일로 다운로드",
                    data=csv,
                    file_name=f"{worker_name}_{report_type}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                )