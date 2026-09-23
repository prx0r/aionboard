"""Explicit approval and isolation checks for consequential actions.

Two layers:
- Prototype helpers (approve_action/execute_outbound): in-memory checks only.
- Authenticated receipts (issue_approval/redeem_approval): customer-bound,
  payload-hashed, expiring, one-time-use tokens with an audit trail.
  Production flows must use the authenticated layer.
"""

from __future__ import annotations

import hashlib
import json
import re
import secrets
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Mapping

SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----"),
    re.compile(
        r"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*\S+"
    ),
)


@dataclass(frozen=True)
class Approval:
    approval_id: str
    client_id: str
    action: str
    target: str
    approver: str
    approved_at: str


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def scan_text(text: str) -> list[str]:
    """Return secret-pattern matches without returning surrounding secrets."""
    findings: list[str] = []
    for pattern in SECRET_PATTERNS:
        for _ in pattern.finditer(text or ""):
            findings.append(f"secret-pattern:{pattern.pattern[:24]}")
    return sorted(set(findings))


def approve_action(*, client_id: str, action: str, target: str, approver: str) -> Approval:
    normalized_client = client_id.strip()
    normalized_action = action.strip()
    normalized_target = target.strip()
    normalized_approver = approver.strip()
    if not all([normalized_client, normalized_action, normalized_target, normalized_approver]):
        raise ValueError("client, action, target, and approver are required")
    return Approval(
        approval_id=uuid.uuid4().hex,
        client_id=normalized_client,
        action=normalized_action,
        target=normalized_target,
        approver=normalized_approver,
        approved_at=utcnow(),
    )


def execute_outbound(*, approval: Approval, client_id: str, action: str, target: str) -> dict:
    """Authorize an outbound action but never perform a live send in this pilot."""
    if (
        approval.client_id != client_id.strip()
        or approval.action != action.strip()
        or approval.target != target.strip()
    ):
        raise PermissionError("approval does not match the requested outbound action")
    return {
        "sent": False,
        "authorized": True,
        "dry_run": True,
        "approval_id": approval.approval_id,
    }


def assert_customer_isolation(client_a: Mapping[str, object], client_b: Mapping[str, object]) -> bool:
    """Ensure two customer records do not share credentials or storage."""
    client_a_id = str(client_a.get("client_id", "")).strip()
    client_b_id = str(client_b.get("client_id", "")).strip()
    if not client_a_id or not client_b_id:
        raise ValueError("both clients require client_id")
    if client_a_id == client_b_id:
        raise ValueError("client records must have different client_id values")

    for field in ("credential_refs", "storage_paths"):
        values_a = set(_as_tuple(client_a.get(field, ())))
        values_b = set(_as_tuple(client_b.get(field, ())))
        shared = values_a & values_b
        if shared:
            joined = ", ".join(sorted(shared))
            raise ValueError(f"customers share {field}: {joined}")
    return True


def _as_tuple(value: object) -> Iterable[str]:
    if value is None:
        return ()
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item).strip()]
    text = str(value).strip()
    return (text,) if text else ()


def stable_client_fingerprint(client_id: str, created_at: str) -> str:
    payload = f"{client_id.strip()}|{created_at.strip()}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def init_approval_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS approvals (
            token TEXT PRIMARY KEY,
            business_id TEXT NOT NULL,
            approver TEXT NOT NULL,
            action TEXT NOT NULL,
            target TEXT NOT NULL,
            payload_hash TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            used INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY,
            at TEXT NOT NULL,
            business_id TEXT NOT NULL,
            action TEXT NOT NULL,
            detail TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS idx_audit_business ON audit_log(business_id);
        """
    )
    connection.commit()


def _payload_hash(payload: Mapping[str, Any] | None) -> str:
    canonical = json.dumps(payload or {}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _audit(connection: sqlite3.Connection, business_id: str, action: str, detail: str = "") -> None:
    connection.execute(
        "INSERT INTO audit_log (at, business_id, action, detail) VALUES (?, ?, ?, ?)",
        (utcnow(), business_id.strip(), action.strip(), detail.strip()),
    )
    connection.commit()


def issue_approval(
    connection: sqlite3.Connection,
    *,
    business_id: str,
    approver: str,
    action: str,
    target: str,
    payload: Mapping[str, Any] | None = None,
    ttl_seconds: int = 300,
) -> str:
    """Issue a one-time approval token bound to customer, action, and exact payload."""
    business = business_id.strip()
    if not business or not approver.strip() or not action.strip() or not target.strip():
        raise ValueError("business_id, approver, action, and target are required")
    if ttl_seconds <= 0:
        raise ValueError("ttl_seconds must be positive")

    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)).isoformat()
    connection.execute(
        """
        INSERT INTO approvals
        (token, business_id, approver, action, target, payload_hash, expires_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            token,
            business,
            approver.strip(),
            action.strip(),
            target.strip(),
            _payload_hash(payload),
            expires_at,
            utcnow(),
        ),
    )
    connection.commit()
    _audit(connection, business, "approval_issued", f"{action} -> {target}")
    return token


def redeem_approval(
    connection: sqlite3.Connection,
    *,
    token: str,
    business_id: str,
    action: str,
    target: str,
    payload: Mapping[str, Any] | None = None,
) -> dict:
    """Redeem a token once. Mismatches, expiry, and replay all fail closed."""
    row = connection.execute(
        "SELECT * FROM approvals WHERE token = ?", (token,)
    ).fetchone()
    if row is None:
        _audit(connection, business_id, "approval_rejected", "unknown token")
        raise PermissionError("unknown approval token")
    if int(row["used"]):
        _audit(connection, business_id, "approval_rejected", "token already used")
        raise PermissionError("approval token already used")
    if row["business_id"] != business_id.strip():
        _audit(connection, business_id, "approval_rejected", "wrong customer")
        raise PermissionError("approval is bound to a different customer")
    if row["action"] != action.strip() or row["target"] != target.strip():
        _audit(connection, business_id, "approval_rejected", "action/target mismatch")
        raise PermissionError("approval does not match the requested action")
    if row["payload_hash"] != _payload_hash(payload):
        _audit(connection, business_id, "approval_rejected", "payload mismatch")
        raise PermissionError("approval does not match the exact payload")
    if datetime.now(timezone.utc).isoformat() > row["expires_at"]:
        _audit(connection, business_id, "approval_rejected", "token expired")
        raise PermissionError("approval token expired")

    connection.execute("UPDATE approvals SET used = 1 WHERE token = ?", (token,))
    connection.commit()
    _audit(connection, business_id, "approval_redeemed", f"{action} -> {target}")
    return {"authorized": True, "sent": False, "dry_run": True, "approval": action}


def audit_history(connection: sqlite3.Connection, business_id: str) -> list[dict]:
    rows = connection.execute(
        "SELECT at, action, detail FROM audit_log WHERE business_id = ? ORDER BY id",
        (business_id.strip(),),
    ).fetchall()
    return [dict(row) for row in rows]


def assert_tenant_rows(rows: list[dict], business_id: str, id_field: str = "business_id") -> bool:
    """Enforce tenant scope: every row must belong to the expected business.

    Call this on any result set before acting on it. Cross-tenant rows
    fail closed rather than leaking into another customer's workflow.
    """
    expected = business_id.strip()
    if not expected:
        raise ValueError("business_id is required")
    for row in rows:
        actual = str(row.get(id_field, "")).strip()
        if actual != expected:
            raise PermissionError(
                f"tenant breach: row belongs to {actual or 'unknown'}, expected {expected}"
            )
    return True


UNTRUSTED_PREFIX = "[untrusted-external] "


def mark_untrusted(text: str) -> str:
    """Tag uploaded files, third-party messages, and imported text.

    Tagged content is data, never instructions. Downstream prompts must
    refuse to execute anything inside a tagged block.
    """
    content = (text or "").strip()
    if content.startswith(UNTRUSTED_PREFIX):
        return content
    return UNTRUSTED_PREFIX + content


def contains_instruction_override(text: str) -> bool:
    """Detect prompt-injection patterns in untrusted material."""
    lowered = (text or "").lower()
    patterns = (
        "ignore previous instructions",
        "ignore all instructions",
        "disregard your instructions",
        "you are now ",
        "system prompt",
        "send without approval",
        "skip approval",
        "approve this automatically",
    )
    return any(pattern in lowered for pattern in patterns)


def approve_automation_policy(
    connection: sqlite3.Connection,
    *,
    business_id: str,
    approver: str,
    scope: str,
    limits: str,
) -> str:
    """Approve a narrowly defined recurring automation policy.

    Covers identical operational reminders only. Promotional broadcasts,
    payment-term changes, unusual quotations, and anything higher-risk
    always require per-action approval instead.
    """
    if not scope.strip() or not limits.strip():
        raise ValueError("scope and limits are required")
    return issue_approval(
        connection,
        business_id=business_id,
        approver=approver,
        action="automation-policy",
        target=scope.strip(),
        payload={"limits": limits.strip()},
        ttl_seconds=30 * 24 * 3600,
    )
