import pandas as pd
import streamlit as st
from typing import Optional

class UploadedFileCheck:
    """
    A utility class for handling uploaded file operations and validations.
    
    This class provides methods to check and process uploaded files, particularly
    Excel files with multiple sheets, allowing users to select specific sheets
    when needed.
    
    Attributes:
        uploaded_file: The uploaded file object to be processed.
        unique_id: A unique identifier for the instance.
        excel_file: The pandas ExcelFile object.
        sheet_names: List of sheet names in the Excel file.
        df: The loaded DataFrame.
    """
    
    def __init__(self, uploaded_file, unique_id: str = "") -> None:
        """
        Initialize the UploadedFileCheck instance.
        
        Args:
            uploaded_file: The uploaded file object (typically from Streamlit file uploader).
            unique_id: A unique identifier for the instance.
        """
        with st.status("Loading file..."):
            self.uploaded_file = uploaded_file
            self.unique_id = unique_id
            self.excel_file = pd.ExcelFile(self.uploaded_file)
            self.sheet_names = self.excel_file.sheet_names
            self.df = pd.DataFrame()
        
    def exist_multiple_sheets(self) -> Optional[pd.DataFrame]:
        """
        Check if the Excel file contains multiple sheets and handle sheet selection.
        
        If the uploaded Excel file contains multiple sheets, presents a selectbox
        to the user for sheet selection. If only one sheet exists, automatically 
        loads that sheet.
        
        Returns:
            Optional[pd.DataFrame]: A pandas DataFrame containing the data from the 
                                   selected or single sheet. Returns None if multiple 
                                   sheets exist but no sheet has been selected yet.
        
        Raises:
            Exception: If the file cannot be read as an Excel file or if there
                      are issues with sheet access.
        """
        try:
            
            # if len(self.sheet_names) > 1:
            #     # Let user select sheet if multiple sheets exist
            #     options = ["-- Select a sheet --"] + self.sheet_names
                
            #     # Apply custom CSS styling for dark theme selectbox
            #     st.markdown("""
            #                 <style>
            #                 /* Target the tooltip text */
            #                 [data-testid="stTooltipContent"] p {
            #                     color: white !important;
                                
            #                 }
                            
            #                 /* Target the selectbox background */
            #                 [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            #                     background-color: #0a1b38 !important;
            #                     color: white !important;
            #                 }
                            
            #                 /* Target the selectbox dropdown menu */
            #                 [data-baseweb="popover"] {
            #                     background-color: #0a1b38 !important;
            #                 }
                            
            #                 /* Target the selectbox options */
            #                 [data-baseweb="menu"] {
            #                     background-color: #0a1b38 !important;
            #                 }
                            
            #                 [data-baseweb="menu"] li {
            #                     background-color: #0a1b38 !important;
            #                     color: white !important;
            #                 }
                            
            #                 /* Hover effect for options */
            #                 [data-baseweb="menu"] li:hover {
            #                     background-color: #1f3a5f !important;
            #                 }
            #                 </style>
            #                 """, unsafe_allow_html=True)
                
            #     # Display selectbox with sheet options
            #     unique_key = f"sheet_selector_{self.unique_id}_{self.uploaded_file.name}"
            #     selected_sheet = st.selectbox(
            #         "Select a sheet:", 
            #         options, 
            #         key=unique_key
            #     )
                
            #     # Return DataFrame if valid sheet selected, otherwise None
            #     if selected_sheet and selected_sheet != "-- Select a sheet --":
            #         self.df = pd.read_excel(self.uploaded_file, sheet_name=selected_sheet)
            #         if self.df is not None:
            #             # st.success(f"File '{self.uploaded_file.name}' uploaded successfully!")
            #             self.display_uploaded_file_info()
            #         return self.df
            #     else:
            #         return None
            # else:
            #     # Single sheet - load automatically
            #     self.df = pd.read_excel(self.uploaded_file)
                
            #     if self.df is not None:
            #         # st.success(f"File '{self.uploaded_file.name}' uploaded successfully!")
            #         self.display_uploaded_file_info()
                
            #     return self.df
            
            if len(self.sheet_names) > 1:
                # Initialize session state key for this specific file
                session_key = f"selected_sheet_{self.unique_id}_{self.uploaded_file.name}"
                
                if session_key not in st.session_state:
                    st.session_state[session_key] = None
                
                # Only show selectbox if no sheet has been selected yet
                if st.session_state[session_key] is None:
                    # Let user select sheet if multiple sheets exist
                    options = ["-- Select a sheet --"] + self.sheet_names
                    
                    # Apply custom CSS styling for dark theme selectbox
                    st.markdown("""
                                <style>
                                /* Target the tooltip text */
                                [data-testid="stTooltipContent"] p {
                                    color: white !important;
                                    
                                }
                                
                                /* Target the selectbox background */
                                [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
                                    background-color: #0a1b38 !important;
                                    color: white !important;
                                }
                                
                                /* Target the selectbox dropdown menu */
                                [data-baseweb="popover"] {
                                    background-color: #0a1b38 !important;
                                }
                                
                                /* Target the selectbox options */
                                [data-baseweb="menu"] {
                                    background-color: #0a1b38 !important;
                                }
                                
                                [data-baseweb="menu"] li {
                                    background-color: #0a1b38 !important;
                                    color: white !important;
                                }
                                
                                /* Hover effect for options */
                                [data-baseweb="menu"] li:hover {
                                    background-color: #1f3a5f !important;
                                }
                                </style>
                                """, unsafe_allow_html=True)
                    
                    # Display selectbox with sheet options
                    unique_key = f"sheet_selector_{self.unique_id}_{self.uploaded_file.name}"
                    selected_sheet = st.selectbox(
                        "Select a sheet:", 
                        options, 
                        key=unique_key
                    )
                    
                    # Store selection in session state if valid
                    if selected_sheet and selected_sheet != "-- Select a sheet --":
                        st.session_state[session_key] = selected_sheet
                        st.rerun()
                    else:
                        return None
                
                # Load DataFrame with the selected sheet
                self.df = pd.read_excel(self.uploaded_file, sheet_name=st.session_state[session_key])
                if self.df is not None:
                    # st.success(f"File '{self.uploaded_file.name}' uploaded successfully!")
                    self.display_uploaded_file_info()
                return self.df
            
            else:
                # Single sheet - load automatically
                self.df = pd.read_excel(self.uploaded_file)
                
                if self.df is not None:
                    # st.success(f"File '{self.uploaded_file.name}' uploaded successfully!")
                    self.display_uploaded_file_info()
                
                return self.df
            
            
        except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        
    def display_uploaded_file_info(self) -> None:
        """
        Display information about the uploaded file.
        
        Shows metrics for the number of rows, columns, and file size
        in a three-column layout.
        """
        
        st.markdown("""
            <style>
            /* Target metric label */
            [data-testid="stMetricLabel"] {
                font-size: 12px !important;
            }
            
            /* Target metric value */
            [data-testid="stMetricValue"] {
                font-size: 16px !important;
            }
            </style>
        """, unsafe_allow_html=True)
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(self.df))
        with col2:
            st.metric("Columns", len(self.df.columns))
        with col3:
            st.metric("File Size", f"{self.uploaded_file.size} bytes")
            
            