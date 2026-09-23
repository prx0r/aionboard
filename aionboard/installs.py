"""Pilot installation checklist state machine."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

REQUIRED_TASKS = (
    "discovery",
    "email_authorization",
    "calendar_authorization",
    "enquiry_workflow",
    "price_book_approval",
    "quote_draft",
    "owner_quote_approval",
    "scheduling_proposal",
    "google_profile_assistance",
    "training",
    "handover",
    "fourteen_day_fixes",
)
OPTIONAL_TASKS = (
    "website_build",
    "live_voice_service",
    "meta_production_integration",
    "custom_integration",
    "lead_generation",
)
STATUSES = ("not_started", "in_progress", "blocked", "verified")
OWNER_TYPES = {"agent", "customer", "supplier"}


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_install(
    connection: sqlite3.Connection,
    *,
    business_id: str,
    vertical: str = "electrician",
    package: str = "standard-ai-setup",
) -> int:
    business = business_id.strip()
    if not business:
        raise ValueError("business_id is required")
    if not vertical.strip():
        raise ValueError("vertical is required")
    if package != "standard-ai-setup":
        raise ValueError("only standard-ai-setup is supported in this pilot")
    if business.lower().startswith("demo-") is False and not business:
        raise ValueError("business_id is required")

    cursor = connection.execute(
        """
        CREATE TABLE IF NOT EXISTS installs (
            id INTEGER PRIMARY KEY,
            business_id TEXT NOT NULL UNIQUE,
            vertical TEXT NOT NULL,
            package TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """,
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS install_tasks (
            id INTEGER PRIMARY KEY,
            install_id INTEGER NOT NULL REFERENCES installs(id) ON DELETE CASCADE,
            task TEXT NOT NULL,
            owner TEXT NOT NULL DEFAULT '',
            authorization TEXT NOT NULL DEFAULT '',
            action TEXT NOT NULL DEFAULT '',
            verification TEXT NOT NULL DEFAULT '',
            evidence TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'not_started',
            updated_at TEXT NOT NULL,
            UNIQUE(install_id, task)
        )
        """,
    )
    cursor = connection.execute(
        "INSERT INTO installs (business_id, vertical, package, created_at) VALUES (?, ?, ?, ?)",
        (business, vertical.strip(), package, utcnow()),
    )
    install_id = int(cursor.lastrowid)
    now = utcnow()
    for task in REQUIRED_TASKS:
        connection.execute(
            """
            INSERT INTO install_tasks
            (install_id, task, status, updated_at)
            VALUES (?, ?, 'not_started', ?)
            """,
            (install_id, task, now),
        )
    connection.commit()
    return install_id


def set_task(
    connection: sqlite3.Connection,
    *,
    install_id: int,
    task: str,
    status: str,
    owner: str = "",
    authorization: str = "",
    action: str = "",
    verification: str = "",
    evidence: str = "",
) -> None:
    if task not in REQUIRED_TASKS and task not in OPTIONAL_TASKS:
        raise ValueError(f"unknown task: {task}")
    if status not in STATUSES:
        raise ValueError(f"unknown status: {status}")
    if task in OPTIONAL_TASKS:
        raise ValueError("optional website, voice, Meta, custom, and lead tasks are separate deliverables")

    normalized_owner = owner.strip()
    normalized_authorization = authorization.strip()
    normalized_action = action.strip()
    normalized_verification = verification.strip()
    normalized_evidence = evidence.strip()

    if status in {"in_progress", "blocked", "verified"}:
        if not normalized_owner:
            raise ValueError("owner is required")
        if normalized_owner not in OWNER_TYPES:
            raise ValueError("unsupported owner")
        if not normalized_authorization:
            raise ValueError("authorization is required")
        if not normalized_action:
            raise ValueError("action is required")
    if status == "verified":
        if not normalized_verification:
            raise ValueError("verification is required")
        if not normalized_evidence:
            raise ValueError("evidence is required")

    cursor = connection.execute(
        """
        UPDATE install_tasks
        SET owner = ?, authorization = ?, action = ?, verification = ?,
            evidence = ?, status = ?, updated_at = ?
        WHERE install_id = ? AND task = ?
        """,
        (
            normalized_owner,
            normalized_authorization,
            normalized_action,
            normalized_verification,
            normalized_evidence,
            status,
            utcnow(),
            install_id,
            task,
        ),
    )
    if cursor.rowcount == 0:
        raise ValueError("unknown installation task")
    connection.commit()


def get_install(connection: sqlite3.Connection, install_id: int) -> dict:
    install = connection.execute(
        "SELECT * FROM installs WHERE id = ?",
        (install_id,),
    ).fetchone()
    if install is None:
        raise ValueError("unknown installation")
    tasks = connection.execute(
        "SELECT * FROM install_tasks WHERE install_id = ? ORDER BY task",
        (install_id,),
    ).fetchall()
    return {"install": dict(install), "tasks": [dict(task) for task in tasks]}


def is_complete(connection: sqlite3.Connection, install_id: int) -> bool:
    state = get_install(connection, install_id)
    required = {task["task"]: task for task in state["tasks"] if task["task"] in REQUIRED_TASKS}
    if len(required) != len(REQUIRED_TASKS):
        return False
    return all(task["status"] == "verified" for task in required.values())
