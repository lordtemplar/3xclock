import streamlit as st  # นำเข้าโมดูล Streamlit สำหรับสร้างเว็บแอปพลิเคชัน
import time  # นำเข้าโมดูล time สำหรับการหน่วงเวลา
from datetime import datetime, timedelta  # นำเข้าโมดูล datetime สำหรับจัดการวันที่และเวลา
import pytz  # นำเข้าโมดูล pytz สำหรับจัดการโซนเวลา

# ตั้งค่าหน้าจอของเว็บแอป
st.set_page_config(page_title="JTLS Clock", layout="wide")

# กำหนดโซนเวลาเป็นกรุงเทพฯ
bangkok_tz = pytz.timezone("Asia/Bangkok")

# กำหนดเวลาเริ่มต้นของเวลาจริงและเวลา JTLS
real_start = datetime.now(bangkok_tz).replace(hour=8, minute=0, second=0, microsecond=0)
jtls_start = datetime.now(bangkok_tz).replace(hour=5, minute=0, second=0, microsecond=0)

# ฟังก์ชันสำหรับคำนวณเวลา JTLS ที่เร่งความเร็ว
def calculate_jtls_time(real_time):
    real_elapsed = real_time - real_start
    
    if real_time.hour < 8:
        return jtls_start  # ก่อน 08:00 น., เวลา JTLS จะหยุดที่ 05:00 น.
    elif real_time.hour < 9:  # ตั้งแต่ 08:00 ถึง 09:00 น. เวลา JTLS เดินที่ความเร็วปกติ
        jtls_elapsed = real_elapsed
    elif real_time.hour < 15:  # ตั้งแต่ 09:00 ถึง 15:00 น. เวลา JTLS เดินที่ความเร็ว 2 เท่า
        jtls_elapsed = timedelta(hours=1) + (real_elapsed - timedelta(hours=1)) * 2
    elif real_time.hour < 16:  # ตั้งแต่ 15:00 ถึง 16:00 น. เวลา JTLS เดินที่ความเร็วปกติ
        jtls_elapsed = timedelta(hours=8) + (real_elapsed - timedelta(hours=7))
    else:  # หลัง 16:00 น. เวลา JTLS จะหยุดที่ 19:00 น.
        return jtls_start + timedelta(hours=14)
    
    return jtls_start + jtls_elapsed

# แสดงนาฬิกาบนหน้าเว็บ
st.write("### JTLS Clocks:")
normal_col, accel_col = st.columns(2)

with normal_col:
    st.write("**Thailand Clock:**")
    normal_time_display = st.empty()

with accel_col:
    st.write("**JTLS Clock:**")
    accel_time_display = st.empty()

# อัพเดทนาฬิกาทุกวินาที
while True:
    current_time = datetime.now(bangkok_tz)  # ดึงเวลาในโซนเวลาปัจจุบัน
    current_normal_time = current_time.strftime("%H:%M:%S")  # แปลงเวลาเป็นรูปแบบ 24 ชั่วโมงสำหรับการแสดงผล
    
    if 8 <= current_time.hour < 16:
        current_jtls_time = calculate_jtls_time(current_time).strftime("%H:%M:%S")
    else:
        current_jtls_time = (jtls_start + timedelta(hours=14)).strftime("%H:%M:%S")
    
    normal_time_display.markdown(
        f"<div style='background-color: lightblue; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_normal_time}</div>", 
        unsafe_allow_html=True
    )
    accel_time_display.markdown(
        f"<div style='background-color: orange; padding: 10px; font-size: 60px; text-align: center; color: black;'>{current_jtls_time}</div>", 
        unsafe_allow_html=True
    )
    
    time.sleep(1)  # หน่วงเวลา 1 วินาที
