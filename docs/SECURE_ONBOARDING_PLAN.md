# Secure onboarding plan — every vertical, kept secure under Muse

> The actual plan. Status: design + building blocks shipped; no paying
> installs yet. Every claim below maps to code, a test, or an explicit gap.

## The one sentence

Onboard each trade vertical with least-privilege OAuth into accounts the
customer already owns, draft-never-send agent behavior, approval receipts
on every consequential action — and **no payment credential ever touches
Muse, our servers, or the agent loop**.

## 1. How each vertical gets onboarded (same spine, per-trade packs)

Every vertical ships a pack (`verticals/<trade>/`): manifest, profile,
INSTALL checklist, PAINS, STACK, DISCOVERY, CAMPAIGN. Electrician is
pilot-ready; 10 more verticals exist. The onboarding spine is identical:

1. **Discovery** — record business, services, areas, existing software.
   No credentials collected. Ever.
2. **OAuth into owned accounts** — customer authorizes email/calendar/
   job software via each provider's OAuth flow. We hold scoped tokens,
   never passwords. Least-privilege scopes per capability
   (connector/manifest.json).
3. **Enquiry workflow** — capture + draft replies. Drafts only.
4. **Price book approval** — customer approves exact prices. The agent
   quotes ONLY from this book (OFFER.md rule; enforced in prompts).
5. **Quote draft + owner approval** — every outbound quote needs a human
   grant via approvals.request_approval/grant_approval. No auto-send path
   exists in code.
6. **Scheduling proposal** — same approval gate as quotes.
7. **Google profile assistance** — manual, through Google's UI.
8. **Training + written handover** — customer demonstrates the workflow
   unaided before completion.
9. **14-day fixes** — support window with measured minutes.

Task states (`not_started/in_progress/blocked/verified`) live in installs.py.
`verified` requires evidence. Failed third-party verification can never be
marked complete.

## 2. Payments: the hard line

**Customers never give Muse — or us — payment credentials. There is no
flow in which that could even happen:**

| Money question | Answer |
|---|---|
| Customer's card/bank details | Never collected. No field, no flow, no storage. |
| Paying suppliers | Customer pays in their own bank/Stripe/banking app. We see amounts only if they tell us or via read-only accounting integration they authorize. |
| Getting paid by THEIR customers | Their existing invoicing/bank transfer. We draft payment *reminders* (text), never initiate transfers. `initiating payments` is in compliance.py HIGH_RISK_ACTIVITIES — always legal-review queue. |
| Paying aionboard (£499/£999/£79) | Stripe payment LINK (Stripe-hosted page). PAN goes customer→Stripe. We keep tokens/references/amounts only (SAQ A posture). |
| Muse + money | The connector manifest exposes NO payment capability. Muse cannot request what isn't declared; Meta review gates what is. Shop Pay / Stripe stay on Stripe-hosted surfaces. |
| Red-team proof | `approval-bypass` + `quote-fraud` attacks run against every install. A bypass that succeeds blocks rollout until fixed. |

If anyone — customer, agent, or Muse — asks where to put card details into
our system, the answer is nowhere: no such field exists by design.

## 3. Staying secure under Muse (ongoing, not one-off)

1. **Connector is read-only + one gated write.** `business_lookup`,
   `pain_lookup`, `install_status`, `opportunity_digest` (reads, no
   approval). `draft_quote` only (write-gated, never sends, approval
   receipt required). This is declared in connector/manifest.json and
   enforced in code, not prompts.
2. **Approval receipts on everything consequential.** Propose → grant →
   execute in separate steps, separate actors. Audit log stores shapes +
   hashes, never values (security.py).
3. **Red-team on schedule.** `aionboard/redteam` runs the 8 attack classes
   against each install's assistant config; evidence JSONL kept per run.
   Any breach blocks that install's Muse exposure until re-tested green.
4. **Regulations expire.** Every rule carries review_date
   (regulations/registry.json). Past-date rules are excluded from agent
   prompts until re-verified. Stale law is worse than no law.
5. **Free checks + paid reports.** security_audit runs domain checks
   (HTTPS, TLS expiry, headers) free; digest-pinned report with red-team
   section as the paid peace-of-mind product.
6. **Rate limits + tiers.** Reads auto-approved; queries logged; writes
   approved; destructive blocked. Per-client sliding windows.
7. **Token hygiene.** Scoped OAuth tokens, short-lived where supported.
   No passwords held. Rotation on any exposure (aocsec scripts).

## 4. Per-vertical rollout order

1. **Electrician** (pilot-pack-ready now) — richest pack, clear pains,
   EV/solar overlap with POW parts intelligence later.
2. **Plumbing/heating** — same job-management shape, gas-safety rules
   already in registry (Gas Safety Regs 1998).
3. **Cleaners, gardeners** — simpler workflows, facilities-contract
   opportunities from powuk signals.
4. Remaining verticals only after 3 paying electrician installs validate
   the 4–6 hour delivery target (OFFER.md constraint).

## 5. Gaps (honest)

- No paying installs yet — all security claims are pre-customer.
- Muse UK availability unconfirmed; everything works without it.
- Shop Pay integration undesigned (needs POW procurement API first).
- WhatsApp production integration blocked on Meta review.
- Cloudflare Access for operator dashboards not yet enabled (aocsec doc exists).
