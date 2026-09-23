"""Seven-day support workflow.

Every question is logged with whether the automated guide resolved it,
whether a human intervened, and how many minutes it required. Repeated
questions feed back into the relevant vertical template.
"""

from __future__ import annotations

import sqlite3

from .crm import utcnow

TICKET_STATUSES = {"open", "resolved", "escalated"}
ISSUE_CATEGORIES = {
    "booking",
    "reminder",
    "quote",
    "payment",
    "account_access",
    "review",
    "rebooking",
    "other",
}


def init_support_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY,
            business_id TEXT NOT NULL,
            question TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'other',
            error_code TEXT NOT NULL DEFAULT '',
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


def open_ticket(
    connection: sqlite3.Connection,
    *,
    business_id: str,
    question: str,
    category: str = "other",
    error_code: str = "",
) -> int:
    if not business_id.strip() or not question.strip():
        raise ValueError("business_id and question are required")
    if category not in ISSUE_CATEGORIES:
        raise ValueError(f"unsupported category: {category}")
    cursor = connection.execute(
        "INSERT INTO support_tickets (business_id, question, category, error_code, opened_at) VALUES (?, ?, ?, ?, ?)",
        (business_id.strip(), question.strip(), category, error_code.strip(), utcnow()),
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


def fleet_support_report(
    connection: sqlite3.Connection, *, viability_minutes: int = 20
) -> dict:
    """Fleet-wide support economics — the metric the £20 product lives or dies by.

    Returns per-business minutes plus fleet medians and a flag list of
    businesses over the viability threshold. A median above the threshold
    means kill or reprice, not hope.
    """
    rows = connection.execute(
        "SELECT business_id, resolved_by, human_minutes, status FROM support_tickets"
    ).fetchall()
    by_business: dict[str, dict] = {}
    for row in rows:
        entry = by_business.setdefault(
            row["business_id"], {"total": 0, "guide_resolved": 0, "human_minutes": 0, "open": 0}
        )
        entry["total"] += 1
        if row["resolved_by"] == "guide":
            entry["guide_resolved"] += 1
        entry["human_minutes"] += int(row["human_minutes"] or 0)
        if row["status"] == "open":
            entry["open"] += 1

    minutes = sorted(entry["human_minutes"] for entry in by_business.values())
    median = minutes[len(minutes) // 2] if minutes else 0
    total_minutes = sum(minutes)
    over_threshold = sorted(
        bid for bid, entry in by_business.items() if entry["human_minutes"] > viability_minutes
    )
    return {
        "businesses": len(by_business),
        "total_tickets": len(rows),
        "total_human_minutes": total_minutes,
        "median_human_minutes": median,
        "viability_threshold_minutes": viability_minutes,
        "viable": median <= viability_minutes,
        "over_threshold": over_threshold,
        "per_business": by_business,
    }
