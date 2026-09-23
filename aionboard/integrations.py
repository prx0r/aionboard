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

# Full capability lifecycle per the dev brief. `connected` means authorised;
# only `verified` means a real action was tested end to end.
CAPABILITY_STATES = {
    "not_supported",
    "eligibility_unknown",
    "available",
    "authorization_pending",
    "connected",
    "verified",
    "blocked",
    "revoked",
}


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
            supplier TEXT NOT NULL DEFAULT '',
            supported_region TEXT NOT NULL DEFAULT '',
            eligible_account_type TEXT NOT NULL DEFAULT '',
            required_plan TEXT NOT NULL DEFAULT '',
            authorised_scopes TEXT NOT NULL DEFAULT '',
            connection_method TEXT NOT NULL DEFAULT '',
            recurring_charges TEXT NOT NULL DEFAULT '',
            docs_reviewed_at TEXT NOT NULL DEFAULT '',
            capability_state TEXT NOT NULL DEFAULT 'eligibility_unknown',
            observed_result TEXT NOT NULL DEFAULT '',
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
    supplier: str = "",
    supported_region: str = "",
    eligible_account_type: str = "",
    required_plan: str = "",
    authorised_scopes: str = "",
    connection_method: str = "",
    recurring_charges: str = "",
    docs_reviewed_at: str = "",
    capability_state: str = "eligibility_unknown",
    observed_result: str = "",
) -> int:
    if not business_id.strip() or not app.strip():
        raise ValueError("business_id and app are required")
    if auth_status not in AUTH_STATUSES:
        raise ValueError(f"unsupported auth status: {auth_status}")
    if capability_state not in CAPABILITY_STATES:
        raise ValueError(f"unsupported capability state: {capability_state}")

    existing = connection.execute(
        "SELECT id FROM integrations WHERE business_id = ? AND app = ?",
        (business_id.strip(), app.strip()),
    ).fetchone()
    now = utcnow()
    values = (
        1 if connection_offered else 0,
        auth_status,
        permissions_granted.strip(),
        actions_tested.strip(),
        manual_remainder.strip(),
        supplier.strip(),
        supported_region.strip(),
        eligible_account_type.strip(),
        required_plan.strip(),
        authorised_scopes.strip(),
        connection_method.strip(),
        recurring_charges.strip(),
        docs_reviewed_at.strip(),
        capability_state,
        observed_result.strip(),
        now,
    )
    if existing is None:
        cursor = connection.execute(
            """
            INSERT INTO integrations
            (business_id, app, connection_offered, auth_status, permissions_granted,
             actions_tested, manual_remainder, supplier, supported_region,
             eligible_account_type, required_plan, authorised_scopes,
             connection_method, recurring_charges, docs_reviewed_at,
             capability_state, observed_result, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (business_id.strip(), app.strip()) + values,
        )
        connection.commit()
        return int(cursor.lastrowid)
    connection.execute(
        """
        UPDATE integrations
        SET connection_offered = ?, auth_status = ?, permissions_granted = ?,
            actions_tested = ?, manual_remainder = ?, supplier = ?,
            supported_region = ?, eligible_account_type = ?, required_plan = ?,
            authorised_scopes = ?, connection_method = ?, recurring_charges = ?,
            docs_reviewed_at = ?, capability_state = ?, observed_result = ?,
            updated_at = ?
        WHERE id = ?
        """,
        values + (int(existing["id"]),),
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


def set_capability_state(
    connection: sqlite3.Connection,
    *,
    business_id: str,
    app: str,
    state: str,
    observed_result: str = "",
) -> None:
    """Move a capability through its lifecycle.

    `verified` requires a tested action on record. A mock test never
    promotes a feature from manual to verified automation.
    """
    if state not in CAPABILITY_STATES:
        raise ValueError(f"unsupported capability state: {state}")
    row = connection.execute(
        "SELECT * FROM integrations WHERE business_id = ? AND app = ?",
        (business_id.strip(), app.strip()),
    ).fetchone()
    if row is None:
        raise ValueError("unknown integration")
    if state == "verified" and not row["actions_tested"].strip():
        raise ValueError("verified requires a tested action on record")
    connection.execute(
        "UPDATE integrations SET capability_state = ?, observed_result = ?, updated_at = ? WHERE id = ?",
        (state, observed_result.strip(), utcnow(), int(row["id"])),
    )
    connection.commit()


def list_integrations(connection: sqlite3.Connection, business_id: str) -> list[dict]:
    rows = connection.execute(
        "SELECT * FROM integrations WHERE business_id = ? ORDER BY app",
        (business_id.strip(),),
    ).fetchall()
    return [dict(row) for row in rows]
