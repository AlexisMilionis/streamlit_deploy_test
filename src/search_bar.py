import streamlit as st
from streamlit_searchbox import st_searchbox
from constants import Constants

class SearchBar:
    
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
    
    def __init__(self, df):
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
    
    def search_buildings_supplies(self, searchterm: str) -> list:
        if not searchterm:
            return self.selection_list
        return [b for b in self.selection_list if searchterm.lower() in str(b).lower()]

    # Use in your app
    # @st.fragment
    def building_searchbox(self):
        
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
