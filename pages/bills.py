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
# Checks for portfolio excel file
if uploaded_file is not None:
    excel_check = UploadedFileCheck(uploaded_file, unique_id=portfolio_type.lower())
    df_portfolio = excel_check.exist_multiple_sheets()

# Portfolio dataframe checks
if uploaded_file is not None and df_portfolio is not None:
    portfolio_checks = MonthlyDataChecks(df_portfolio, portfolio_name=portfolio_type.lower())
    portfolio_checks.single_file_checks_pipeline()

        

    

st.write("")
st.write("")
st.write("")
