# LeadTrack — Automated Lead Management & Email Tracking System

A full-stack automated lead management system built with **Python + Streamlit + FastAPI**.

## ✨ Features

| Feature | Details |
|---------|---------|
| 📋 Lead Capture Form | Name, Email, Phone, Company, Requirement with validation |
| 💾 Database Storage | SQLite — zero config, file-based |
| 📧 Personalized Email | HTML email with name & requirement via Gmail SMTP |
| 👁️ Open Tracking | 1×1 pixel GIF detects email opens |
| 🔗 Click Tracking | Trackable redirect links log every click |
| 📊 Analytics Dashboard | KPIs, charts, funnel, gauges — all live |
| 🤖 AI Classification | Gemini AI classifies leads by category & priority |
| 🗂️ Admin Panel | Filter, search, and export all leads to CSV |

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
copy .env.example .env
```
Edit `.env` with your credentials:
```
GMAIL_ADDRESS=your@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
TRACKING_BASE_URL=http://localhost:8000
REDIRECT_URL=https://yourwebsite.com
GEMINI_API_KEY=                          # Optional
```

### 3. Run the system
```bash
python run.py
```
This starts both servers:
- **FastAPI** (tracking) → http://localhost:8000
- **Streamlit** (app) → http://localhost:8501

---

## 🏗️ Architecture

```
User Submits Form
      │
      ▼
Streamlit Lead Form (port 8501)
      │
      ├── SQLite DB ← saves lead data
      │
      ├── AI Service ← classifies category & priority
      │
      └── Gmail SMTP ← sends personalized HTML email
                              │
                    Email contains:
                    ├── Tracking Pixel: GET /track/open?tid=<uuid>
                    └── Trackable Link: GET /track/click?tid=<uuid>&url=...
                              │
                      FastAPI Server (port 8000)
                              │
                    ├── /track/open → logs open event → returns 1x1 GIF
                    └── /track/click → logs click → redirects to real URL
                              │
                    SQLite DB ← updated with tracking events
                              │
                    Streamlit Dashboard (port 8501)
                              │
                    Shows live analytics & charts
```

---

## 📁 File Structure

```
intrenproject/
├── app.py                    # Home page (Streamlit entry point)
├── tracking_server.py        # FastAPI tracking endpoints
├── run.py                    # Launch script for both servers
├── requirements.txt
├── .env.example              # Config template
├── database.db               # SQLite DB (auto-created)
├── services/
│   ├── db.py                 # All DB queries
│   ├── email_service.py      # Email sending & HTML template
│   └── ai_service.py         # Gemini AI lead classification
└── pages/
    ├── 1_Lead_Form.py        # Lead submission form
    ├── 2_Dashboard.py        # Analytics dashboard
    └── 3_Admin.py            # Admin panel
```

---

## 📧 How Email Tracking Works

### Open Tracking
1. Each email contains a hidden `<img>` tag with a unique UUID URL
2. When the email client loads images, it hits `GET /track/open?tid=<uuid>`
3. FastAPI records the open timestamp in `email_events` table
4. Dashboard shows real-time open counts and open rate

### Click Tracking
1. Every link in the email points to `GET /track/click?tid=<uuid>&url=<destination>`
2. FastAPI logs the click in `link_clicks` table
3. User is immediately redirected to the actual destination (302 redirect)
4. Dashboard shows click count and click rate

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python 3.10+ | Core language |
| Streamlit | UI framework |
| FastAPI | Tracking HTTP server |
| SQLite | Database |
| Uvicorn | ASGI server for FastAPI |
| Gmail SMTP | Email delivery |
| Google Gemini API | AI lead classification |
| Plotly Express | Charts & visualizations |
| python-dotenv | Environment config |

---

## 📊 Database Schema

### `leads`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| name | TEXT | Full name |
| email | TEXT | Email address |
| phone | TEXT | Phone number |
| company | TEXT | Company (optional) |
| requirement | TEXT | Lead message |
| submitted_at | DATETIME | Timestamp |
| email_sent | BOOLEAN | Email delivery status |
| ai_category | TEXT | AI-classified category |
| ai_priority | TEXT | High / Medium / Low |

### `email_events`
| Column | Type | Description |
|--------|------|-------------|
| lead_id | INTEGER FK | Reference to lead |
| tracking_id | TEXT UNIQUE | UUID per email |
| sent_at | DATETIME | When email was sent |
| opened_at | DATETIME | When email was opened |
| is_opened | BOOLEAN | Open status |

### `link_clicks`
| Column | Type | Description |
|--------|------|-------------|
| lead_id | INTEGER FK | Reference to lead |
| tracking_id | TEXT | UUID (same as email) |
| clicked_at | DATETIME | Click timestamp |
| redirect_url | TEXT | Actual destination |

---

## 🔐 Gmail App Password Setup

1. Enable 2-Step Verification on your Google account
2. Go to **Google Account → Security → App Passwords**
3. Generate a password for "Mail" on "Windows Computer"
4. Copy the 16-character password into your `.env` file

> ⚠️ Never use your real Gmail password. Always use App Passwords.

---

## 🌐 Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy `app.py` from your repo
4. Add secrets in Streamlit Cloud settings (equivalent to `.env`)
5. For tracking: use a separate server (Railway/Render) for FastAPI

---

## 👤 Author

Built as part of an Automated Lead Management System assignment.
