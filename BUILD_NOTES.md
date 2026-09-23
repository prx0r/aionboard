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

## Adding new build notes

When you make changes, add a new session header with:
1. Context (why)
2. What was done (specifics)
3. Current state (numbers)
4. Files changed (list)
5. Next steps
