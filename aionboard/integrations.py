"""Capability-aware integration inventory.

For each app, record whether the platform offers a supported connection,
whether the customer authorised it, what permissions were granted, which
actions were actually tested, and what remains manual. Never mark an app
connected merely because the customer uses it.
"""

from __future__ import annotations

import sqlite3

from .crm import utcnow

AUTH_STATUSES = {"pending", "granted", "failed", "unsupported"}


def init_integration_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS integrations (
            id INTEGER PRIMARY KEY,
            business_id TEXT NOT NULL,
            app TEXT NOT NULL,
            connection_offered INTEGER NOT NULL DEFAULT 0,
            auth_status TEXT NOT NULL DEFAULT 'pending',
            permissions_granted TEXT NOT NULL DEFAULT '',
            actions_tested TEXT NOT NULL DEFAULT '',
            manual_remainder TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL,
            UNIQUE(business_id, app)
        );
        CREATE INDEX IF NOT EXISTS idx_integrations_business ON integrations(business_id);
        """
    )
    connection.commit()


def record_integration(
    connection: sqlite3.Connection,
    *,
    business_id: str,
    app: str,
    connection_offered: bool,
    auth_status: str = "pending",
    permissions_granted: str = "",
    actions_tested: str = "",
    manual_remainder: str = "",
) -> int:
    if not business_id.strip() or not app.strip():
        raise ValueError("business_id and app are required")
    if auth_status not in AUTH_STATUSES:
        raise ValueError(f"unsupported auth status: {auth_status}")

    existing = connection.execute(
        "SELECT id FROM integrations WHERE business_id = ? AND app = ?",
        (business_id.strip(), app.strip()),
    ).fetchone()
    now = utcnow()
    if existing is None:
        cursor = connection.execute(
            """
            INSERT INTO integrations
            (business_id, app, connection_offered, auth_status, permissions_granted,
             actions_tested, manual_remainder, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                business_id.strip(),
                app.strip(),
                1 if connection_offered else 0,
                auth_status,
                permissions_granted.strip(),
                actions_tested.strip(),
                manual_remainder.strip(),
                now,
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)
    connection.execute(
        """
        UPDATE integrations
        SET connection_offered = ?, auth_status = ?, permissions_granted = ?,
            actions_tested = ?, manual_remainder = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            1 if connection_offered else 0,
            auth_status,
            permissions_granted.strip(),
            actions_tested.strip(),
            manual_remainder.strip(),
            now,
            int(existing["id"]),
        ),
    )
    connection.commit()
    return int(existing["id"])


def is_connected(connection: sqlite3.Connection, business_id: str, app: str) -> bool:
    """Connected only when offered, authorised, and at least one action tested."""
    row = connection.execute(
        "SELECT * FROM integrations WHERE business_id = ? AND app = ?",
        (business_id.strip(), app.strip()),
    ).fetchone()
    if row is None:
        return False
    return bool(row["connection_offered"]) and row["auth_status"] == "granted" and bool(
        row["actions_tested"].strip()
    )


def list_integrations(connection: sqlite3.Connection, business_id: str) -> list[dict]:
    rows = connection.execute(
        "SELECT * FROM integrations WHERE business_id = ? ORDER BY app",
        (business_id.strip(),),
    ).fetchall()
    return [dict(row) for row in rows]
