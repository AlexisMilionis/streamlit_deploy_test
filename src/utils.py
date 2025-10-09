import streamlit as st
import time

def loading_spinner(message="Processing..."):
    """
    Create a loading spinner with text displayed side by side.
    
    Parameters:
    message: str - Message to display next to the spinner
    
    Returns:
    spinner context manager
    
    Example:
    >>> with loading_spinner("Loading data..."):
    >>>     # Your processing logic here
    >>>     time.sleep(2)
    """
    return st.spinner(message)


def custom_loading_display(message="Processing...", show_spinner=True):
    """
    Create a custom loading display with text and spinner side by side.
    
    Parameters:
    message: str - Message to display
    show_spinner: bool - Whether to show the spinner (default: True)
    
    Returns:
    col1, col2: Column objects for custom content
    
    Example:
    >>> col1, col2 = custom_loading_display("Loading files...")
    >>> with col2:
    >>>     with st.spinner(""):
    >>>         # Your processing logic
    >>>         time.sleep(2)
    """
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.text(message)
    
    with col2:
        if show_spinner:
            with st.spinner(""):
                pass
    
    return col1, col2


def show_loading_message(message="Processing..."):
    """
    Simple function to display a loading message with spinner.
    Use as context manager for automatic cleanup.
    
    Parameters:
    message: str - Message to display
    
    Example:
    >>> with show_loading_message("Uploading files..."):
    >>>     upload_files()
    """
    container = st.empty()
    
    class LoadingContext:
        def __enter__(self):
            with container:
                cols = st.columns([4, 1])
                with cols[0]:
                    st.text(message)
                with cols[1]:
                    st.spinner("")
            return self
        
        def __exit__(self, *args):
            container.empty()
    
    return LoadingContext()