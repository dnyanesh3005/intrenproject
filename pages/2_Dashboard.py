"""
pages/2_Dashboard.py — Analytics Dashboard
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.db import (
    init_db, get_dashboard_stats, get_all_leads,
    get_leads_over_time, get_category_distribution, get_priority_distribution
)

init_db()

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analytics Dashboard — LeadTrack",
    page_icon="📊",
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

/* Dashboard Header */
.dash-header { padding: 32px 0 24px; animation: fadeIn 0.6s ease; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.dash-badge {
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
    margin-bottom: 16px;
}
.dash-title { font-size: 40px; font-weight: 800; color: #fff; letter-spacing: -2px; margin-bottom: 6px; }
.dash-subtitle { font-size: 15px; color: rgba(255,255,255,0.5); }

/* KPI Cards */
.kpi-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    animation: fadeInUp 0.5s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(15px); }
    to   { opacity: 1; transform: translateY(0); }
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, linear-gradient(90deg, #667eea, #764ba2));
}
.kpi-card:hover {
    background: rgba(255,255,255,0.1);
    border-color: rgba(102,126,234,0.4);
    transform: translateY(-3px);
}
.kpi-icon { font-size: 28px; margin-bottom: 10px; }
.kpi-value {
    font-size: 42px;
    font-weight: 800;
    color: #fff;
    letter-spacing: -2px;
    line-height: 1;
}
.kpi-label { font-size: 13px; color: rgba(255,255,255,0.5); font-weight: 500; margin-top: 6px; letter-spacing: 0.5px; }

/* Charts container */
.chart-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}
.chart-title { font-size: 17px; font-weight: 600; color: #fff; margin-bottom: 16px; }

/* Live indicator */
.live-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #34d399;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(52,211,153,0.4); }
    50% { opacity: 0.7; box-shadow: 0 0 0 6px rgba(52,211,153,0); }
}
.live-label { font-size: 13px; color: #34d399; font-weight: 600; }

/* Recent activity table */
.stDataFrame { background: rgba(255,255,255,0.03) !important; border-radius: 12px !important; }

/* Empty state */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: rgba(255,255,255,0.4);
}
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-text { font-size: 16px; }
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
    - 📊 **Dashboard** ← You are here
    - 🗂️ [Admin Panel](/Admin)
    """)
    st.markdown("---")
    auto_refresh = st.toggle("🔄 Auto-refresh (30s)", value=False)

# ─── Auto-refresh ─────────────────────────────────────────────────────────────
if auto_refresh:
    import time
    st.markdown(
        '<span class="live-dot"></span><span class="live-label">Live — auto-refreshing every 30s</span>',
        unsafe_allow_html=True,
    )
    time.sleep(30)
    st.rerun()

# ─── Header ──────────────────────────────────────────────────────────────────
col_title, col_refresh = st.columns([5, 1])
with col_title:
    st.markdown("""
    <div class="dash-header">
        <div class="dash-badge">📊 Analytics</div>
        <h1 class="dash-title">Analytics Dashboard</h1>
        <p class="dash-subtitle">Real-time email engagement & lead conversion metrics</p>
    </div>
    """, unsafe_allow_html=True)
with col_refresh:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# ─── Load Data ─────────────────────────────────────────────────────────────
stats = get_dashboard_stats()
leads_over_time = get_leads_over_time()
category_data = get_category_distribution()
priority_data = get_priority_distribution()
all_leads = get_all_leads()

# ─── KPI Cards ───────────────────────────────────────────────────────────────
kpis = [
    ("👥", stats["total_leads"], "Total Leads",     "linear-gradient(90deg,#667eea,#764ba2)"),
    ("📧", stats["emails_sent"], "Emails Sent",     "linear-gradient(90deg,#f093fb,#f5576c)"),
    ("👁️", stats["emails_opened"], "Emails Opened", "linear-gradient(90deg,#4facfe,#00f2fe)"),
    (f"{stats['open_rate']}%", None, "Open Rate",   "linear-gradient(90deg,#43e97b,#38f9d7)"),
    ("🔗", stats["links_clicked"], "Links Clicked", "linear-gradient(90deg,#fa709a,#fee140)"),
    (f"{stats['click_rate']}%", None, "Click Rate", "linear-gradient(90deg,#a18cd1,#fbc2eb)"),
]

gradients = [k[3] for k in kpis]
cols = st.columns(6)
for col, (icon, value, label, gradient) in zip(cols, kpis):
    with col:
        display_value = icon if value is None else value
        display_icon = "📊" if value is None else icon
        st.markdown(
            f"""<div class="kpi-card" style="--accent:{gradient};">
                <div class="kpi-icon">{display_icon}</div>
                <div class="kpi-value">{display_value}</div>
                <div class="kpi-label">{label}</div>
            </div>""",
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ─── Charts Row ───────────────────────────────────────────────────────────────
if not all_leads:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📭</div>
        <div class="empty-text">No leads yet. Submit a lead to see analytics!</div>
    </div>
    """, unsafe_allow_html=True)
else:
    chart_col1, chart_col2 = st.columns([3, 2])

    # ── Leads Over Time (Line Chart) ─────────────────────────────────────────
    with chart_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Leads Over Time</div>', unsafe_allow_html=True)

        if leads_over_time:
            df_time = pd.DataFrame(leads_over_time)
            fig_line = px.area(
                df_time, x="date", y="count",
                labels={"date": "Date", "count": "New Leads"},
                color_discrete_sequence=["#667eea"],
            )
            fig_line.update_traces(
                fill="tozeroy",
                fillcolor="rgba(102,126,234,0.15)",
                line=dict(color="#667eea", width=2.5),
            )
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="rgba(255,255,255,0.6)", family="Inter"),
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)", showgrid=True),
                yaxis=dict(gridcolor="rgba(255,255,255,0.06)", showgrid=True),
                height=280,
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No time data available yet.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Email Funnel (Funnel Chart) ──────────────────────────────────────────
    with chart_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🔽 Email Engagement Funnel</div>', unsafe_allow_html=True)

        funnel_data = dict(
            number=[stats["total_leads"], stats["emails_sent"], stats["emails_opened"], stats["links_clicked"]],
            stage=["Leads Captured", "Emails Sent", "Emails Opened", "Links Clicked"],
        )
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_data["stage"],
            x=funnel_data["number"],
            textinfo="value+percent initial",
            marker=dict(
                color=["#667eea", "#764ba2", "#f093fb", "#f5576c"],
                line=dict(width=0),
            ),
            connector=dict(line=dict(color="rgba(255,255,255,0.1)", width=1)),
        ))
        fig_funnel.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.7)", family="Inter", size=13),
            margin=dict(l=0, r=0, t=10, b=0),
            height=280,
        )
        st.plotly_chart(fig_funnel, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 2 Charts ──────────────────────────────────────────────────────────
    chart_col3, chart_col4 = st.columns(2)

    # ── Category Distribution (Donut) ─────────────────────────────────────────
    with chart_col3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🤖 Lead Categories (AI)</div>', unsafe_allow_html=True)

        if category_data:
            df_cat = pd.DataFrame(category_data)
            fig_donut = px.pie(
                df_cat, names="ai_category", values="count",
                hole=0.6,
                color_discrete_sequence=px.colors.sequential.Purpor,
            )
            fig_donut.update_traces(
                textinfo="label+percent",
                textfont=dict(color="white", size=11),
            )
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="rgba(255,255,255,0.7)", family="Inter"),
                margin=dict(l=0, r=0, t=10, b=0),
                legend=dict(
                    font=dict(color="rgba(255,255,255,0.6)"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                height=280,
            )
            fig_donut.add_annotation(
                text=f"{sum(d['count'] for d in category_data)}<br>Leads",
                x=0.5, y=0.5, font_size=18,
                font_color="white", showarrow=False,
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No category data yet.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Priority Distribution (Bar) ───────────────────────────────────────────
    with chart_col4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">⚡ Lead Priority Distribution</div>', unsafe_allow_html=True)

        if priority_data:
            df_pri = pd.DataFrame(priority_data)
            color_map = {"High": "#f87171", "Medium": "#fbbf24", "Low": "#34d399"}
            fig_bar = px.bar(
                df_pri, x="ai_priority", y="count",
                color="ai_priority",
                color_discrete_map=color_map,
                labels={"ai_priority": "Priority", "count": "Leads"},
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="rgba(255,255,255,0.6)", family="Inter"),
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
                showlegend=False,
                height=280,
            )
            fig_bar.update_traces(marker_line_width=0)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No priority data yet.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Open Rate Gauge ───────────────────────────────────────────────────────
    gauge_col1, gauge_col2 = st.columns(2)

    with gauge_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">👁️ Email Open Rate Gauge</div>', unsafe_allow_html=True)
        fig_gauge1 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=stats["open_rate"],
            number={"suffix": "%", "font": {"color": "white", "size": 36}},
            delta={"reference": 40, "valueformat": ".1f"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "rgba(255,255,255,0.3)"},
                "bar": {"color": "#667eea"},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "rgba(239,68,68,0.2)"},
                    {"range": [30, 60], "color": "rgba(251,191,36,0.2)"},
                    {"range": [60, 100], "color": "rgba(52,211,153,0.2)"},
                ],
                "threshold": {
                    "line": {"color": "#34d399", "width": 3},
                    "thickness": 0.8,
                    "value": 60,
                },
            },
            title={"text": "Open Rate", "font": {"color": "rgba(255,255,255,0.6)", "size": 14}},
        ))
        fig_gauge1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"),
            margin=dict(l=20, r=20, t=30, b=10),
            height=240,
        )
        st.plotly_chart(fig_gauge1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with gauge_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🔗 Click Rate Gauge</div>', unsafe_allow_html=True)
        fig_gauge2 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=stats["click_rate"],
            number={"suffix": "%", "font": {"color": "white", "size": 36}},
            delta={"reference": 20, "valueformat": ".1f"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "rgba(255,255,255,0.3)"},
                "bar": {"color": "#f093fb"},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 15], "color": "rgba(239,68,68,0.2)"},
                    {"range": [15, 35], "color": "rgba(251,191,36,0.2)"},
                    {"range": [35, 100], "color": "rgba(52,211,153,0.2)"},
                ],
            },
            title={"text": "Click Rate", "font": {"color": "rgba(255,255,255,0.6)", "size": 14}},
        ))
        fig_gauge2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"),
            margin=dict(l=20, r=20, t=30, b=10),
            height=240,
        )
        st.plotly_chart(fig_gauge2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Recent Leads Table ─────────────────────────────────────────────────────
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📋 Recent Leads</div>', unsafe_allow_html=True)

    df_leads = pd.DataFrame(all_leads[:10])
    if not df_leads.empty:
        display_cols = {
            "name": "Name",
            "email": "Email",
            "company": "Company",
            "requirement": "Requirement",
            "ai_category": "Category",
            "ai_priority": "Priority",
            "email_sent": "Email Sent",
            "is_opened": "Opened",
            "click_count": "Clicks",
            "submitted_at": "Submitted",
        }
        available = [c for c in display_cols.keys() if c in df_leads.columns]
        df_display = df_leads[available].rename(columns=display_cols)

        # Format booleans
        if "Email Sent" in df_display.columns:
            df_display["Email Sent"] = df_display["Email Sent"].map({1: "✅ Yes", 0: "❌ No", None: "—"})
        if "Opened" in df_display.columns:
            df_display["Opened"] = df_display["Opened"].map({1: "✅ Yes", 0: "❌ No", None: "—"})

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
