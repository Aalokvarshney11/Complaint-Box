import streamlit as st
from database import get_all_complaints, get_unsolved_complaints, get_solved_complaints, mark_solved
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Manager Dashboard", layout="wide")

# CSS
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none !important;}
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2e 40%, #1a0d2e 70%, #0a1220 100%);
    }
</style>
""", unsafe_allow_html=True)

# Session check
if "role" not in st.session_state or st.session_state["role"] != "manager":
    st.error(" Access Denied!")
    st.stop()

# Sidebar
st.sidebar.markdown("### 🗳️ Complaint Box")
st.sidebar.markdown("---")
page = st.sidebar.radio("Menu", [" Dashboard", " Unsolved", " Solved"])

# ---- DASHBOARD PAGE ----
if page == " Dashboard":
    st.title(" All Complaints")
    complaints = get_all_complaints()
    
    if len(complaints) == 0:
        st.info("Abhi koi complaint nahi hai!")
    else:
        for c in complaints:
            with st.expander(f" Complaint #{c[0]} — {c[4][:50]}"):
                st.write(f"** Client:** {c[1]}")
                st.write(f"** House No:** {c[2]}")
                st.write(f"** Phone:** {c[3]}")
                st.write(f"** Problem:** {c[4]}")
                st.write(f"** Time:** {c[6]}")
                st.write(f"**Status:** {c[5]}")

# ---- UNSOLVED PAGE ----
elif page == " Unsolved":
    st.title(" Unsolved Complaints")
    complaints = get_unsolved_complaints()
    
    if len(complaints) == 0:
        st.success("✅ Saari complaints solve ho gayi!")
    else:
        for c in complaints:
            with st.expander(f"Complaint #{c[0]} — {c[1]}"):
                st.write(f"** House No:** {c[2]}")
                st.write(f"** Phone:** {c[3]}")
                st.write(f"** Problem:** {c[4]}")
                st.write(f"** Time:** {c[6]}")
                if st.button(f" Mark Solved", key=f"solve_{c[0]}"):
                    mark_solved(c[0])
                    st.success("Complaint solved mark ho gayi!")
                    st.rerun()

# ---- SOLVED PAGE ----
elif page == " Solved":
    st.title(" Solved Complaints")
    complaints = get_solved_complaints()
    
    if len(complaints) == 0:
        st.info("Abhi koi solved complaint nahi hai!")
    else:
        df = pd.DataFrame(complaints, columns=["ID", "Username", "House No", "Phone", "Problem", "Status", "Time"])
        st.dataframe(df)
        
        # Excel download
        excel_file = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=" Download Excel",
            data=excel_file,
            file_name="solved_complaints.csv",
            mime="text/csv"
        )