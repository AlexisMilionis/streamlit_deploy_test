"""
CPS Utilities Management App - Main Application Entry Point.

This is the main entry point for the Streamlit-based utilities management application.
It handles session state initialization, authentication, and navigation setup.

To run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from src.authentication import authenticate
from constants import Constants

# Initialize session state
if 'name' not in st.session_state:
    st.session_state['name'] = None
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

st.set_page_config(layout="wide")
st.logo("static/logo-cps-compact-white@4x.png", size="large")

st.markdown("""
    <style>
            /* Remove blank space at top and bottom */ 
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
            }
            
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <h1 style="color: #0db1f2; text-align: center; margin-top: 0;">
        CPS Utilities Management App
    </h1>
    """,
    unsafe_allow_html=True
)

constants = Constants()
if constants.AUTHENTICATION:
    authenticate()
else:
    pg = st.navigation(constants.navigation_menu)
    pg.run()

