import streamlit as st

with open("mask_editor.html", "r") as f:
    html_code = f.read()

st.components.v1.html(html_code, height=600, scrolling=True)
