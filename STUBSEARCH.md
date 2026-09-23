# STUBSEARCH.md

> What's actually working vs what's a stub. Honest audit.

## Summary

| Status | Count | What it means |
|--------|-------|---------------|
| ✅ REAL | 38 | Actually works, can use today |
| ❌ STUB | 3 | Returns fake data, needs credentials |
| ❌ NOT BUILT | 11 | Doesn't exist yet |
| **Total** | **52** | |

**We are NOT ready for outreach.** We have stubs where it matters.

---

## What's REAL (can use today)

### Prospect data ✅

| Source | Data | Records |
|--------|------|---------|
| SerpAPI Google Maps | Business name, phone, rating, reviews, website, address | 1,059 |
| Companies House | Company status, directors, SIC codes, incorporation date | 120 |
| powuk planning apps | Planning applications with descriptions | 2,550 |
| powuk contracts | Procurement contracts with buyer emails | 15,000 |
| powuk electrical businesses | Company numbers, postcodes, SIC codes | 1,420 |

### Pipeline database ✅

| Component | What it does |
|-----------|-------------|
| SQLite schema | prospects, outreach, conversations, onboardings, followups |
| Data ingestion | imports from CSV, scores prospects 0-100 |
| Stage tracking | new → contacted → responded → interested → onboarded → paying |

### Message templates ✅

| Component | What it does |
|-----------|-------------|
| Initial templates | Per vertical, personalised with business name, rating, reviews |
| Follow-up templates | Day 2, 5, 12 sequences |
| Pain messages | "You're losing £X/year" per vertical |

### Demo websites ✅

| Component | What it does |
|-----------|-------------|
| HTML generation | 1,059 pages with chat interface |
| Chat interface | Vanilla JS, works in browser |
| Knowledge base | Services, prices from Google data |
| Sample questions | Clickable, trigger responses |

### Lead generation ✅

| Component | What it does |
|-----------|-------------|
| Planning app scanner | Reads powuk JSONL, filters for trade keywords |
| Instagram keyword generator | Generates search queries per vertical |
| Pain calculator | Calculates annual/monthly/weekly loss per vertical |
| Visibility scorer | 0-100 based on data completeness |

### ChatGPT visibility ✅

| Component | What it does |
|-----------|-------------|
| Schema markup generator | schema.org per vertical (LocalBusiness, BeautySalon, etc.) |
| llms.txt generator | AI-readable business summary |
| robots.txt generator | Allows all AI crawlers |
| Visibility scorer | 0-100 based on data |

### aocsec backend ✅

| Component | What it does |
|-----------|-------------|
| Onboarding pipeline | 8-stage state machine with gates |
| Runbooks | Per vertical install steps |
| Support tickets | SLA, handoff, knowledge base |
| Company verification | Companies House API lookup |
| Business Agent eligibility | 5-point checklist |
| Audit chain | Hash-chained append-only log |
| Gateway | MCP bridge with bearer auth |

### influence backend ✅

| Component | What it does |
|-----------|-------------|
| Booking pipeline | intake → quote → schedule → confirm → invoice |
| Availability engine | Slot finding with Google Calendar |
| Knowledge YAML | Per business config |
| MCP server | 19 tools |

### JEV triage ✅

| Component | What it does |
|-----------|-------------|
| Enquiry classification | respond_now / respond_later / escalate / ignore |
| Demo verification | Checks accuracy before sending |
| Outreach gate | Quality check before sending |
| Ticket triage | Priority assignment |

---

## What's a STUB (returns fake data)

### WhatsApp messaging ❌ STUB

**File:** `pipeline/messaging.py`

**What it does now:**
- Returns `{"ok": True, "stubbed": True}` for every message
- Logs the message but doesn't actually send it
- Says "set WHATSAPP_TOKEN for live sends"

**What's needed:**
- WhatsApp Business account (Meta)
- WHATSAPP_TOKEN (Cloud API access token)
- WHATSAPP_PHONE_NUMBER_ID (business phone number)
- WhatsApp Business verification (Meta review)

**Cost:** Free (WhatsApp Cloud API has free tier)

**Time to wire:** 30 minutes (if account exists) + Meta review (days/weeks)

### SMS messaging ❌ STUB

**File:** `pipeline/messaging.py`

**What it does now:**
- Returns `{"ok": True, "stubbed": True}` for every SMS
- Says "set TELNYX_API_KEY for live sends"

**What's needed:**
- Telnyx account
- TELNYX_API_KEY
- TELNYX_PHONE_NUMBER
- Phone number purchased

**Cost:** ~£1/month for number + ~£0.01/SMS

**Time to wire:** 15 minutes

### Demo response logic ❌ STUB

**File:** `demos/engine.py`

**What it does now:**
- 10 if/else statements matching keywords
- Returns hardcoded responses from service list
- Not real AI

**What's needed:**
- OpenAI API key for real AI responses
- Or: keep keyword matching (it works for demos)

**Cost:** ~£0.01 per message (OpenAI) or £0 (keyword matching)

**Time to wire:** 1 hour (OpenAI) or 0 (keep keywords)

---

## What's NOT BUILT (doesn't exist)

### Instagram/Reddit scraping ❌ NOT BUILT

**What we have:** Keyword generators that create search queries
**What's missing:** Actually scraping Instagram/Reddit for posts

**What's needed:**
- Instagram Graph API access (Meta Business Partner)
- Reddit API access
- Or: manual searching (we do this ourselves)

**Cost:** Instagram API free (with Meta Business Partner), Reddit API free tier

**Time to build:** 1 day per platform

### Google Business Profile optimisation ❌ NOT BUILT

**What we have:** Nothing
**What's missing:** GBP audit, photo upload, review response, post creation

**What's needed:**
- Google Business Profile API billing enabled
- GBP API access
- Photo upload workflow
- Review response templates

**Cost:** Free (GBP API has free tier, needs billing)

**Time to build:** 2 days

### Schema/llms.txt deployment ❌ NOT BUILT

**What we have:** Generators that create the code
**What's missing:** Actually adding it to their websites

**What's needed:**
- Access to their website hosting
- Or: instructions for them to add it themselves

**Cost:** £0

**Time to build:** 1 day (instructions) or 1 week (if we need to access their hosting)

### Bing Webmaster submission ❌ NOT BUILT

**What we have:** Nothing
**What's needed:** Bing Webmaster Tools account + submission

**Cost:** Free

**Time to build:** 1 hour

### Voice agent ❌ NOT BUILT

**What we have:** influence has the brain (booking pipeline, availability, knowledge YAML)
**What's missing:** The voice runtime (STT, TTS, real-time conversation)

**What's needed:**
- LiveKit for SIP routing
- Qwen-Omni or similar for voice AI
- Telnyx for phone numbers

**Cost:** ~£50-100/month for infrastructure

**Time to build:** 1-2 weeks

---

## What we need before outreach

### Minimum viable outreach (Week 1)

| What | Status | Action needed |
|------|--------|---------------|
| Prospect list | ✅ Ready | None |
| Message templates | ✅ Ready | None |
| Pipeline database | ✅ Ready | None |
| WhatsApp messaging | ❌ Stub | Set up WhatsApp Business account |
| Demo websites | ⚠️ Partial | Deploy to a server |
| Pain calculator | ✅ Ready | None |
| JEV triage | ✅ Ready | None |

### What to tell customers

> "We find you customers from planning applications and make sure you show up when people ask ChatGPT. Try it free for 7 days."

**What we can actually deliver in 7 days:**
1. ✅ Find them leads from planning applications
2. ✅ Calculate how much they're losing
3. ✅ Generate schema markup for their website
4. ✅ Generate llms.txt for AI visibility
5. ✅ Generate robots.txt allowing AI crawlers
6. ✅ Show them their visibility score
7. ❌ Set up WhatsApp AI (needs account)
8. ❌ Optimise Google profile (needs API)
9. ❌ Deploy schema to their website (needs hosting access)

### Honest pitch

> "We'll find you 5 customers from planning applications this week. We'll also generate the code to make you show up in ChatGPT. You'll need to add it to your website (we'll show you how). Free for 7 days."

---

## Priority order for wiring

### Week 1: WhatsApp (critical)
1. Set up WhatsApp Business account
2. Get WHATSAPP_TOKEN
3. Wire into messaging.py
4. Test with real message

### Week 2: Demo hosting
1. Set up simple HTTP server
2. Deploy demos to a URL
3. Test demo links work

### Week 3: GBP optimisation
1. Enable GBP API billing
2. Build GBP audit tool
3. Build photo upload workflow

### Week 4: Schema deployment
1. Build instructions for customers to add schema
2. Or: build website editor that adds it automatically

---

## The honest truth

**We have good data and good code, but the last mile is stubs.**

The prospect data is real. The pipeline is real. The templates are real. The aocsec backend is real.

But WhatsApp doesn't actually send messages. The demos are keyword matching, not AI. Google Maps optimisation doesn't exist. Schema generation works but deployment doesn't.

**We need 1-2 weeks of wiring before we can do real outreach.**

Until then, we can:
1. Manual outreach (call them ourselves)
2. Manual demos (show them the HTML pages)
3. Manual visibility checks (check their Google profile ourselves)

But we can't automate any of it yet.
