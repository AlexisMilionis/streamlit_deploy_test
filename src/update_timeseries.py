"""
Time series update module for the Streamlit application.

This module provides functionality to append new monthly portfolio data to
historical database files while checking for duplicates and data integrity.
"""

import pandas as pd
import streamlit as st
import time
from io import BytesIO
from constants import Constants
from src.single_file_checks import MonthlyDataChecks
from src.utils import animate_progress
from datetime import datetime
from typing import Literal, Optional, Union

class TimeSeriesUpdate:
    """
    A class for updating time series historical databases with new portfolio data.
    
    This class handles the process of appending new monthly portfolio data to
    existing historical databases while performing validation checks to ensure
    data integrity and prevent duplicate entries.
    
    Attributes:
        new_file (pd.DataFrame): The newly uploaded portfolio DataFrame to be added.
        portfolio_type (str): Type of portfolio ('eurobank' or 'management').
        timeseries (pd.DataFrame): The existing historical database DataFrame.
        path (str): Base path for time series storage (class attribute).
        export_path (str): Path for exported files (class attribute).
    """
    
    path = Constants.TIMESERIES_PATH
    export_path = Constants.EXPORT_PATH
    
    def __init__(self, new_file: pd.DataFrame, portfolio_type: Literal["eurobank", "management"]) -> None:
        """
        Initialize the TimeSeriesUpdate with new portfolio data.
        
        Args:
            new_file (pd.DataFrame): The newly uploaded portfolio DataFrame to append.
            portfolio_type (Literal["eurobank", "management"]): The type of portfolio to process.
        
        Returns:
            None
        """
        self.new_file = new_file
        self.portfolio_type = portfolio_type.lower()
        if self.portfolio_type == "eurobank":
            self.timeseries = pd.read_excel(self.path + "eurobank_historical_db.xlsx")
        elif self.portfolio_type == "management":
            self.timeseries = pd.read_excel(self.path + "management_historical_db.xlsx")

    def add_new_data(self) -> Union[pd.DataFrame, bool]:
        """
        Add new portfolio data to the historical database after validation.
        
        This method performs a series of validation checks before appending new data:
        1. Checks for missing columns in the time series
        2. Checks for duplicate rows within the time series
        3. Checks if the new data already exists in the time series
        
        If all checks pass, the new data is concatenated with the existing time series
        and offered as a download. The process is visualized with an animated progress bar.
        
        Returns:
            Union[pd.DataFrame, bool]: The updated DataFrame if successful, False if
                                      duplicate data is found, or None if validation fails.
                                      
        Side Effects:
            - Displays progress bar and status messages during processing
            - Shows error/warning/info messages for various validation states
            - Provides download button for updated database
            - Displays expandable DataFrames for duplicate rows
        """
                
        progress_bar = st.progress(0)
        status_text = st.empty()
        info_messages = []
        
        # Check 1: Column presence
        status_text.text("Checking columns...")
        progress_bar = animate_progress(progress_bar, 0, 33)
        single_file_checks = MonthlyDataChecks(self.timeseries, self.portfolio_type)
        missing_cols = single_file_checks.exist_all_columns()
        if len(missing_cols) > 0:
            status_text.empty()
            progress_bar.empty()
            st.error(f"Missing columns or different name in {self.portfolio_type} Timeseries: {', '.join(missing_cols)}")
            return
        else:
            info_placeholder = st.empty()
            info_messages.append(info_placeholder)
            
        # Check 2: Duplicates
        status_text.text("Checking for duplicates in timeseries...")
        progress_bar = animate_progress(progress_bar, 33, 66)
        num_duplicates, all_duplicates = single_file_checks.exist_duplicates()
        if num_duplicates > 0:
            status_text.empty()
            progress_bar.empty()
            st.error(f"{self.portfolio_type} Timeseries has {num_duplicates} duplicate rows")
            with st.expander("View duplicate rows based on 'ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ' column"):
                st.dataframe(all_duplicates)
            return
        else:
            info_placeholder = st.empty()
            info_messages.append(info_placeholder)
            
        # Check 3: Check if new data already in timeseries
        unique_invoice_timeseries = set(self.timeseries['ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ'].astype(str).unique())
        unique_invoice_newfile = set(self.new_file['ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ'].astype(str).unique())
        common_ids = unique_invoice_timeseries.intersection(unique_invoice_newfile)
        common_ids = list(common_ids)
        if common_ids:
            status_text.empty()
            progress_bar.empty()
            if len(common_ids) == len(list(unique_invoice_newfile)):
                st.info(f"File already in database.")
            else:
                st.info(f"{len(common_ids)}/{len(unique_invoice_newfile)} records already in database.")
                df_duplicates = self.new_file[self.new_file['ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ'].astype(str).isin(common_ids)]
                st.error(f"{self.portfolio_type} portfolio has {len(df_duplicates)} duplicate rows with database")
                with st.expander("View duplicate rows based on 'ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ' column"):
                    st.dataframe(df_duplicates)
                
            status_text.empty()
            progress_bar.empty()
            return False
        
        else:
        
            status_text.text("Appending new file to timeseries...")
            progress_bar = animate_progress(progress_bar, 66, 100)
            updated_timeseries = pd.concat([self.timeseries, self.new_file], ignore_index=True)
            updated_timeseries.reset_index(drop=True, inplace=True)
            buffer = BytesIO()
            updated_timeseries.to_excel(buffer, index=False)
            buffer.seek(0)
            current_date = datetime.now().strftime("%Y%m%d")
            st.download_button(
                label=f"Download Updated {self.portfolio_type.title()} Database",
                data=buffer,
                file_name=f"{self.portfolio_type}_historical_db_{current_date}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # Complete
        # status_text.text("Timeseries Update complete!")
        status_text.markdown('<span style="color: #0db1f2;">Timeseries Update complete ✓</span>', unsafe_allow_html=True)
        time.sleep(1)
        
        # Clear all info messages
        for info_msg in info_messages:
            info_msg.empty()
            
        progress_bar.empty()
        
        return updated_timeseries