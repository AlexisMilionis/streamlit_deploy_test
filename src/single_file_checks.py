from constants import Constants
from src.utils import animate_progress
import pandas as pd
import streamlit as st
import time
class MonthlyDataChecks:
    column_names = Constants.COLUMN_NAMES
    mandatory_columns = Constants.NON_NULLABLE_COLUMNS
    
    def __init__(self, portfolio, portfolio_name):
        self.portfolio = portfolio
        self.portfolio_name = portfolio_name

    def exist_all_columns(self):
        missing_cols = [col for col in self.column_names if col not in self.portfolio.columns]
        return missing_cols

    
    def exist_empty_rows(self):
        num_rows_before = len(self.portfolio)
        self.portfolio.dropna(how='all', inplace=True)
        num_rows_after = len(self.portfolio)
        if num_rows_before != num_rows_after:
            return num_rows_before - num_rows_after
        else:
            return 0
        

    def exist_unfilled_values_in_mandatory_columns(self):
        missing_columns = [col for col in self.mandatory_columns if col not in self.portfolio.columns]
        mandatory_cols_unfilled = []
        for col in self.mandatory_columns:
            if self.portfolio[col].isnull().any():
                mandatory_cols_unfilled.append(col)
        return mandatory_cols_unfilled
    
    def exist_duplicates(self, cols="ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ"):
        duplicates = self.portfolio[cols].duplicated()
        num_duplicates = duplicates.sum()
        # Get duplicate rows
        duplicate_rows = self.portfolio[duplicates]
        #  Check for duplicates keeping all occurrences
        all_duplicates = self.portfolio[self.portfolio.duplicated(keep=False)]
        
        if num_duplicates > 0:
            return num_duplicates, all_duplicates
        else:
            return 0, None
        
    def single_file_checks_pipeline(self):
        # Initialize progress bar and status text
        progress_bar = st.progress(0)
        status_text = st.empty()
        info_messages = []
        
        # Check 1: Column presence
        status_text.text("Checking columns...")
        progress_bar = animate_progress(progress_bar, 0, 25)
        # progress_bar.progress(0)
        missing_cols = self.exist_all_columns()
        if len(missing_cols) > 0:
            status_text.empty()
            progress_bar.empty()
            st.error(f"Missing columns or different name in {self.portfolio_name} portfolio: {', '.join(missing_cols)}")
            return False
        else: 
            info_placeholder = st.empty()
            info_placeholder.success(f"No missing columns")
            info_messages.append(info_placeholder)
        
        # Check 2: Empty rows
        status_text.text("Checking for empty rows...")
        progress_bar = animate_progress(progress_bar, 25, 50)
        num_empty_rows = self.exist_empty_rows()
        if num_empty_rows != 0:
            st.warning(f"{self.portfolio_name} portfolio has {num_empty_rows} completely empty rows, that are now deleted.")
        else:
            info_placeholder = st.empty()
            info_placeholder.success(f"No empty rows")
            info_messages.append(info_placeholder)
        
        # Check 3: Mandatory columns
        status_text.text("Checking mandatory columns...")
        progress_bar = animate_progress(progress_bar, 50, 75)
        mandatory_cols_unfilled = self.exist_unfilled_values_in_mandatory_columns()
        if mandatory_cols_unfilled:
            status_text.empty()
            progress_bar.empty()
            st.error(f"The following mandatory columns have missing values in {self.portfolio_name} portfolio: {', '.join(mandatory_cols_unfilled)}")
            return False
        else:
            info_placeholder = st.empty()
            info_placeholder.success(f"No missing values in mandatory columns")
            info_messages.append(info_placeholder)
        
        # Check 4: Duplicates
        status_text.text("Checking for duplicates...")
        progress_bar = animate_progress(progress_bar, 75, 100)
        num_duplicates, all_duplicates = self.exist_duplicates()
        if num_duplicates > 0:
            status_text.empty()
            progress_bar.empty()
            st.error(f"{self.portfolio_name} portfolio has {num_duplicates} duplicate rows")
            with st.expander("View duplicate rows based on 'ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ' column"):
                st.dataframe(all_duplicates)
            return False
        else:
            info_placeholder = st.empty()
            info_placeholder.success(f"No duplicate rows")
            info_messages.append(info_placeholder)

        # Complete
        status_text.markdown('<span style="color: #0db1f2;">Validation complete ✓</span>', unsafe_allow_html=True)
        time.sleep(1)
        
        # Clear all info messages
        for info_msg in info_messages:
            info_msg.empty()
        
        # status_text.empty()
        progress_bar.empty()
    
        return True


    #TODO: check για ενταξη/απενταξη παροχών
    #TODO: check for large fluctuations in price for the same παροχη btw months