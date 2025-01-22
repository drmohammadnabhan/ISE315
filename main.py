import streamlit as st
from apps import type1_type2_properties

# Dictionary of available apps
apps = {
    "Type I and II Properties": type1_type2_properties
}

st.sidebar.title("ISE315 - Interactive Tutorials")
choice = st.sidebar.radio("Select a tutorial", list(apps.keys()))

# Run selected app
apps[choice].run()
