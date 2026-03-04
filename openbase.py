import streamlit as st

# --- 1. 기본 설정 ---
st.set_page_config(
    page_title="오픈베이스 ITO 서비스",
    page_icon="🏢",
    layout="wide"
)

# --- 커스텀 CSS (오픈베이스 코퍼레이트 컬러 및 UI 디자인 반영) ---
st.markdown("""
<style>
    .hero-title {
        color: #0055A5;
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        color: #333333;
        font-size: 1.5rem;
        font-weight: 500;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .section-title {
        color: #0055A5;
        font-size: 2rem;
        font-weight: bold;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #0055A5;
        padding-bottom: 0.5rem;
    }
    .service-card {
        background-color: #F8F9FA;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        height: 100%;
        border-top: 4px solid #0055A5;
    }
    .service-card h3 {
        color: #0055A5;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .service-card p {
        color: #555555;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- Section 1: Hero ---
st.markdown('<div class="hero-title">한 차원 수준 높은 IT Total Outsourcing</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">다년간의 풍부한 경험과 기술력으로 고객의 비즈니스 혁신을 지원하는 오픈베이스 ITO 서비스</div>', unsafe_allow_html=True)
st.write("오픈베이스는 고객의 핵심 업무와 프로세스에 대한 깊은 이해를 바탕으로, 전문가 조직의 효과적인 기술지원 체계를 제공합니다.")
st.divider()

# --- Section 2: Pain Points ---
st.markdown('<div class="section-title">고객사의 IT 운영, 이런 고민이 있으신가요?</div>', unsafe_allow_html=True)

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.info("📉 **운영 비용 증가**\n\nIT 인프라 규모가 커지면서 관리 인력 및 유지보수 비용이 기하급수적으로 늘어나고 있습니다.")
with col_p2:
    st.info("🚨 **보안 및 장애 위험**\n\n복잡해지는 사이버 위협과 예기치 못한 시스템 장애로 인해 비즈니스 연속성 확보가 어렵습니다.")
with col_p3:
    st.info("🧑‍💻 **전문 인력 부재**\n\n신기술(Cloud, AI 등) 도입을 이끌어갈 내부 IT 전문 인력을 채용하고 유지하기가 쉽지 않습니다.")

# --- Section 3: Solutions ---
st.markdown('<div class="section-title">오픈베이스 핵심 ITO 서비스 영역</div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown("""
    <div class="service-card">
        <h3>🖥️ 인프라 운영 관리</h3>
        <p>서버, 스토리지, 네트워크 등 엔터프라이즈 환경의 IT 자산을 안정적으로 유지보수하고 최적의 상태로 관리합니다.</p>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    st.markdown("""
    <div class="service-card">
        <h3>🛡️ 보안 및 컴플라이언스 관리</h3>
        <p>침해사고 예방부터 위협 탐지, 신속 대응까지 고객 환경에 최적화된 맞춤형 보안 관제를 제공합니다.</p>
    </div>
    """, unsafe_allow_html=True)

with col_s3:
    st.markdown("""
    <div class="service-card">
        <h3>☁️ 클라우드 전환 & MSP</h3>
        <p>온프레미스에서 하이브리드·멀티 클라우드로의 유연한 전환 및 체계적인 매니지드 서비스를 지원합니다.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("") # 간격 띄우기
col_s4, col_s5, col_s6 = st.columns(3)
with col_s4:
    st.markdown("""
    <div class="service-card">
        <h3>💾 애플리케이션 및 DB 유지보수</h3>
        <p>비즈니스 핵심 애플리케이션과 데이터베이스의 성능 튜닝 및 무중단 운영을 완벽하게 보장합니다.</p>
    </div>
    """, unsafe_allow_html=True)

with col_s5:
    st.markdown("""
    <div class="service-card">
        <h3>🎧 24/365 통합 관제 & 헬프데스크</h3>
        <p>전문 PM 및 SM 인력이 상주하여 실시간 모니터링을 수행하고, 신속한 이슈 해결을 지원합니다.</p>
    </div>
    """, unsafe_allow_html=True)

with col_s6:
    st.markdown("""
    <div class="service-card">
        <h3>📊 IT 시스템 컨설팅</h3>
        <p>고객의 IT 인프라 구조를 진단하고 비즈니스 Needs에 맞춘 정보시스템 분석 및 설계를 제안합니다.</p>
    </div>
    """, unsafe_allow_html=True)


# --- Section 4: Why Openbase? ---
st.markdown('<div class="section-title">왜 오픈베이스 ITO를 선택해야 할까요?</div>', unsafe_allow_html=True)

with st.expander("🥇 1. 다년간의 풍부한 경험과 축적된 노하우", expanded=True):
    st.write("""
    오픈베이스는 1995년 설립 이래 공공, 금융, 엔터프라이즈 등 다양한 산업군에서 대규모 IT 프로젝트를 성공적으로 수행해왔습니다. 
    이러한 경험을 바탕으로 어떠한 복잡한 IT 환경에서도 가장 안정적이고 효율적인 정보시스템 운영 방안을 제시합니다.
    """)

with st.expander("💡 2. 고객 비즈니스 프로세스에 대한 깊은 이해"):
    st.write("""
    단순한 기술 지원을 넘어 고객사의 핵심 비즈니스 로직과 워크플로우를 분석합니다. 
    비즈니스 목표 달성을 위한 맞춤형 IT 전략을 수립하여 실질적인 비즈니스 가치 창출과 경쟁력 강화에 기여합니다.
    """)

with st.expander("⚙️ 3. 체계적인 ITIL 기반 기술지원 및 SLA 관리"):
    st.write("""
    전문가 조직을 통한 명확하고 표준화된 프로세스(ITIL)를 준수합니다. 
    엄격한 서비스 수준 협약(SLA) 지표를 관리하여 일관성 있는 고품질의 IT 서비스를 365일 무중단으로 보장합니다.
    """)


# --- Section 5: Process ---
st.markdown('<div class="section-title">서비스 도입 및 운영 절차</div>', unsafe_allow_html=True)

st.write("오픈베이스의 ITO 서비스는 체계적이고 투명한 프로세스를 통해 단계별로 완벽하게 지원됩니다.")

# 프로세스를 시각적으로 보여주기 위한 컬럼 구성
col_pr1, col_pr2, col_pr3, col_pr4, col_pr5 = st.columns(5)
with col_pr1:
    st.success("📝 **1. 요구사항 분석**\n\nIT 인프라 현황 진단 및 Needs 파악")
with col_pr2:
    st.success("📐 **2. 서비스 설계**\n\n맞춤형 운영 방안 및 SLA 기준 수립")
with col_pr3:
    st.success("🤝 **3. 계약 및 이관**\n\n운영 프로세스 정립 및 지식 인수인계")
with col_pr4:
    st.success("⚙️ **4. 시스템 운영**\n\n24/365 모니터링, 장애 대응, 정기 점검")
with col_pr5:
    st.success("📈 **5. 최적화 & 보고**\n\nSLA 실적 보고 및 IT 인프라 고도화 제안")


# --- Section 6: Contact Us ---
st.markdown('<div class="section-title">서비스 도입 문의</div>', unsafe_allow_html=True)
st.write("사내 IT 인력 부족이나 운영 비용으로 고민하고 계신다면, 지금 바로 오픈베이스 전문가와 상담하세요.")

with st.form("contact_form"):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        company = st.text_input("회사명 *")
        name = st.text_input("담당자명 *")
    with col_f2:
        contact = st.text_input("연락처 (예: 010-1234-5678) *")
        email = st.text_input("이메일 주소 *")
    
    inquiry_type = st.selectbox(
        "관심 서비스 분야", 
        ["인프라 운영 관리", "보안 및 컴플라이언스", "클라우드 전환 및 MSP", "애플리케이션/DB 유지보수", "통합 관제 및 헬프데스크", "기타"]
    )
    message = st.text_area("문의 내용 (현재 고민이신 IT 운영 이슈를 자유롭게 적어주세요.)")
    
    # 폼 제출 버튼
    submitted = st.form_submit_button("상담 신청하기", use_container_width=True)
    
    if submitted:
        if company and name and contact and email:
            st.success(f"✅ {name}님, 상담 신청이 완료되었습니다! 빠른 시일 내에 오픈베이스 ITO 담당자가 연락드리겠습니다.")
        else:
            st.error("⚠️ 필수 항목(*)을 모두 입력해 주세요.")