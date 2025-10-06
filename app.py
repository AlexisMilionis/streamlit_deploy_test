import streamlit as st
import pandas as pd


# streamlit run app.py

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

pg = st.navigation([st.Page("Utility Bills.py"), st.Page("Property Management.py"), st.Page("Budget & Forecast.py")])
pg.run()






