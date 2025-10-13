import pandas as pd
import streamlit as st
import time
from io import BytesIO
from constants import Constants
from src.single_file_checks import MonthlyDataChecks
from src.utils import animate_progress
from datetime import datetime

class TimeSeriesUpdate:
    path = Constants.TIMESERIES_PATH
    export_path = Constants.EXPORT_PATH
    
    def __init__(self, new_file, portfolio_type):
        self.new_file = new_file
        self.portfolio_type = portfolio_type.lower()
        if self.portfolio_type == "eurobank":
            self.timeseries = pd.read_excel(self.path + "eurobank_historical_db.xlsx")
        elif self.portfolio_type == "management":
            self.timeseries = pd.read_excel(self.path + "management_historical_db.xlsx")

    def add_new_data(self):
                
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