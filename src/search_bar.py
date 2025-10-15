"""
Search bar component module for the Streamlit application.

This module provides a customizable search bar widget for searching buildings
and supply IDs within the portfolio data using the streamlit_searchbox library.
"""

import streamlit as st
from streamlit_searchbox import st_searchbox
from constants import Constants
import pandas as pd
from typing import List, Optional

class SearchBar:
    """
    A search bar component for filtering buildings and supply IDs.
    
    This class creates a searchable dropdown interface that allows users to
    search through both building addresses and supply IDs from a portfolio
    DataFrame. It includes custom styling consistent with the application theme.
    
    Attributes:
        df (pd.DataFrame): The portfolio DataFrame containing building and supply data.
        building_list (List[str]): Unique list of building addresses from the portfolio.
        supply_list (List[str]): Unique list of supply IDs from the portfolio.
        selection_list (List[str]): Combined list of buildings and supply IDs for searching.
        style_overrides (dict): Custom CSS styling configuration for the search box.
    """
    
    style_overrides = style_overrides = {
        "clear": {
            "width": 20,
            "height": 20,
            "icon": "cross",
            "clearable": "always"
        },
        "dropdown": {
            "rotate": True,
            "width": 30,
            "height": 30,
            "fill": "blue",
        },
        "searchbox": {
            "control": {
                "backgroundColor": Constants.BACKGROUND_COLOR,
                "border": f"2px solid {Constants.PRIMARY_COLOR}",
                ":hover": {
                    "border": f"2px solid {Constants.PRIMARY_COLOR}",
                },
            },
            "menuList": {
                # "backgroundColor": "transparent",
                "backgroundColor": Constants.BACKGROUND_COLOR,
            },
            "singleValue": {
                "color": Constants.PRIMARY_COLOR
            },
            "option": {
                "color": "white",
                "backgroundColor": Constants.BACKGROUND_COLOR,
                "highlightColor": "green"
            },
            "noOptionsMessage": {
                "backgroundColor": "grey",
                "color": Constants.PRIMARY_COLOR,
            }
        }
    }
    
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize the SearchBar with portfolio data.
        
        Args:
            df (pd.DataFrame): Portfolio DataFrame containing 'ΔΙΕΥΘΥΝΣΗ' (building address)
                              and 'ΑΡ.ΠΑΡΟΧΗΣ' (supply ID) columns.
        
        Returns:
            None
        """
        self.df = df
        self.building_list = [str(x) for x in df['ΔΙΕΥΘΥΝΣΗ'].unique().tolist()]
        print(f"Building List: {len(self.building_list)} items")
        self.supply_list = [str(x) for x in df['ΑΡ.ΠΑΡΟΧΗΣ'].unique().tolist()]
        print(f"Supply List: {len(self.supply_list)} items")
        self.selection_list = self.building_list + self.supply_list

    # Extract unique values from your dataframe
    # def search_buildings(self, searchterm: str) -> list:
    #     if not searchterm:
    #         return self.building_list
    #     return [b for b in self.building_list if searchterm.lower() in str(b).lower()]

    # def search_supplies(self, searchterm: str) -> list:
    #     if not searchterm:
    #         return self.supply_list
    #     return [s for s in self.supply_list if searchterm.lower() in str(s).lower()]
    
    def search_buildings_supplies(self, searchterm: str) -> List[str]:
        """
        Filter buildings and supply IDs based on search term.
        
        This method performs case-insensitive substring matching on both
        building addresses and supply IDs.
        
        Args:
            searchterm (str): The search string entered by the user.
        
        Returns:
            List[str]: Filtered list of buildings and supply IDs matching the search term.
                      Returns full list if searchterm is empty.
        """
        if not searchterm:
            return self.selection_list
        return [b for b in self.selection_list if searchterm.lower() in str(b).lower()]

    def building_searchbox(self) -> Optional[str]:
        """
        Render the search box widget in the Streamlit interface.
        
        Creates an interactive search box using streamlit_searchbox with custom
        styling and behavior. The search box allows users to search through
        buildings and supply IDs with debounced input for performance.
        
        Returns:
            Optional[str]: The selected building address or supply ID, or None if nothing selected.
            
        Side Effects:
            - Renders a search box widget in the Streamlit UI
            - Triggers rerun when selection is updated
        """
        
        selected_option = st_searchbox(
            self.search_buildings_supplies,
            placeholder="Search for building or supply ID...",
            # label="Select Building or Supply ID",
            key="building_searchbox",
            default_options=self.selection_list,
            style_overrides=self.style_overrides,
            rerun_on_update=True, 
            # rerun_scope="fragment",
            debounce=300,  # Add debounce to limit calls
        )
        return selected_option
