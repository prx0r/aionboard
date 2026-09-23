# DASHBOARD_SPEC.md

> Integrated customer dashboard. aocsec backend + powpowpow frontend patterns.

## Architecture

```
aocsec (backend)              powpowpow (frontend pattern)     AI Onboard (us)
├── onboarding/pipeline.py    ├── single-file HTML/CSS/JS      ├── company login
├── onboarding/runbooks.py    ├── stdlib HTTP server            ├── integrated dashboard
├── support/tickets.py        ├── token-gated access            ├── read-only company graph
├── support/kb.py             ├── rail + sidebar + tabs         ├── pi agent under the hood
├── company/lookup.py         ├── canvas charts                 ├── Meta Business Agent setup
├── business_agent/           ├── bottom ops panel              ├── Google Maps optimisation
├── presence/checklist.py     ├── resizable chat panel          ├── AI visibility package
├── audit_chain/              └── dense data tables             └── lead generation
└── gateway/server.py
```

## What we build

### 1. Company login system

**Flow:**
```
Customer signs up → gets company token → logs in → sees their dashboard
```

**Implementation:**
- Token-based auth (like powpowpow's `?token=` pattern)
- Each company gets a unique token
- Token maps to company profile in aocsec's business graph
- Read-only access to their own data

**Database:**
```sql
CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    token TEXT UNIQUE NOT NULL,
    company_number TEXT,
    business_name TEXT,
    vertical TEXT,
    city TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    onboarding_stage TEXT DEFAULT 'new',
    subscription_status TEXT DEFAULT 'trial',
    subscription_expires TIMESTAMP
);
```

### 2. Integrated dashboard

**Layout (powpowpow pattern):**

```
┌─────────────────────────────────────────────────────────────┐
│ AI ONBOARD                              [company name]  🟢 │ ← title bar
├────┬──────────────────────────────────────────────────────┤
│    │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ 🏠 │ │ Leads    │ │ Website  │ │ Google   │ │ AI       │ │ ← rail navigation
│ 📊 │ │ 12 this  │ │ Live at  │ │ 85%      │ │ Visible  │ │
│ 🌐 │ │ week     │ │ site.url │ │ complete │ │ in ChatGPT│ │
│ 🤖 │ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│ 📈 │                                                      │
│    │ ┌──────────────────────────────────────────────────┐ │
│    │ │ Recent Leads                                      │ │ ← main content
│    │ │ ┌────────────────────────────────────────────────┐ │ │   (tabbed)
│    │ │ │ "Looking for nail tech Manchester" Instagram   │ │ │
│    │ │ │ "Gel nails near Deansgate" Reddit 2d ago       │ │ │
│    │ │ │ "Prom nails Saturday" TikTok today             │ │ │
│    │ │ └────────────────────────────────────────────────┘ │ │
│    │ │                                                    │ │
│    │ │ Website Chat Analytics                             │ │
│    │ │ ┌────────────────────────────────────────────────┐ │ │
│    │ │ │ Questions asked: 47  │  Bookings made: 12      │ │ │
│    │ │ │ Avg response: 2.3s  │  Conversion: 25%        │ │ │
│    │ │ └────────────────────────────────────────────────┘ │ │
│    │ └──────────────────────────────────────────────────┘ │
├────┴──────────────────────────────────────────────────────┤
│ OPS: GBP verified ✓ │ Website live ✓ │ AI visible ✓ │ Leads flowing ✓│
└─────────────────────────────────────────────────────────────┘
```

**Tech:**
- Single-file `dashboard.html` (vanilla JS/CSS, no framework)
- Python stdlib HTTP server (like powpowpow)
- Token-gated access
- Cloudflare tunnel for public access

### 3. Read-only company graph

**What the customer sees:**

| Section | Data | Source |
|---------|------|--------|
| **Overview** | Business name, vertical, city, rating, reviews | SerpAPI |
| **Company** | Company number, status, directors, SIC codes | Companies House |
| **Website** | Chat analytics, questions asked, bookings made | Our chatbot logs |
| **Google Maps** | Profile completeness, review count, response rate | GBP API |
| **AI Visibility** | Schema markup status, llms.txt, Bing submission | Our checks |
| **Leads** | Local demand signals, planning apps, social mentions | Our lead gen |
| **Support** | Open tickets, SLA status, resolution history | aocsec support module |

**Read-only means:**
- Customer can VIEW everything
- Customer can APPROVE actions (approve lead response, approve review reply)
- Customer CANNOT modify data directly
- All changes go through our approval flow

### 4. Pi agent under the hood

**What Pi does:**
- Monitors website chat questions
- Drafts responses to enquiries
- Monitors Google Maps reviews
- Drafts review responses
- Monitors lead signals
- Alerts customer when action needed

**How it works:**
```
Customer's website gets a chat question
  ↓
Pi receives the question + knowledge bundle
  ↓
Pi drafts a response
  ↓
Customer approves (or Pi auto-responds if pre-approved)
  ↓
Response sent to customer's website
```

**Pi is NOT:**
- A chatbot the customer talks to directly
- An autonomous agent that acts without approval
- A replacement for the customer's judgment

**Pi IS:**
- A background assistant that drafts responses
- A monitor that alerts when action needed
- A builder that creates their digital presence

### 5. Meta Business Agent setup

**What we do:**
- Turn on Business Agent in their WhatsApp Business app
- Configure on their services, prices, hours
- Set up product catalogue
- Configure escalation rules
- Test with fake enquiries
- Train owner on dashboard

**What the customer sees:**
- "Your WhatsApp AI is live and answering enquiries"
- Dashboard shows: enquiries handled, bookings made, response time

### 6. Google Maps optimisation

**What we do:**
- Complete all GBP fields
- Add service menu with prices
- Add 10+ photos
- Set up Q&A with AI answers
- Configure booking link
- Add posts weekly
- Respond to every review

**What the customer sees:**
- "Your Google profile is 85% complete (was 45%)"
- Dashboard shows: profile views, direction requests, call clicks

### 7. AI visibility package

**What we do:**
- Add schema markup (LocalBusiness, Service, FAQPage)
- Add llms.txt (AI-readable business summary)
- Add robots.txt (allow AI crawlers)
- Ensure NAP consistency
- Submit to Bing Webmaster Tools

**What the customer sees:**
- "Your business now appears when people ask ChatGPT"
- Dashboard shows: AI visibility score, platforms indexed

### 8. Lead generation

**What we do:**
- Monitor planning applications (for trades)
- Monitor OZEV grants (for electricians)
- Monitor Instagram/TikTok demand
- Monitor letting agents (for cleaners)
- Score and rank leads
- Send weekly lead digest

**What the customer sees:**
- "Here are 5 people who need your services this week"
- Dashboard shows: leads received, response rate, conversion

---

## Files to build

### Backend (from aocsec)

| File | Source | What to change |
|------|--------|---------------|
| `onboarding/pipeline.py` | aocsec | Keep as-is, add company table |
| `onboarding/runbooks.py` | aocsec | Keep as-is, verticals already match |
| `support/tickets.py` | aocsec | Keep as-is |
| `support/kb.py` | aocsec | Keep as-is |
| `support/agent.py` | aocsec | Keep as-is |
| `company/lookup.py` | aocsec | Keep as-is |
| `business_agent/onboarding.py` | aocsec | Keep as-is |
| `presence/checklist.py` | aocsec | Keep as-is |
| `audit_chain/chain.py` | aocsec | Keep as-is |

### Frontend (from powpowpow pattern)

| File | What it does |
|------|-------------|
| `site/index.html` | Single-file dashboard (vanilla JS/CSS) |
| `site/server.py` | Stdlib HTTP server, token-gated |
| `site/api.py` | API endpoints for dashboard data |

### New modules (for AI Onboard)

| File | What it does |
|------|-------------|
| `dashboard/auth.py` | Company login, token management |
| `dashboard/graph.py` | Read-only company graph (combines aocsec modules) |
| `dashboard/leads.py` | Lead generation and scoring |
| `dashboard/chat.py` | Website chatbot analytics |
| `dashboard/gbp.py` | Google Business Profile optimisation |
| `dashboard/ai_visibility.py` | Schema, llms.txt, robots.txt management |

---

## API endpoints

```
GET  /api/health                    → health check
GET  /api/company?token=xxx         → company profile
GET  /api/leads?token=xxx           → leads for this company
GET  /api/chat/analytics?token=xxx  → website chat analytics
GET  /api/gbp/status?token=xxx      → Google profile status
GET  /api/ai_visibility?token=xxx   → AI visibility status
GET  /api/tickets?token=xxx         → support tickets
GET  /api/tickets/history?token=xxx → ticket history
POST /api/tickets/approve?token=xxx → approve ticket response
GET  /api/onboarding/status?token=xxx → onboarding progress
GET  /api/ops                       → service health (ops panel)
POST /api/chat                      → AI analyst chat
```

---

## Deployment

```
localhost:8795 (dashboard)
    ↓
Cloudflare Tunnel
    ↓
dashboard.aionboard.co.uk (public)
```

**Systemd services:**
- `aionboard-dashboard.service` — main dashboard server
- `aionboard-leads.service` — lead generation monitor
- `aionboard-chat.service` — website chatbot analytics

---

## What we build first (priority)

### Week 1: Company login + basic dashboard
- [ ] Company token system
- [ ] Basic dashboard HTML (powpowpow pattern)
- [ ] API endpoints for company data
- [ ] Token-gated access

### Week 2: Integrate aocsec modules
- [ ] Wire onboarding pipeline
- [ ] Wire support tickets
- [ ] Wire company verification
- [ ] Wire presence checklist

### Week 3: Add value features
- [ ] Lead generation monitor
- [ ] Chat analytics
- [ ] GBP status checker
- [ ] AI visibility checker

### Week 4: Pi integration + polish
- [ ] Pi agent monitoring
- [ ] Review response drafting
- [ ] Lead response drafting
- [ ] Dashboard polish

---

## Revenue model

| Feature | Price | What they get |
|---------|-------|--------------|
| Company dashboard | Included | Login, view their data |
| Lead generation | £10/week | 5-10 scored leads per week |
| Chat analytics | Included | Questions, bookings, conversion |
| GBP optimisation | £10 one-off | Profile completion + monitoring |
| AI visibility | £10 one-off | Schema, llms.txt, Bing |
| Pi monitoring | £50/month | Background assistant + alerts |
| **Total** | **£20 + £10/week + £50/month** | Full digital presence |

---

## The one-liner

> "Your business, on one dashboard. See your leads, your website, your Google profile, your AI visibility — all in one place. We build it, you approve it."
