# BUILD_NOTES.md

> Session-by-session build log for AI Onboard.

---

## Session 2026-09-23 — Initial setup + research

### Context
AI Onboard is a UK trades business onboarding service. The insight: use existing data (powuk, cgraphuk, influence, BigQuery) to identify prospects, define services, and deliver installations using Muse infrastructure.

### What was done

#### 1. Repository setup
- Created `/root/aionboard/` repo
- Saved VISION.md (full market research)
- Created REPORT.md (powuk × aionboard integration)
- Created INTEGRATION.md (how repos connect)
- Created SERVICE_CATALOG.md (service offerings by sector)
- Created PROSPECT_SCORING.md (scoring system)
- Created SALES_PLAYBOOK.md (sales scripts + objection handling)
- Created BUILD_NOTES.md (this file)

#### 2. Data research
- Cloned ographuk, cgraphuk, influence repos
- Analyzed BigQuery graph (24 verticals, 73 pain points, 374 nodes)
- Exported 10,000 electrical businesses from powuk
- Mapped Muse capabilities to services

#### 3. Key findings

**BigQuery graph shows:**
- Electrician = #1 vertical (score 4.6, tier 1)
- Beauty = #2 (score 4.5)
- Barber = #3 (score 4.4)
- 73 pain points across 16 categories
- 174 stack tools indexed
- 8 opportunities identified

**cgraphuk already has:**
- Electrician campaign fully developed
- 24 vertical templates
- 72 pain points
- Onboarding strategy

**influence already has:**
- 15-minute onboarding guide
- Email/phone/WhatsApp provisioning
- Job pipeline (lead → invoice)
- Voice agent infrastructure

**powuk has:**
- 10,000+ electrical businesses
- 184 postcode regions
- Planning applications
- Procurement contracts
- Labour market data

### Current state
```
10,000 prospects exported (prospects_electrical.csv)
24 sectors analyzed (BigQuery)
5 service packages defined
3 founding client slots available
Sales playbook ready
```

### Files created
```
/root/aionboard/
├── VISION.md              (17KB) — full market research
├── REPORT.md              (12KB) — powuk integration
├── INTEGRATION.md         (18KB) — repo connections + Muse
├── SERVICE_CATALOG.md     (12KB) — service offerings
├── PROSPECT_SCORING.md    (4KB) — scoring system
├── SALES_PLAYBOOK.md      (8KB) — sales scripts
├── BUILD_NOTES.md         (this file)
└── prospects_electrical.csv (1MB) — 10,000 businesses
```

### Next steps
1. Build demonstration workflow using influence
2. Set up BigQuery dataset for aionboard
3. Create Google Business Profile checker
4. Build first sales email template
5. Start making calls to Greater Manchester prospects

---

## Session 2026-09-23 — Peer-review checkpoint

### Context
The peer review found untested API claims, expanded-bundle pricing, unverified sales outcomes, and missing executable software.

### What was done
- Added canonical narrow pilot scope in `OFFER.md`.
- Corrected Google, Meta, OpenMuse/Muse, pricing, discovery, prospect, and sales claims.
- Added `verticals/electrician/` and a reusable vertical template.
- Built local SQLite CRM, install state machine, fictional demo, handover generator, approval/isolation checks, and static pilot website.
- Added 19 acceptance tests and GitHub Actions CI.
- Marked website builds, live voice, Meta production integration, custom integrations, and lead generation as separate future deliverables.

### Current state
- 19 tests pass.
- No completed paying installation is recorded.
- Public prospect CSV remains research-only, with no verified phone numbers, permission, or TPS/CTPS results.

### Next steps
1. Validate OAuth, Google, and Meta access manually before promising automation.
2. Run the fictional demo during one qualified sales conversation.
3. Record delivery time for the first real pilot before changing pricing.

---

## Session 2026-09-23 — Beauty vertical and subdomain decision

### Context
Beauty is a strong second pilot because missed calls, deposits, repeat bookings, packages, and reviews map cleanly onto the same narrow installation workflow.

### What was done
- Added `verticals/beauty/` using the reusable vertical template.
- Added vertical-pack acceptance tests.
- Kept `beauty.aionboard.co.uk` as the proposed subdomain.
- Did not create a separate beauty domain or customer database.

### Current state
- 23 tests pass.
- Pilot verticals: electrician and beauty.
- No completed paying installation is recorded.

### Next steps
1. Validate one electrician installation before expanding beauty outreach.
2. Keep shared CRM, install checklist, handover, security, and website code vertical-agnostic.
3. Add new verticals by copying `verticals/_template/`, not by forking infrastructure.

---

## Session 2026-09-23 — Nine niche packs

### Context
The nine `targets.md` niches needed the same repeatable folder structure as electrician and beauty.

### What was done
- Added niche packs for nails, lashes, hair, dog groomers, cleaners, gardeners/window cleaners, car detailers, driving instructors, and weddings.
- Reused the shared manifest, README, pains, stack, campaign, discovery, and install skeleton.
- Marked car detailers, driving instructors, and wedding photography as research stubs where dedicated upstream assets are missing.
- Kept all proposed public surfaces under `aionboard.co.uk`.

### Current state
- 23 tests pass.
- Pilot verticals: electrician and beauty.
- Niche packs: 9 research/pilot skeletons.
- No completed paying installation is recorded.

### Next steps
1. Validate electrician first.
2. Validate nails/lashes as the second pilot.
3. Promote other niche packs from research stub to pilot only after dedicated discovery.

---

## Session 2026-09-23 — MCP, stack capture, data policy, vertical legal

### Context
Peer review asked for an MCP-first direction, a clear existing-stack strategy, data/security/backup policy, and per-vertical legalities plus UK opportunities.

### What was done
- Added `MCP.md` and `mcp/tools.json`: 5 read tools, 4 gated write tools, OAuth/scoped-token design, audit requirements.
- Added `STACK_CAPTURE.md`: ask → classify → verify → record flow with integrate/import-from/replace verdicts.
- Added `stack_items` table to the CRM with replace-gate (customer approval required).
- Added `DATA_POLICY.md`: data classes, retention, backups, incident response, customer rights.
- Added `aionboard/backup.py`: timestamped SQLite backups with SHA-256 manifests and verify.
- Added `legal` + `uk_opportunities` to all 11 vertical profiles from cgraphuk legislation registry and powuk sources.
- Added 9 new tests (stack capture, backups, MCP contracts).

### Current state
- 32 tests pass.
- No completed paying installation is recorded.
- Ongoing tech support deliberately deferred.

### Next steps
1. Build the remote HTTPS MCP server (read tools first).
2. Validate one electrician installation before expanding outreach.
3. Submit Muse connector when eligible.

---

## Session 2026-09-23 — Finance and tax per vertical

### Context
Each vertical needed legislation detail plus what businesses normally use for money: accounting, payments, and tax obligations.

### What was done
- Researched UK trade accounting (QuickBooks/Xero/FreeAgent/Sage), beauty payments (Fresha/Stripe/Square/Treatwell), and MTD ITSA thresholds (£50k Apr 2026, £30k Apr 2027, £20k Apr 2028).
- Added `finance` (accounting, payments, typical monthly cost, notes) and `tax` (MTD, VAT £90k, CIS, CT, payroll) sections to all 11 vertical profiles.
- Extended profile template and validation tests.

### Current state
- 32 tests pass.
- Finance data marked with sources; cost ranges marked hypothesis.
- No completed paying installation is recorded.

### Next steps
1. Validate finance stacks with the first real customer per vertical.
2. Confirm MTD filing workflows with the customer's accountant.
3. Record actual monthly software spend to replace hypotheses.

---

## Session 2026-09-23 — Integration pipelines and checkpoints

### Context
Needed an honest answer to whether an automated existing-stack → integrated-stack pipeline exists, plus checkpoint definitions for pilot vs retention.

### What was done
- Added `integration_pipeline` to the profile schema: tool, current_state, target_state, method, mcp_tool, approval, evidence, status.
- Backfilled all 11 verticals. Every step is honestly marked `manual`; no MCP server is deployed and no OAuth flows exist yet.
- Added `CHECKPOINTS.md`: checkpoint 1 (manual pilot with evidence) vs checkpoint 2 (retention wedge with separate consent/pricing).

### Current state
- 32 tests pass.
- Control plane exists (CRM, installs, handover, approvals). Connectors do not.
- No completed paying installation is recorded.

### Next steps
1. Validate one manual electrician installation.
2. Automate one integration step at a time with customer evidence.
3. Only then build checkpoint 2 retention features.

---

## Session 2026-09-23 — Peer-review checkpoint 2: quickstart product

### Context
Peer review found the CRM excluded sole traders, installs only supported one package, approvals and backups were documentary, and pricing didn't include the £20 product.

### What was done
- Canonical `business_id` with optional Companies House identity; sole traders supported.
- Channel-specific marketing consent plus separate POW opportunity consent.
- Package registry: `standard-ai-setup` (£499) and `muse-quickstart` (£20) across all 11 manifests.
- Configurable onboarding engine with 3 recipes; vertical task overlays (nails no longer needs electrician quoting).
- Completion separated from the 7-day support window.
- Capability-aware integration inventory: offered/auth/tested/manual-never-connected-without-proof.
- Manual generator with vertical prompts, checklist, privacy, troubleshooting, access removal.
- Seven-day support workflow with guide/human/minutes tracking.
- Authenticated approvals: customer-bound, payload-hashed, expiring, one-time, audited.
- Backups via SQLite backup API + integrity_check + Fernet encryption + restore test.
- DATA_POLICY breach rules corrected (ICO 72h, individuals without undue delay, controller notification, international transfers).
- E2E test: fictional nail tech, no company number, full journey, POW consent stays off.

### Current state
- 41 tests pass.
- No completed paying installation is recorded.

### Next steps
1. Validate one manual electrician installation.
2. Validate one £20 nail-tech quickstart and measure support minutes.
3. Build the remote HTTPS MCP server starting with read tools.

---

## Session 2026-09-23 — Full devplan implementation

### Context
Saved the competitive research + dev brief as `devplan.md`, then implemented Checkpoints A–J.

### What was done
- Checkpoint A: `muse-quickstart` (£20) alongside `standard-ai-setup` in OFFER, CHECKPOINTS, website, all 11 manifests. Support allowance + abuse limits documented.
- Checkpoint B: canonical `business_id` CRM already existed; verified sole-trader support, channel-specific marketing consent, separate POW consent.
- Checkpoint C: capability registry upgraded with supplier/region/plan/scopes/method/charges/review states; `set_capability_state` with verified-gate.
- Checkpoint D: onboarding tasks gained prerequisites, execution method, recovery actions; `resume_onboarding` for idempotent resume.
- Checkpoint E: tenant-scope enforcement, untrusted-input marking, prompt-injection detection, long-lived automation policies.
- Checkpoint F: export/delete procedures; suppression tombstones (not indefinite); breach policy already corrected.
- Checkpoint G: capability-filtered vertical prompts; uploadable non-sensitive manual version.
- Checkpoint H: support issue categories + error codes.
- Checkpoint I: versioned compliance registry (6 seed rules) + legal-review queue + staleness check.
- Checkpoint J: 12 new acceptance tests including 5 fictional installs, Booksy no-migration, unsupported connector, failed auth, tenant isolation, modified quote, financial draft-only, marketing refusal, export/revocation, interrupted setup, support closure.

### Current state
- 53 tests pass.
- No completed paying installation is recorded.
- PEER_REVIEW pricing block superseded by OFFER.md.

### Next steps
1. Validate one manual electrician installation.
2. Validate one £20 nail-tech quickstart and measure support minutes.
3. Build the remote HTTPS MCP server starting with read tools.

---

## Session 2026-09-23 — Trust-first process reframing

### Context
Exact per-tool API automation is the wrong deliverable. Customers won't hand over credentials; trust is the product. Reframed around customer-led process with security guarantees at each step.

### What was done
- New `TRUST_MODEL.md`: five guarantees (no passwords, no money movement, no silent sends, revocable everything, minimal data) plus see/never-see table.
- Rewrote `AUTOMATION_PLAYBOOK.md` as trust-first process cards: goal, customer action, our action, what we see, what we never touch, how to revoke, if-blocked fallback. Removed untested API code samples.
- Added trust-rules pointer to all 11 vertical INSTALL.md files.

### Current state
- 53 tests pass.
- No completed paying installation is recorded.

### Next steps
1. Validate one manual electrician installation.
2. Validate one £20 nail-tech quickstart and measure support minutes.

---

## Session 2026-09-23 — Geographic opportunities + strategy doc

### Context
Saved the strategic analysis as STRATEGY.md, then combined it with powuk signals geographically so the retention pitch becomes "your assistant finds opportunities near you."

### What was done
- `STRATEGY.md`: flaws, security deployed-vs-documented gap, per-vertical AI-vs-human table, honest unit economics (£20 loses standalone, £499 funds the business).
- Audited powuk signals: planning descriptions + authority entities, OCDS buyer localities/postcodes, ONS labour by region, 10k businesses across 184 areas.
- `aionboard/opportunities.py`: keyword scoring per vertical, outward-area matching, approval-gated digest. Conservative by design.
- `GEO_OPPORTUNITIES.md`: per-vertical signal map, matching flow, Muse angle, stated limits.
- 14 new matcher tests.

### Current state
- 67 tests pass.
- No completed paying installation is recorded.

### Next steps
1. Validate one manual electrician installation.
2. Validate one £20 nail-tech quickstart and measure support minutes.
3. Feed live powuk signals into the matcher on a schedule.

---

## Session 2026-09-23 — Two-sided matching

### Context
Opportunity matching only answered "what work is coming." The inverse — "who near me might need me" — completes the loop and powers the retention pitch.

### What was done
- `match_customers()` + `customer_digest()`: same scoring engine, customer-side framing with compliant next steps per vertical.
- Planning applicants treated as research, never prospects. Contact still needs verified details, permission, TPS/CTPS.
- `GEO_OPPORTUNITIES.md`: two-sided model table plus hard-parts analysis (what Meta absorbs vs what we own).
- 4 new matcher tests.

### Current state
- 71 tests pass.
- No completed paying installation is recorded.

### Next steps
1. Validate one manual electrician installation.
2. Validate one £20 nail-tech quickstart and measure support minutes.
3. Feed live powuk signals into the matcher on a schedule.

---

## Session 2026-09-23 — Combined regulations source

### Context
Needed one combined source for legislation, tax, finance, security, voice, marketing, and AI-agent rules that every vertical pack, manual, and prompt can read from.

### What was done
- `regulations/registry.json`: 36 rules — 26 imported from cgraphuk (attributed) + 10 new (VAT, CT, payroll/NICs, FCA payments, PECR, call recording, secrets, tenant isolation, Muse UK, ChatGPT MCP).
- `regulations/README.md`: domains, review policy, honesty rules, read pattern.
- `compliance.py` now seeds from the registry file (falls back to built-in seeds).
- Tests enforce schema, parseable review dates, known verticals, honest design-rule labelling, DB seeding parity, staleness, and that every profile `legal[]` ID exists in the registry.

### Current state
- 81 tests pass.
- No completed paying installation is recorded.

### Next steps
1. Validate one manual electrician installation.
2. Validate one £20 nail-tech quickstart and measure support minutes.
3. Re-verify registry entries on schedule; stale rules must not be used.

---

## Session 2026-09-23 — Knowledge graph + free chatbot wedge

### Context
Needed a zero-marginal-cost funnel (TikTok → site → £20) and a queryable structure over all vertical packs plus regulations.

### What was done
- `aionboard/graph.py`: 111 nodes, 179 edges from verticals + registry. Keyword retrieval with cited answers; honest ignorance on no match.
- `site/chat.html` + `site/knowledge.json`: static demo chatbot. Same retrieval logic in JS, disclaimer on page, no accounts, no sends.
- `FUNNEL.md`: content plan (one pain → one number → one demo question), conversion metrics, kill rules for videos.
- 10 new tests (graph coverage, cited answers, demo status, no guarantees, bundle parity).

### Current state
- 91 tests pass.
- No completed paying installation is recorded.

### Next steps
1. Publish 5 pilot TikToks and measure views → chat → email.
2. Validate one manual electrician installation.
3. Validate one £20 nail-tech quickstart and measure support minutes.

---

## Adding new build notes

When you make changes, add a new session header with:
1. Context (why)
2. What was done (specifics)
3. Current state (numbers)
4. Files changed (list)
5. Next steps
