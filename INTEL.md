# INTEL.md

> Research gold extracted from archived docs. Sources attributed, hypotheses marked. This is reference material — not a product spec.

---

## 1. Market evidence

### UK Business Data Survey (DSIT, Oct 2025–Jan 2026)

| Stat | Value | Denominator |
|------|-------|-------------|
| Sole traders using AI | 40% | Among businesses handling digitised data |
| Sole-trader AI users with integration | 18% | Among sole traders already using AI |
| Construction AI users with integration | 14% | Among construction businesses already using AI |
| Construction businesses with a website | 65% | Among all surveyed construction businesses |
| Uncomfortable with AI training on their data | 73% | Among businesses handling digitised data |

**Implication:** AI awareness is not the problem. The 18% integration figure means implementation is the separate opportunity. Privacy, permissions, and control should be selling points.

### Federation of Master Builders (Jul–Dec 2025, 493 SMEs)

- 72% affected by skilled-labour shortages
- 49% reported project delays

### Checkatrade 2025 survey (850 tradespeople)

- 79% identified rising materials and tools costs as a barrier to growth

### UK business population (GOV.UK 2025)

- ~885,000 construction SMEs
- ~3.2 million sole proprietorships (Companies House-only misses most)

---

## 2. Competitor pricing intelligence

### Trades software

| Competitor | UK offering | Price |
|-----------|------------|-------|
| Checkatrade / TradeMore | AI-assisted job management, unified inbox | Approved membership from £30/month |
| Tradify | Job management, quoting, invoicing | £34/user/month; Plus plan £44/user/month (includes AI tools) |
| Powered Now | Job management, invoicing | From £28/month; AI receptionist from £29/month additional |
| ServiceM8 | Complete system, unlimited users | Free single-user; £25/month Starter with AI smart helpers |

### Beauty/salon software

| Competitor | UK offering | Price |
|-----------|------------|-------|
| Square Appointments | Booking site, automated reminders, payments | UK free plan |
| Booksy | Booking, marketing, client management, payments | £40/month plus VAT |
| Fresha | Booking, deposits, client records, reminders, marketplace | Free (monetises on payments) |
| Manychat | Social automation, WhatsApp, AI | Free limited (2 channels, 4 automations); $14/month expanded; $29/month Pro |

### Cleaning/round management

| Competitor | UK offering | Price |
|-----------|------------|-------|
| ZenMaid | Scheduling, automated comms, invoicing, payments | $19/month entry |
| CleanerPlanner | Round management, invoicing | £19/month single user; £29/month with GoCardless integration |

### Key insight

The service we build is a cross-platform onboarding, security, and AI-training layer — NOT a competitor to these providers. Configure the customer's existing tools; don't force migration.

---

## 3. Data assets

### powuk datasets

| Dataset | Records | What it measures |
|---------|---------|------------------|
| Electrical businesses (SIC 43210) | 10,000+ | Companies House filtered |
| ons_labour | 175,181 | Online job adverts by SOC code × region |
| ons_salaries | 50,973 | Asking salaries from job adverts |
| ons_skills | 4,282 | Skills mentioned in job adverts |
| ashe_wages | 3,906 | Official wage data by region × occupation |
| contracts_finder | 5,000 | Public procurement contracts (OCDS) |
| find_tender | 50 | Higher-value procurement |
| planning_apps | 5,000 | Planning applications |
| apar | 1,424 | Apprenticeship providers |
| ofqual | 10,000+ | Regulated qualifications |
| refcom | 11,295 | F-gas certified companies |
| evspark_trades | 55,925 | Electrical businesses by postcode |

### cgraphuk assets

| Asset | Count |
|-------|-------|
| Vertical templates | 24 |
| Prioritised pain points | 72 (3 per vertical) |
| Indexed tools | 174 |
| Campaign briefs | 24 |
| Voice profiles | 11 verticals |

### BigQuery dataset (project-ff2366d2-8fda-4fcb-9ba, dataset: drop)

| Table | Records | What it has |
|-------|---------|-------------|
| vertical_rankings | 24 | Ranked verticals with scores |
| pain_points | 73+ | Pain points by industry |
| graph_nodes | 374 | Business entities, tools, patterns |
| graph_observations | 150+ | Readiness, leaks, installed base |
| opportunities | 8 | Business models with ticket ranges |

### Data quality

| Status | What |
|--------|------|
| Good | Electrical businesses (10K+ verified), labour data (175K+), procurement (5K+) |
| Needs work | Phone numbers, websites, team size, existing software |
| Blocked | nomis_supply (API key), dfe_apprenticeships (URL fix), mcs_installers (data request), ozev_installers (scraping) |

---

## 4. Regional business density (top 20 postcode areas)

```
BT  215  Belfast              NG  209  Nottingham
CM  197  Chelmsford           RM  163  Romford
DA  160  Dartford             BS  159  Bristol
CF  156  Cardiff              LE  152  Leicester
BN  151  Brighton             ME  149  Medway
PO  148  Portsmouth           NE  145  Newcastle
SS  142  Southend             PE  142  Peterborough
TN  134  Tunbridge Wells      HA  128  Harrow
DN  124  Doncaster            RG  120  Reading
GU  116  Guildford            DE  114  Derby
```

---

## 5. Service definitions with setup times

| # | Service | Setup time | Price (hypothesis) | Industries |
|---|---------|-----------|-------------------|------------|
| 1 | Missed Call Recovery | 15 min | £99 | Electrician, Builder, HVAC, Garage, Funeral, Restaurant |
| 2 | No-Show Elimination | 30 min | £149 | Barber, Beauty, Restaurant, Hotel, Medspa |
| 3 | Review Engine | 20 min | £79 | All (universal) |
| 4 | Quote Follow-Up | 30 min | £129 | Electrician, Builder, HVAC, Garage, Medspa |
| 5 | Google Business Profile | 1 hr | £199 | All (universal) |
| 6 | AI Discovery Setup | 45 min | £179 | All (universal) |
| 7 | WhatsApp Business Setup | 30 min | £99 | All (universal) |
| 8 | Compliance Tracker | 1 hr | £199 | Electrician (EICR, Part P), HVAC (F-Gas), Builder (CHAS, CSCS), Tree Surgeon (NPTC), Care (CQC) |
| 9 | Win-Back Engine | 1 hr | £149 | Barber, Beauty, Cleaning, Petcare, Tutor, Retail, Vet |
| 10 | Direct Booking Migration | 2 hr | £299 | Restaurant, Hotel, Petcare, Tutor, Barber, Beauty |

**Pricing note:** All prices are superseded research hypotheses. Canonical pricing is in OFFER.md.

### Pain statistics (from research)

- 8% of bookings no-show; 6-chair barber loses £10,000/year
- 30% close rate if quotes chased vs 5% if not
- 30% aggregator commission (Deliveroo, Just Eat, Booking.com, Rover); businesses paying £30k+/year
- 34% net margin (direct) vs 12% (aggregator)
- 91% of SMBs score below 60/100 in AI visibility
- 19 industries have silent churn
- 3-5x more reviews within 60 days (target)

---

## 6. Compliance certifications by industry

| Industry | Key certs |
|----------|----------|
| Electrician | EICR, Part P |
| HVAC | F-Gas |
| Builder | CHAS, CSCS |
| Tree Surgeon | NPTC |
| Care | CQC |

---

## 7. Legal and compliance details

### Controller vs processor

- AI Onboard likely controller for own customer relationships
- Processor when handling client's end-customer information
- Article 28 written agreement required for processor role
- Do not quietly reuse client's appointment history or customer messages for POW intelligence

### PECR marketing rules for sole traders

- Sole traders and certain partnerships are individual subscribers
- Unsolicited promotional emails, WhatsApp messages, social-media DMs generally require consent
- Corporate-subscriber marketing has different PECR rules
- Separate choices for: essential service messages, 7-day support, product updates, paid opportunity alerts
- No pre-ticked marketing boxes

### MTD thresholds

| Threshold | Date | Qualifying income |
|-----------|------|------------------|
| >£50k | Apr 2026 | Gross self-employment + property income before expenses |
| >£30k | Apr 2027 | Same |
| >£20k | Apr 2028 | Same |

- Muse is not a substitute for compatible MTD software
- VAT registration: £90k taxable turnover (rolling 12 months)

### FCA

- Account-information and payment-initiation services are regulated
- Do not directly aggregate bank accounts or initiate payments as an unregulated service

### Incident response

- Processor must inform controller without undue delay
- Controller must assess whether breach is reportable to ICO within 72 hours
- Document every breach, including those not requiring external notification

---

## 8. Multi-language opportunity

Many UK trades businesses are run by people whose first language isn't English. A Polish electrician in Birmingham can now serve English-speaking customers through AI, and vice versa.

**Untapped market.** Multi-language voice agent (Polish, Urdu, Arabic), multi-language website for £149 extra.

---

## 9. Manchester prospect examples

| Business | Services | Website |
|----------|----------|---------|
| GES Electrons | Domestic, EV, commercial | geselectrons.co.uk |
| U & O Electrical | Commercial/industrial, EV, solar | uaofuture.co.uk |
| Manchester Electric | Domestic, commercial, industrial, fire/security | manchesterelectric.co.uk |
| Mili Electrician | Domestic, commercial, EV, inspections | mili-electrician-manchester.co.uk |

**Note:** Research examples, not confirmed sales leads. Team size, existing software, and appetite for AI onboarding not established.

---

## 10. Referral channels

- Electricians' accountants
- Local electrical wholesalers
- Businesses already providing trade websites

These encounter people setting up or growing firms and may introduce a complementary implementation service.

---

## 11. Measurement framework

### Before/after metrics (capture at join and 30 days)

- Calls answered %
- Missed-call leads captured
- No-show %
- Quote response time
- Quote close %
- Reviews count/rating
- Google Maps rank
- AI assistant citations
- Direct booking share
- Overdue invoice days

### Pilot success targets (hypotheses, not measured)

| Metric | Before | Target |
|--------|--------|--------|
| Calls answered | 40% | 90%+ |
| No-shows | 8% | <2% |
| Reviews | 0 | 5+ new |
| Quotes converted | 5% | 30%+ |
| Google ranking | Unranked | Top 3 |

### Verified onboarding format

```json
{
  "business_id": "aionboard-elec-manchester-001",
  "vertical": "electrician",
  "package": "standard-ai-setup",
  "installed_at": "2026-09-23",
  "baseline": {"answer_rate": 0.41, "no_show": 0.08, "reviews": 6},
  "day_30": {"answer_rate": 0.93, "no_show": 0.01, "reviews": 14},
  "verified": true,
  "review_allowed": true
}
```

---

## 12. Standing orders

- Don't promise subscriptions as the product
- Don't invent uplift numbers
- Don't mix customer PII into POW without explicit opt-in
- Don't scale paid ads before referral proof exists
- No proof, no claim — publish per-sector proof pages
- Price against the human alternative, not your costs

---

## 13. Meta WhatsApp Business Tools MCP

Meta is introducing a WhatsApp Business Tools MCP for supported AI coding agents to assist with setting up business accounts, numbers, message templates, and test messaging. Rolling out gradually, aimed at development and testing. Could remove considerable work from advanced WhatsApp installations.

---

## 14. Checkatrade API limitation

Lead-delivery and booking webhooks documented for strategic accounts only. Ordinary tradespeople may only have app and notification emails. Do not promise a fully automated Checkatrade integration.

---

*Extracted from archived research docs. All content is research, not proof.*
