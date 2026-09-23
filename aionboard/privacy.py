"""Data export and deletion procedures.

Covers the operational database. Backups, object storage, and connected
third-party accounts need their own deletion passes, recorded in the
audit log. Suppression tombstones are retained only to prevent further
unwanted marketing — never used for marketing themselves.
"""

from __future__ import annotations

import sqlite3

TABLES_WITH_BUSINESS = (
    "prospects",
    "contacts",
    "contact_attempts",
    "tps_checks",
    "stack_items",
    "integrations",
    "consents",
    "support_tickets",
    "onboardings",
)

BUSINESS_ID_COLUMNS = {
    "prospects": "company_number",
    "contacts": "company_number",
    "contact_attempts": "company_number",
    "tps_checks": "company_number",
    "stack_items": "company_number",
    "integrations": "business_id",
    "consents": "business_id",
    "support_tickets": "business_id",
    "onboardings": "business_id",
}


def export_business(
    connection: sqlite3.Connection, *, business_key: str, by: str = "business_id"
) -> dict:
    """Export everything held about a business. Used for subject-access requests."""
    if by not in ("business_id", "company_number"):
        raise ValueError("by must be business_id or company_number")
    key = business_key.strip()
    if not key:
        raise ValueError("business key is required")

    export: dict[str, list[dict]] = {}
    for table in TABLES_WITH_BUSINESS:
        column = BUSINESS_ID_COLUMNS[table]
        if (column == "business_id") != (by == "business_id"):
            continue
        try:
            rows = connection.execute(
                f"SELECT * FROM {table} WHERE {column} = ?", (key,)
            ).fetchall()
        except sqlite3.OperationalError:
            export[table] = []
            continue
        export[table] = [dict(row) for row in rows]
    # Include onboarding state when present.
    try:
        rows = connection.execute(
            "SELECT o.*, COUNT(t.id) AS task_count FROM onboardings o "
            "LEFT JOIN onboarding_tasks t ON t.onboarding_id = o.id "
            "WHERE o.business_id = ? GROUP BY o.id",
            (key,),
        ).fetchall() if by == "business_id" else []
        export["onboardings"] = [dict(row) for row in rows]
    except sqlite3.OperationalError:
        export["onboardings"] = []
    return export


def delete_business(
    connection: sqlite3.Connection,
    *,
    business_id: str | None = None,
    company_number: str | None = None,
    keep_suppression: bool = True,
) -> dict:
    """Delete a business and its records.

    When keep_suppression is true and a do-not-contact record exists, a
    minimal tombstone (identifier + suppression flag only) is retained to
    prevent further unwanted marketing. Tombstones are reviewed
    periodically and never used for marketing.
    """
    deleted: dict[str, int] = {}
    suppressed = False

    if company_number:
        key, column = company_number.strip().upper(), "company_number"
    elif business_id:
        key, column = business_id.strip(), "business_id"
    else:
        raise ValueError("business_id or company_number is required")

    if keep_suppression and column == "company_number":
        row = connection.execute(
            "SELECT 1 FROM contact_attempts WHERE company_number = ? AND outcome = 'do_not_contact' LIMIT 1",
            (key,),
        ).fetchone()
        suppressed = row is not None

    for table in TABLES_WITH_BUSINESS:
        if BUSINESS_ID_COLUMNS[table] != column:
            continue
        try:
            if keep_suppression and suppressed and table == "contact_attempts":
                cursor = connection.execute(
                    f"DELETE FROM {table} WHERE {column} = ? AND outcome != 'do_not_contact'",
                    (key,),
                )
            else:
                cursor = connection.execute(f"DELETE FROM {table} WHERE {column} = ?", (key,))
            deleted[table] = cursor.rowcount
        except sqlite3.OperationalError:
            deleted[table] = 0
    if column == "business_id":
        try:
            cursor = connection.execute(
                "DELETE FROM onboarding_tasks WHERE onboarding_id IN "
                "(SELECT id FROM onboardings WHERE business_id = ?)",
                (key,),
            )
            deleted["onboarding_tasks"] = cursor.rowcount
            cursor = connection.execute("DELETE FROM onboardings WHERE business_id = ?", (key,))
            deleted["onboardings"] = cursor.rowcount
        except sqlite3.OperationalError:
            deleted.setdefault("onboarding_tasks", 0)
            deleted.setdefault("onboardings", 0)

    try:
        if column == "business_id":
            cursor = connection.execute("DELETE FROM businesses WHERE business_id = ?", (key,))
        else:
            cursor = connection.execute(
                "DELETE FROM businesses WHERE company_number = ?", (key,)
            )
        deleted["businesses"] = cursor.rowcount
    except sqlite3.OperationalError:
        deleted["businesses"] = 0

    connection.commit()
    deleted["suppression_tombstone_kept"] = int(suppressed)
    return deleted
