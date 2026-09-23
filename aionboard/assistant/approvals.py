"""Approval receipts for agent actions.

Receipt shape adapted from agentcom v2 qpsdk (approval_id + evidence on
every write); storage and redaction delegated to aionboard.security
(audit_tool_call, redact_args). Nothing here touches customer systems.

Receipt shape (stable contract for dashboard + MCP):
    {"sent": False, "authorized": bool, "approval_id": str, "evidence": str}
"""

from __future__ import annotations

import sqlite3
from typing import Any, Mapping

from ..security import audit_tool_call


def request_approval(
    connection: sqlite3.Connection,
    *,
    action: str,
    business_id: str,
    arguments: Mapping[str, Any] | None = None,
    evidence: str = "",
) -> dict:
    """Propose an action. Never executes. Returns a pending receipt.

    The human (or policy) approves separately via grant_approval().
    """
    rowid = audit_tool_call(
        connection,
        identity=business_id,
        tool_name=action,
        arguments=arguments,
        scopes=["assistant:propose"],
        result="denied_approval",
    )
    return {
        "sent": False,
        "authorized": False,
        "approval_id": f"apr-{rowid:06d}",
        "evidence": evidence,
        "action": action,
        "business_id": business_id,
    }


def grant_approval(
    connection: sqlite3.Connection,
    receipt: dict,
    *,
    approver: str,
    evidence: str = "",
) -> dict:
    """Human approves a proposed receipt. Still does not execute.

    Execution happens in the owning workflow, which must present this
    receipt. Audit trail records both proposal and grant.
    """
    rowid = audit_tool_call(
        connection,
        identity=approver,
        tool_name=receipt.get("action", ""),
        arguments={"approval_id": receipt.get("approval_id", "")},
        scopes=["assistant:approve"],
        result="success",
    )
    return {
        **receipt,
        "authorized": True,
        "approval_id": f"apr-{rowid:06d}",
        "grant_evidence": evidence or receipt.get("evidence", ""),
    }
