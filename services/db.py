import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize all database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            email           TEXT NOT NULL,
            phone           TEXT NOT NULL,
            company         TEXT,
            requirement     TEXT NOT NULL,
            submitted_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
            email_sent      BOOLEAN DEFAULT 0,
            ai_category     TEXT,
            ai_priority     TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_events (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id         INTEGER,
            tracking_id     TEXT UNIQUE,
            sent_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
            opened_at       DATETIME,
            is_opened       BOOLEAN DEFAULT 0,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS link_clicks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id         INTEGER,
            tracking_id     TEXT,
            clicked_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
            redirect_url    TEXT,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """)

    conn.commit()
    conn.close()


# ─── Write Operations ────────────────────────────────────────────────────────

def insert_lead(name, email, phone, company, requirement):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO leads (name, email, phone, company, requirement) VALUES (?, ?, ?, ?, ?)",
        (name, email, phone, company, requirement),
    )
    lead_id = c.lastrowid
    conn.commit()
    conn.close()
    return lead_id


def insert_email_event(lead_id, tracking_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO email_events (lead_id, tracking_id) VALUES (?, ?)",
        (lead_id, tracking_id),
    )
    conn.commit()
    conn.close()


def mark_email_sent(lead_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE leads SET email_sent = 1 WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()


def mark_email_opened(tracking_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """UPDATE email_events
           SET is_opened = 1, opened_at = CURRENT_TIMESTAMP
           WHERE tracking_id = ? AND is_opened = 0""",
        (tracking_id,),
    )
    conn.commit()
    conn.close()


def insert_link_click(tracking_id, redirect_url):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT lead_id FROM email_events WHERE tracking_id = ?", (tracking_id,))
    row = c.fetchone()
    lead_id = row["lead_id"] if row else None
    c.execute(
        "INSERT INTO link_clicks (lead_id, tracking_id, redirect_url) VALUES (?, ?, ?)",
        (lead_id, tracking_id, redirect_url),
    )
    conn.commit()
    conn.close()


def update_ai_fields(lead_id, category, priority):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE leads SET ai_category = ?, ai_priority = ? WHERE id = ?",
        (category, priority, lead_id),
    )
    conn.commit()
    conn.close()


# ─── Read Operations ─────────────────────────────────────────────────────────

def get_dashboard_stats():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) AS count FROM leads")
    total_leads = c.fetchone()["count"]

    c.execute("SELECT COUNT(*) AS count FROM leads WHERE email_sent = 1")
    emails_sent = c.fetchone()["count"]

    c.execute("SELECT COUNT(*) AS count FROM email_events WHERE is_opened = 1")
    emails_opened = c.fetchone()["count"]

    c.execute("SELECT COUNT(*) AS count FROM link_clicks")
    links_clicked = c.fetchone()["count"]

    open_rate = round((emails_opened / emails_sent * 100) if emails_sent > 0 else 0, 1)
    click_rate = round((links_clicked / emails_sent * 100) if emails_sent > 0 else 0, 1)

    conn.close()
    return {
        "total_leads": total_leads,
        "emails_sent": emails_sent,
        "emails_opened": emails_opened,
        "links_clicked": links_clicked,
        "open_rate": open_rate,
        "click_rate": click_rate,
    }


def get_all_leads():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT
            l.*,
            ee.is_opened,
            ee.opened_at,
            ee.tracking_id,
            (SELECT COUNT(*) FROM link_clicks lc WHERE lc.lead_id = l.id) AS click_count
        FROM leads l
        LEFT JOIN email_events ee ON ee.lead_id = l.id
        ORDER BY l.submitted_at DESC
        """
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_leads_over_time():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT DATE(submitted_at) AS date, COUNT(*) AS count
        FROM leads
        GROUP BY DATE(submitted_at)
        ORDER BY date
        """
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_category_distribution():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT ai_category, COUNT(*) AS count
        FROM leads
        WHERE ai_category IS NOT NULL
        GROUP BY ai_category
        ORDER BY count DESC
        """
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_priority_distribution():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT ai_priority, COUNT(*) AS count
        FROM leads
        WHERE ai_priority IS NOT NULL
        GROUP BY ai_priority
        """
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recent_opens(limit=10):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT l.name, l.email, ee.opened_at
        FROM email_events ee
        JOIN leads l ON l.id = ee.lead_id
        WHERE ee.is_opened = 1
        ORDER BY ee.opened_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]
