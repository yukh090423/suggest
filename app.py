import streamlit as st

# 페이지 제목
st.set_page_config(page_title="한 줄 건의함", page_icon="📮")
st.title("📮 익명 한 줄 건의함")
st.write("자유롭게 의견을 남겨주세요. (이름은 수집하지 않습니다.)")

# 세션 상태(session_state)에 건의사항 리스트 초기화
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []

# 입력 폼 (제출 시 입력창 자동 초기화)
with st.form("suggestion_form", clear_on_submit=True):
    user_input = st.text_input("건의 내용", placeholder="여기에 건의할 내용을 적어주세요.", label_visibility="collapsed")
    submitted = st.form_submit_button("제출")
    
    if submitted:
        if user_input.strip() == "":
            # 빈 내용 제출 방지
            st.warning("건의 내용을 입력해 주세요.")
        else:
            # 최신순으로 보여주기 위해 리스트의 맨 앞(index 0)에 추가
            st.session_state.suggestions.insert(0, user_input.strip())
            st.success("건의가 성공적으로 제출되었습니다!")

st.divider()

# 제출된 건의 목록 출력
st.subheader("📝 최근 접수된 건의")

if len(st.session_state.suggestions) == 0:
    st.info("아직 접수된 건의가 없습니다.")
else:
    # 최신순으로 추가되었으므로 그대로 순회하여 출력
    for suggestion in st.session_state.suggestions:
        st.markdown(f"- {suggestion}")