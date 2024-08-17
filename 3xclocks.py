import streamlit as st
import time
from datetime import datetime, timedelta
import pytz

# Set the page configuration
st.set_page_config(page_title="JTLS Clock", layout="wide")

# Initialize the Bangkok time zone
bangkok_tz = pytz.timezone("Asia/Bangkok")

# Set the start times
real_start = datetime.now(bangkok_tz).replace(hour=8, minute=0, second=0, microsecond=0)
jtls_start = datetime.now(bangkok_tz).replace(hour=5, minute=0, second=0, microsecond=0)

# Function to calculate the accelerated JTLS time
def calculate_jtls_time(real_time):
    real_elapsed = real_time - real_start
    
    if real_time.hour < 8:
        return jtls_start  # Before 08:00, JTLS time is frozen at 05:00
    elif real_time.hour < 9:  # From 08:00 to 09:00 - 1x speed
        jtls_elapsed = real_elapsed
    elif real_time.hour < 15:  # From 09:00 to 15:00 - 2x speed
        jtls_elapsed = timedelta(hours=1) + (real_elapsed - timedelta(hours=1)) * 2
    elif real_time.hour < 16:  # From 15:00 to 16:00 - 1x speed again
        jtls_elapsed = timedelta(hours=8) + (real_elapsed - timedelta(hours=7))
    else:  # After 16:00, JTLS time stops at 19:00
        return jtls_start + timedelta(hours=14)
    
    return jtls_start + jtls_elapsed

# Display clocks
st.write("### JTLS Clocks:")
normal_col, accel_col = st.columns(2)

with normal_col:
    st.write("**Thailand Clock:**")
    normal_time_display = st.empty()

with accel_col:
    st.write("**JTLS Clock:**")
    accel_time_display = st.empty()

# Update the clocks every second
while True:
    current_time = datetime.now(bangkok_tz)
    current_normal_time = current_time.strftime("%H:%M:%S")
    
    if 8 <= current_time.hour < 16:
        current_jtls_time = calculate_jtls_time(current_time).strftime("%H:%M:%S")
    else:
        current_jtls_time = (jtls_start + timedelta(hours=14)).strftime("%H:%M:%S")
    
    normal_time_display.markdown(f"<div style='background-color: lightblue; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_normal_time}</div>", unsafe_allow_html=True)
    accel_time_display.markdown(f"<div style='background-color: orange; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_jtls_time}</div>", unsafe_allow_html=True)
    
    time.sleep(1)
