"""Seven-day support workflow.

Every question is logged with whether the automated guide resolved it,
whether a human intervened, and how many minutes it required. Repeated
questions feed back into the relevant vertical template.
"""

from __future__ import annotations

import sqlite3

from .crm import utcnow

TICKET_STATUSES = {"open", "resolved", "escalated"}


def init_support_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY,
            business_id TEXT NOT NULL,
            question TEXT NOT NULL,
            resolved_by TEXT NOT NULL DEFAULT '',
            human_minutes INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'open',
            opened_at TEXT NOT NULL,
            closed_at TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS idx_support_business ON support_tickets(business_id);
        """
    )
    connection.commit()


def open_ticket(connection: sqlite3.Connection, *, business_id: str, question: str) -> int:
    if not business_id.strip() or not question.strip():
        raise ValueError("business_id and question are required")
    cursor = connection.execute(
        "INSERT INTO support_tickets (business_id, question, opened_at) VALUES (?, ?, ?)",
        (business_id.strip(), question.strip(), utcnow()),
    )
    connection.commit()
    return int(cursor.lastrowid)


def resolve_ticket(
    connection: sqlite3.Connection,
    *,
    ticket_id: int,
    resolved_by: str,
    human_minutes: int = 0,
) -> None:
    """resolved_by is 'guide' or 'human'. Human minutes are always recorded."""
    if resolved_by not in {"guide", "human"}:
        raise ValueError("resolved_by must be 'guide' or 'human'")
    if human_minutes < 0:
        raise ValueError("human_minutes cannot be negative")
    cursor = connection.execute(
        """
        UPDATE support_tickets
        SET resolved_by = ?, human_minutes = ?, status = 'resolved', closed_at = ?
        WHERE id = ?
        """,
        (resolved_by, human_minutes, utcnow(), ticket_id),
    )
    if cursor.rowcount == 0:
        raise ValueError("unknown ticket")
    connection.commit()


def support_stats(connection: sqlite3.Connection, business_id: str) -> dict:
    rows = connection.execute(
        "SELECT resolved_by, human_minutes, status FROM support_tickets WHERE business_id = ?",
        (business_id.strip(),),
    ).fetchall()
    total = len(rows)
    guide_resolved = sum(1 for r in rows if r["resolved_by"] == "guide")
    human_minutes = sum(int(r["human_minutes"] or 0) for r in rows)
    open_count = sum(1 for r in rows if r["status"] == "open")
    return {
        "total": total,
        "guide_resolved": guide_resolved,
        "human_minutes": human_minutes,
        "open": open_count,
    }
