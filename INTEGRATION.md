# INTEGRATION.md — How the Repos Connect

> Three existing repos + BigQuery + powuk = the complete AI Onboard stack.

---

## Executive Summary

You don't need to build AI Onboard from scratch. The infrastructure already exists across four repositories and one BigQuery dataset. The work is packaging, not engineering.

```
ographuk    → FIND prospects (UK business intelligence)
cgraphuk    → DECIDE what to sell (playbooks, pain points, campaigns)
influence   → DELIVER the installation (email, phone, job management, invoicing)
powuk       → POWER lead generation (labour data, procurement, planning)
BigQuery    → STORE everything (graph, observations, opportunities)
```

---

## Repository Map

### 1. ographuk — UK Business Intelligence

**Purpose:** Canonical Oracle runtime for UK data collection.

**What it has:**
- Entity identity system (stable IDs across sources)
- Raw evidence storage (hash-addressed, immutable)
- Provenance records
- Schema manifest
- Companies House adapter (fixture-backed)
- 56 passing tests

**What it's missing:**
- Live data ingestion (Companies House not wired yet)
- Geographic matching
- Cross-source entity resolution
- MCP query interface

**Role in AI Onboard:**
- Prospect database (electrical businesses)
- Geographic targeting (postcode → region)
- Business age/status verification
- Growth signal detection

**Key files:**
```
oracle/ids.py           — content-hash IDs
oracle/contracts.py     — schemas-as-code
oracle/provenance.py    — raw hashing + ingest receipts
oracle/sources/         — source adapters
```

---

### 2. cgraphuk — Business Playbooks

**Purpose:** Industry-specific pain points, solutions, tools, and campaigns.

**What it has:**
- **24 vertical templates** (electrician, barber, beauty, restaurant, etc.)
- **72 prioritised pain points** (3 per vertical)
- **174 indexed tools** (software solutions)
- **24 campaign briefs** (go-to-market strategies)
- Voice profiles for 11 verticals
- Electrician campaign fully developed

**What it's missing:**
- Company population layer (empty)
- Revenue validation
- Live customer data

**Role in AI Onboard:**
- "What to sell" — pain points and solutions for each trade
- "How to sell" — campaign briefs and messaging
- "What tools to configure" — software recommendations
- "What problems to solve" — prioritized by severity

**Key files:**
```
graph/campaigns/CAMP-ELECTRICIAN-GB.md    — electrician campaign
graph/docs/UK_ONBOARDING_CAMPAIGNS.md     — full onboarding strategy
graph/pain/PAIN_POINT_REGISTRY.md         — ~100 pain points
graph/tool/tools.json                     — 174 tools
tpl/tpl-electrician-gb.json               — electrician template
```

**The electrician campaign already proposes:**
1. Free wedge: missed-call recovery (voice agent)
2. Soft onboarding: email, phone, basic website
3. Full stack: voice agent, booking, invoicing, reviews
4. ChatGPT-native: everything through ChatGPT

---

### 3. influence — Implementation Infrastructure

**Purpose:** Business identity provisioning, email, phone, job management, automation.

**What it has:**
- Domain management (Porkbun/Name.com integration)
- Email provisioning (Cloudflare Workers)
- Phone/Telnyx integration
- WhatsApp Cloud API integration
- LiveKit voice agent infrastructure
- Job management (lead → qualified → quoted → scheduled → done → invoiced)
- Quote builder
- Invoice generation
- Google Calendar integration
- MCP server for AI agents
- Dashboard

**What it's missing:**
- Multi-tenant client isolation (security audit needed)
- Production-ready deployment
- Client billing system

**Role in AI Onboard:**
- "How to deliver" — the actual installation infrastructure
- "What to configure" — email, phone, voice, calendar
- "How to manage" — job pipeline, quotes, invoices
- "How to automate" — voice agent, WhatsApp, approvals

**Key files:**
```
stevejobless/SKILL.md                    — 15-min onboarding guide
stevejobless/stevejobless/tradie.py      — job pipeline (lead → invoice)
stevejobless/stevejobless/knowledge/     — business config YAMLs
stevejobless/stevejobless/domain_deals.py — domain management
dash/mcp.py                              — MCP server for AI agents
```

**The tradie system already models:**
- Enquiries (voice, WhatsApp, email, SMS, web)
- Quotes (price book, draft, confirm)
- Scheduling (availability, slots)
- Jobs (status tracking, photos)
- Invoices (generation, payment)
- Stats (answer rate, quote win rate, revenue)

---

### 4. powuk — UK Physical Economy Data

**Purpose:** UK physical constraint graph — where demand outstrips supply.

**What it has:**
- 10,000+ electrical businesses (Companies House, SIC 43210)
- 175,000+ job adverts (ONS labour demand)
- 50,000+ salary records (ONS salaries)
- 5,000+ procurement contracts (Contracts Finder)
- 5,000+ planning applications
- 1,424 training providers (APAR)
- 11,295 F-gas certified companies (REFCOM)
- Regional breakdown (183 postcode areas)

**Role in AI Onboard:**
- "Who to call" — prospect database with postcodes
- "Where to focus" — regional density analysis
- "What's happening" — planning apps, procurement signals
- "What's the market" — labour demand, salary data

---

## BigQuery Dataset

### Project
```
project-ff2366d2-8fda-4fcb-9ba
```

### Dataset: `drop`

| Table | Records | What it has | AI Onboard use |
|-------|---------|-------------|----------------|
| `vertical_rankings` | 24 | Ranked verticals with scores | Which trades to target first |
| `pain_points` | 73+ | Pain points by industry | What problems to solve |
| `graph_nodes` | 374 | Business entities, tools, patterns | Prospect database |
| `graph_observations` | 150+ | Readiness, leaks, installed base | Market intelligence |
| `opportunities` | 8 | Business models with ticket ranges | Revenue planning |
| `country_data` | — | UK-specific metrics | Market sizing |

### Key queries for AI Onboard

```sql
-- Top verticals to target
SELECT vertical, overall_score, tier, first_capability
FROM drop.vertical_rankings
ORDER BY overall_score DESC
LIMIT 5;

-- Pain points for trades
SELECT pain_id, pain_name, pain_category, annual_impact_gbp
FROM drop.pain_points
WHERE pain_category = 'missed_inbound';

-- Business readiness by vertical
SELECT node_id, metric_name, metric_value
FROM drop.graph_observations
WHERE metric_name = 'readiness.has_owned';

-- Opportunities
SELECT name, category, ticket_range, countries
FROM drop.opportunities;
```

---

## How They Connect

```
                    AI Onboard
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    FIND PROSPECTS   DECIDE WHAT    DELIVER INSTALL
         │           TO SELL            │
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │ographuk │    │cgraphuk  │    │influence │
    │         │    │          │    │          │
    │UK data  │    │Playbooks │    │Email     │
    │Business │    │Pain pts  │    │Phone     │
    │Identities│    │Campaigns │    │WhatsApp  │
    └────┬────┘    └────┬─────┘    │Jobs      │
         │              │          │Invoices  │
         ▼              ▼          └────┬─────┘
    ┌─────────┐    ┌──────────┐        │
    │ powuk   │    │ BigQuery │        │
    │         │    │          │        │
    │10K elec │    │Graph     │        │
    │business │    │Observations       │
    │Labour   │    │Verticals │        │
    │Procure  │    │Pain pts  │        │
    └─────────┘    └──────────┘        │
                                       │
                                       ▼
                              ┌──────────────┐
                              │  Customer    │
                              │  Business    │
                              │  (live)      │
                              └──────────────┘
```

---

## What to Build First

### Phase 1: Package existing work (week 1)

1. **Take cgraphuk's electrician campaign** → turn into customer-discovery questionnaire
2. **Take influence's onboarding SKILL.md** → turn into installation checklist
3. **Take powuk's electrical businesses** → export as prospect CSV
4. **Take BigQuery's vertical_rankings** → use for sales prioritization

### Phase 2: First paid installation (weeks 2-3)

1. **Use influence** to provision AI Onboard's own domain/email/phone
2. **Build demonstration** using influence's tradie system
3. **Manually research 100 electrical businesses** from powuk data
4. **Make cold calls** using cgraphuk's messaging
5. **Deliver 3 founding-client installations** using influence's infrastructure

### Phase 3: Scale (months 2-3)

1. **Automate prospect scoring** using powuk + BigQuery
2. **Build repeatable installation** from influence's workflow
3. **Add lead generation** using powuk's procurement/planning data
4. **Submit Muse connector** when UK access available

---

## Security Issues to Fix

Before any client deployment:

1. **influence/dash/mcp.py** — `phone.send` lacks per-message approval check
2. **influence** — multi-tenant client data isolation not verified
3. **influence** — voice system needs security audit
4. **All repos** — ensure no secrets in code

---

## Data Flow

```
Customer signs up
        ↓
AI Onboard creates prospect record (BigQuery)
        ↓
Uses cgraphuk playbook to identify pain points
        ↓
Uses influence to provision domain/email/phone
        ↓
Uses influence to configure voice agent/WhatsApp
        ↓
Customer starts receiving enquiries
        ↓
AI Onboard monitors (influence dashboard)
        ↓
Uses powuk data to find additional leads
        ↓
Customer gets more jobs
        ↓
Customer pays monthly subscription
```

---

## Revenue Model (revised)

| Service | Price | What you're doing |
|---------|-------|-------------------|
| AI Business Setup | £499 one-off | Installation (influence infrastructure) |
| Advisory Support | £79/month | Monitoring + adjustments |
| Lead Generation | £149/month | powuk data → targeted leads |
| Invoice/Payment | 2.5% of invoices | Transaction revenue |
| Custom Development | £750+ | Bespoke integrations |

**Year 1 target (100 installations):**
```
80 × £499 = £39,920
20 × £79/mo × 6 months = £9,480
10 × £149/mo × 6 months = £8,940
─────────────────────────────
Total: ~£58,340
```

---

## Summary

| What | Where | Status |
|------|-------|--------|
| Prospect database | powuk (10K+ electrical businesses) | ✅ Ready |
| Pain points | cgraphuk (72 pains, 24 verticals) | ✅ Ready |
| Campaign briefs | cgraphuk (24 campaigns) | ✅ Ready |
| Installation infra | influence (email, phone, jobs, invoices) | ⚠️ Needs security audit |
| Market intelligence | BigQuery (verticals, graph, observations) | ✅ Ready |
| Lead generation | powuk (labour, procurement, planning) | ✅ Ready |

**You don't need another large software project. You need to turn selected parts of this existing work into a repeatable, paid installation.**

---

## The Advertising Wedge

The real business isn't onboarding. It's the relationship.

### The insight

Every trades business has the same problems:
- Finding customers
- Converting enquiries to jobs
- Managing admin
- Staying compliant
- Growing without burning out

**AI Onboard solves the first two problems (finding and converting customers) using data.** That's the wedge. Once you're in the door, you become their trusted advisor for everything else.

### The services ladder

```
FREE (acquisition)
  Market intelligence report
  "Here's what's happening in your area"
  Source: powuk data (planning apps, procurement, labour demand)
        ↓
£499 (setup)
  AI Business Setup
  Email, phone, calendar, AI assistant
  Source: influence infrastructure
        ↓
£79/month (retainer)
  Monthly check-in
  Workflow adjustments
  1 hour support
        ↓
£149/month (lead generation)
  Weekly lead alerts
  Procurement opportunities
  Planning application signals
  Source: powuk data (contracts_finder, planning_apps)
        ↓
£299/month (consulting)
  Legal questions (via AI + human review)
  Advertising creation
  Google Business Profile optimization
        ↓
£499/month (growth)
  Business strategy
  Hiring support
  Supplier negotiations
  Custom integrations
        ↓
£999/month (full service)
  Everything above
  + dedicated account manager
  + priority support
```

### How the data powers each service

| Service | Data source | What we deliver |
|---------|-------------|-----------------|
| Market intelligence | powuk (planning apps, procurement) | "Here's what's happening in your area" |
| Lead generation | powuk (contracts_finder, ons_labour) | "Here are 5 potential jobs this week" |
| Advertising | powuk (regional data) + cgraphuk (messaging) | "Here's your Google Business Profile copy" |
| Legal questions | cgraphuk (legislation, compliance) | "Here's what the new regulations mean for you" |
| Supplier sourcing | powuk (procurement data) | "Here's where to get the best price on [part]" |
| Training | powuk (apar, ofqual) | "Here are 3 courses to upskill your team" |
| Growth strategy | BigQuery (vertical rankings, pain points) | "Here's how to grow your business" |

### The relationship flywheel

```
We know their business
  → We give them relevant advice
    → They trust us
      → They ask us more questions
        → We learn more about their business
          → We give them better advice
            → They tell other tradespeople
              → More customers
                → More data
                  → Better advice for everyone
```

### Revenue projection

| Year | Customers | Avg monthly | Annual revenue |
|------|-----------|-------------|----------------|
| 1 | 100 | £99 | £119K |
| 2 | 200 | £149 | £358K |
| 3 | 300 | £199 | £716K |

**The setup fee is a loss leader. The monthly retainer is the business.**
