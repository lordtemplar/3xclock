import streamlit as st
import time
from datetime import datetime, timedelta
import pytz

# Set the page configuration
st.set_page_config(page_title="JTLS Clock 3x", layout="wide")

# Initialize the Bangkok time zone
bangkok_tz = pytz.timezone("Asia/Bangkok")

# Set fixed acceleration factor
acceleration = 3

# Initialize state variables if not set
if 'normal_start' not in st.session_state:
    st.session_state.normal_start = datetime.now(bangkok_tz)
if 'accel_start' not in st.session_state:
    st.session_state.accel_start = datetime.now(bangkok_tz).replace(hour=7, minute=0, second=0, microsecond=0)

# Function to calculate the accelerated time
def get_accelerated_time(real_start, accel_start, multiplier=3):
    elapsed_real = datetime.now(bangkok_tz) - real_start
    elapsed_accel = elapsed_real * multiplier
    return accel_start + elapsed_accel

# Display clocks
st.write("### JTLS Clocks:")
normal_col, accel_col = st.columns(2)

with normal_col:
    st.write("**Thailand Clock:**")
    normal_time_display = st.empty()

with accel_col:
    st.write(f"**JTLS Clock ({acceleration}x):**")
    accel_time_display = st.empty()

# Update the clocks every second
while True:
    current_time = datetime.now(bangkok_tz)
    current_normal_time = current_time.strftime("%H:%M:%S")
    
    if current_time.hour >= 8 and current_time.hour < 16:
        current_accel_time = get_accelerated_time(st.session_state.normal_start.replace(hour=8, minute=0, second=0), st.session_state.accel_start, acceleration).strftime("%H:%M:%S")
    else:
        current_accel_time = st.session_state.accel_start.strftime("%H:%M:%S")
    
    normal_time_display.markdown(f"<div style='background-color: lightblue; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_normal_time}</div>", unsafe_allow_html=True)
    accel_time_display.markdown(f"<div style='background-color: orange; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_accel_time}</div>", unsafe_allow_html=True)
    
    time.sleep(1)
