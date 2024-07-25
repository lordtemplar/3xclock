import streamlit as st
import time
from datetime import datetime, timedelta

# Set up the layout
st.title("Normal Clock vs. Accelerated Clock")

# Initialize state variables if not set
if 'normal_start' not in st.session_state:
    st.session_state.normal_start = datetime.now()
if 'accel_start' not in st.session_state:
    st.session_state.accel_start = datetime.now()
if 'acceleration' not in st.session_state:
    st.session_state.acceleration = 3

# Function to calculate the accelerated time
def get_accelerated_time(real_start, accel_start, multiplier=3):
    elapsed_real = datetime.now() - real_start
    elapsed_accel = elapsed_real * multiplier
    return accel_start + elapsed_accel

# Display clocks
st.write("### Clocks:")
normal_col, accel_col = st.columns(2)

with normal_col:
    st.write("**Normal Clock:**")
    normal_time_display = st.empty()

with accel_col:
    st.write(f"**Accelerated Time ({st.session_state.acceleration}x):**")
    accel_time_display = st.empty()

# Update the clocks every second
while True:
    current_normal_time = (st.session_state.normal_start + (datetime.now() - st.session_state.normal_start)).strftime("%H:%M:%S")
    current_accel_time = get_accelerated_time(st.session_state.normal_start, st.session_state.accel_start, st.session_state.acceleration).strftime("%H:%M:%S")
    
    normal_time_display.markdown(f"<div style='background-color: lightblue; padding: 10px; font-size: 80px; text-align: center;'>{current_normal_time}</div>", unsafe_allow_html=True)
    accel_time_display.markdown(f"<div style='background-color: orange; padding: 10px; font-size: 80px; text-align: center;'>{current_accel_time}</div>", unsafe_allow_html=True)
    
    time.sleep(1)
