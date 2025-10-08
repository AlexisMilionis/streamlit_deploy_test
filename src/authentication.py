import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from constants import Constants

def authenticate():
    constants = Constants()
    
    st.markdown("""
    <style>
            /* Style for input fields (username and password) */
            .stTextInput > div > div > input {
                background-color: #f0f8ff !important;
                border: 2px solid #0db1f2 !important;
                border-radius: 5px !important;
                color: #333 !important;
            }
            
            /* Style for input fields on focus */
            .stTextInput > div > div > input:focus {
                background-color: #e6f3ff !important;
                border-color: #0880bf !important;
                box-shadow: 0 0 5px rgba(13, 177, 242, 0.3) !important;
            }
            
            /* Style for password input specifically if needed */
            input[type="password"] {
                background-color: #f0f8ff !important;
                border: 2px solid #0db1f2 !important;
                border-radius: 5px !important;
                color: #333 !important;
            }

            [data-testid="stBaseButton-secondary"] {
                background-color: #0db1f2 !important;
                color: white !important;
                border: none !important;
                border-radius: 5px !important;
    }

    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
<style>
    /* Style for logout button */
    
</style>
""", unsafe_allow_html=True)
    

    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        # config['preauthorized']
    )

    stauth.Hasher.hash_passwords(config['credentials'])

    # Get authentication status from session state
    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{st.session_state["name"]}*')
        
        
        pg = st.navigation(constants.navigation_menu)
        pg.run()
    else:
        # Show login form for both None and False authentication status
        authenticator.login(location='main')
        
        if st.session_state["authentication_status"] == False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] == None:
            st.warning('Please enter your username and password')
        
        # Force rerun after successful login
        if st.session_state["authentication_status"]:
            st.rerun()
