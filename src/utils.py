import streamlit as st
import time

def animate_progress(progress_bar, start, end, steps=10, delay=0.1):
        """Animate progress bar from start to end percentage"""
        for i in range(steps + 1):
            current = start + (end - start) * i / steps
            progress_bar.progress(int(current))
            time.sleep(delay)
            
        return progress_bar
