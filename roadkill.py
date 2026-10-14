import streamlit as st
import pandas as pd
from ai_helper import ask_ai

# 페이지 설정
st.set_page_config(
    page_title="로드킬 분석",
    page_icon="🦌",
    layout="wide"
)

# 제목
st.title("🦌 속리산 로드킬 분석 앱")
st.markdown("---")

# CSV 파일 로드
@st.cache_data
def load_roadkill_data():
    try:
        df = pd.read_csv("roadkill.csv", encoding="cp949")
    except Exception as e:
        st.error(f"CSV 파일 로드 오류: {e}")
        return pd.DataFrame()
    return df

# 데이터 로드
df = load_roadkill_data()

# 사이드바에서 동물이름 입력
with st.sidebar:
    st.header("🔍 검색")

    # 동물 목록 (CSV의 자원명 컬럼)
    animal_list = sorted(df["자원명"].unique().tolist())

    selected_animal = st.selectbox(
        "동물을 선택하세요",
        ["전체"] + animal_list,
        help="로드킬에 당한 동물을 선택하면 해당 데이터를 조회합니다"
    )

# 메인 영역
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"📊 {selected_animal} 로드킬 데이터")

    # 데이터 필터링
    if selected_animal == "전체":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["자원명"] == selected_animal]

    # 결과 표시
    if len(filtered_df) > 0:
        st.metric("발견된 데이터 수", len(filtered_df))

        # 데이터 테이블 표시
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        # 통계 정보
        st.subheader("📈 통계")
        stat_col1, stat_col2, stat_col3 = st.columns(3)

        with stat_col1:
            st.metric("발견 위치 수", filtered_df["위치명"].nunique())

        with stat_col2:
            st.metric("조사 기간", f"{filtered_df['조사일자'].min()} ~ {filtered_df['조사일자'].max()}")

        with stat_col3:
            st.metric("로드킬 구간", filtered_df["로드킬구간명"].nunique())
    else:
        st.warning("해당 동물의 데이터가 없습니다.")

with col2:
    st.subheader("ℹ️ 정보")
    if selected_animal != "전체" and len(filtered_df) > 0:
        # Claude API를 사용해 동물 정보 조회
        if st.button("AI 정보 조회", key="ai_button"):
            with st.spinner(f"{selected_animal}에 대해 알아보는 중..."):
                prompt = f"{selected_animal}는 어떤 동물입니까? 한 문단 정도로 간단히 설명해주세요."
                response = ask_ai(prompt)
                st.info(response)

# 푸터
st.markdown("---")
st.markdown("💡 팁: 왼쪽 사이드바에서 동물을 선택하여 로드킬 데이터를 조회할 수 있습니다.")
