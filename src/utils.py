import streamlit as st
import time
import secrets
import streamlit_authenticator as stauth

def animate_progress(progress_bar, start, end, steps=10, delay=0.1):
        """Animate progress bar from start to end percentage"""
        for i in range(steps + 1):
            current = start + (end - start) * i / steps
            progress_bar.progress(int(current))
            time.sleep(delay)
            
        return progress_bar
    
    
def generate_hashed_passwords(passwords):
    """Generate hashed passwords for a list of plain text passwords"""
    return stauth.Hasher().generate(passwords)


def create_token_hex():
    """Generate a secure random token in hexadecimal format"""
    return secrets.token_hex(32)
