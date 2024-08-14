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
    st.session_state.normal_start = datetime.now(bangkok_tz).replace(hour=8, minute=0, second=0, microsecond=0)
if 'accel_start' not in st.session_state:
    st.session_state.accel_start = datetime.now(bangkok_tz).replace(hour=5, minute=0, second=0, microsecond=0)

# Function to calculate the accelerated time based on the speed
def get_accelerated_time(real_time, accel_start, speed):
    elapsed_real = real_time - st.session_state.normal_start
    elapsed_accel = elapsed_real * speed
    return accel_start + elapsed_accel

# Function to determine the game speed and time based on the real time
def get_game_speed_and_jtls_time(real_time):
    hour = real_time.hour
    if hour == 8:  # From 08:00 to 09:00, game speed is 1x
        return 1, st.session_state.accel_start
    elif hour >= 9 and hour < 15:  # From 09:00 to 15:00, game speed is 2x
        return 2, st.session_state.accel_start + timedelta(hours=1)  # JTLS should have progressed to 06:00 at 09:00
    elif hour == 15:  # At 15:00, game speed is 1x again
        return 1, st.session_state.accel_start + timedelta(hours=8)  # JTLS should be at 18:00 at 15:00
    elif hour == 16:  # From 16:00 to 17:00, continue 1x speed until JTLS reaches 19:00
        return 1, st.session_state.accel_start + timedelta(hours=9)
    else:
        return 1, st.session_state.accel_start + timedelta(hours=9)  # Stop at 19:00

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
    
    # Get the current game speed and JTLS time based on the real time
    speed, jtls_time = get_game_speed_and_jtls_time(current_time)
    
    # Calculate the accelerated time based on the current speed
    current_accel_time = get_accelerated_time(current_time, jtls_time, speed).strftime("%H:%M:%S")
    
    normal_time_display.markdown(f"<div style='background-color: lightblue; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_normal_time}</div>", unsafe_allow_html=True)
    accel_time_display.markdown(f"<div style='background-color: orange; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_accel_time}</div>", unsafe_allow_html=True)
    
    time.sleep(1)
