"""
pages/3_Admin.py — Admin Panel: View & Manage All Leads
"""

import streamlit as st
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.db import init_db, get_all_leads

init_db()

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Admin Panel — LeadTrack",
    page_icon="🗂️",
    layout="wide",
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

/* Header */
.admin-header { padding: 32px 0 20px; }
.admin-badge {
    display: inline-block;
    background: rgba(251,191,36,0.15);
    border: 1px solid rgba(251,191,36,0.4);
    color: #fbbf24;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 50px;
    margin-bottom: 14px;
}
.admin-title { font-size: 40px; font-weight: 800; color: #fff; letter-spacing: -2px; margin-bottom: 6px; }
.admin-subtitle { font-size: 15px; color: rgba(255,255,255,0.5); }

/* Filter bar */
.filter-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
}

/* Table styling */
.stDataFrame { border-radius: 12px !important; }

/* Summary pills */
.summary-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.summary-pill {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 50px;
    padding: 8px 18px;
    font-size: 13px;
    color: rgba(255,255,255,0.7);
    font-weight: 500;
}
.summary-pill strong { color: white; }

/* Selectbox & multiselect */
.stSelectbox label, .stMultiSelect label { color: rgba(255,255,255,0.7) !important; font-size: 13px !important; }
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: rgba(255,255,255,0.4);
}
.empty-icon { font-size: 56px; margin-bottom: 16px; }

/* Export button */
.stDownloadButton > button {
    background: rgba(102,126,234,0.2) !important;
    border: 1px solid rgba(102,126,234,0.5) !important;
    color: #a5b4fc !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover {
    background: rgba(102,126,234,0.4) !important;
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
    - 📋 [Lead Form](/Lead_Form)
    - 📊 [Dashboard](/Dashboard)
    - 🗂️ **Admin Panel** ← You are here
    """)
    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="admin-header">
    <div class="admin-badge">🗂️ Admin Panel</div>
    <h1 class="admin-title">Lead Management</h1>
    <p class="admin-subtitle">View, filter, and export all leads and email tracking data</p>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────────────────────────────────────
all_leads = get_all_leads()

if not all_leads:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📭</div>
        <p style="font-size:18px;color:rgba(255,255,255,0.5);">No leads yet.</p>
        <p style="font-size:14px;color:rgba(255,255,255,0.3);margin-top:8px;">Submit the first lead using the Lead Form.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📋 Go to Lead Form", type="primary"):
        st.switch_page("pages/1_Lead_Form.py")
else:
    df = pd.DataFrame(all_leads)

    # ─── Summary Pills ────────────────────────────────────────────────────────
    total = len(df)
    sent = int(df["email_sent"].sum()) if "email_sent" in df.columns else 0
    opened = int(df["is_opened"].sum()) if "is_opened" in df.columns else 0
    high_priority = int((df["ai_priority"] == "High").sum()) if "ai_priority" in df.columns else 0

    st.markdown(f"""
    <div class="summary-row">
        <div class="summary-pill">👥 Total Leads: <strong>{total}</strong></div>
        <div class="summary-pill">📧 Emails Sent: <strong>{sent}</strong></div>
        <div class="summary-pill">👁️ Emails Opened: <strong>{opened}</strong></div>
        <div class="summary-pill">🔴 High Priority: <strong>{high_priority}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    # ─── Filters ──────────────────────────────────────────────────────────────
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    st.markdown("**🔍 Filters**")
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        search = st.text_input("Search by name or email", placeholder="Type to search...", label_visibility="collapsed")
    with filter_col2:
        categories = ["All"] + sorted(df["ai_category"].dropna().unique().tolist()) if "ai_category" in df.columns else ["All"]
        selected_cat = st.selectbox("Category", categories)
    with filter_col3:
        priorities = ["All", "High", "Medium", "Low"]
        selected_pri = st.selectbox("Priority", priorities)
    with filter_col4:
        email_statuses = ["All", "Sent", "Not Sent"]
        selected_email = st.selectbox("Email Status", email_statuses)

    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Apply Filters ────────────────────────────────────────────────────────
    df_filtered = df.copy()

    if search:
        mask = (
            df_filtered["name"].str.contains(search, case=False, na=False) |
            df_filtered["email"].str.contains(search, case=False, na=False)
        )
        df_filtered = df_filtered[mask]

    if selected_cat != "All" and "ai_category" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["ai_category"] == selected_cat]

    if selected_pri != "All" and "ai_priority" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["ai_priority"] == selected_pri]

    if selected_email == "Sent" and "email_sent" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["email_sent"] == 1]
    elif selected_email == "Not Sent" and "email_sent" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["email_sent"] == 0]

    st.markdown(f"**Showing {len(df_filtered)} of {total} leads**", unsafe_allow_html=False)
    st.markdown("")

    # ─── Display Columns ─────────────────────────────────────────────────────
    col_map = {
        "id": "ID",
        "name": "Name",
        "email": "Email",
        "phone": "Phone",
        "company": "Company",
        "requirement": "Requirement",
        "ai_category": "Category",
        "ai_priority": "Priority",
        "email_sent": "Email Sent",
        "is_opened": "Opened",
        "click_count": "Clicks",
        "submitted_at": "Submitted At",
    }

    available_cols = [c for c in col_map if c in df_filtered.columns]
    df_display = df_filtered[available_cols].rename(columns=col_map).copy()

    # Format boolean columns
    if "Email Sent" in df_display.columns:
        df_display["Email Sent"] = df_display["Email Sent"].map({1: "✅", 0: "❌", None: "—"})
    if "Opened" in df_display.columns:
        df_display["Opened"] = df_display["Opened"].map({1: "✅", 0: "❌", None: "—"})

    # Color priority
    def style_priority(val):
        colors = {"High": "color: #f87171", "Medium": "color: #fbbf24", "Low": "color: #34d399"}
        return colors.get(val, "")

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=min(600, 80 + 35 * len(df_display)),
    )

    # ─── Export ───────────────────────────────────────────────────────────────
    st.markdown("")
    export_col1, export_col2 = st.columns([1, 5])
    with export_col1:
        csv_data = df_display.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Export CSV",
            data=csv_data,
            file_name="leads_export.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ─── Detailed Tracking View ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔍 Lead Detail View")
    st.markdown(
        "<p style='color:rgba(255,255,255,0.5);font-size:14px;'>Select a lead ID to see full tracking details</p>",
        unsafe_allow_html=True,
    )

    if not df_filtered.empty:
        lead_options = {
            f"#{row['id']} — {row['name']} ({row['email']})": row
            for _, row in df_filtered.iterrows()
        }
        selected_label = st.selectbox("Select Lead", list(lead_options.keys()), label_visibility="collapsed")

        if selected_label:
            lead = lead_options[selected_label]
            det_col1, det_col2, det_col3 = st.columns(3)

            with det_col1:
                st.markdown("**Contact Info**")
                st.markdown(f"👤 **Name:** {lead.get('name', '—')}")
                st.markdown(f"📧 **Email:** {lead.get('email', '—')}")
                st.markdown(f"📞 **Phone:** {lead.get('phone', '—')}")
                st.markdown(f"🏢 **Company:** {lead.get('company') or '—'}")

            with det_col2:
                st.markdown("**Requirement**")
                req = lead.get('requirement', '—')
                st.markdown(f"💬 _{req}_")
                st.markdown(f"🤖 **Category:** {lead.get('ai_category') or '—'}")
                priority = lead.get('ai_priority') or '—'
                priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "⚪")
                st.markdown(f"{priority_color} **Priority:** {priority}")

            with det_col3:
                st.markdown("**Email Tracking**")
                email_sent = "✅ Yes" if lead.get("email_sent") else "❌ No"
                st.markdown(f"📧 **Email Sent:** {email_sent}")
                opened = "✅ Yes" if lead.get("is_opened") else "❌ No"
                st.markdown(f"👁️ **Opened:** {opened}")
                if lead.get("opened_at"):
                    st.markdown(f"🕒 **Opened At:** {lead['opened_at']}")
                clicks = lead.get("click_count", 0) or 0
                st.markdown(f"🔗 **Link Clicks:** {clicks}")
                st.markdown(f"📅 **Submitted:** {lead.get('submitted_at', '—')}")
