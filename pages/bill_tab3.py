import streamlit as st
import pandas as pd
from src.generate_metrics import Metrics

def create_tab3():
    st.write("Placeholder for Comparison Tab")
    
    
    
    # st.subheader("KPIs Historical Data")
    # eurobank_historical_db = pd.read_excel("data/eurobank_historical_db.xlsx")
    # historical_metrics = Metrics(eurobank_historical_db)
    # historical_metrics.display_historical_kpis()
    # st.markdown("""
    #     <style>
    #             /* Style for input fields (username and password) */
    #             .stTextInput > div > div > input {
    #                 background-color: #f0f8ff !important;
    #                 border: 2px solid #0db1f2 !important;
    #                 border-radius: 5px !important;
    #                 color: #333 !important;
    #             }
                
    #             /* Style for input fields on focus */
    #             .stTextInput > div > div > input:focus {
    #                 background-color: #e6f3ff !important;
    #                 border-color: #0880bf !important;
    #                 box-shadow: 0 0 5px rgba(13, 177, 242, 0.3) !important;
    #             }
                
    #             /* Style for password input specifically if needed */
    #             input[type="password"] {
    #                 background-color: #f0f8ff !important;
    #                 border: 2px solid #0db1f2 !important;
    #                 border-radius: 5px !important;
    #                 color: #333 !important;
    #             }

    #             [data-testid="stBaseButton-secondary"] {
    #                 background-color: #0db1f2 !important;
    #                 color: white !important;
    #                 border: none !important;
    #                 border-radius: 5px !important;
    #     }

    #     </style>
    #     """, unsafe_allow_html=True)
    # supply_id_input = st.text_input(
    #     "Enter Supply ID to retrieve historical information:",
    #     placeholder="Type supply ID here..."
    # )
    # if supply_id_input:
    #     historical_metrics.display_historical_supply_id_info(supply_id_input)