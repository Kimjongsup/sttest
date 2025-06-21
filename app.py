import streamlit as st
from openai import OpenAI

# 비밀번호 확인 함수
def check_password():
    def password_entered():
        if st.session_state["password_input"] == st.secrets["app_password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("비밀번호를 입력하세요:", type="password", on_change=password_entered, key="password_input")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("비밀번호를 다시 입력하세요:", type="password", on_change=password_entered, key="password_input")
        st.error("비밀번호가 틀렸어요.")
        return False
    else:
        return True

# 비밀번호가 올바를 때만 앱 실행
if check_password():
    st.title("넌 내꺼야!")

    client = OpenAI()

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4.1"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
