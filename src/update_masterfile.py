import pandas as pd
from constants import Constants
import streamlit as st

class MasterFileUpdate:
    
    path = Constants.MASTERFILE_PATH
    
    def __init__(self, new_file, portfolio_type):
        self.portfolio_type = portfolio_type.lower() 
        if self.portfolio_type == "eurobank":
            self.masterfile = pd.read_excel(self.path + "eurobank_masterfile.xlsx")
        elif self.portfolio_type == "management":
            self.masterfile = pd.read_excel(self.path + "management_masterfile.xlsx")
        self.new_file = new_file
        
    def update_masterfile(self):
        
        unique_supply_ids_newfile = set(self.new_file['ΑΡ.ΠΑΡΟΧΗΣ'].unique())
        unique_supply_ids_masterfile = set(self.masterfile['Παροχή'].unique())
        untracked_supply_ids = list(unique_supply_ids_newfile - unique_supply_ids_masterfile)
        untracked_rows = self.new_file[self.new_file['ΑΡ.ΠΑΡΟΧΗΣ'].isin(untracked_supply_ids)]
        
        if untracked_supply_ids:
            st.warning(f"There are new supply IDs! Please add them to the master file")
            st.dataframe(untracked_rows)
        else:
            st.info("No new supply IDs found compared to masterfile.")