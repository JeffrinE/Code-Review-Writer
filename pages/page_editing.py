import streamlit as st

container = st.container(border= True)

container.write(st.session_state.generated_content)

with st.sidebar:
    messages = st.container(height=300)
    if prompt := st.chat_input("Say something"):
        messages.chat_message("user").write(prompt)