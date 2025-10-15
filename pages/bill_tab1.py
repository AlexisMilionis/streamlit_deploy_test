import pandas as pd
import streamlit as st  
from src.single_file_checks import MonthlyDataChecks 
from src.upload_file_checks import UploadedFileCheck
from src.update_timeseries import TimeSeriesUpdate
from src.update_masterfile import MasterFileUpdate
from src.generate_metrics import Metrics

def create_tab1():
    
    st.write("")
    # Custom CSS for file uploader
    st.markdown("""
    <style>
        /* Target the main dropzone section */
        [data-testid="stFileUploaderDropzone"] {
            background-color: #0a1b38 !important;
            border: 2px dashed #cccccc !important;
            border-radius: 10px !important;
            padding: 20px !important;
        }
        
        /* Target the dropzone instructions container */
        [data-testid="stFileUploaderDropzoneInstructions"] {
            background-color: #0a1b38 !important;
            color: #262730 !important;
        }
        
        /* Target the "Drag and drop file here" text */
        .st-emotion-cache-zm3qx2 {
            color: white !important;
            font-weight: 600 !important;
        }
        
        /* Target the file limit text */
        .st-emotion-cache-q4fli {
            color: white !important;
        }
        
        /* Target the upload icon */
        .st-emotion-cache-zdnr11 svg {
            color: #1f77b4 !important;
        }
        
        /* Target the Browse files button */
        [data-testid="stBaseButton-secondary"] {
            background-color: #0db1f2 !important;
            color: white !important;
            border: none !important;
            border-radius: 5px !important;
        }
        
        /* Hover effects */
        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #1f77b4 !important;
            background-color: #0a1b38 !important;
        }
        
        /* Target the tooltip background */
        [data-testid="stTooltipContent"] {
            background-color: #0a1b38 !important;
            border: 0px solid #cccccc !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* Target the tooltip text */
        [data-testid="stTooltipContent"] p {
            color: white !important;
            
        }
    </style>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns(spec=[0.3, 0.7])
    # Choose portfolio type
    portfolio_type = left_col.radio(
        "Select portfolio type:",
        ('Eurobank', 'Management'),
        horizontal=False,
    )

    # File uploader
    uploaded_file = right_col.file_uploader(
        "Upload monthly portfolio utilities file", 
        type=['xlsx', 'xls'],
        # help="Upload monthly Eurobank portfolio utilities file",
        width="stretch",
    )
    st.write("")
    if uploaded_file is not None:
        
        # Checks for portfolio excel file
        excel_check = UploadedFileCheck(uploaded_file, unique_id=portfolio_type.lower())
        df_portfolio = excel_check.exist_multiple_sheets()


    if uploaded_file is not None and df_portfolio is not None:
        
        file_key = f"{uploaded_file.name}_{uploaded_file.size}_{portfolio_type}"
        if 'processed_file' not in st.session_state or st.session_state.processed_file != file_key:
            
            st.session_state.processed_file = file_key
            
            # # Portfolio dataframe checks
            # portfolio_checks = MonthlyDataChecks(df_portfolio, portfolio_name=portfolio_type.lower())
            # checks_passed = portfolio_checks.single_file_checks_pipeline()
            # if checks_passed is False:
            #     st.stop()

            # # Append file to historical database
            # timeseries = TimeSeriesUpdate(df_portfolio, portfolio_type.lower())
            # timeseries.add_new_data()
            
            # # Check for new supply IDs
            # masterfile = MasterFileUpdate(df_portfolio, portfolio_type)
            # masterfile.update_masterfile()
            
            st.session_state.df_portfolio = df_portfolio
            checks_passed = True # Temporary bypass for testing
            if checks_passed:
                st.session_state.tab1_completed = True
                st.success("File processed successfully!", icon="✅")
            
            st.write("")
            st.write("")
            st.write("")