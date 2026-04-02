import streamlit as st
from database import get_connection
from speak_fx import speak
import base64
import os
import csv
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASS")
OWNER_EMAIL = os.getenv("OWNER_EMAIL")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
MANAGER_WP = os.getenv("MANAGER_WHATSAPP")

st.set_page_config(page_title="Complaint Box - Client", layout="centered")

st.markdown("""
<style>
    audio {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2e 40%, #1a0d2e 70%, #0a1220 100%);
    }
    .stTextInput input {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(100, 220, 180, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    .stTextInput label, .stTextArea label {
        color: rgba(100, 220, 180, 0.8) !important;
        font-size: 12px !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
    }
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(100, 220, 180, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    .stButton button {
        width: 100% !important;
        background: linear-gradient(135deg, #1a7a5e, #0f5c44) !important;
        border: 1px solid rgba(100, 220, 180, 0.4) !important;
        border-radius: 10px !important;
        color: white !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    .box {
        padding: 1rem;
        border-radius: 14px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(100,220,180,0.2);
        margin-bottom: 1rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

if "role" not in st.session_state or st.session_state["role"] != "client":
    st.error("Access Denied! Pehle login karo!")
    st.stop()

defaults = {
    "step": "welcome",
    "problem": "",
    "home": "",
    "phone": "",
    "welcome_played": False,
    "note_played": False,
    "final_played": False,
    "repeat_welcome_played": False,
    "repeat_note_played": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown("""
<div style="text-align:center; padding: 1rem 0;">
    <h1 style="color:white; letter-spacing:3px; font-size:22px;">COMPLAINT BOX</h1>
    <p style="color:rgba(100,220,180,0.8); letter-spacing:3px; font-size:11px;">Feedback Transformed</p>
    <hr style="border-color:rgba(100,220,180,0.2);">
</div>
""", unsafe_allow_html=True)

def play_voice(text):
    audio_bytes = speak(text)
    if audio_bytes:
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

def export_csv():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints")
    rows = cursor.fetchall()
    conn.close()
    file_name = "complaints.csv"
    with open(file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "username", "house_no", "phone_no", "problem", "status", "time"])
        writer.writerows(rows)
    return file_name

def send_email(house_no, phone_no, problem, file_path):
    if not SENDER_EMAIL or not APP_PASSWORD or not OWNER_EMAIL:
        return
    try:
        msg = EmailMessage()
        msg["Subject"] = "New Complaint Registered!"
        msg["From"] = SENDER_EMAIL
        msg["To"] = OWNER_EMAIL
        msg.set_content(f"""
New Complaint Details:
House Number: {house_no}
Phone Number: {phone_no}
Problem: {problem}
        """)
        with open(file_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="csv", filename="complaints.csv")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        st.error(f"Email error: {e}")

def send_whatsapp(house_no, phone_no, problem):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(
            body=f"New Complaint!\nHouse: {house_no}\nPhone: {phone_no}\nProblem: {problem}",
            from_=TWILIO_FROM,
            to=MANAGER_WP
        )
    except Exception as e:
        st.error(f"WhatsApp error: {e}")

def save_complaint(home, phone, problem):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO complaints (username, house_number, phone_number, problem)
        VALUES (?,?,?,?)
    """, (st.session_state["username"], home, phone, problem))
    conn.commit()
    conn.close()
    file_path = export_csv()
    send_email(home, phone, problem, file_path)
    send_whatsapp(home, phone, problem)

def reset_for_new():
    st.session_state.problem = ""
    st.session_state.home = ""
    st.session_state.phone = ""
    st.session_state.step = "repeat_problem"
    st.session_state.repeat_welcome_played = False
    st.session_state.repeat_note_played = False
    st.session_state.final_played = False

# STEP 1: WELCOME
if st.session_state.step == "welcome":
    st.markdown('<div class="box">Namaste! Complaint Box mein aapka swagat hai.</div>', unsafe_allow_html=True)
    if not st.session_state.welcome_played:
        play_voice("Namaste! Complaint Box mein aapka swagat hai. Aap mujhe apni complaint batayiye.")
        st.session_state.welcome_played = True
    problem = st.text_area("Aapki problem batayiye", placeholder="Jaise: Mere ghar mein paani nahi aa raha...")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Next", use_container_width=True):
            if problem.strip():
                st.session_state.problem = problem.strip()
                st.session_state.step = "details"
                st.rerun()
            else:
                st.error("Pehle apni complaint likho!")
    with col2:
        if st.button("Clear", use_container_width=True):
            st.rerun()

# STEP 2: DETAILS
elif st.session_state.step == "details":
    st.markdown('<div class="box">Complaint note kar li gayi. Ab details dijiye.</div>', unsafe_allow_html=True)
    st.write(f"**Your Complaint:** {st.session_state.problem}")
    if not st.session_state.note_played:
        play_voice("Maine aapki problem note kar li hai. Bahut jaldi solve ho jayegi. Apni details bata dijiye.")
        st.session_state.note_played = True
    home = st.text_input("House Number", placeholder="Jaise: A-12")
    phone = st.text_input("Phone Number", placeholder="10 digit number")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Submit Complaint", use_container_width=True):
            if not home.strip() or not phone.strip():
                st.error("House Number aur Phone Number dono bharo!")
            elif not phone.strip().isdigit() or len(phone.strip()) < 10:
                st.error("Valid phone number dalo (10 digits)!")
            else:
                st.session_state.home = home.strip()
                st.session_state.phone = phone.strip()
                save_complaint(home.strip(), phone.strip(), st.session_state.problem)
                st.session_state.step = "done"
                st.rerun()
    with col2:
        if st.button("Back", use_container_width=True):
            st.session_state.step = "welcome"
            st.rerun()

# STEP 3: DONE
elif st.session_state.step == "done":
    st.success("Complaint successfully registered!")
    st.markdown('<div class="box">Complaint Details</div>', unsafe_allow_html=True)
    st.write(f"**House Number:** {st.session_state.home}")
    st.write(f"**Phone Number:** {st.session_state.phone}")
    st.write(f"**Problem:** {st.session_state.problem}")
    if not st.session_state.final_played:
        play_voice("Okay! Maine aapki problem dekh li hai. Jald hi aapke flat par humare volunteer visit karenge.")
        st.session_state.final_played = True
    st.info("Aapko aur koi problem hai?")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Yes, Another Complaint", use_container_width=True):
            reset_for_new()
            st.rerun()
    with col2:
        if st.button("No, Done", use_container_width=True):
            play_voice("Thank you! Aapki complaint 24 hours mein solve kar di jayegi!")
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()

# STEP 4: REPEAT PROBLEM
elif st.session_state.step == "repeat_problem":
    st.markdown('<div class="box">Dobara Complaint Register Karein</div>', unsafe_allow_html=True)
    if not st.session_state.repeat_welcome_played:
        play_voice("Aapka dobara swagat hai. Aap mujhe apni agli complaint batayiye.")
        st.session_state.repeat_welcome_played = True
    problem = st.text_area("Apni dusri complaint batayiye", placeholder="Jaise: Ghar ke bahar safai nahi hui...")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Next", use_container_width=True, key="repeat_next"):
            if problem.strip():
                st.session_state.problem = problem.strip()
                st.session_state.step = "repeat_details"
                st.rerun()
            else:
                st.error("Pehle apni complaint likho!")
    with col2:
        if st.button("Cancel", use_container_width=True, key="repeat_cancel"):
            st.session_state.step = "done"
            st.rerun()

# STEP 5: REPEAT DETAILS
elif st.session_state.step == "repeat_details":
    st.markdown('<div class="box">Dusri complaint note kar li. Details dijiye.</div>', unsafe_allow_html=True)
    st.write(f"**Second Complaint:** {st.session_state.problem}")
    if not st.session_state.repeat_note_played:
        play_voice("Maine aapki problem note kar li hai. Apni details bata dijiye.")
        st.session_state.repeat_note_played = True
    home = st.text_input("House Number", placeholder="Jaise: B-21", key="repeat_home")
    phone = st.text_input("Phone Number", placeholder="10 digit number", key="repeat_phone")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Submit", use_container_width=True, key="repeat_submit"):
            if not home.strip() or not phone.strip():
                st.error("Dono fields bharo!")
            elif not phone.strip().isdigit() or len(phone.strip()) < 10:
                st.error("Valid phone number dalo!")
            else:
                save_complaint(home.strip(), phone.strip(), st.session_state.problem)
                st.success("Dusri complaint bhi register ho gayi!")
                st.write(f"**House:** {home.strip()}")
                st.write(f"**Phone:** {phone.strip()}")
                st.write(f"**Problem:** {st.session_state.problem}")
                play_voice("Aapko aur koi problem hai?")
                col_a, col_b = st.columns([1, 1])
                with col_a:
                    if st.button("One More", use_container_width=True, key="more"):
                        reset_for_new()
                        st.rerun()
                with col_b:
                    if st.button("Finish", use_container_width=True, key="finish"):
                        play_voice("Thank you! Aapki complaint 24 hours mein solve kar di jayegi!")
                        for k, v in defaults.items():
                            st.session_state[k] = v
                        st.rerun()
    with col2:
        if st.button("Back", use_container_width=True, key="repeat_back"):
            st.session_state.step = "repeat_problem"
            st.rerun()