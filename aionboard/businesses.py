"""Canonical business identity for AI Onboard.

Companies House numbers are optional. The internal business_id is canonical,
so sole traders, partnerships, and limited companies share one identity from
enquiry through installation to later subscriptions.
"""

from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone

from .crm import utcnow

BUSINESS_KINDS = {"sole_trader", "partnership", "limited_company"}
CONSENT_PURPOSES = {"onboarding", "marketing", "pow_opportunity_alerts"}
CONSENT_STATUSES = {"granted", "withdrawn", "pending"}
MARKETING_CHANNELS = {"phone", "sms", "whatsapp", "email"}


def init_business_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS businesses (
            business_id TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            kind TEXT NOT NULL,
            company_number TEXT UNIQUE,
            vertical TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS consents (
            id INTEGER PRIMARY KEY,
            business_id TEXT NOT NULL REFERENCES businesses(business_id) ON DELETE CASCADE,
            purpose TEXT NOT NULL,
            channel TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL,
            recorded_at TEXT NOT NULL,
            notes TEXT NOT NULL DEFAULT ''
        );

        CREATE INDEX IF NOT EXISTS idx_consents_business ON consents(business_id);
        """
    )
    connection.commit()


def new_business_id() -> str:
    return f"biz-{uuid.uuid4().hex[:12]}"


def create_business(
    connection: sqlite3.Connection,
    *,
    display_name: str,
    kind: str,
    company_number: str | None = None,
    vertical: str = "",
) -> str:
    """Create a business. company_number is optional; sole traders have none."""
    name = display_name.strip()
    if not name:
        raise ValueError("display_name is required")
    if kind not in BUSINESS_KINDS:
        raise ValueError(f"unsupported kind: {kind}")
    normalized_company = (company_number or "").strip().upper() or None

    business_id = new_business_id()
    try:
        connection.execute(
            """
            INSERT INTO businesses
            (business_id, display_name, kind, company_number, vertical, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (business_id, name, kind, normalized_company, vertical.strip(), utcnow()),
        )
    except sqlite3.IntegrityError as exc:
        raise ValueError(f"company_number already registered: {normalized_company}") from exc
    connection.commit()
    return business_id


def get_business(connection: sqlite3.Connection, business_id: str) -> dict | None:
    row = connection.execute(
        "SELECT * FROM businesses WHERE business_id = ?",
        (business_id.strip(),),
    ).fetchone()
    return dict(row) if row else None


def find_by_company_number(connection: sqlite3.Connection, company_number: str) -> dict | None:
    row = connection.execute(
        "SELECT * FROM businesses WHERE company_number = ?",
        (company_number.strip().upper(),),
    ).fetchone()
    return dict(row) if row else None


def record_consent(
    connection: sqlite3.Connection,
    *,
    business_id: str,
    purpose: str,
    status: str,
    channel: str = "",
    notes: str = "",
) -> int:
    """Record consent. Marketing consent is channel-specific; POW alerts are separate."""
    if get_business(connection, business_id) is None:
        raise ValueError("unknown business")
    if purpose not in CONSENT_PURPOSES:
        raise ValueError(f"unsupported purpose: {purpose}")
    if status not in CONSENT_STATUSES:
        raise ValueError(f"unsupported status: {status}")
    if purpose == "marketing":
        if channel not in MARKETING_CHANNELS:
            raise ValueError("marketing consent requires a channel: phone, sms, whatsapp, or email")
    elif channel:
        raise ValueError("channel is only valid for marketing consent")

    cursor = connection.execute(
        """
        INSERT INTO consents
        (business_id, purpose, channel, status, recorded_at, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (business_id.strip(), purpose, channel, status, utcnow(), notes.strip()),
    )
    connection.commit()
    return int(cursor.lastrowid)


def latest_consent(
    connection: sqlite3.Connection, business_id: str, purpose: str, channel: str = ""
) -> dict | None:
    row = connection.execute(
        """
        SELECT * FROM consents
        WHERE business_id = ? AND purpose = ? AND channel = ?
        ORDER BY id DESC LIMIT 1
        """,
        (business_id.strip(), purpose, channel),
    ).fetchone()
    return dict(row) if row else None


def has_consent(
    connection: sqlite3.Connection, business_id: str, purpose: str, channel: str = ""
) -> bool:
    """Current consent state. Absence of a record means no consent."""
    record = latest_consent(connection, business_id, purpose, channel)
    return record is not None and record["status"] == "granted"


def marketing_allowed(connection: sqlite3.Connection, business_id: str, channel: str) -> bool:
    """Channel-specific marketing permission. Onboarding consent is never enough."""
    if channel not in MARKETING_CHANNELS:
        raise ValueError(f"unsupported channel: {channel}")
    return has_consent(connection, business_id, "marketing", channel)
