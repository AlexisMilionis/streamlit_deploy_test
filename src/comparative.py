"""
Comparative file module for the Streamlit application.

This module provides functionality for comparing portfolio data across time periods
and updating databases with new supply IDs.
"""

import pandas as pd
from typing import Set

class ComparativeFile:
    """
    A class for creating comparative analyses between portfolio periods.
    
    This class facilitates comparisons between current and previous portfolio
    data, identifies new supply IDs, and generates comparative reports. It
    also handles database updates with newly registered supply IDs.
    
    Attributes:
        portfolio_current (pd.DataFrame): The current period's portfolio data.
        portfolio_previous (pd.DataFrame): The previous period's portfolio data.
        database (pd.DataFrame): The historical database containing all supply IDs.
        portfolio_comparable (pd.DataFrame): DataFrame for storing comparative analysis.
        inactive_supply_ids (Set): Supply IDs that exist in database but not in current portfolio.
        supply_id_col (str): Column name for supply IDs (class attribute).
    """
    
    supply_id_col = "ΑΡ.ΠΑΡΟΧΗΣ"

    def __init__(self, portfolio_current: pd.DataFrame, portfolio_previous: pd.DataFrame, database: pd.DataFrame) -> None:
        """
        Initialize the ComparativeFile with portfolio data.
        
        Args:
            portfolio_current (pd.DataFrame): The current period's portfolio DataFrame.
            portfolio_previous (pd.DataFrame): The previous period's portfolio DataFrame.
            database (pd.DataFrame): The historical database DataFrame.
        
        Returns:
            None
        """
        self.portfolio_current = portfolio_current
        self.portfolio_previous = portfolio_previous
        self.database = database
        self.portfolio_comparable = pd.DataFrame()
        
    
    def database_update(self) -> None:
        """
        Update the database with new supply IDs from the current portfolio.
        
        This method identifies supply IDs that exist in the current portfolio but
        not in the database, adds those records to the database, and identifies
        inactive supply IDs (those in database but not in current portfolio).
        
        Returns:
            None
            
        Side Effects:
            - Modifies self.database by appending new supply ID rows
            - Sets self.inactive_supply_ids with IDs not in current portfolio
            
        Note:
            TODO: Add duplicate check for database after update
        """
        current_supply_ids = set(self.portfolio_current[self.supply_id_col].unique())
        current_database_ids = set(self.database[self.supply_id_col].unique())
        # unregistered_supply_ids = exist in current portfolio but not in db
        unregistered_supply_ids = (current_supply_ids - current_database_ids).tolist()
        rows_to_add_to_database = self.portfolio_current[self.portfolio_current[self.supply_id_col].isin(unregistered_supply_ids)]
        self.database = pd.concat([self.database, rows_to_add_to_database], ignore_index=True)
        # TODO: elegxos an db exei duplicates
        # inactive ids = exist in db but not in current portfolio
        self.inactive_supply_ids = current_database_ids - current_supply_ids.tolist()
        

    def build_comparative_file(self) -> None:
        """
        Generate an Excel file with comparative portfolio data.
        
        Creates a multi-sheet Excel workbook containing:
        - Current portfolio data
        - Previous portfolio data
        - Comparative analysis sheet
        
        The file is saved as "ΣΥΓΚΡΙΤΙΚΟΣ ΕΥΔΑΠ.xlsx" in the current directory.
        
        Returns:
            None
            
        Side Effects:
            - Creates an Excel file in the current working directory
        """
        with pd.ExcelWriter("ΣΥΓΚΡΙΤΙΚΟΣ ΕΥΔΑΠ.xlsx") as writer:
            self.portfolio_current.to_excel(writer, sheet_name="Current Portfolio", index=False)
            self.portfolio_previous.to_excel(writer, sheet_name="Previous Portfolio", index=False)
            self.portfolio_comparable.to_excel(writer, sheet_name="ΣΥΓΚΡΙΤΙΚΟΣ", index=False)

