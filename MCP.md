# MCP.md — MCP-first architecture

> One audited MCP gateway, scoped tools, approval receipts. Usable by ChatGPT today, Muse when available, human operators in the meantime.

## Status

Design contract only. No MCP server is deployed yet. Tool definitions live in `mcp/tools.json`.

## Architecture

```
ChatGPT / Muse / Claude / human operator
        ↓ OAuth 2.1 + scoped tokens
AI Onboard MCP gateway
        ↓ per-action approval + audit log
Local CRM / installs / handovers
```

The agent never touches customer systems directly. Every write produces an approval receipt and an audit entry.

## Tool tiers

### Read-only tools (no approval needed)

| Tool | What it returns |
|------|-----------------|
| `vertical_lookup` | Vertical manifest + profile |
| `pain_lookup` | Pain mappings with verification basis |
| `stack_lookup` | Current-software intelligence |
| `install_status` | Checklist state for a business |
| `handover_read` | Generated handover (never secrets) |

### Gated write tools (explicit approval + evidence)

| Tool | Gate |
|------|------|
| `record_contact_attempt` | TPS/CTPS + suppression check |
| `set_install_task` | Evidence required for `verified` |
| `generate_handover` | Rejected if secrets detected |
| `draft_quote` | Never auto-sends; returns draft + approval receipt |

Every write returns:

```json
{
  "sent": false,
  "authorized": true,
  "approval_id": "...",
  "evidence": "..."
}
```

## Platform reality

| Platform | Status |
|----------|--------|
| ChatGPT custom connectors | Real, gated: Developer Mode + paid plan, remote HTTPS only, per-action confirmation |
| ChatGPT plugin directory | Real, repackaged MCP apps/skills; availability varies by plan/region/workspace |
| Meta Muse | US-only, no confirmed UK date; connector platform open with Meta review, no published fees/timeline |
| OpenMuse | Separate open-source project; does not grant Meta access |
| Local CRM/installs | Working Python implementation in `aionboard/` |

## Security rules

1. OAuth 2.1 with PKCE and audience-bound tokens (RFC 8707). Reject tokens issued for other resources. No broad API keys, no static keys.
2. Tool-level RBAC at the gateway, not per server. Per-tool scopes; a read token can never invoke writes.
3. Short-lived tokens (15–60 min), rotation, tested revocation path.
4. Rate limits per client and per tool (`RateLimiter`).
5. Audit every call including denials: identity, tool, argument hash (never values), scopes, result, latency (`audit_tool_call()`).
6. Never log tokens, headers, secrets, or full payloads. Redact at the source (`redact_args()`), not downstream.
7. Customer data isolation: one client's credentials and storage paths must never be reachable from another client's session.
8. Secrets never enter prompts, handovers, logs. `scan_text()` rejects them.
9. Failed verification can never be recorded as complete.
10. Approval tiers: auto-approve reads → log-and-proceed queries → require-approval writes → block destructive.
11. HTTPS only. Prompt-injection defense in layers (scopes + rate limits + confirmations + audit), never prompt wording alone.

Full design: `SECURITY_ARCHITECTURE.md`.

## What to build

1. Remote HTTPS MCP server exposing the 5 read tools first.
2. OAuth with `verticals:read` and `installs:read` scopes.
3. Tool-call audit log table.
4. Gated write tools behind approval receipts.
5. ChatGPT Developer Mode test with read-only tools.
6. Muse connector submission when eligible.
