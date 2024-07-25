import streamlit as st
import time
from datetime import datetime, timedelta

# Set up the layout
st.title("Real-World Clock vs. Accelerated Clock")

# Input for start time
start_time = st.time_input("Select start time", datetime.now().time())

# Acceleration adjustment
acceleration = st.slider("Select acceleration factor", 1, 10, 3)

# Apply changes button
if st.button("Apply Changes"):
    st.session_state.real_start = datetime.combine(datetime.today(), start_time)
    st.session_state.accel_start = datetime.combine(datetime.today(), start_time)
    st.session_state.acceleration = acceleration

# Initialize state variables if not set
if 'real_start' not in st.session_state:
    st.session_state.real_start = datetime.combine(datetime.today(), start_time)
if 'accel_start' not in st.session_state:
    st.session_state.accel_start = datetime.combine(datetime.today(), start_time)
if 'acceleration' not in st.session_state:
    st.session_state.acceleration = acceleration

# Function to calculate the accelerated time
def get_accelerated_time(real_start, accel_start, multiplier=3):
    elapsed_real = datetime.now() - real_start
    elapsed_accel = elapsed_real * multiplier
    return accel_start + elapsed_accel

# Display clocks
st.write("### Clocks:")
real_col, accel_col = st.columns(2)

with real_col:
    st.write("**Real-World Time:**")
    real_time_display = st.empty()

with accel_col:
    st.write(f"**JTLS Time ({st.session_state.acceleration}x):**")
    accel_time_display = st.empty()

# Update the clocks every second
while True:
    current_real_time = datetime.now().strftime("%H:%M:%S")
    current_accel_time = get_accelerated_time(st.session_state.real_start, st.session_state.accel_start, st.session_state.acceleration).strftime("%H:%M:%S")
    
    real_time_display.markdown(f"<div style='background-color: lightblue; padding: 10px; font-size: 80px; text-align: center;'>{current_real_time}</div>", unsafe_allow_html=True)
    accel_time_display.markdown(f"<div style='background-color: lightorange; padding: 10px; font-size: 80px; text-align: center;'>{current_accel_time}</div>", unsafe_allow_html=True)
    
    time.sleep(1)
