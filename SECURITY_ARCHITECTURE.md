# SECURITY_ARCHITECTURE.md

> How AI Onboard stays secure by never touching what matters: no card data, no passwords, no live money movement.

## The core design: money never touches us

Card data flows customer → payment provider directly. Our systems only ever see tokens, references, and metadata.

```
Customer card ──→ Stripe Checkout / Elements / payment link ──→ Stripe
                         (hosted by Stripe, PCI Level 1)
                                     ↓
AI Onboard sees only: payment_id, amount, status, last4
AI Onboard never sees: PAN, CVC, expiry, bank credentials
```

This is the industry-standard pattern (Stripe Connect, SAQ A):

1. **Tokenization, not storage.** Card numbers are replaced by tokens at capture. Tokens carry no exploitable value. A system holding only tokens falls outside full PCI DSS scope.
2. **Hosted fields.** Card entry happens in Stripe-hosted iframes or payment links, never in our pages or prompts.
3. **No raw PANs in logs, prompts, handovers, or backups.** `scan_text()` rejects them; audit logs hash arguments instead of storing values.
4. **No bank aggregation.** We never collect banking credentials. Account-information or payment-initiation needs go to FCA-authorised providers.

If our entire infrastructure were compromised tomorrow, an attacker would find configuration pointers and metadata — no card numbers, no bank logins, no money to move.

## Scoped mandates: the agent can't overspend by design

Borrowed from agentic-commerce practice (Stripe SPTs, Mastercard Agent Pay, AP2 mandates): every approval is a token bound to customer + action + exact payload + expiry. It cannot be:

- **Reused** — one-time use, marked spent on redeem.
- **Retargeted** — payload hash mismatch fails closed.
- **Transferred** — bound to one customer ID.
- **Replayed later** — 5-minute default expiry.

Long-lived automation (e.g. weekly reminders) uses narrowly-scoped policies approved explicitly, never blanket permissions. Promotional sends, payment-term changes, and unusual amounts always require fresh per-action approval.

## MCP server hardening (for the future remote server)

From current MCP security guidance, applied in order:

1. **OAuth 2.1 + PKCE**, audience-bound tokens (RFC 8707). Reject tokens issued for other resources.
2. **Per-tool scopes**, not one broad scope. A read tool's token can't invoke writes.
3. **Short-lived tokens** (15–60 min), refresh rotation, revocation path tested.
4. **Rate limits** per client and per tool — a runaway agent can't fire 10k calls/minute.
5. **Audit every call including denials**, with argument *hashes* not values.
6. **Never log** tokens, headers, secrets, or full payloads.
7. **Approval tiers**: auto-approve reads → log-and-proceed queries → require-approval writes → block destructive.
8. **Prompt-injection defense in layers**: least-privilege scopes + rate limits + human confirmation for consequential tools + audit. No single layer is trusted alone.
9. **HTTPS only**, valid certificates, no plaintext tokens.
10. **Tool drift detection**: pin approved tool definitions; flag changes before deployment.

## Audit rules

Every tool call logs: timestamp, identity, tool name, argument hash (SHA-256, never values), scopes, result, latency. Denials log louder than successes — 200 denied calls from one client is the security event, not the success that preceded it.

Audit logs live append-only, separate from the systems they monitor, retained 3 years (see `DATA_POLICY.md`).

## What we deliberately don't build

- No card vault. No PAN storage. No SAQ D burden.
- No bank credential collection. No screen-scraping.
- No autonomous payments. No "AI pays suppliers for you."
- No shared master logins. No password sharing of any kind.

## Sources

- Stripe PCI/tokenization guides; Connect payment-links docs
- MCP authorization spec (OAuth 2.1, 2025-11-25) and security best-practice guides (CSA, Data Workers, moeed.app, DVNC)
- Visa Artemis agentic-payments report; Mastercard Verifiable Intent; AgentWallet/Cream control-plane pattern
