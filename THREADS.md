# THREADS.md — open threads

> Every unfinished thing in one place. Each thread has an owner, a blocker (or "none — just do it"), and a definition of done. Close threads by doing them, not by editing this file.

## How to read status

- `OPEN` — not started, actionable now
- `IN PROGRESS` — someone is actively working it
- `BLOCKED` — waiting on something outside our control
- `DONE` — verified complete (moved to bottom on close)

---

## T1 — First real electrician installation (CRITICAL PATH)

- **Status:** OPEN
- **Owner:** founder (sales + delivery, cannot delegate yet)
- **What:** One manual £20 pilot install for a real electrical business. Measure delivery hours end-to-end.
- **Blocked by:** Nothing. Prospects exist in `prospects_electrical.csv`; playbook in `SALES_PLAYBOOK.md`; checklist in `verticals/electrician/INSTALL.md`.
- **Done when:** Install checklist all `verified`, handover generated, delivery hours recorded, customer permission (or refusal) for case study logged.
- **Why first:** Every economic assumption, every automation decision, and every sales claim depends on this number.

## T2 — First £20 nail-tech quickstart + support tracking

- **Status:** OPEN
- **Owner:** founder
- **What:** One £20 muse-quickstart for a real nail technician. Track every support minute, failed connection, refund risk, and 7-day active use.
- **Blocked by:** Nothing. E2E path tested (`tests/test_quickstart.py`).
- **Done when:** Onboarded per `is_onboarded()`, manual delivered, support stats show median human minutes. If median > 20 min: kill or reprice per STRATEGY.md.
- **Why second:** Validates or kills the loss-leader thesis with real data.

## T3 — Prospect outreach (Greater Manchester)

- **Status:** OPEN
- **Owner:** founder
- **What:** Enrich, screen (TPS/CTPS + suppression), and call Manchester-area electrical prospects. Aim: 5 discovery conversations.
- **Blocked by:** Nothing. CSV has 10k records; scoring in `PROSPECT_SCORING.md`; scripts in `SALES_PLAYBOOK.md`.
- **Done when:** 5 substantive discovery conversations logged in CRM with objections recorded.
- **Note:** Objections are research data. "Tradify already does that" is as valuable as a yes.

## T4 — TikTok batch production + measurement loop

- **Status:** OPEN (scripts ready, nothing filmed)
- **Owner:** founder
- **What:** Produce the 5 videos in `TIKTOK_BATCH_01.md` via the aoc pipeline. Measure views → chat visits → booking emails weekly per `FUNNEL.md`.
- **Blocked by:** Nothing.
- **Done when:** 5 videos posted, first week of funnel metrics recorded, kill/double-down decisions made.

## T5 — Remote HTTPS MCP server (read tools first)

- **Status:** OPEN
- **Owner:** unassigned (security agent is the natural owner)
- **What:** Deploy the `mcp/tools.json` contract as a running server: OAuth 2.1 + PKCE, audience-bound tokens, per-tool scopes, starting with the 5 read tools.
- **Blocked by:** Nothing technical; needs focused build time. Design in `MCP.md` + `SECURITY_ARCHITECTURE.md`.
- **Done when:** ChatGPT Developer Mode connects to it, read tools return scoped data, audit log captures every call including denials.

## T6 — Muse connector submission

- **Status:** BLOCKED
- **Owner:** unassigned
- **What:** Submit the `connector/` pack to Meta's directory.
- **Blocked by:** T5 (needs running MCP) + T1/T2 (needs a verified install for the review's end-to-end test) + Meta review itself (unpublished timeline).
- **Done when:** Listed in the Muse directory, or rejected with documented reasons.

## T7 — Automate integration steps one at a time

- **Status:** OPEN (nothing to automate yet)
- **Owner:** unassigned
- **What:** Promote individual `manual` pipeline steps to verified automation, one tool at a time, each with customer evidence.
- **Blocked by:** T1/T2 (need repeated manual successes first).
- **Done when (per step):** 3+ successful manual runs → automated → 1 successful automated run with evidence → status flipped in profile.
- **Rule:** Never automate a workflow that still regularly needs human diagnosis.

## T8 — Finance stack validation per vertical

- **Status:** OPEN
- **Owner:** unassigned
- **What:** Replace `typical_monthly_cost_gbp` hypotheses in all 11 profiles with measured customer spend. Confirm MTD filing workflows with each customer's accountant.
- **Blocked by:** T1/T2 (needs real customers).
- **Done when:** Every `pilot-pack-ready` profile cites at least one real customer's stack.

## T9 — Promote research-stub verticals

- **Status:** OPEN (correctly deferred)
- **Owner:** unassigned
- **Verticals:** `car-detailers`, `driving-instructors`, `weddings` (photography side).
- **Blocked by:** Dedicated discovery per vertical (no upstream teardown exists).
- **Done when (each):** Discovery calls done, dedicated pain/stack/campaign written from evidence, status flipped to `pilot-pack-ready`, tests still green.

## T10 — Compliance registry re-verification loop

- **Status:** OPEN (nothing stale today; process needed, not action)
- **Owner:** unassigned
- **What:** Calendar + owner for re-review. Annual for statutes; quarterly for platform rules (`AI-MUSE-UK`, `AI-CHATGPT-MCP`) since Meta/OpenAI shift without notice.
- **Blocked by:** Nothing.
- **Done when:** Review calendar exists and first scheduled re-verification completes. `stale_rules()` is the enforcement mechanism — wire it into CI or a monthly job.

## T11 — Google Business Profile checker

- **Status:** OPEN (carried over from first build session, still unbuilt)
- **Owner:** unassigned
- **What:** Given a business name + postcode, report GBP claim status, completeness, review count/rating. Read-only, public data.
- **Blocked by:** Nothing (public data, no auth needed for basic checks).
- **Done when:** CLI command returns structured GBP status for a test business; used in discovery calls.

## T12 — BigQuery dataset for aionboard

- **Status:** OPEN but DEFERRED (peer review: local CRM first, BigQuery can wait)
- **Owner:** unassigned
- **What:** Prospect/install/support aggregates for dashboards and analysis.
- **Blocked by:** Deliberately deferred until 10+ paying customers make local SQLite painful.
- **Done when:** Deferred item is re-evaluated, not before.

## Closed threads (kept for history)

- Thread hygiene: every BUILD_NOTES "Next steps" item either became a thread above or was completed. No orphaned next-steps remain.
