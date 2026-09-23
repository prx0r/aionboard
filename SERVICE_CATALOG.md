# SERVICE_CATALOG.md

> AI Onboard service offerings by sector, powered by Muse + data.

---

## Capability distinction

Current pilot scope is defined in `OFFER.md`.

- **Meta Muse:** Meta’s assistant ecosystem. Access and UK availability depend on Meta; it is not included in the pilot setup.
- **OpenMuse:** A separate open-source personal-agent project. Installing or studying it does not provide Meta Muse access.
- **WhatsApp Cloud API and Meta business management:** Require access, business verification, review, payment terms, and explicit customer authorization. They are separate from the pilot.
- **OpenMuse capabilities below are reference architecture only**, not delivered pilot features unless the customer separately authorizes access and pays the relevant supplier charges.

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

## Current pilot package

The standard AI Setup is £499 one-off and is defined in `OFFER.md`:

1. Setup for existing email and calendar workflows the customer authorizes.
2. Enquiry-capture preparation using customer-approved contacts.
3. Quotation drafting from the customer-approved price book, with owner approval.
4. Google Business Profile assistance through Google’s ordinary interface.
5. Live training.
6. Written handover.
7. Fourteen days of fixes for configured workflows.

Website development, live voice service, Meta production integration, custom integrations, and lead generation are separate future offerings.

## Future service roadmap

---

### Future offering: Lead Generation (£149/month, not in pilot)

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

### Future offering: AI Consulting (£299/month, not in pilot)

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

### Future offering: Growth Strategy (£499/month, not in pilot)

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

### Future offering: Full Service (£999/month, not in pilot)

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

**Illustrative future configuration:**
- Voice agent answers missed calls
- WhatsApp sends quote follow-ups
- Calendar blocks EICR reminders
- Gmail monitors enquiry threads

**Illustrative sequence:**
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

**Illustrative future configuration:**
- Deposit system for bookings
- SMS reminders at 24h + 2h
- Win-back engine for lapsed clients
- Product recommendation engine

**Illustrative sequence:**
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

**Illustrative future configuration:**
- Booking page with deposits
- Walk-in queue management
- Post-cut review requests
- Referral programme

**Illustrative sequence:**
1. Booking page live (day 1)
2. Deposit system active (day 2)
3. Review requests automated (day 3)
4. First referral campaign (day 7)
5. Monthly review scheduled (day 30)

---

## Pricing strategy

The current pilot offer is the £499 standard setup in `OFFER.md`. Monthly packages and add-ons below are future roadmap items, not current products.

### Future monthly packages

| Package | Monthly |
|---------|---------|
| Lead Generation | £149 |
| AI Consulting | £299 |
| Growth Strategy | £499 |
| Full Service | £999 |

### Future add-ons

| Service | Price | Status |
|---------|-------|--------|
| Extra voice agent | Separate quote | Separate supplier costs apply |
| SMS package | Separate quote | Separate supplier costs apply |
| WhatsApp API | Separate quote | Blocked/approval required |
| Custom integration | Separate quote | Separate deliverable |
| Emergency support | Separate quote | Separate deliverable |

---

## Success metrics

These are targets to validate with a real customer, not current results.

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
