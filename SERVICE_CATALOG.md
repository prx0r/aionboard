# SERVICE_CATALOG.md

> AI Onboard service offerings by sector, powered by Muse + data.

---

## Muse Infrastructure

OpenMuse (github.com/CopilotKit/OpenMuse) provides:
- **Chat interface** — CopilotKit headless chat with AG-UI events
- **Agent computer** — persistent browser, Linux terminal, file workspace
- **Gmail & Calendar** — Google OAuth adapters, mail threads, event creation
- **Activity** — task plans, progress, approvals, receipts
- **Documents** — PDF processing, form filling, attachments
- **Finance** — transaction CSV import, spending summaries
- **Goals & Tracking** — recurring checks, price alerts, change detection

**Meta Business integration adds:**
- WhatsApp Cloud API
- Facebook/Instagram messaging
- Business call handling
- Unified inbox across all channels

---

## Sector Targeting (from BigQuery graph)

### Tier 1 — Launch sectors (score 4.0+)

| Sector | Score | Pains | Muse capability | Service wedge |
|--------|-------|-------|-----------------|---------------|
| **Electrician** | 4.6 | missed_inbound, compliance_drift | Voice agent, WhatsApp | "Answer every call" |
| **Beauty** | 4.5 | no-shows, silent_churn | Booking, reminders | "Stop no-shows" |
| **Barber** | 4.4 | no-shows, payment_flow | Deposit system, SMS | "Collect deposits" |
| **Restaurant** | 4.2 | missed_inbound, waste | Order management, inventory | "Track every order" |
| **Window cleaner** | 4.1 | recurring_ops, payment_flow | Route planning, DD | "Automate rounds" |
| **Cleaning** | 4.0 | silent_churn, scheduling | Win-back engine, booking | "Bring back lapsed clients" |

### Tier 2 — Growth sectors (score 3.0-3.9)

| Sector | Score | Pains | Muse capability | Service wedge |
|--------|-------|-------|-----------------|---------------|
| **Garage** | 3.7 | compliance_drift, missed_inbound | MOT reminders, booking | "Never miss an MOT" |
| **Petcare** | 3.6 | scheduling, no-shows | Direct booking, reminders | "Fill your diary" |
| **Tutor** | 3.5 | scheduling, payment_flow | Exam countdown, packages | "Track progress" |
| **MSP** | 3.4 | compliance_drift, triage | Ticket prioritizer, SLA | "Fix tickets faster" |

### Tier 3 — Expansion sectors (score 2.0-2.9)

| Sector | Score | Pains | Muse capability | Service wedge |
|--------|-------|-------|-----------------|---------------|
| **Builder** | 3.0 | scope_creep, variations | Variation tracker, quotes | "Track every change" |
| **HVAC** | 2.7 | compliance_drift, F-Gas | F-Gas tracker, scheduling | "Stay certified" |
| **Funeral** | 2.3 | missed_inbound, data_gaps | First call capture | "Never miss a call" |

---

## Service Packages

### Package 1: AI Business Setup (£499 one-off)

**What we do:**
1. Configure email, calendar, WhatsApp integration
2. Set up voice agent for missed calls
3. Create quote builder workflow
4. Connect to existing software (Tradify, Xero, etc.)
5. Train owner on AI assistant
6. 14 days of fixes

**Muse capabilities used:**
- Gmail integration (enquiry detection)
- Calendar integration (scheduling)
- WhatsApp Cloud API (customer comms)
- Task management (quote follow-up)

**Delivery time:** 4-6 hours

---

### Package 2: Lead Generation (£149/month)

**What we do:**
1. Weekly lead alerts from powuk data
2. Planning application signals
3. Procurement opportunity alerts
4. Competitor activity monitoring
5. Market intelligence reports

**Data sources:**
- powuk: planning_apps, contracts_finder, ons_labour
- BigQuery: vertical_rankings, pain_points

**Delivery:** Automated weekly email + dashboard

---

### Package 3: AI Consulting (£299/month)

**What we do:**
1. Monthly business review
2. Legal/regulatory questions (AI + human review)
3. Google Business Profile optimization
4. Advertising copy creation
5. Process improvement recommendations

**Muse capabilities used:**
- Browser research (regulations, competitors)
- Document processing (contracts, compliance)
- Email drafting (customer communications)
- Goal tracking (business KPIs)

---

### Package 4: Growth Strategy (£499/month)

**What we do:**
1. Business strategy sessions
2. Hiring support (job postings, screening)
3. Supplier negotiations (bulk pricing)
4. Custom integrations
5. Expansion planning

**Muse capabilities used:**
- All of the above
- Finance tracking (spending, margins)
- Market research (new opportunities)
- Document creation (business plans)

---

### Package 5: Full Service (£999/month)

**What we do:**
1. Everything above
2. Dedicated account manager
3. Priority support (4h response)
4. Quarterly strategy reviews
5. Custom AI development

---

## Sector-Specific Playbooks

### Electrician playbook

**Pain points:**
- 62% of calls missed while on tools
- EICR compliance tracking
- Quote follow-up automation

**Muse setup:**
- Voice agent answers missed calls
- WhatsApp sends quote follow-ups
- Calendar blocks EICR reminders
- Gmail monitors enquiry threads

**First 30 days:**
1. Voice agent live (day 1)
2. Quote builder configured (day 3)
3. WhatsApp template ready (day 5)
4. First lead alert sent (day 7)
5. Monthly review scheduled (day 30)

---

### Beauty playbook

**Pain points:**
- No-shows cost £10K/year per chair
- Client reactivation poor
- Product recommendations missed

**Muse setup:**
- Deposit system for bookings
- SMS reminders at 24h + 2h
- Win-back engine for lapsed clients
- Product recommendation engine

**First 30 days:**
1. Deposit system live (day 1)
2. SMS reminders active (day 2)
3. Client import complete (day 3)
4. First win-back campaign (day 7)
5. Monthly review scheduled (day 30)

---

### Barber playbook

**Pain points:**
- 8% no-show rate
- Walk-in management poor
- Review collection weak

**Muse setup:**
- Booking page with deposits
- Walk-in queue management
- Post-cut review requests
- Referral programme

**First 30 days:**
1. Booking page live (day 1)
2. Deposit system active (day 2)
3. Review requests automated (day 3)
4. First referral campaign (day 7)
5. Monthly review scheduled (day 30)

---

## Pricing strategy

### Founding client offer

- **£299** (instead of £499) for first 3 customers
- In exchange for: feedback, referral, case study permission
- Goal: prove delivery time and value

### Standard pricing

| Package | Monthly | Annual (discount) |
|---------|---------|-------------------|
| Lead Generation | £149 | £1,490 (17% off) |
| AI Consulting | £299 | £2,990 (17% off) |
| Growth Strategy | £499 | £4,990 (17% off) |
| Full Service | £999 | £9,990 (17% off) |

### Add-ons

| Service | Price | What it is |
|---------|-------|------------|
| Extra voice agent | £29/mo | Additional phone number |
| SMS package | £19/mo | 500 SMS/month |
| WhatsApp API | £39/mo | Business WhatsApp |
| Custom integration | £750 one-off | Bespoke workflow |
| Emergency support | £99/call | Out-of-hours support |

---

## Success metrics

### Per customer

| Metric | Target | How we measure |
|--------|--------|----------------|
| Quote win rate | >40% | influence job pipeline |
| Answer rate | >90% | Voice agent logs |
| Review velocity | >2/month | Google Business Profile |
| Monthly revenue growth | >10% | Invoice tracking |
| Support tickets | <3/month | Help desk |

### Per sector

| Metric | Target | How we measure |
|--------|--------|----------------|
| Customer acquisition cost | <£200 | Marketing spend / customers |
| Monthly churn | <5% | Cancellations / total |
| Net promoter score | >50 | Quarterly survey |
| Referral rate | >20% | New customers from referrals |
