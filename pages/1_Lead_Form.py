"""
pages/1_Lead_Form.py — Lead Capture Form
"""

import streamlit as st
import sys
import os
import re
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.db import init_db, insert_lead, insert_email_event, mark_email_sent, update_ai_fields
from services.email_service import send_email
from services.ai_service import classify_lead

init_db()

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Submit a Lead — LeadTrack",
    page_icon="📋",
    layout="centered",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] * { color: white !important; }

/* Form container */
.form-header {
    text-align: center;
    padding: 40px 0 30px;
    animation: fadeInUp 0.6s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.form-badge {
    display: inline-block;
    background: rgba(102,126,234,0.2);
    border: 1px solid rgba(102,126,234,0.5);
    color: #a5b4fc;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 50px;
    margin-bottom: 20px;
}
.form-title {
    font-size: 36px;
    font-weight: 800;
    color: #fff;
    letter-spacing: -1.5px;
    margin-bottom: 10px;
}
.form-subtitle {
    font-size: 16px;
    color: rgba(255,255,255,0.55);
}

/* Form fields */
.stTextInput > label,
.stTextArea > label,
.stSelectbox > label { color: rgba(255,255,255,0.8) !important; font-weight: 500 !important; font-size: 14px !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
    font-size: 15px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(102,126,234,0.7) !important;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.15) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder { color: rgba(255,255,255,0.3) !important; }

/* Submit button */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 0 !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(102,126,234,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(102,126,234,0.6) !important;
}

/* Success banner */
.success-card {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.15));
    border: 1px solid rgba(16,185,129,0.4);
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    animation: fadeInUp 0.5s ease;
}
.success-icon { font-size: 56px; margin-bottom: 16px; }
.success-title { font-size: 24px; font-weight: 700; color: #34d399; margin-bottom: 10px; }
.success-text { font-size: 15px; color: rgba(255,255,255,0.7); line-height: 1.6; }

/* AI pill */
.ai-result {
    display: inline-flex;
    gap: 12px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 50px;
    padding: 8px 20px;
    margin-top: 12px;
}
.ai-pill {
    font-size: 13px;
    font-weight: 600;
    color: rgba(255,255,255,0.8);
}
.priority-high { color: #f87171; }
.priority-medium { color: #fbbf24; }
.priority-low { color: #34d399; }

/* Error */
.error-card {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 12px;
    padding: 16px 20px;
    color: #fca5a5;
    font-size: 14px;
}

/* Divider */
.section-divider {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 LeadTrack")
    st.markdown("---")
    st.markdown("""
    **Navigation**
    - 🏠 [Home](/)
    - 📋 **Lead Form** ← You are here
    - 📊 [Dashboard](/Dashboard)
    - 🗂️ [Admin Panel](/Admin)
    """)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="form-header">
    <div class="form-badge">📋 Lead Submission</div>
    <h1 class="form-title">Get In Touch</h1>
    <p class="form-subtitle">Fill out the form below and we'll get back to you within 24 hours</p>
</div>
""", unsafe_allow_html=True)

# ─── Form ─────────────────────────────────────────────────────────────────────
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    with st.form("lead_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name *", placeholder="e.g. Rahul Sharma")
        with col2:
            email = st.text_input("📧 Email Address *", placeholder="e.g. rahul@gmail.com")

        col3, col4 = st.columns(2)
        with col3:
            phone = st.text_input("📞 Phone Number *", placeholder="e.g. 9876543210")
        with col4:
            company = st.text_input("🏢 Company Name (Optional)", placeholder="e.g. ABC Pvt Ltd")

        requirement = st.text_area(
            "💬 Requirement / Message *",
            placeholder="Tell us what you need — e.g. 'I need an AI chatbot for my website'",
            height=130,
        )

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.markdown(
                "<p style='color:rgba(255,255,255,0.4);font-size:12px;'>* Required fields. Your info is kept confidential.</p>",
                unsafe_allow_html=True,
            )
        with col_right:
            submitted = st.form_submit_button("🚀 Submit Lead", use_container_width=True)

    # ─── Validation & Processing ────────────────────────────────────────────
    if submitted:
        errors = []

        if not name.strip():
            errors.append("Full Name is required.")
        if not email.strip() or not re.match(r"^[^@]+@[^@]+\.[^@]+$", email.strip()):
            errors.append("A valid Email Address is required.")
        if not phone.strip() or not re.match(r"^\+?[\d\s\-]{7,15}$", phone.strip()):
            errors.append("A valid Phone Number is required.")
        if not requirement.strip() or len(requirement.strip()) < 10:
            errors.append("Requirement must be at least 10 characters.")

        if errors:
            for err in errors:
                st.markdown(f'<div class="error-card">⚠️ {err}</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Processing your lead..."):
                # 1. Save to DB
                lead_id = insert_lead(
                    name.strip(), email.strip(), phone.strip(),
                    company.strip() or None, requirement.strip()
                )

                # 2. AI Classification
                category, priority = classify_lead(requirement.strip())
                update_ai_fields(lead_id, category, priority)

                # 3. Send Email
                tracking_id, email_error = send_email(lead_id, name.strip(), email.strip(), requirement.strip())

                if tracking_id:
                    insert_email_event(lead_id, tracking_id)
                    mark_email_sent(lead_id)

                # Store results in session state
                st.session_state.submitted = True
                st.session_state.lead_name = name.strip()
                st.session_state.lead_email = email.strip()
                st.session_state.ai_category = category
                st.session_state.ai_priority = priority
                st.session_state.email_sent = tracking_id is not None
                st.session_state.email_error = email_error

            st.rerun()

else:
    # ─── Success State ────────────────────────────────────────────────────────
    priority_class = {
        "High": "priority-high",
        "Medium": "priority-medium",
        "Low": "priority-low",
    }.get(st.session_state.get("ai_priority", "Medium"), "priority-medium")

    email_status = "✅ Confirmation email sent!" if st.session_state.get("email_sent") else (
        f"⚠️ Email not sent: {st.session_state.get('email_error', 'Unknown error')}"
    )

    st.markdown(f"""
    <div class="success-card">
        <div class="success-icon">🎉</div>
        <div class="success-title">Lead Submitted Successfully!</div>
        <div class="success-text">
            Thank you, <strong>{st.session_state.get('lead_name', '')}</strong>!
            Your lead has been saved and our team will get back to you at
            <strong>{st.session_state.get('lead_email', '')}</strong> within 24 hours.<br><br>
            {email_status}
        </div>
        <div class="ai-result">
            <span class="ai-pill">🤖 Category: <strong>{st.session_state.get('ai_category', 'General')}</strong></span>
            <span class="ai-pill">⚡ Priority: <strong class="{priority_class}">{st.session_state.get('ai_priority', 'Medium')}</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Submit Another Lead", use_container_width=True, type="primary"):
            for key in ["submitted", "lead_name", "lead_email", "ai_category", "ai_priority", "email_sent", "email_error"]:
                st.session_state.pop(key, None)
            st.rerun()
    with col2:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.switch_page("pages/2_Dashboard.py")
    with col3:
        if st.button("🗂️ Admin Panel", use_container_width=True):
            st.switch_page("pages/3_Admin.py")
