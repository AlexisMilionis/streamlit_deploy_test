
"""
Bill Tab 2 - KPIs & Metrics view for the Bills page.

This module provides the second tab interface for displaying bill KPIs,
interactive charts, and searchable metrics for buildings and supply IDs.
"""

import streamlit as st
from src.generate_metrics import Metrics
from src.search_bar import SearchBar

def create_tab2() -> None:
    """
    Create and render the KPIs and metrics tab interface.
    
    This function provides:
    - Overall bill-level metrics and visualizations
    - Interactive search bar for buildings and supply IDs
    - Drill-down metrics for selected buildings or supply IDs
    - Donut charts for debt distribution
    - Time series charts for consumption and costs
    
    The function uses data from st.session_state.df_portfolio which must
    be set by the file upload tab.
    
    Returns:
        None
        
    Side Effects:
        - Renders KPIs, charts, and search interface in the Streamlit UI
        - Applies custom CSS styling for consistent font sizes
    """
    
    st.write("")
    st.subheader("Bill Metrics")
    st.write("")
    bill_metrics = Metrics(st.session_state.df_portfolio)
    col1, col2 = st.columns(2)
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write("**KPIs**")
        bill_metrics.build_kpis()
    with col2:
        bill_metrics.build_donut_chart()
    bill_metrics.build_cost_timeseries()
    
    # st.write("")
    # st.subheader("Building Metrics", divider="grey")
    # st.write("")
    # building_metrics = Metrics(st.session_state.df_portfolio, 
    #                         level='building', 
    #                         dropdown_selection='ΚΑΛΛΙΡΡΟΗΣ 21  Δήμος ΑΘΗΝΑΙΩΝ ΤΚ 11743',
    #                         )
    # col1, col2 = st.columns(2)
    # with col1:
    #     building_metrics.build_kpis()
    # with col2:
    #     building_metrics.build_donut_chart()
    # building_metrics.build_cost_timeseries()

    # st.write("")
    # st.subheader("Supply ID Metrics", divider="grey")
    # st.write("")
    # supply_id_metrics = Metrics(st.session_state.df_portfolio, 
    #                         level='supply_id', 
    #                         dropdown_selection=1533178,
    #                         )
    # col1, col2 = st.columns(2)
    # with col1:
    #     supply_id_metrics.build_kpis()
    # with col2:
    #     supply_id_metrics.build_donut_chart()
    # supply_id_metrics.build_cost_timeseries()

    # st.markdown("""
    #     <style>
    #         /* Style for selectbox container */
    #         div[data-baseweb="select"] {
    #             background-color: black !important;
    #         }
            
    #         /* Style for selectbox input */
    #         div[data-baseweb="select"] > div {
    #             background-color: #1a2332 !important;
    #             border: 2px solid #0db1f2 !important;
    #             border-radius: 5px !important;
    #         }
            
    #         /* Style for selectbox text */
    #         div[data-baseweb="select"] input {
    #             color: #ffffff !important;
    #         }
            
    #         /* Style for selectbox dropdown menu */
    #         ul[role="listbox"] {
    #             background-color: #1a2332 !important;
    #             border: 2px solid #0db1f2 !important;
    #         }
            
    #         /* Style for dropdown options */
    #         li[role="option"] {
    #             color: #ffffff !important;
    #         }
            
    #         /* Style for dropdown options on hover */
    #         li[role="option"]:hover {
    #             background-color: #2a3342 !important;
    #         }
            
    #         /* Style for selected option */
    #         li[role="option"][aria-selected="true"] {
    #             background-color: #0db1f2 !important;
    #             color: white !important;
    #         }
    #     </style>
    #     """, unsafe_allow_html=True)

    search_bar = SearchBar(st.session_state.df_portfolio)
    
    selected_option = search_bar.building_searchbox()
    if selected_option is not None and selected_option in (st.session_state.df_portfolio['ΔΙΕΥΘΥΝΣΗ'].unique().tolist()):

        st.write(f"Selected Building: {selected_option}")
        building_metrics = Metrics(st.session_state.df_portfolio,
                                level='building',
                                dropdown_selection=selected_option,
                                )
        col1, col2 = st.columns(2)
        with col1:
            building_metrics.build_kpis()
        with col2:
            building_metrics.build_donut_chart()
        building_metrics.build_cost_timeseries()

    elif selected_option is not None and selected_option in (st.session_state.df_portfolio['ΑΡ.ΠΑΡΟΧΗΣ'].unique().tolist()):
        st.write(f"Selected Supply ID: {selected_option}")
        supply_metrics = Metrics(st.session_state.df_portfolio,
                                level='supply_id',
                                dropdown_selection=selected_option,
                                )
        col1, col2 = st.columns(2)
        with col1:
            supply_metrics.build_kpis()
        with col2:
            supply_metrics.build_donut_chart()
        supply_metrics.build_cost_timeseries()
        
    # elif selected_option is None:
    #     st.info("Please select a valid Building or Supply ID from the search box above to view metrics.")
        # building_metrics.build_scatterplot()
    
    # bill_metrics.build_scatterplot()
    
    # st.markdown("""
    #     <style>
    #             /* Style for input fields (username and password) */
    #             .stTextInput > div > div > input {
    #                 background-color: #f0f8ff !important;
    #                 border: 2px solid #0db1f2 !important;
    #                 border-radius: 5px !important;
    #                 color: #333 !important;
    #             }
                
    #             /* Style for input fields on focus */
    #             .stTextInput > div > div > input:focus {
    #                 background-color: #e6f3ff !important;
    #                 border-color: #0880bf !important;
    #                 box-shadow: 0 0 5px rgba(13, 177, 242, 0.3) !important;
    #             }
                
    #             /* Style for password input specifically if needed */
    #             input[type="password"] {
    #                 background-color: #f0f8ff !important;
    #                 border: 2px solid #0db1f2 !important;
    #                 border-radius: 5px !important;
    #                 color: #333 !important;
    #             }

    #             [data-testid="stBaseButton-secondary"] {
    #                 background-color: #0db1f2 !important;
    #                 color: white !important;
    #                 border: none !important;
    #                 border-radius: 5px !important;
    #     }

    #     </style>
    #     """, unsafe_allow_html=True)

    # monthly_supply_id_input = st.text_input(
    #     "Enter Supply ID to retrieve information:",
    #     placeholder="Type supply ID here..."
    # )
    # if monthly_supply_id_input:
    #     monthly_metrics.display_supply_id_info(monthly_supply_id_input)
        
    st.write("")
    st.write("")
    st.write("")