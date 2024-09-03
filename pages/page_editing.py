import streamlit as st
from app import llm_response_generator

container = st.container(border= True)
memory = []

try:
    generated_content = st.session_state.generated_content
    switched = st.session_state.switch_page
    memory.append(generated_content)
except Exception as e:
    generated_content = e
    st.session_state.switch_page = False

if st.session_state.switch_page and not st.session_state.switched_page:
    container.write(generated_content)
    st.session_state.switched_page = True

with st.sidebar:
    messages = st.container(height=100)
    if prompt := st.chat_input("User Prompt"):
        messages.chat_message("user").write(prompt)

        try:
            generated_content = llm_response_generator.editor_agent_response(st.session_state.generated_content, prompt,
                                                                             memory, st.session_state.llm)
            st.session_state.generated_content = generated_content
            container.write(st.session_state.generated_content)
            memory.append(generated_content)
        except Exception as e:
            container.warning(f"Sorry an error occured, refresh page")

    container_structure = st.container(border= True)
    container_structure.title(f"File Structure\n")
    try:
        container_structure.text(st.session_state.structure)
    except Exception as e:
        pass

if len(memory) > 3:
    memory = memory[1:]
