# DEVPLAN_NEXT.md — what happens from here

> The companion to `devplan.md` (the brief that built the current system) and `THREADS.md` (the open work list). This file says *in what order, to what standard, and what kills what.*

## 0. Honest baseline (23 Sep 2026)

- 147 tests passing, secrets clean, tree organized, remote in sync.
- 11 vertical packs, 36-rule regulations registry, working CRM/install/manual/support/backup code.
- Static site + demo chatbot + dashboard mock, all generated and honest.
- MCP contracts designed, connector pack drafted, neither deployed nor submitted.
- **Zero paying customers. Zero measured delivery hours. Zero support minutes.**
- Three agents share the repo; merge discipline (pull-rebase-verify-push) is load-bearing.

Everything below is sequenced to change exactly one of those zeroes at a time.

---

## 1. Phase 0 — Prove the unit works (now → first revenue)

**Goal:** One £20 electrician install and one £20 nail-tech quickstart, both measured.

### 1A. Sell (threads T1, T2, T3)

1. Enrich 50 Manchester electrical prospects: find numbers, verify trading status, screen TPS/CTPS, record provenance. No calls before screening — ever.
2. Work the call list with `SALES_PLAYBOOK.md`. Log every objection as research.
3. Parallel track: 20 nail techs via Instagram/TikTok DMs (permission-first, no spam).
4. Target: 5 discovery conversations (electrician) + 5 (nails) before changing the offer.

**Gate:** If 50 enriched prospects yield zero conversations, the problem is the offer or the channel, not the tooling. Pause and rewrite the pitch before building anything.

### 1B. Deliver (threads T1, T2)

1. Run the install checklists manually. Time every task with a stopwatch.
2. Generate handover + manual from the actual state, not the template.
3. Record: delivery hours, support minutes per day, failed connections, customer comprehension (can they demo the workflow back?), refund risk.
4. Ask for referral + case-study permission. Accept no gracefully.

**Gate:** If median support minutes exceed 20 on the £20 product, kill or reprice it. If the £20 install takes >8 hours, narrow its scope. Numbers decide, not optimism.

### 1C. Measure (threads T2, T4)

1. Publish the 5 TikToks. Measure views → chat → email weekly.
2. Run `fleet_support_report()` after every support interaction.
3. Kill videos that don't move email. Double down on repeated chatbot questions.

**Phase 0 exit criteria:**
- [ ] 1 verified £20 install with measured hours + handover
- [ ] 1 verified £20 install with measured support minutes
- [ ] Funnel metrics exist (even if bad — bad numbers are data)
- [ ] Go/no-go decision on both price points, in writing, in BUILD_NOTES

---

## 2. Phase 1 — Repeat it five times (first revenue → repeatability)

**Goal:** Prove the install is a process, not a heroic one-off.

1. Run 4 more installs (mix of electrician + nails) using *only* the documented checklists — no improvisation that isn't written down afterward.
2. After each: update the vertical pack with what actually happened (real stack, real minutes, real objections).
3. Promote nothing to automation yet. The rule stands: 3+ successful manual runs before any step graduates.
4. Start the referral ask at day 30 for every customer.

**Phase 1 exit criteria:**
- [ ] 5 verified installs with manuals
- [ ] Median delivery/support minutes known per package
- [ ] At least 1 referral received (proof the flywheel has a pulse)
- [ ] Vertical packs updated with real (not hypothesized) stacks

---

## 3. Phase 2 — Automate one step at a time (repeatability → leverage)

**Goal:** Convert repeated manual successes into verified automation, cheapest step first.

Order (by evidence burden, lowest first):

1. **Booking-link verification** — already coded (`verify.py`), needs real-customer runs to graduate from `manual`.
2. **Review-request workflow** — deterministic, low risk, high visibility.
3. **Reminder preparation** — templates + scheduling, owner approves sends.
4. **Quote drafting** — highest value, highest risk; last to automate, approval receipts mandatory.

Each graduation requires: 3+ manual successes → automated implementation → 1 successful automated run with evidence → profile status flip → test update. Skip any step and the status stays `manual`.

**Phase 2 exit criteria:**
- [ ] ≥3 steps graduated with customer evidence
- [ ] No step graduated on mock-test evidence alone
- [ ] Support-minutes trend flat or falling as automation lands

---

## 4. Phase 3 — Deploy the gateway (leverage → platform)

**Goal:** The MCP contracts become a running server. (Security agent's territory — coordinate, don't duplicate.)

1. Remote HTTPS server, OAuth 2.1 + PKCE, audience-bound tokens, per-tool scopes — read tools first.
2. Approval receipts + tenant isolation + audit pipeline switched on, then pen-tested.
3. ChatGPT Developer Mode connection test with read tools.
4. Muse connector submission *only* when: gateway live + OAuth tested + ≥1 verified install for end-to-end review.

**Phase 3 exit criteria:**
- [ ] Gateway live with deny-logging and audit trail
- [ ] ChatGPT connected in Developer Mode
- [ ] Connector submitted (or documented blocker from Meta)

---

## 5. Phase 4 — Retention wedge (platform → revenue expansion)

**Goal:** Give customers a reason to stay. Only after Phase 1 proves the core.

Order:

1. **Opportunity alerts** — weekly digest from the matcher, separately consented and priced. Prove accuracy before charging.
2. **Ad creation via aoc** — per-creative quotes, measured per FUNNEL.md.
3. **Custom dashboard backend** — only after 5+ customers ask for it.
4. **POW opportunities** — opt-in only, charged separately after proving useful.

**Phase 4 exit criteria:**
- [ ] ≥1 retention product with paying users and measured accuracy
- [ ] No customer data flows to POW without explicit opt-in (audited)

---

## 6. What NOT to do (standing orders)

1. **No new verticals** until electrician + nails are validated. The 9 niche packs stay as skeletons.
2. **No BigQuery migration** until 10+ paying customers make SQLite painful (thread T12).
3. **No subscription products** until retention is proven, not projected.
4. **No Muse dependency** in any customer promise until UK launch + connector approval.
5. **No architecture documents** without accompanying code or customer evidence. Docs describe what exists or what was measured — never what might exist.
6. **No touching other agents' active work** without coordinating. Three agents, one `main`: pull, rebase, full suite, push.

## 7. Kill criteria (agree these now, while calm)

| Signal | Action |
|--------|--------|
| 50 enriched prospects → 0 conversations | Rewrite pitch/channel, pause building |
| £20 median support > 20 min after 5 installs | Kill or reprice to £49+ |
| £20 install consistently > 8 hours | Narrow scope, split package |
| 0 referrals after 5 happy customers | Flywheel thesis wrong; investigate before scaling |
| Muse UK delayed past Q2 2027 | Rebrand quickstart assistant-agnostic permanently |
| Any phase's exit criteria unmet after 90 days | Retrospective: wrong goal, wrong method, or wrong market? |

## 8. Source documents

| This plan draws on | For |
|---|---|
| `THREADS.md` T1–T12 | The open work list |
| `STRATEGY.md` | Economics that constrain every decision |
| `devplan.md` Checkpoints A–J | The build order that got us here |
| `CHECKPOINTS.md` | Pilot vs retention boundary |
| `FUNNEL.md` + `TIKTOK_BATCH_01.md` | Acquisition mechanics |
| `GEO_OPPORTUNITIES.md` | Retention product spec |
| `PEER_REVIEW.md` | What not to repeat |
