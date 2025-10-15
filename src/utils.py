"""
Utility functions for the Streamlit application.

This module provides helper functions for progress bar animation, password hashing,
and token generation used throughout the application.
"""

import streamlit as st
import time
import secrets
import streamlit_authenticator as stauth
from typing import List

def animate_progress(progress_bar: st.delta_generator.DeltaGenerator, start: int, end: int, steps: int = 10, delay: float = 0.1) -> st.delta_generator.DeltaGenerator:
    """
    Animate a Streamlit progress bar from start to end percentage.
    
    Creates a smooth animation effect by incrementally updating the progress bar
    value over a specified number of steps with a delay between each update.
    
    Args:
        progress_bar (st.delta_generator.DeltaGenerator): The Streamlit progress bar object to animate.
        start (int): The starting percentage value (0-100).
        end (int): The ending percentage value (0-100).
        steps (int, optional): Number of animation steps. Defaults to 10.
        delay (float, optional): Delay in seconds between each step. Defaults to 0.1.
    
    Returns:
        st.delta_generator.DeltaGenerator: The updated progress bar object.
        
    Example:
        >>> progress_bar = st.progress(0)
        >>> animate_progress(progress_bar, 0, 50)
    """
    for i in range(steps + 1):
        current = start + (end - start) * i / steps
        progress_bar.progress(int(current))
        time.sleep(delay)
        
    return progress_bar
    
    
def generate_hashed_passwords(passwords: List[str]) -> List[str]:
    """
    Generate hashed passwords for a list of plain text passwords.
    
    Uses the streamlit_authenticator library's Hasher to securely hash
    passwords for storage in the authentication configuration.
    
    Args:
        passwords (List[str]): List of plain text passwords to hash.
    
    Returns:
        List[str]: List of hashed passwords in the same order as input.
        
    Example:
        >>> plain_passwords = ["password123", "secret456"]
        >>> hashed = generate_hashed_passwords(plain_passwords)
    """
    return stauth.Hasher().generate(passwords)


def create_token_hex() -> str:
    """
    Generate a secure random token in hexadecimal format.
    
    Creates a cryptographically secure random token that can be used for
    session management, CSRF protection, or other security purposes.
    
    Returns:
        str: A 64-character hexadecimal string (32 bytes).
        
    Example:
        >>> token = create_token_hex()
        >>> len(token)
        64
    """
    return secrets.token_hex(32)
