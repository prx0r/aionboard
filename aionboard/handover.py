"""Customer handover generation."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Iterable, Mapping

from .security import scan_text

REQUIRED_SECTIONS = (
    "Configured accounts",
    "Ownership and permissions",
    "Working features",
    "Pending third-party approvals",
    "Recurring subscriptions",
    "Test results",
    "Revoke access",
)


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_handover(
    *,
    business: Mapping[str, object],
    package: str,
    tasks: Iterable[Mapping[str, object]],
    accounts: Iterable[Mapping[str, object]],
    permissions: Iterable[Mapping[str, object]],
    subscriptions: Iterable[Mapping[str, object]],
    test_results: Iterable[Mapping[str, object]],
    revocation: Iterable[str],
    generated_at: str | None = None,
) -> str:
    business_name = str(business.get("name", "")).strip()
    business_id = str(business.get("business_id", "")).strip()
    if not business_name or not business_id:
        raise ValueError("business name and business_id are required")
    if package != "standard-ai-setup":
        raise ValueError("only standard-ai-setup handovers are supported in this pilot")

    normalized_tasks = [_normalize_task(task) for task in tasks]
    if not normalized_tasks:
        raise ValueError("handover requires installation tasks")
    normalized_accounts = [_normalize_account(account) for account in accounts]
    normalized_permissions = [_normalize_permission(permission) for permission in permissions]
    normalized_subscriptions = [_normalize_subscription(subscription) for subscription in subscriptions]
    normalized_tests = [_normalize_test(test) for test in test_results]
    normalized_revocation = [str(step).strip() for step in revocation if str(step).strip()]
    if not normalized_revocation:
        raise ValueError("revocation instructions are required")

    markdown = "\n".join(
        [
            f"# Handover — {business_name}",
            "",
            f"Business ID: `{business_id}`",
            f"Package: `{package}`",
            f"Generated: {generated_at or utcnow()}",
            "",
            "## Configured accounts",
            "",
            *[f"- {account['name']}: owner={account['owner']}, status={account['status']}" for account in normalized_accounts],
            "",
            "## Ownership and permissions",
            "",
            *[f"- {permission['scope']}: {permission['granted_to']} ({permission['method']})" for permission in normalized_permissions],
            "",
            "## Working features",
            "",
            *[
                f"- {task['task']}: {task['status']} — {task['verification'] or 'verification recorded separately'}"
                for task in normalized_tasks
                if task["status"] == "verified"
            ],
            "",
            "## Pending third-party approvals",
            "",
            *[
                f"- {task['task']}: {task['status']} — {task['action'] or 'no action recorded'}"
                for task in normalized_tasks
                if task["status"] != "verified"
            ],
            "",
            "## Recurring subscriptions",
            "",
            *[
                f"- {subscription['name']}: payer={subscription['payer']}, amount={subscription['amount']}"
                for subscription in normalized_subscriptions
            ],
            "",
            "## Test results",
            "",
            *[f"- {test['name']}: {test['result']} ({test['evidence']})" for test in normalized_tests],
            "",
            "## Revoke access",
            "",
            *[f"{index + 1}. {step}" for index, step in enumerate(normalized_revocation)],
            "",
        ]
    )
    findings = scan_text(markdown)
    if findings:
        raise ValueError("handover must not contain secrets")
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in markdown:
            raise ValueError(f"handover is missing section: {section}")
    return markdown


def write_handover(path: str, markdown: str, *, mode: int = 0o600) -> str:
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    os.chmod(path, mode)
    return path


def _normalize_task(task: Mapping[str, object]) -> dict:
    name = str(task.get("task", "")).strip()
    status = str(task.get("status", "")).strip()
    if not name or not status:
        raise ValueError("handover tasks require task and status")
    return {
        "task": name,
        "status": status,
        "action": str(task.get("action", "")).strip(),
        "verification": str(task.get("verification", "")).strip(),
        "evidence": str(task.get("evidence", "")).strip(),
    }


def _normalize_account(account: Mapping[str, object]) -> dict:
    name = str(account.get("name", "")).strip()
    owner = str(account.get("owner", "")).strip()
    status = str(account.get("status", "")).strip()
    if not all([name, owner, status]):
        raise ValueError("handover accounts require name, owner, and status")
    return {"name": name, "owner": owner, "status": status}


def _normalize_permission(permission: Mapping[str, object]) -> dict:
    scope = str(permission.get("scope", "")).strip()
    granted_to = str(permission.get("granted_to", "")).strip()
    method = str(permission.get("method", "")).strip()
    if not all([scope, granted_to, method]):
        raise ValueError("handover permissions require scope, granted_to, and method")
    return {"scope": scope, "granted_to": granted_to, "method": method}


def _normalize_subscription(subscription: Mapping[str, object]) -> dict:
    name = str(subscription.get("name", "")).strip()
    payer = str(subscription.get("payer", "")).strip()
    amount = str(subscription.get("amount", "")).strip()
    if not all([name, payer, amount]):
        raise ValueError("handover subscriptions require name, payer, and amount")
    return {"name": name, "payer": payer, "amount": amount}


def _normalize_test(test: Mapping[str, object]) -> dict:
    name = str(test.get("name", "")).strip()
    result = str(test.get("result", "")).strip()
    evidence = str(test.get("evidence", "")).strip()
    if not all([name, result, evidence]):
        raise ValueError("handover tests require name, result, and evidence")
    return {"name": name, "result": result, "evidence": evidence}
