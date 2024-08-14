import streamlit as st
import time
from datetime import datetime, timedelta
import pytz

# Set the page configuration
st.set_page_config(page_title="JTLS Clock with Custom Speed", layout="wide")

# Initialize the Bangkok time zone
bangkok_tz = pytz.timezone("Asia/Bangkok")

# Initialize state variables if not set
if 'normal_start' not in st.session_state:
    st.session_state.normal_start = datetime.now(bangkok_tz)
if 'accel_start' not in st.session_state:
    st.session_state.accel_start = datetime.now(bangkok_tz).replace(hour=5, minute=0, second=0, microsecond=0)

# Function to calculate the accelerated time based on custom speed
def get_accelerated_time(real_time, accel_start, speed):
    elapsed_real = real_time - st.session_state.normal_start
    elapsed_accel = elapsed_real * speed
    return accel_start + elapsed_accel

# Function to determine the game speed and JTLS start time based on the real time
def get_game_speed_and_jtls_start(real_time):
    hour = real_time.hour
    if hour == 8:
        return 1, datetime.now(bangkok_tz).replace(hour=5, minute=0, second=0, microsecond=0)
    elif hour == 9:
        return 2, datetime.now(bangkok_tz).replace(hour=6, minute=0, second=0, microsecond=0)
    elif hour == 10:
        return 2, datetime.now(bangkok_tz).replace(hour=8, minute=0, second=0, microsecond=0)
    elif hour == 11:
        return 2, datetime.now(bangkok_tz).replace(hour=10, minute=0, second=0, microsecond=0)
    elif hour == 12:
        return 2, datetime.now(bangkok_tz).replace(hour=12, minute=0, second=0, microsecond=0)
    elif hour == 13:
        return 2, datetime.now(bangkok_tz).replace(hour=14, minute=0, second=0, microsecond=0)
    elif hour == 14:
        return 2, datetime.now(bangkok_tz).replace(hour=16, minute=0, second=0, microsecond=0)
    elif hour == 15:
        return 2, datetime.now(bangkok_tz).replace(hour=18, minute=0, second=0, microsecond=0)
    elif hour == 16:
        return 1, datetime.now(bangkok_tz).replace(hour=19, minute=0, second=0, microsecond=0)
    else:
        return 1, datetime.now(bangkok_tz).replace(hour=5, minute=0, second=0, microsecond=0)

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
    
    # Get game speed and JTLS start time based on the real time
    speed, jtls_start_time = get_game_speed_and_jtls_start(current_time)
    
    # Calculate the accelerated time based on the current speed
    current_accel_time = get_accelerated_time(current_time, jtls_start_time, speed).strftime("%H:%M:%S")
    
    normal_time_display.markdown(f"<div style='background-color: lightblue; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_normal_time}</div>", unsafe_allow_html=True)
    accel_time_display.markdown(f"<div style='background-color: orange; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_accel_time}</div>", unsafe_allow_html=True)
    
    time.sleep(1)
