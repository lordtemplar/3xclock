import streamlit as st
import time
from datetime import datetime, timedelta
import pytz

# Set the page configuration
st.set_page_config(page_title="JTLS Clock", layout="wide")

# Initialize the Bangkok time zone
bangkok_tz = pytz.timezone("Asia/Bangkok")

# Initialize state variables if not set
if 'real_start' not in st.session_state:
    st.session_state.real_start = datetime.now(bangkok_tz).replace(hour=8, minute=0, second=0, microsecond=0)
if 'jtls_start' not in st.session_state:
    st.session_state.jtls_start = datetime.now(bangkok_tz).replace(hour=5, minute=0, second=0, microsecond=0)

# Function to calculate the accelerated JTLS time
def calculate_jtls_time(real_time):
    real_elapsed = real_time - st.session_state.real_start
    
    # JTLS starts at 08:00 and stops at 16:00
    if real_time.hour < 8:
        return st.session_state.jtls_start  # Before 08:00, JTLS time is frozen at 05:00
    elif real_time.hour < 9:  # From 08:00 to 09:00 - 1x speed
        jtls_elapsed = real_elapsed
    elif real_time.hour < 15:  # From 09:00 to 15:00 - 2x speed
        jtls_elapsed = timedelta(hours=1) + (real_elapsed - timedelta(hours=1)) * 2
    elif real_time.hour < 16:  # From 15:00 to 16:00 - 1x speed again
        jtls_elapsed = timedelta(hours=8) + (real_elapsed - timedelta(hours=7))
    else:  # After 16:00, JTLS time stops
        return st.session_state.jtls_start + timedelta(hours=14)
    
    return st.session_state.jtls_start + jtls_elapsed

# Display clocks
st.write("### JTLS Clocks:")
normal_col, accel_col = st.columns(2)

with normal_col:
    st.write("**Thailand Clock:**")
    normal_time_display = st.empty()

with accel_col:
    st.write(f"**JTLS Clock:**")
    accel_time_display = st.empty()

# Update the clocks every second
while True:
    current_time = datetime.now(bangkok_tz)
    current_normal_time = current_time.strftime("%H:%M:%S")
    
    # Calculate the JTLS time only within the 08:00 to 16:00 range
    if current_time.hour >= 8 and current_time.hour < 16:
        current_jtls_time = calculate_jtls_time(current_time).strftime("%H:%M:%S")
    else:
        # Stop the JTLS clock outside 08:00 to 16:00 range
        current_jtls_time = (st.session_state.jtls_start + timedelta(hours=14)).strftime("%H:%M:%S")
    
    normal_time_display.markdown(f"<div style='background-color: lightblue; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_normal_time}</div>", unsafe_allow_html=True)
    accel_time_display.markdown(f"<div style='background-color: orange; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_jtls_time}</div>", unsafe_allow_html=True)
    
    time.sleep(1)
