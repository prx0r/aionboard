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

## Adding new build notes

When you make changes, add a new session header with:
1. Context (why)
2. What was done (specifics)
3. Current state (numbers)
4. Files changed (list)
5. Next steps
