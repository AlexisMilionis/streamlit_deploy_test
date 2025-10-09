import pandas as pd
import streamlit as st  
from io import BytesIO
from src.single_file_checks import MonthlyDataChecks 
from src.upload_file_checks import UploadedFileCheck

st.header("Utility Bills Analysis", divider="grey")

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


# File uploader for Eurobank
left_col, right_col = st.columns(2)
uploaded_file_eurobank = left_col.file_uploader(
    "Upload monthly Eurobank portfolio utilities file", 
    type=['xlsx', 'xls'],
    # help="Upload monthly Eurobank portfolio utilities file",
    width=600,
)

# Checks for Eurobank excel file
if uploaded_file_eurobank is not None:
    with left_col:
        excel_check = UploadedFileCheck(uploaded_file_eurobank, unique_id="eurobank")
        df_eurobank = excel_check.exist_multiple_sheets()
        # excel_check.display_uploaded_file_info()

# File uploader for Management
uploaded_file_management = right_col.file_uploader(
    "Upload monthly management portfolio utilities file", 
    type=['xlsx', 'xls'],
    # help="Upload monthly management portfolio utilities file",
    width=600,
)

# Checks for Management excel file
if uploaded_file_management is not None:
    with right_col:
        excel_check = UploadedFileCheck(uploaded_file_management, unique_id="management")
        df_management = excel_check.exist_multiple_sheets()
        # excel_check.display_uploaded_file_info()

# Eurobank dataframe checks
if uploaded_file_eurobank is not None and df_eurobank is not None:
    
    with left_col:
        eurobank_portfolio_checks = MonthlyDataChecks(df_eurobank, portfolio_name="Eurobank")
        eurobank_portfolio_checks.single_file_checks_pipeline()   
        st.success("Eurobank Portfolio validated successfully!")

if uploaded_file_management is not None and df_management is not None:
    # Management dataframe checks
    with right_col:
        management_portfolio_checks = MonthlyDataChecks(df_management, portfolio_name="Management")
        management_portfolio_checks.single_file_checks_pipeline()
        st.success("Management Portfolio validated successfully!")

        
    # cf = ComparativeFile(current_portfolio=eurobank_portfolio_checks.portfolio, 
    #                      previous_portfolio=management_portfolio_checks.portfolio)
    
    
    

st.write("")
st.write("")
st.write("")