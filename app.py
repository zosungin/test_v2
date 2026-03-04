import streamlit as st
import win32com.client
import pandas as pd
from datetime import datetime, timedelta
import google.generativeai as genai
import pythoncom

# ============================================================
# 설정 (Config) 블록
GEMINI_API_KEY = "AIzaSyA60k0EOXZ9XZBEOwXSXiikjrKQj8PFRWg"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models" 
GEMINI_MODEL = "gemini-2.5-flash"
# --- [1] AI 설정 ---
genai.configure(api_key=GEMINI_API_KEY)
# SDK가 API URL을 자동으로 매핑하므로 모델명 변수만 전달하면 됩니다.
model = genai.GenerativeModel(GEMINI_MODEL)

# --- [2] Outlook 검색 함수 ---
def search_outlook_emails(sender_keyword, start_date, end_date):
    pythoncom.CoInitialize()  
    
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6) 
        messages = inbox.Items
        
        messages.Sort("[ReceivedTime]", True)
        
        email_data = []
        
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())

        for msg in messages:
            try:
                msg_date = msg.ReceivedTime.replace(tzinfo=None)
                
                if start_dt <= msg_date <= end_dt:
                    if sender_keyword.lower() in msg.SenderName.lower() or sender_keyword.lower() in msg.Subject.lower():
                        email_data.append({
                            "날짜": msg_date.strftime("%Y-%m-%d %H:%M"),
                            "발송자": msg.SenderName,
                            "제목": msg.Subject,
                            "본문": msg.Body[:1000] 
                        })
                
                elif msg_date < start_dt:
                    break
            except Exception:
                continue
                
        return pd.DataFrame(email_data)
    finally:
        pythoncom.CoUninitialize()  

# --- [3] AI 분석 함수 ---
def analyze_emails_with_ai(email_df):
    if email_df.empty:
        return "검색된 메일이 없습니다."
    
    combined_text = ""
    for idx, row in email_df.iterrows():
        combined_text += f"[{row['날짜']}] {row['발송자']} - {row['제목']}\n내용: {row['본문']}\n\n"
    
    prompt = f"""
    아래는 고객사와의 이메일 수발신 내역입니다. 
    이 내용을 바탕으로 다음 3가지 항목으로 나누어 가독성 좋게 분석해 주세요.
    
    1. 주제별 요약 (이메일들의 핵심 주제를 1~2줄로 요약)
    2. 요청사항 (고객이 구체적으로 요구한 액션 아이템 리스트)
    3. 진행내역 (현재까지 어떻게 일이 진행되었는지 흐름 요약)
    
    이메일 데이터:
    {combined_text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 분석 중 오류가 발생했습니다.\n(에러 내용: {str(e)})"

# --- [4] Streamlit 웹 UI 구성 ---
st.set_page_config(page_title="고객사 메일 AI 요약기", layout="wide")
st.title("📧 Outlook 고객사 메일 AI 요약 대시보드")
st.markdown("로컬 Outlook과 연동하여 특정 고객사의 메일을 모아보고, AI가 핵심 내용을 요약합니다.")

with st.sidebar:
    st.header("검색 조건 설정")
    sender_input = st.text_input("고객사명 또는 발송자명", placeholder="예: 구글, 홍길동")
    
    today = datetime.today()
    default_start = today - timedelta(days=7)
    date_range = st.date_input("검색 기간", value=(default_start, today))
    
    search_button = st.button("메일 검색 및 AI 분석 시작", type="primary")

if search_button:
    if not sender_input:
        st.warning("고객사명이나 발송자명을 입력해 주세요.")
    elif len(date_range) != 2:
        st.warning("시작일과 종료일을 모두 선택해 주세요.")
    else:
        with st.spinner(f"Outlook 메일을 검색하고 {GEMINI_MODEL} 모델이 분석 중입니다..."):
            start_date, end_date = date_range
            
            df_emails = search_outlook_emails(sender_input, start_date, end_date)
            
            if df_emails.empty:
                st.info("해당 조건에 맞는 메일이 없습니다. 날짜나 키워드를 변경해 보세요.")
            else:
                ai_result = analyze_emails_with_ai(df_emails)
                
                st.subheader(f"💡 '{sender_input}' 관련 AI 분석 결과")
                st.info(f"총 {len(df_emails)}건의 메일을 기반으로 작성되었습니다.")
                st.markdown(ai_result)
                
                st.divider()
                
                st.subheader("📁 원본 메일 리스트")
                st.dataframe(df_emails[['날짜', '발송자', '제목']], use_container_width=True)
                
                with st.expander("상세 메일 본문 확인하기"):
                    for idx, row in df_emails.iterrows():
                        st.markdown(f"**[{row['날짜']}] {row['제목']}** (발송: {row['발송자']})")
                        st.text(row['본문'][:500] + "...(생략)")
                        st.divider()