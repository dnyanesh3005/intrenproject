"""
app.py — LeadTrack Home Page (Streamlit entry point)
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from services.db import init_db

# Initialize DB on startup
init_db()

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LeadTrack — Lead Management System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Hide Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* App background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stSelectbox label { color: rgba(255,255,255,0.7) !important; }

/* Hero section */
.hero-container {
    text-align: center;
    padding: 60px 20px;
    animation: fadeInUp 0.8s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
.hero-badge {
    display: inline-block;
    background: rgba(102, 126, 234, 0.2);
    border: 1px solid rgba(102, 126, 234, 0.5);
    color: #a5b4fc;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 20px;
    border-radius: 50px;
    margin-bottom: 28px;
}
.hero-title {
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    letter-spacing: -2px;
    margin-bottom: 20px;
}
.hero-title span {
    background: linear-gradient(135deg, #667eea, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 18px;
    color: rgba(255,255,255,0.6);
    max-width: 560px;
    margin: 0 auto 40px;
    line-height: 1.7;
}

/* Feature cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 20px;
    margin: 40px 0;
}
.feature-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 28px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    cursor: default;
    animation: fadeInUp 0.8s ease;
}
.feature-card:hover {
    background: rgba(255,255,255,0.1);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}
.feature-icon { font-size: 36px; margin-bottom: 16px; }
.feature-title { font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 10px; }
.feature-desc { font-size: 14px; color: rgba(255,255,255,0.55); line-height: 1.65; }

/* Stats row */
.stat-row {
    display: flex;
    justify-content: center;
    gap: 60px;
    padding: 40px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    margin: 20px 0;
}
.stat-item { text-align: center; }
.stat-number {
    font-size: 40px;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label { font-size: 13px; color: rgba(255,255,255,0.5); font-weight: 500; margin-top: 4px; }

/* Flow diagram */
.flow-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 30px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    margin: 20px 0;
    flex-wrap: wrap;
}
.flow-step {
    background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
    border: 1px solid rgba(102,126,234,0.4);
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
    min-width: 120px;
}
.flow-icon { font-size: 24px; margin-bottom: 6px; }
.flow-label { font-size: 12px; font-weight: 600; color: #a5b4fc; }
.flow-arrow { font-size: 20px; color: rgba(255,255,255,0.3); }

/* Tech stack badges */
.tech-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin: 20px 0;
}
.tech-badge {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.8);
    font-size: 13px;
    font-weight: 500;
    padding: 8px 18px;
    border-radius: 50px;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 LeadTrack")
    st.markdown("---")
    st.markdown("""
    **Navigation**
    - 📋 [Lead Form](/Lead_Form)
    - 📊 [Dashboard](/Dashboard)
    - 🗂️ [Admin Panel](/Admin)
    """)
    st.markdown("---")
    st.markdown("""
    <div style='font-size:12px; color:rgba(255,255,255,0.4);'>
    Built with Streamlit + FastAPI<br>
    SQLite · Gmail SMTP · Gemini AI
    </div>
    """, unsafe_allow_html=True)

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">✨ Automated Lead Management</div>
    <h1 class="hero-title">
        Capture, Track &<br>
        <span>Convert Leads</span><br>
        Automatically
    </h1>
    <p class="hero-subtitle">
        A full-stack system that captures leads, sends personalized emails, 
        tracks opens & clicks in real-time, and displays live analytics.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Quick Navigation ─────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📋 Submit a Lead", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Lead_Form.py")
with col2:
    if st.button("📊 View Dashboard", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")
with col3:
    if st.button("🗂️ Admin Panel", use_container_width=True):
        st.switch_page("pages/3_Admin.py")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Features ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <div class="feature-title">Smart Lead Capture</div>
        <div class="feature-desc">Beautiful form that collects name, email, phone, company & requirement with real-time validation.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📧</div>
        <div class="feature-title">Automated Emails</div>
        <div class="feature-desc">Personalized HTML emails sent instantly via Gmail SMTP with the lead's name & requirement.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">👁️</div>
        <div class="feature-title">Open Tracking</div>
        <div class="feature-desc">1×1 tracking pixel detects when emails are opened and logs the timestamp.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔗</div>
        <div class="feature-title">Click Tracking</div>
        <div class="feature-desc">Every link in the email is trackable — logs clicks and seamlessly redirects users.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Live Analytics</div>
        <div class="feature-desc">Real-time dashboard showing open rates, click rates, leads over time, and more.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Classification</div>
        <div class="feature-desc">Gemini AI auto-classifies each lead's requirement by category and priority.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Flow Diagram ─────────────────────────────────────────────────────────────
st.markdown("### 🔄 How It Works")
st.markdown("""
<div class="flow-container">
    <div class="flow-step">
        <div class="flow-icon">📋</div>
        <div class="flow-label">Lead Submits Form</div>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-step">
        <div class="flow-icon">💾</div>
        <div class="flow-label">Saved to SQLite</div>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-step">
        <div class="flow-icon">🤖</div>
        <div class="flow-label">AI Classifies</div>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-step">
        <div class="flow-icon">📧</div>
        <div class="flow-label">Email Sent</div>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-step">
        <div class="flow-icon">👁️</div>
        <div class="flow-label">Opens Tracked</div>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-step">
        <div class="flow-icon">🔗</div>
        <div class="flow-label">Clicks Tracked</div>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-step">
        <div class="flow-icon">📊</div>
        <div class="flow-label">Dashboard</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tech Stack ───────────────────────────────────────────────────────────────
st.markdown("### 🛠️ Technology Stack")
st.markdown("""
<div class="tech-grid">
    <span class="tech-badge">🐍 Python 3.10+</span>
    <span class="tech-badge">⚡ Streamlit</span>
    <span class="tech-badge">🔌 FastAPI</span>
    <span class="tech-badge">🗄️ SQLite</span>
    <span class="tech-badge">📧 Gmail SMTP</span>
    <span class="tech-badge">🤖 Google Gemini AI</span>
    <span class="tech-badge">📈 Plotly Express</span>
    <span class="tech-badge">🔗 Uvicorn</span>
</div>
""", unsafe_allow_html=True)
