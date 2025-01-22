import streamlit as st

st.set_page_config(page_title="ISE315 - Interactive Tutorials", layout="wide")

st.title("Welcome to ISE315 Interactive Tutorials")
st.markdown("### Navigate to different tutorials from the sidebar.")

st.sidebar.title("Navigation")
st.sidebar.page_link("pages/type1_type2_properties.py", label="Type I and II Error Properties")
