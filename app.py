import streamlit as st
from ultralytics import YOLO
import cv2
import smtplib
import os
import time
import pandas as pd
from email.message import EmailMessage
from datetime import datetime
from PIL import Image
import tempfile

# --- 1. DIRECTORY SETUP ---
BASE_DIR = "detections_history"
DIRS = {"images": f"{BASE_DIR}/images", "videos": f"{BASE_DIR}/videos", "webcam": f"{BASE_DIR}/webcam"}
for folder in DIRS.values():
    os.makedirs(folder, exist_ok=True)

CSV_PATH = f"{BASE_DIR}/detections_log.csv"

# --- 2. SIDEBAR SETUP ---
st.set_page_config(page_title="AI Safety Guard Pro", layout="wide")
st.sidebar.title("🛡️ Admin Control Panel")

if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False
if 'last_alert_time' not in st.session_state:
    st.session_state.last_alert_time = 0

if st.sidebar.button("📧 Email Settings (Hide/Show)"):
    st.session_state.show_settings = not st.session_state.show_settings

sender_email = "your-email@gmail.com"
sender_password = ""
admin_email = "admin@example.com"
alert_cooldown = 60

if st.session_state.show_settings:
    st.sidebar.markdown("---")
    sender_email = st.sidebar.text_input("Sender Email", value=sender_email)
    show_pass = st.sidebar.checkbox("Show Password")
    sender_password = st.sidebar.text_input("Google App Password", type="default" if show_pass else "password")
    admin_email = st.sidebar.text_input("Admin Email", value=admin_email)
    alert_cooldown = st.sidebar.slider("Alert Cooldown (Seconds)", 30, 600, 60)

st.sidebar.markdown("### 🎮 Controls")
stop_monitor = st.sidebar.checkbox("🛑 KILL ALL PROCESSES")
show_logs = st.sidebar.checkbox("Show Detailed Logs", value=True)

# --- 3. CORE FUNCTIONS ---
@st.cache_resource
def load_model():
    return YOLO("best.pt")

def log_to_csv(type_name, filename, violations_list):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    has_violation = len(violations_list) > 0
    v_text = ", ".join(violations_list) if has_violation else "None"
    status = "🔴 ALERT (NOT SAFE)" if has_violation else "🟢 SAFE"
    
    new_data = {
        "Timestamp": now, "Source": type_name, "File": filename,
        "Violations": v_text.replace(',', '|'), "Status": status
    }
    df = pd.DataFrame([new_data])
    df.to_csv(CSV_PATH, mode='a', header=not os.path.exists(CSV_PATH), index=False)

def send_email_alert(frame, violation_text):
    if not sender_password: return
    try:
        msg = EmailMessage()
        msg['Subject'] = f"🚨 SAFETY ALERT: {violation_text}"
        msg['From'] = sender_email
        msg['To'] = admin_email
        msg.set_content(f"Violation Detected: {violation_text}\nTime: {datetime.now()}")
        _, buffer = cv2.imencode('.jpg', frame)
        msg.add_attachment(buffer.tobytes(), maintype='image', subtype='jpeg', filename="alert.jpg")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
    except: pass

# --- 4. MAIN APP ---
st.title("👷‍♂️ AI PPE Safety Monitor")
model = load_model()
source = st.radio("Select Mode", ("Live Webcam", "Upload Video", "Upload Image"), horizontal=True)

# --- WEBCAM MODE ---
if source == "Live Webcam":
    run = st.checkbox("Start Monitoring")
    st_frame = st.empty()
    if run and not stop_monitor:
        cap = cv2.VideoCapture(0)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        vid_name = f"webcam_{ts}.mp4"
        out = cv2.VideoWriter(os.path.join(DIRS["webcam"], vid_name), cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (640, 480))
        try:
            while run and not stop_monitor:
                ret, frame = cap.read()
                if not ret: break
                frame = cv2.resize(frame, (640, 480))
                res = model(frame)
                plotted = res[0].plot()
                out.write(plotted)
                v_list = [model.names[int(c)] for c in res[0].boxes.cls if "NO-" in model.names[int(c)]]
                if v_list:
                    curr_time = time.time()
                    if (curr_time - st.session_state.last_alert_time) > alert_cooldown:
                        log_to_csv("Webcam", vid_name, v_list)
                        send_email_alert(plotted, ", ".join(v_list))
                        st.session_state.last_alert_time = curr_time
                st_frame.image(plotted, channels="BGR", use_container_width=True)
        finally:
            cap.release()
            out.release()
            st.rerun()

# --- VIDEO MODE (STABLE FIX) ---
elif source == "Upload Video":
    up_vid = st.file_uploader("Upload Video", type=['mp4', 'avi'])
    if up_vid:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(up_vid.read())
        
        col1, col2 = st.columns(2)
        start_btn = col1.button("🚀 Start Processing Video")
        stop_btn = col2.button("⏹️ Stop & Save Now")

        if start_btn:
            cap = cv2.VideoCapture(tfile.name)
            fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_path = os.path.join(DIRS["videos"], f"temp_{ts}.mp4")
            width, height = int(cap.get(3)), int(cap.get(4))
            out = cv2.VideoWriter(temp_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
            
            st_frame = st.empty()
            progress_bar = st.progress(0)
            found_violations = []
            
            frame_idx = 0
            while cap.isOpened():
                # Check for manual stop button or sidebar kill switch
                if stop_btn or stop_monitor:
                    break
                
                ret, frame = cap.read()
                if not ret: break
                
                results = model(frame)
                v_in_frame = [model.names[int(c)] for c in results[0].boxes.cls if "NO-" in model.names[int(c)]]
                for v in v_in_frame:
                    if v not in found_violations: found_violations.append(v)
                
                plotted = results[0].plot()
                out.write(plotted)
                st_frame.image(plotted, channels="BGR", use_container_width=True)
                
                frame_idx += 1
                if total_frames > 0:
                    progress_bar.progress(min(frame_idx / total_frames, 1.0))

            cap.release()
            out.release()
            time.sleep(1) # Buffer time for file system

            v_tag = "_".join(found_violations) if found_violations else "SAFE"
            final_name = f"video_{v_tag}_{ts}.mp4"
            final_path = os.path.join(DIRS["videos"], final_name)
            
            if os.path.exists(temp_path):
                os.rename(temp_path, final_path)
                log_to_csv("Video", final_name, found_violations)
                st.success(f"✅ Video Logged & Saved: {final_name}")
                time.sleep(1)
                st.rerun()

# --- IMAGE MODE ---
elif source == "Upload Image":
    file = st.file_uploader("Upload Image", type=['jpg', 'png'])
    if file:
        img = Image.open(file)
        results = model(img)
        res_plotted = results[0].plot()
        st.image(res_plotted, use_container_width=True)
        violations = [model.names[int(c)] for c in results[0].boxes.cls if "NO-" in model.names[int(c)]]
        if st.button("💾 Save Analysis"):
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            v_tag = "_".join(violations) if violations else "SAFE"
            fname = f"img_{v_tag}_{ts}.jpg"
            cv2.imwrite(os.path.join(DIRS["images"], fname), cv2.cvtColor(res_plotted, cv2.COLOR_RGB2BGR))
            log_to_csv("Image", fname, violations)
            st.success(f"Saved: {fname}")
            st.rerun()

# --- 5. LOG DISPLAY (NEWEST FIRST) ---
if show_logs and os.path.exists(CSV_PATH):
    st.markdown("---")
    st.markdown("### 📊 Enterprise Safety Logs")
    df = pd.read_csv(CSV_PATH, on_bad_lines='skip', engine="python")
    st.dataframe(df.iloc[::-1].head(15).style.applymap(
        lambda x: 'color: red' if 'ALERT' in str(x) else 'color: green', 
        subset=['Status']
    ), use_container_width=True)