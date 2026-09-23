"""Per-target assistant factory.

Builds the system prompt from target identity + legislation + live
opportunities, then runs it through the OpenAI Agents SDK when installed,
or returns a dry-run session payload otherwise (agentcom control-plane
harness pattern: dry-run is the default, live needs key + explicit flag).

The agent never executes writes itself. Consequential actions go through
approvals.request_approval() and need a human grant.
"""

from __future__ import annotations

import os
from typing import Any

from .legislation import cite, rules_for_target
from .powuk_bridge import opportunities_for_target
from .targets import TargetProfile

try:
    import agents  # openai-agents SDK (optional)
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False


def build_system_prompt(
    profile: TargetProfile,
    *,
    topic: str = "",
    top_n_opportunities: int = 5,
) -> str:
    """Compose the assistant's instructions for one target."""
    parts = [profile.system_identity()]

    rules = rules_for_target(profile.vertical, topic=topic)
    if rules:
        parts.append(
            "Rules that apply to this business "
            "(verify before acting; never quote expired rules):"
        )
        parts.extend(f"- {cite(r)}" for r in rules)

    try:
        opps = opportunities_for_target(profile, top_n=top_n_opportunities)
    except Exception:
        opps = []
    if opps:
        parts.append(
            f"Live nearby opportunities ({len(opps)} matched from public "
            "procurement/planning signals — leads, not confirmed jobs):"
        )
        parts.extend(
            f"- [{o.get('score', 0)}] {o.get('title', '')[:120]} "
            f"({_src(o)})"
            for o in opps
        )
    else:
        parts.append("No live opportunities matched right now.")

    parts.append(
        "Operating rules: draft, never send. Quote only from the approved "
        "price book. Every consequential action needs a human approval "
        "receipt first. Say what you don't know."
    )
    return "\n".join(parts)


def _src(o: dict) -> str:
    return str(o.get("_source", "unknown source"))


def build_session(
    profile: TargetProfile,
    task: str,
    *,
    topic: str = "",
    model: str | None = None,
    mcp_servers: list[dict] | None = None,
    execute: bool = False,
) -> dict:
    """Build (and optionally run) an agent session for a target.

    Returns a dry-run payload dict unless execute=True AND the SDK is
    installed AND OPENAI_API_KEY is set. Anything else raises.
    """
    prompt = build_system_prompt(profile, topic=topic)
    tools = [{"type": "mcp", "server_label": m["label"], "url": m["url"]}
             for m in (mcp_servers or [])]
    payload = {
        "agent": {"model": model or os.environ.get("OPENAI_AGENT_MODEL", "gpt-5"),
                  "tools": tools},
        "target": {"business_id": profile.business_id,
                   "vertical": profile.vertical,
                   "postcode": profile.postcode},
        "input": f"{prompt}\n\nTASK: {task}",
    }
    if not execute:
        return {"dry_run": True, "payload": payload}
    if not AGENTS_AVAILABLE:
        raise RuntimeError("openai-agents SDK not installed")
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not configured")
    from agents import Agent, Runner
    agent = Agent(name=f"aionboard-{profile.business_id}",
                  instructions=prompt)
    result = Runner.run_sync(agent, task)
    return {"dry_run": False, "output": result.final_output,
            "payload": payload}


def assistant_status() -> dict[str, Any]:
    """What the assistant layer can do in this environment."""
    return {
        "agents_sdk": AGENTS_AVAILABLE,
        "live_execution": AGENTS_AVAILABLE and bool(os.environ.get("OPENAI_API_KEY")),
        "default": "dry_run",
    }
