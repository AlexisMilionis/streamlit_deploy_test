"""
Constants module for the Streamlit application.

This module defines all constant values used throughout the application including
column names, file paths, color schemes, and navigation configuration.
"""

import streamlit as st
from typing import List

class Constants:
    """
    Central configuration class containing all application constants.
    
    This class serves as a single source of truth for configuration values
    used across the application, including file paths, column definitions,
    validation rules, and UI styling constants.
    
    Attributes:
        AUTHENTICATION (bool): Flag to enable/disable authentication.
        navigation_menu (List[st.Page]): List of navigation pages for the app.
        DATAPATH (str): Base path for input data files.
        COLUMN_NAMES (List[str]): Expected column names for portfolio files.
        NON_NULLABLE_COLUMNS (List[str]): Columns that must not contain null values.
        TIMESERIES_PATH (str): Path for time series database files.
        EXPORT_PATH (str): Path for exported files.
        MASTERFILE_PATH (str): Path for master files.
        BACKGROUND_COLOR (str): Hex color code for UI background.
        PRIMARY_COLOR (str): Hex color code for primary UI elements.
        DONUT_COLORING (List[str]): RGB color palette for donut charts.
        DUAL_COLORING (List[str]): RGB color palette for dual-colored charts.
    """
    
    AUTHENTICATION = False

    navigation_menu = [
        st.Page("pages/bills.py", title="Utility Bills"), 
        st.Page("pages/property_management.py", title="Property Management"), 
        st.Page("pages/budget_forecast.py", title="Budget & Forecast")
        ]
    
    DATAPATH = "data/input/"
    
    COLUMN_NAMES = [
        'ΔΙΑΔΡΟΜΗ',
        'ΑΡ.ΠΑΡΟΧΗΣ',
        'ΠΕΡΙΟΔΟΣ ΚΑΤΑΝΑΛΩΣΗΣ ΑΠΌ',
        'ΠΕΡΙΟΔΟΣ ΚΑΤΑΝΑΛΩΣΗΣ ΕΩΣ',
        'ΗΜΕΡ.ΛΗΞΕΩΣ',
        'ΗΜ.ΚΑΤΑΝΑΛΩΣΗΣ',
        'ΠΕΡΙΦ.ΓΡΑΦ.',
        'ΤΙΜΟΛΟΓΙΟ',
        'ΙΔΙΟΚΤΗΤΗΣ',
        'ΕΝΟΙΚΟΣ',
        'ΔΙΕΥΘΥΝΣΗ',
        'ΑΦΜ',
        'ΑΡ.ΜΕΤΡΗΤΗ',
        'ΔΙΑΜ.',
        'ΠΡΟΗΓ.ΕΝΔ.',
        'ΠΑΡ.ΕΝΔΕΙΞΗ',
        'ΤΕΚΜ.',
        'ΤΡΙΜ',
        'ΠΡΟΣΘ',
        'ΤΥΠΟΣ ΛΟΓΑΡΙΑΣΜΟΥ',
        'ΚΥΒΙΚΑ 1',
        'ΤΙΜΗΜΑ 1',
        'ΚΥΒΙΚΑ 2',
        'ΤΙΜΗΜΑ 2',
        'ΚΥΒ.3',
        'ΤΙΜ.3',
        'ΚΥΒ.4',
        'ΤΙΜΗΜΑ 4',
        'ΚΥΒ.5',
        'ΤΙΜΗΜΑ 5',
        'ΤΙΜΗΜΑ',
        'ΠΑΓΙΟ',
        'ΤΕΑΠ',
        'ΟΑΠ',
        'ΦΠΑ ΤΙΜ.',
        'ΦΠΑ ΛΟΙΠΩΝ',
        'ΕΡΓΑΣΙΕΣ',
        'ΔΙΑΦ.ΚΕΡΜ.',
        'ΚΥΡΙΑ ΟΦ.',
        'ΠΙΣΤΩΤΙΚΟ',
        'ΟΦΕΙΛΗ',
        'ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ',
        'ΗΜΕΡΟΜ.ΕΚΔΟΣΗΣ'
        ]

    NON_NULLABLE_COLUMNS = [
        'ΑΡ.ΠΑΡΟΧΗΣ',
        'ΚΥΡΙΑ ΟΦ.',
        'ΕΝΟΙΚΟΣ',
        'ΠΑΡ.ΕΝΔΕΙΞΗ',
        'ΑΦΜ',
        'ΠΙΣΤΩΤΙΚΟ',
        'ΙΔΙΟΚΤΗΤΗΣ',
        'ΔΙΑΦ.ΚΕΡΜ.',
        'ΠΡΟΣΘ',
        'ΦΠΑ ΤΙΜ.',
        'ΗΜΕΡ.ΛΗΞΕΩΣ',
        'ΟΦΕΙΛΗ',
        'ΠΕΡΙΦ.ΓΡΑΦ.',
        'ΤΕΚΜ.',
        'ΗΜΕΡΟΜ.ΕΚΔΟΣΗΣ',
        'ΑΡ.ΠΑΡΑΣΤΑΤΙΚΟΥ',
        'ΔΙΕΥΘΥΝΣΗ',
        'ΤΡΙΜ',
        'ΠΡΟΗΓ.ΕΝΔ.',
        'ΤΥΠΟΣ ΛΟΓΑΡΙΑΣΜΟΥ'
    ]
    
    TIMESERIES_PATH = "data/"
    
    EXPORT_PATH = "data/exports/"
    
    MASTERFILE_PATH = "data/"
    
    BACKGROUND_COLOR = "#0a1b38"
    
    PRIMARY_COLOR = "#0db1f2"
    
    DONUT_COLORING = [ # from darker to lighter
        "rgb(8,106,145)",
        "rgb(10,142,194)",
        "rgb(13,177,242)",
        "rgb(61,193,245)",
        "rgb(110,208,247)",
        "rgb(158,224,250)",
    ]
    
    DUAL_COLORING = [
        "rgb(10,102,194)",  # skouro
        "rgb(158,224,250)",  # anoixto
    ]