import streamlit as st

page_editing = st.Page("pages/page_editing.py", title= "Editing")

pg = st.navigation([
    st.Page("pages/page_main.py", title="Github ReadMe Writer", icon=":material/person:"),
    st.Page("pages/page_editing.py", title= "Editing", icon=":material/edit:")
])

pg.run()

try:
    if st.session_state.switch_page:
        st.session_state.switch_page = False
        st.switch_page(page_editing)

except Exception as e:
    pass


