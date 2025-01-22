import streamlit as st

st.set_page_config(page_title="ISE-315 Tutorials", layout="wide")

st.title("Welcome to ISE-315 Interactive Tutorials")
st.markdown("""
### Available Tutorials
- Navigate to the tutorials using the sidebar.
""")

st.sidebar.title("Navigation")
st.sidebar.info("Use the sidebar to navigate through different tutorials.")
