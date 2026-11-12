import streamlit as st
import os
from supabase import create_client, Client

# 1. Supabase 연결 설정 (환경 변수에서 불러오기)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_connection()

# 페이지 설정
st.set_page_config(page_title="한 줄 건의함", page_icon="📮")
st.title("📮 익명 한 줄 건의함")
st.write("자유롭게 의견을 남겨주세요. (이름은 수집하지 않습니다.)")

# 2. 입력 폼
with st.form("suggestion_form", clear_on_submit=True):
    user_input = st.text_input("건의 내용", placeholder="여기에 건의할 내용을 적어주세요.", label_visibility="collapsed")
    submitted = st.form_submit_button("제출")
    
    if submitted:
        if user_input.strip() == "":
            st.warning("건의 내용을 입력해 주세요.")
        else:
            # Supabase suggestions 테이블에 데이터 삽입
            # id와 created_at은 DB에서 자동 생성되도록 설정되어 있다고 가정합니다.
            # category와 likes는 기본값을 사용하거나 비워둡니다.
            data = {"content": user_input.strip()}
            supabase.table("suggestions").insert(data).execute()
            st.success("건의가 성공적으로 제출되었습니다!")

st.divider()

# 3. DB에서 데이터 불러오기 및 출력
st.subheader("📝 최근 접수된 건의")

# 최신순(created_at 내림차순)으로 데이터 조회
response = supabase.table("suggestions").select("*").order("created_at", desc=True).execute()
suggestions = response.data

if not suggestions:
    st.info("아직 접수된 건의가 없습니다.")
else:
    for item in suggestions:
        st.markdown(f"- {item['content']}")