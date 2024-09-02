import os
import shutil
import run
import wx
import streamlit as st
from pages import page_editing
from app import code_to_text, llm_response_generator, local_models, setModel

st.title("Github ReadMe Writer")

if os.path.exists("output"):
    shutil.rmtree("output")

def get_folder_path():
    app = wx.App(False)
    folder_path = wx.DirDialog(None, "Select a folder:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if folder_path.ShowModal() == wx.ID_OK:
        return folder_path.GetPath()
    return None

#sidebar
sidebar = st.sidebar
sidebar.header('This program assumes you have Ollama running')

if 'disabled_main_button' not in st.session_state:
    st.session_state.disabled_main_button = False
if 'main_folder_path' not in st.session_state:
    st.session_state.main_folder_path = None

container_models = sidebar.container(border= True)
if 'llm' not in st.session_state:
    st.session_state.llm = ""
if 'model' not in st.session_state:
    st.session_state.model = False

option = container_models.selectbox(
    "Model",
    local_models.get_local_models(),
    index=None,
    placeholder="Select model",
    key= "model_selectable"
)

st.session_state.model = option

if st.session_state.model:
    llm = setModel.llm(st.session_state.model)
    st.session_state.llm = llm.set_llm()

def click_main():
    st.session_state.disabled_main_button = True


container_browse_main = sidebar.container(border=True)
container_browse_main.write("Project Folder")

if container_browse_main.button("Upload", key="main_folder", on_click=click_main,
                             disabled=st.session_state.disabled_main_button):
    path = get_folder_path()
    st.session_state.main_folder_path = path

if st.session_state.disabled_main_button:
    container_browse_main.markdown(f":material/folder: {os.path.basename(st.session_state.main_folder_path)}")

#Container Excluded Files

if 'excluded_files' not in st.session_state:
    st.session_state.excluded_files = []
if 'exclusion_bt_clicked' not in st.session_state:
    st.session_state.exclusion_bt_clicked = False

def click_exclusion():
    st.session_state.exclusion_bt_clicked = True

container_browse_excluded = sidebar.container(border= True)
container_browse_excluded.write("Excluded Folders")

if container_browse_excluded.button("Upload", key="excluded_folder", on_click= click_exclusion):
    path = get_folder_path()
    st.session_state.excluded_files.append(path)

file_written = ""

if st.session_state.exclusion_bt_clicked:
    for files in st.session_state.excluded_files:
        file_written += f":material/folder: {os.path.basename(files)}\n\n"

    container_browse_excluded.markdown(file_written)

# Multi Select

options = st.multiselect(
    "Select Subheaders in sequence: ",
    ["Introduction", "Project Description", "Table of Contents", "Installation", "Usage", "Contribution", "License", "Technologies Used", "Requirements", "Support and Contact information", "Acknowledgements"],
    key= "multiselect"
)

sequence_list = [i for i in options]

#generate

if 'generated_content' not in st.session_state:
    st.session_state.generated_content = False

if 'generate_clicked' not in st.session_state:
    st.session_state.generate_clicked = False
def clicked_generate():
    st.session_state.generate_clicked = True


st.button("Generate", key="generate", on_click= clicked_generate)

container_response = st.container(border= True)

if "structure" not in st.session_state:
    st.session_state.structure = ""

if st.session_state.generate_clicked and not st.session_state.generated_content:
    code_to_text_database = code_to_text.codeToText.codeToTextRun(st.session_state.main_folder_path, st.session_state.excluded_files)
    llm_response_generator.set_llm(option)
    st.session_state.structure = code_to_text_database
    response = llm_response_generator.main(sequence_list)
    st.session_state.generated_content = response
    container_response.write(response)

# Switch Page
if 'switch_page' not in st.session_state:
    st.session_state.switch_page = False

def switch_page():
    st.session_state.switch_page = True
    st.session_state.switched_page = False


if st.session_state.generate_clicked:
    st.button("Edit", key="Edit", on_click= switch_page)

