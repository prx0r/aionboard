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

## Adding new build notes

When you make changes, add a new session header with:
1. Context (why)
2. What was done (specifics)
3. Current state (numbers)
4. Files changed (list)
5. Next steps
