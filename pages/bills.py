"""
Utility Bills Analysis Page.

This is the main page for utility bills analysis, providing a tabbed interface
for file upload, KPI visualization, and comparative analysis.
"""

import pandas as pd
import streamlit as st  
from io import BytesIO
from pages import bill_tab1
from src.single_file_checks import MonthlyDataChecks 
from src.upload_file_checks import UploadedFileCheck
from src.update_timeseries import TimeSeriesUpdate
from src.update_masterfile import MasterFileUpdate
from src.generate_metrics import Metrics
import pygwalker as pyg
from pages.bill_tab1 import create_tab1
from pages.bill_tab2 import create_tab2
from pages.bill_tab3 import create_tab3

st.header("Utility Bills Analysis")

# Initialize session state for tab completion
if 'tab1_completed' not in st.session_state:
    st.session_state.tab1_completed = False
    
tab1, tab2, tab3 = st.tabs(["File Upload & Checks", "Bill KPIs", "Comparison"])

with tab1:
    create_tab1()
    
with tab2:
    if st.session_state.tab1_completed:
        create_tab2()
    else:
        st.info("⏳ Please complete the file upload in the first tab before accessing KPIs.")
    
with tab3:
    if st.session_state.tab1_completed:
        create_tab3()
    else:
        st.info("⏳ Please complete the file upload in the first tab before accessing comparisons.")

    # st.subheader("Data Quality Checks")


    # # Custom CSS for file uploader
    # st.markdown("""
    # <style>
    #     /* Target the main dropzone section */
    #     [data-testid="stFileUploaderDropzone"] {
    #         background-color: #0a1b38 !important;
    #         border: 2px dashed #cccccc !important;
    #         border-radius: 10px !important;
    #         padding: 20px !important;
    #     }
        
    #     /* Target the dropzone instructions container */
    #     [data-testid="stFileUploaderDropzoneInstructions"] {
    #         background-color: #0a1b38 !important;
    #         color: #262730 !important;
    #     }
        
    #     /* Target the "Drag and drop file here" text */
    #     .st-emotion-cache-zm3qx2 {
    #         color: white !important;
    #         font-weight: 600 !important;
    #     }
        
    #     /* Target the file limit text */
    #     .st-emotion-cache-q4fli {
    #         color: white !important;
    #     }
        
    #     /* Target the upload icon */
    #     .st-emotion-cache-zdnr11 svg {
    #         color: #1f77b4 !important;
    #     }
        
    #     /* Target the Browse files button */
    #     [data-testid="stBaseButton-secondary"] {
    #         background-color: #0db1f2 !important;
    #         color: white !important;
    #         border: none !important;
    #         border-radius: 5px !important;
    #     }
        
    #     /* Hover effects */
    #     [data-testid="stFileUploaderDropzone"]:hover {
    #         border-color: #1f77b4 !important;
    #         background-color: #0a1b38 !important;
    #     }
        
    #     /* Target the tooltip background */
    #     [data-testid="stTooltipContent"] {
    #         background-color: #0a1b38 !important;
    #         border: 0px solid #cccccc !important;
    #         border-radius: 8px !important;
    #         box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    #     }
        
    #     /* Target the tooltip text */
    #     [data-testid="stTooltipContent"] p {
    #         color: white !important;
            
    #     }
    # </style>
    # """, unsafe_allow_html=True)

    # left_col, right_col = st.columns(spec=[0.3, 0.7])
    # # Choose portfolio type
    # portfolio_type = left_col.radio(
    #     "Select portfolio type:",
    #     ('Eurobank', 'Management'),
    #     horizontal=False,
    # )

    # # File uploader
    # uploaded_file = right_col.file_uploader(
    #     "Upload monthly portfolio utilities file", 
    #     type=['xlsx', 'xls'],
    #     # help="Upload monthly Eurobank portfolio utilities file",
    #     width="stretch",
    # )

    # if uploaded_file is not None:
        
    #     # Checks for portfolio excel file
    #     excel_check = UploadedFileCheck(uploaded_file, unique_id=portfolio_type.lower())
    #     df_portfolio = excel_check.exist_multiple_sheets()


    # if uploaded_file is not None and df_portfolio is not None:
        
    #     file_key = f"{uploaded_file.name}_{uploaded_file.size}_{portfolio_type}"
    #     if 'processed_file' not in st.session_state or st.session_state.processed_file != file_key:
            
    #         st.session_state.processed_file = file_key
            
    #         # Portfolio dataframe checks
    #         portfolio_checks = MonthlyDataChecks(df_portfolio, portfolio_name=portfolio_type.lower())
    #         checks_passed = portfolio_checks.single_file_checks_pipeline()
    #         if checks_passed is False:
    #             st.stop()

    #         # Append file to historical database
    #         timeseries = TimeSeriesUpdate(df_portfolio, portfolio_type.lower())
    #         timeseries.add_new_data()
            
    #         # Check for new supply IDs
    #         masterfile = MasterFileUpdate(df_portfolio, portfolio_type)
    #         masterfile.update_masterfile()
            
            # # walker = pyg.walk(df_portfolio)
            
            # st.session_state.df_portfolio = df_portfolio
            
        # # This code runs on every rerun - outside the initialization block
        # st.subheader("KPIs Monthly Bill")
        # monthly_metrics = Metrics(df_portfolio)        
        # monthly_metrics.display_monthly_kpis()
        # monthly_metrics.build_scatterplot()
        
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

        # monthly_supply_id_input = st.text_input(
        #     "Enter Supply ID to retrieve information:",
        #     placeholder="Type supply ID here..."
        # )
        # if monthly_supply_id_input:
        #     monthly_metrics.display_supply_id_info(monthly_supply_id_input)

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

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
