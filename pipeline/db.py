"""Outreach pipeline database schema and operations."""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "outreach.db"

SCHEMA = """
-- Prospects: every business we might contact
CREATE TABLE IF NOT EXISTS prospects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vertical TEXT NOT NULL,
    city TEXT NOT NULL,
    business_name TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    postcode TEXT,
    rating REAL,
    review_count INTEGER,
    website TEXT,
    email TEXT,
    instagram TEXT,
    facebook TEXT,
    services TEXT,
    description TEXT,
    -- Companies House enrichment
    company_number TEXT,
    company_name TEXT,
    company_status TEXT,
    incorporation_date TEXT,
    sic_codes TEXT,
    registered_address TEXT,
    director_name TEXT,
    director_role TEXT,
    -- Scoring
    score INTEGER DEFAULT 0,
    score_reasons TEXT,
    -- Pipeline stage
    stage TEXT DEFAULT 'new',  -- new/contacted/responded/interested/onboarded/paying/churned
    stage_changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Source
    source TEXT,  -- serpapi/powuk/manual
    source_query TEXT,
    -- Meta
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    UNIQUE(vertical, city, business_name)
);

-- Outreach: every message we send
CREATE TABLE IF NOT EXISTS outreach (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id INTEGER NOT NULL,
    channel TEXT NOT NULL,  -- whatsapp/email/phone/instagram
    direction TEXT NOT NULL,  -- outbound/inbound
    message TEXT NOT NULL,
    template_id TEXT,
    status TEXT DEFAULT 'sent',  -- sent/delivered/read/replied/bounced
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prospect_id) REFERENCES prospects(id)
);

-- Conversations: threaded view of outreach
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id INTEGER NOT NULL UNIQUE,
    first_contact_at TIMESTAMP,
    last_contact_at TIMESTAMP,
    response_count INTEGER DEFAULT 0,
    sentiment TEXT,  -- positive/neutral/negative
    next_action TEXT,
    next_action_at TIMESTAMP,
    assigned_to TEXT,
    FOREIGN KEY (prospect_id) REFERENCES prospects(id)
);

-- Onboardings: free trial tracking
CREATE TABLE IF NOT EXISTS onboardings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id INTEGER NOT NULL UNIQUE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    week2_checkin_at TIMESTAMP,
    week4_review_at TIMESTAMP,
    status TEXT DEFAULT 'pending',  -- pending/active/completed/cancelled
    metrics_before TEXT,  -- JSON
    metrics_after TEXT,  -- JSON
    feedback TEXT,
    converted_to_paid BOOLEAN DEFAULT 0,
    paid_amount REAL,
    paid_at TIMESTAMP,
    FOREIGN KEY (prospect_id) REFERENCES prospects(id)
);

-- Follow-ups: scheduled actions
CREATE TABLE IF NOT EXISTS followups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id INTEGER NOT NULL,
    action TEXT NOT NULL,  -- send_message/call/check_in/review
    channel TEXT,
    message_template TEXT,
    scheduled_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    status TEXT DEFAULT 'pending',  -- pending/completed/skipped/overdue
    notes TEXT,
    FOREIGN KEY (prospect_id) REFERENCES prospects(id)
);

-- Metrics: daily aggregates
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    vertical TEXT,
    city TEXT,
    prospects_added INTEGER DEFAULT 0,
    messages_sent INTEGER DEFAULT 0,
    messages_replied INTEGER DEFAULT 0,
    onboardings_started INTEGER DEFAULT 0,
    onboardings_completed INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue REAL DEFAULT 0,
    UNIQUE(date, vertical, city)
);

CREATE INDEX IF NOT EXISTS idx_prospects_stage ON prospects(stage);
CREATE INDEX IF NOT EXISTS idx_prospects_vertical ON prospects(vertical);
CREATE INDEX IF NOT EXISTS idx_prospects_city ON prospects(city);
CREATE INDEX IF NOT EXISTS idx_outreach_prospect ON outreach(prospect_id);
CREATE INDEX IF NOT EXISTS idx_followups_status ON followups(status);
CREATE INDEX IF NOT EXISTS idx_followups_scheduled ON followups(scheduled_at);
"""


def get_db():
    """Get database connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Initialize database with schema."""
    conn = get_db()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")


def upsert_prospect(conn, data: dict) -> int:
    """Insert or update a prospect. Returns prospect ID."""
    existing = conn.execute(
        "SELECT id FROM prospects WHERE vertical=? AND city=? AND business_name=?",
        (data["vertical"], data["city"], data["business_name"])
    ).fetchone()
    
    if existing:
        pid = existing["id"]
        updates = {k: v for k, v in data.items() if v and k != "vertical" and k != "city" and k != "business_name"}
        updates["updated_at"] = datetime.now().isoformat()
        if updates:
            set_clause = ", ".join(f"{k}=?" for k in updates)
            conn.execute(f"UPDATE prospects SET {set_clause} WHERE id=?", list(updates.values()) + [pid])
        return pid
    else:
        cols = [k for k, v in data.items() if v is not None]
        vals = [data[k] for k in cols]
        placeholders = ", ".join(["?"] * len(cols))
        col_names = ", ".join(cols)
        cur = conn.execute(f"INSERT INTO prospects ({col_names}) VALUES ({placeholders})", vals)
        return cur.lastrowid


def record_outreach(conn, prospect_id: int, channel: str, direction: str, message: str, template_id: str = None) -> int:
    """Record an outreach message."""
    cur = conn.execute(
        "INSERT INTO outreach (prospect_id, channel, direction, message, template_id) VALUES (?, ?, ?, ?, ?)",
        (prospect_id, channel, direction, message, template_id)
    )
    # Update prospect stage
    if direction == "outbound":
        conn.execute(
            "UPDATE prospects SET stage='contacted', stage_changed_at=?, updated_at=? WHERE id=? AND stage='new'",
            (datetime.now().isoformat(), datetime.now().isoformat(), prospect_id)
        )
    elif direction == "inbound":
        conn.execute(
            "UPDATE prospects SET stage='responded', stage_changed_at=?, updated_at=? WHERE id=?",
            (datetime.now().isoformat(), datetime.now().isoformat(), prospect_id)
        )
    # Update conversation
    conn.execute(
        "INSERT OR REPLACE INTO conversations (prospect_id, last_contact_at, response_count) VALUES (?, ?, COALESCE((SELECT response_count FROM conversations WHERE prospect_id=?), 0) + ?)",
        (prospect_id, datetime.now().isoformat(), prospect_id, 1 if direction == "inbound" else 0)
    )
    return cur.lastrowid


def schedule_followup(conn, prospect_id: int, action: str, channel: str, message_template: str, scheduled_at: datetime) -> int:
    """Schedule a follow-up action."""
    cur = conn.execute(
        "INSERT INTO followups (prospect_id, action, channel, message_template, scheduled_at) VALUES (?, ?, ?, ?, ?)",
        (prospect_id, action, channel, message_template, scheduled_at.isoformat())
    )
    return cur.lastrowid


def get_due_followups(conn, limit: int = 50) -> list:
    """Get follow-ups that are due."""
    return conn.execute(
        "SELECT f.*, p.business_name, p.phone, p.vertical, p.city FROM followups f JOIN prospects p ON f.prospect_id=p.id WHERE f.status='pending' AND f.scheduled_at<=? ORDER BY f.scheduled_at LIMIT ?",
        (datetime.now().isoformat(), limit)
    ).fetchall()


def get_pipeline_stats(conn) -> dict:
    """Get pipeline statistics."""
    stats = {}
    for row in conn.execute("SELECT stage, COUNT(*) as count FROM prospects GROUP BY stage"):
        stats[row["stage"]] = row["count"]
    
    stats["total"] = sum(stats.values())
    stats["by_vertical"] = {}
    for row in conn.execute("SELECT vertical, stage, COUNT(*) as count FROM prospects GROUP BY vertical, stage"):
        stats["by_vertical"].setdefault(row["vertical"], {})[row["stage"]] = row["count"]
    
    stats["outreach_today"] = conn.execute(
        "SELECT COUNT(*) FROM outreach WHERE sent_at>=?", (datetime.now().date().isoformat(),)
    ).fetchone()[0]
    
    stats["responses_today"] = conn.execute(
        "SELECT COUNT(*) FROM outreach WHERE direction='inbound' AND sent_at>=?", (datetime.now().date().isoformat(),)
    ).fetchone()[0]
    
    stats["active_onboardings"] = conn.execute(
        "SELECT COUNT(*) FROM onboardings WHERE status='active'"
    ).fetchone()[0]
    
    stats["conversions"] = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(paid_amount),0) FROM onboardings WHERE converted_to_paid=1"
    ).fetchone()
    
    return stats


if __name__ == "__main__":
    init_db()
    print("Database ready.")
