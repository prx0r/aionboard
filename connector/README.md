# connector/

Muse directory submission pack for the AI Onboard Buddy. Status: **draft, not submitted.**

## Files

- `manifest.json` — product description, capabilities, auth model, privacy posture, review readiness, pricing, and limitations. This is what a Muse connector submission is built from.

## What happens before submission

1. One verified paying installation (any package).
2. Remote HTTPS MCP server running the 5 read tools from `mcp/tools.json`.
3. OAuth 2.1 with the scopes in the manifest, tested end to end.
4. Security review of the approval receipts and tenant isolation.
5. Legal review of the privacy posture against UK GDPR.

Until all five are true, this directory stays a draft. Submitting earlier wastes the one shot at review.

## Design rules for the connector

- Read tools ship first. `draft_quote` ships only with approval receipts enforced server-side.
- The connector never sends, books, pays, or changes customer systems.
- Every answer cites its source: vertical pack, regulation, or installation record.
- Unknown questions get honest ignorance, never invention.
- No customer PII leaves the customer's scope. Ever.
