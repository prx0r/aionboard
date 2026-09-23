"""Explicit approval and isolation checks for consequential actions."""

from __future__ import annotations

import hashlib
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Mapping

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
