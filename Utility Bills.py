import pandas as pd
import streamlit as st  
from io import BytesIO

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

# File uploader
uploaded_file = st.file_uploader(
    "Upload an Excel file", 
    type=['xlsx', 'xls'],
    help="Upload your utility bills Excel file",
    width=1000,
)

if uploaded_file is not None:
    try:
        # Read Excel file and get sheet names
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        
        if len(sheet_names) > 1:
            # Let user select sheet if multiple sheets exist
            selected_sheet = st.selectbox("Select a sheet:", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("File Size", f"{uploaded_file.size} bytes")
        
        # Display DataFrame
        st.write("**Data Preview:**")
        st.dataframe(df, use_container_width=True)
        
        df['ΝΕΑ ΣΤΗΛΗ'] = "ΤΕΣΤ"
        
        # Convert DataFrame to Excel bytes
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)

        # Download button
        st.download_button(
            label="Download Modified Excel File",
            data=excel_buffer.getvalue(),
            file_name=f"modified_{uploaded_file.name}",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        
