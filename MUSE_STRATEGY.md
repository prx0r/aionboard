# MUSE_STRATEGY.md

> Meta's two AI products, what's live today, and how we ride both waves.

## The two products

### Meta Business Agent (for businesses) — LIVE in UK NOW

| Detail | Value |
|--------|-------|
| Launched | June 3, 2026 (Conversations event, London) |
| Availability | Global — UK included |
| Where | WhatsApp Business app, Messenger, Instagram DMs |
| Cost | Free for now (paid tiers coming) |
| What it does | Answers customer queries, recommends products, books appointments, qualifies leads |
| Integrations | Shopify, Zendesk, Shopee (via Business Agent Platform, June 12) |
| Setup | WhatsApp Business app → Tools → Your Business AI → guided setup |
| Status | **Live. Selling onboarding today.** |

### Muse (personal agent for consumers) — US-only, no UK date

| Detail | Value |
|--------|-------|
| Launched | September 8, 2026 (US only) |
| Availability | US only — iOS, Android, muse.ai |
| UK status | No date. No waitlist. No country list beyond US. |
| Cost | Free tier + $20/mo (Power) + $100/mo (Maximum) |
| What it does | Personal AI agent: email, calendar, shopping, payments, cross-app tasks |
| Connectors | Gmail, Google Calendar, Stripe, Notion, Canva, + custom connectors |
| Connector Platform | Opened September 18 — submit at muse.ai/platform |
| UK launch | **Unknown. Could be months. Could be never soon.** |
| Status | **Monitor. Prepare connector. Don't wait.** |

---

## Our strategy: three phases

### Phase 1: NOW — Meta Business Agent (live in UK)

**Sell onboarding for Meta Business Agent TODAY.**

What businesses get:
- AI answers WhatsApp queries 24/7
- AI recommends products from catalogue
- AI books appointments
- AI qualifies leads
- Human escalation when needed

What we charge:
- Basic onboarding: £20 (set up Business Agent, train on services)
- Starter bundle: £40 (Business Agent + booking link + GBP)
- Integrated: £50/mo (monitoring + support + consulting)

What we do:
1. Set up WhatsApp Business app (if not already)
2. Turn on Business Agent
3. Configure on services, prices, hours
4. Set up product catalogue (if applicable)
5. Configure escalation rules
6. Test with fake enquiries
7. Train owner on dashboard

### Phase 2: WHEN MUSE LAUNCHES IN UK — Upgrade to full agent

**When Muse becomes available in UK:**

What businesses get (everything from Phase 1, plus):
- Cross-app agent (email + calendar + WhatsApp + Instagram)
- Proactive task completion
- Personal AI assistant for the business owner
- Connector ecosystem (third-party integrations)

What we charge:
- £50 one-off to upgrade Business Agent → Muse
- £75/mo for Muse-level Integrated package

What we do:
1. Connect Muse to business email, calendar, booking tool
2. Configure cross-app workflows
3. Set up proactive reminders and tasks
4. Train on owner's communication style
5. Configure approval gates for sensitive actions

### Phase 3: CONNECTOR — Submit vertical-specific connectors

**When Muse Connector Platform opens in UK:**

What we build:
- "AI Onboard for Nail Techs" connector
- "AI Onboard for Electricians" connector
- "AI Onboard for Dog Groomers" connector
- etc. (one per vertical)

What each connector does:
- Connects to vertical-specific booking tools (Booksy, Fresha, Tradify)
- Handles enquiries with vertical-specific knowledge
- Books appointments with breed/service-aware timing
- Manages deposits and payments
- Tracks compliance (EICR, COSHH, etc.)

What we charge:
- Connector listing: free (Meta doesn't charge yet)
- Ongoing management: included in Integrated package

---

## Business Agent setup per vertical

### What's the same for all verticals

1. WhatsApp Business app installed and verified
2. Business profile complete (name, hours, description, category)
3. Product/service catalogue loaded
4. Business Agent turned on
5. Trained on: services, prices, hours, location, policies
6. Escalation rules set (human handoff for complex queries)
7. Tested with 5 fake enquiries
8. Owner trained on dashboard

### What's different per vertical

| Vertical | Catalogue items | Special config | Escalation trigger |
|----------|----------------|---------------|-------------------|
| Nails | Gel, acrylic, pedicure, art | Deposit required for bookings >£30 | "I want nail art" (custom pricing) |
| Beauty | Facial, wax, tint, brow lamination | Patch test required for tint/lift | "I have allergies" |
| Hair | Cut, colour, balayage, braids | Travel area check | "I'm outside your area" |
| Lashes | Extensions, lift, tint, infill | Allergy declaration required | "I have eye conditions" |
| Electrician | EICR, EV charger, fault, rewire | Emergency triage | "It's urgent" / "I smell gas" |
| Car detailers | Basic, premium, ceramic coating | Photo intake required | "I need a quote" (needs photos) |
| Driving instructors | Lessons, intensive, test prep | Block booking | "I need my test booked" |
| Cleaners | Weekly, fortnightly, deep clean | Key access required | "I need access instructions" |
| Dog groomers | Bath, full groom, de-shed, puppy | Breed-specific timing | "What breed?" (needs duration) |
| Gardeners | Lawn, hedge, tidy, clearance | Seasonal availability | "I need it this week" (capacity) |
| Weddings | Photography, video, planning | Date availability check | "I want a bespoke package" |

---

## GDPR compliance for Business Agent

### What the ICO requires

1. **Privacy notice update** — mention automated handling in customer chats
2. **Lawful basis** — legitimate interest (Article 6(1)(f)) for customer service automation
3. **Human escalation** — customers must be able to reach a human
4. **Transparency** — customers should know they're talking to AI (Meta handles this)
5. **Data minimisation** — only process what's needed for the query
6. **Retention** — Meta's retention policy applies; check WhatsApp Business data settings

### What we do for each customer

1. Update their privacy notice to mention AI handling
2. Configure human escalation path
3. Test that AI doesn't collect unnecessary data
4. Document the setup for ICO compliance
5. Advise on 72-hour breach notification (if applicable)

---

## Compatibility check

### Does Business Agent work with our existing stack?

| Our feature | Business Agent compatible? | Notes |
|------------|--------------------------|-------|
| WhatsApp AI receptionist | ✅ YES | Business Agent IS the AI receptionist |
| Booking link in bios | ✅ YES | Separate — Business Agent doesn't replace this |
| Deposit system | ⚠️ PARTIAL | Business Agent can recommend but can't collect deposits directly |
| Automated reminders | ⚠️ PARTIAL | Business Agent can send within conversation; separate reminder tools needed |
| Review requests | ⚠️ PARTIAL | Business Agent can ask; dedicated review flow better |
| Quote follow-up | ⚠️ PARTIAL | Business Agent handles initial enquiry; follow-up needs separate tool |
| Invoice/payment chasing | ❌ NO | Business Agent doesn't do financial transactions |
| GPS tracking | ❌ NO | Business Agent is chat-only |
| Photo geo-tagging | ❌ NO | Business Agent is chat-only |
| Compliance tracking | ❌ NO | Business Agent doesn't track certificates |

### What Business Agent covers vs what we still need

| Business Agent handles | We still need |
|----------------------|---------------|
| Answering customer queries | Booking link (separate) |
| Recommending services | Deposit collection (Stripe link) |
| Qualifying leads | Automated reminders (separate) |
| Booking appointments (basic) | Fill cycle reminders (our automation) |
| Human escalation | Invoice/payment (separate) |
| Product recommendations | GPS tracking (separate) |
| | Photo workflow (separate) |
| | Compliance tracking (separate) |

**Key insight:** Business Agent is the FRONT DOOR — it handles the conversation. Everything behind the conversation (bookings, payments, reminders, compliance) is still our stack.

---

## The pitch

### For businesses today

> "Meta just released an AI agent for WhatsApp. It answers your customer queries 24/7. We set it up for £20. Takes 15 minutes."

### When Muse launches in UK

> "Meta's personal AI agent is now in the UK. We upgrade your WhatsApp AI to handle email, calendar, and cross-app tasks. £50 one-off to upgrade."

### When we have connectors

> "We built a custom AI agent specifically for [nail techs/electricians/groomers]. It knows your services, your prices, your breed timings. It's not generic — it's built for your industry."

---

## Timeline

| Date | Event | Our action |
|------|-------|-----------|
| Now | Business Agent live in UK | Start selling onboarding |
| Q4 2026 | Monitor Muse UK timeline | Prepare connector, build case studies |
| Q1 2027? | Muse UK launch (if it happens) | Upgrade existing customers |
| Q2 2027? | Muse Connector Platform in UK | Submit vertical connectors |
| Ongoing | Business Agent improvements | Stay current, update setup guides |

---

## Risk: what if Muse never launches in UK?

**We don't need Muse.** Business Agent is live, free, and does the core job (answer queries, book appointments). Muse is a bonus — cross-app tasks, proactive assistance, personal agent. Our business works with Business Agent alone.

**Worst case:** Business Agent is our only platform. We still sell onboarding (£20), bundles (£40), and integrated support (£50/mo). The connector play becomes a bonus, not a dependency.

**Best case:** Muse launches in UK, we upgrade customers, submit connectors, become the vertical-specific Muse onboarding partner.

**Either way, we sell today.**
