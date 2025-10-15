"""
Master file update module for the Streamlit application.

This module provides functionality to update master files by checking for new
supply IDs in uploaded portfolio files and alerting users to add them.
"""

import pandas as pd
from constants import Constants
import streamlit as st
from typing import Literal

class MasterFileUpdate:
    """
    A class for updating master files with new supply IDs from portfolio data.
    
    This class compares uploaded portfolio files against existing master files
    to identify new supply IDs that need to be added to the master file. It
    supports both Eurobank and Management portfolio types.
    
    Attributes:
        portfolio_type (str): Type of portfolio ('eurobank' or 'management').
        masterfile (pd.DataFrame): The existing master file DataFrame.
        new_file (pd.DataFrame): The newly uploaded portfolio DataFrame.
        path (str): Base path for master file storage (class attribute).
    """
    
    path = Constants.MASTERFILE_PATH
    
    def __init__(self, new_file: pd.DataFrame, portfolio_type: Literal["eurobank", "management"]) -> None:
        """
        Initialize the MasterFileUpdate with new portfolio data.
        
        Args:
            new_file (pd.DataFrame): The newly uploaded portfolio DataFrame containing supply IDs.
            portfolio_type (Literal["eurobank", "management"]): The type of portfolio to process.
        
        Returns:
            None
        """
        self.portfolio_type = portfolio_type.lower() 
        if self.portfolio_type == "eurobank":
            self.masterfile = pd.read_excel(self.path + "eurobank_masterfile.xlsx")
        elif self.portfolio_type == "management":
            self.masterfile = pd.read_excel(self.path + "management_masterfile.xlsx")
        self.new_file = new_file
        
    def update_masterfile(self) -> None:
        """
        Check for new supply IDs and display untracked ones.
        
        Compares supply IDs in the new file against the master file and identifies
        any supply IDs that exist in the new file but not in the master file.
        Displays a warning with the untracked rows if new supply IDs are found.
        
        Returns:
            None
            
        Side Effects:
            - Displays warning message if new supply IDs are found
            - Shows DataFrame with untracked rows
            - Displays info message if no new supply IDs found
        """
        
        unique_supply_ids_newfile = set(self.new_file['ΑΡ.ΠΑΡΟΧΗΣ'].unique())
        unique_supply_ids_masterfile = set(self.masterfile['Παροχή'].unique())
        untracked_supply_ids = list(unique_supply_ids_newfile - unique_supply_ids_masterfile)
        untracked_rows = self.new_file[self.new_file['ΑΡ.ΠΑΡΟΧΗΣ'].isin(untracked_supply_ids)]
        
        if untracked_supply_ids:
            st.warning(f"There are new supply IDs! Please add them to the master file")
            st.dataframe(untracked_rows)
        else:
            st.info("No new supply IDs found compared to masterfile.")