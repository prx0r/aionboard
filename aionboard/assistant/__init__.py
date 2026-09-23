"""Per-target integrated chatbot package.

One assistant per business. It knows who they are (target profile),
what rules apply to them (legislation), and what work is nearby
(opportunities from powuk signals).

Pattern sources (read-only, never vendored):
- powops web/server.py ......... dashboard structure (see aionboard/dashboard.py)
- powops mcp.py ................ MCP stdio server shape
- agentcom control-plane ....... OpenAI Agents harness (dry-run default)
- agentcom v2 qpsdk ............ approval-receipt shape
"""

from .targets import TargetProfile, profile_from_business
from .legislation import cite, rules_for_target, is_stale
from .powuk_bridge import load_powuk_signals, opportunities_for_target
from .approvals import request_approval, grant_approval
from .agent import build_system_prompt, build_session, assistant_status

__all__ = [
    "TargetProfile",
    "profile_from_business",
    "cite",
    "rules_for_target",
    "is_stale",
    "load_powuk_signals",
    "opportunities_for_target",
    "request_approval",
    "grant_approval",
    "build_system_prompt",
    "build_session",
    "assistant_status",
]
