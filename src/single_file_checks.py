from constants import Constants
import pandas as pd
import streamlit as st

class MonthlyDataChecks:
    column_names = Constants.COLUMN_NAMES
    mandatory_columns = Constants.NON_NULLABLE_COLUMNS
    
    def __init__(self, portfolio, portfolio_name):
        self.portfolio = portfolio
        self.column_names = Constants.COLUMN_NAMES
        self.portfolio_name = portfolio_name
        self.mandatory_columns = Constants.NON_NULLABLE_COLUMNS

    def exist_all_columns(self):
        missing_cols = [col for col in self.column_names if col not in self.portfolio.columns]
        error_portfolio = None
        if missing_cols:
            error_portfolio = f"Missing columns or different name in {self.portfolio_name} portfolio: {', '.join(missing_cols)}"
        return error_portfolio
    
    def exist_empty_rows(self):
        num_rows_before = len(self.portfolio)
        self.portfolio.dropna(how='all', inplace=True)  # Drop completely empty rows
        num_rows_after = len(self.portfolio)
        if num_rows_before != num_rows_after:
            return num_rows_before - num_rows_after
        else:
            return 0        

    def exist_filled_columns(self):
        
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
        error_portfolio = self.exist_all_columns()
        if error_portfolio:
            st.error(error_portfolio)
        else: 
            st.info(f"All required columns are present in {self.portfolio_name} portfolio.")
        num_empty_rows = self.exist_empty_rows()
        if num_empty_rows != 0:
            st.warning(f"{self.portfolio_name} portfolio has {num_empty_rows} completely empty rows, that are now deleted.")
        else:
            st.info(f"No completely empty rows found in {self.portfolio_name} portfolio.")
        mandatory_cols_unfilled = self.exist_filled_columns()
        if mandatory_cols_unfilled:
            st.error(f"The following mandatory columns have missing values in {self.portfolio_name} portfolio: {', '.join(mandatory_cols_unfilled)}")

        num_duplicates, all_duplicates = self.exist_duplicates()
        if num_duplicates > 0:
            st.error(f"{self.portfolio_name} portfolio has {num_duplicates}")
            with st.expander("View duplicate rows based on 'ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ' column"):
                st.dataframe(all_duplicates)
        else:
            st.info(f"No duplicate rows found in {self.portfolio_name} portfolio based on 'ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ' column.")


    #TODO: check για ετταξη/απενταξη παροχών
    #TODO: check for large fluctuations in price for the same παροχη btw months