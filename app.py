import streamlit as st
import hashlib
from database import login_user, register_client

st.set_page_config(
    page_title="Complaint Box",
    page_icon="🗳️",
    layout="centered"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none !important;}
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
    .stTextInput label {
        color: rgba(100, 220, 180, 0.8) !important;
        font-size: 12px !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
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
    .stTabs [data-baseweb="tab"] {
        color: rgba(100, 220, 180, 0.6) !important;
    }
    .stTabs [aria-selected="true"] {
        color: rgba(100, 220, 180, 1) !important;
    }
</style>
""", unsafe_allow_html=True)

# Logo + Title
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem;">
    <svg width="70" height="70" viewBox="0 0 70 70" fill="none">
        <polygon points="35,2 65,18 65,52 35,68 5,52 5,18" fill="none" stroke="rgba(100,220,180,0.6)" stroke-width="1.5"/>
        <polygon points="35,10 58,22 58,48 35,60 12,48 12,22" fill="rgba(100,220,180,0.05)" stroke="rgba(100,220,180,0.3)" stroke-width="1"/>
        <line x1="35" y1="2" x2="35" y2="68" stroke="rgba(100,220,180,0.2)" stroke-width="0.8"/>
        <line x1="5" y1="18" x2="65" y2="52" stroke="rgba(100,220,180,0.2)" stroke-width="0.8"/>
        <line x1="65" y1="18" x2="5" y2="52" stroke="rgba(100,220,180,0.2)" stroke-width="0.8"/>
        <rect x="28" y="26" width="14" height="10" rx="2" fill="none" stroke="rgba(100,220,180,0.8)" stroke-width="1.5"/>
        <rect x="31" y="22" width="8" height="5" rx="1" fill="none" stroke="rgba(100,220,180,0.6)" stroke-width="1.2"/>
        <line x1="31" y1="30" x2="39" y2="30" stroke="rgba(100,220,180,0.5)" stroke-width="0.8"/>
        <line x1="31" y1="33" x2="37" y2="33" stroke="rgba(100,220,180,0.5)" stroke-width="0.8"/>
    </svg>
    <h1 style="color:white; letter-spacing:3px; font-size:24px; margin:0.5rem 0 0.2rem;">COMPLAINT BOX</h1>
    <p style="color:rgba(100,220,180,0.8); letter-spacing:3px; font-size:11px; text-transform:uppercase;">Feedback Transformed</p>
    <hr style="border-color:rgba(100,220,180,0.2); margin: 1rem 0;">
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs([" Login", " Register"])

# ---- LOGIN TAB ----
with tab1:
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        if username and password:
            role = login_user(username, password)
            if role == "manager":
                st.session_state["role"] = "manager"
                st.session_state["username"] = username
                st.switch_page("pages/manager_dashboard.py")
            elif role == "client":
                st.session_state["role"] = "client"
                st.session_state["username"] = username
                st.switch_page("pages/client_page.py")
            else:
                st.error(" No account found!")
        else:
            st.warning(" Username aur Password dono bharo!")

# ---- REGISTER TAB ----
with tab2:
    reg_username = st.text_input("Username", key="reg_user")
    reg_password = st.text_input("Password", type="password", key="reg_pass")
    reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register", key="reg_btn"):
        if reg_password != reg_confirm:
            st.error("❌ Passwords match nahi kar rahe!")
        elif len(reg_username) == 0:
            st.error("❌ Username empty nahi hona chahiye!")
        else:
            success = register_client(reg_username, reg_password)
            if success:
                st.success("✅ Account ban gaya! Ab login karo!")
            else:
                st.error("❌ Username already exists!")