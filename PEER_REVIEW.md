# PEER_REVIEW.md

> How do we make AI Onboard work? Honest assessment of what exists, what's missing, and what to build.

---

## The core insight

**Clean, one-time setup. No subscription bullshit.**

The wedge isn't "pay us monthly." The wedge is:

> Earlier draft positioning: "We'll make your business AI-native."
>
> Corrected offer: "We make public business information accurate, accessible, and understandable. We cannot guarantee ChatGPT, Maps, or other AI-assistant placement." See `OFFER.md`.

Then optional: lead generation, custom builds, consulting.

---

## What we have vs what we need

### What exists (ready to use)

| Asset | Where | Status |
|-------|-------|--------|
| 10,000 electrical businesses | powuk → prospects_electrical.csv | ✅ Ready |
| 24 vertical playbooks | cgraphuk (electrician, beauty, barber, etc) | ✅ Ready |
| Installation infrastructure | influence (email, phone, jobs, invoices) | ✅ Ready (needs security audit) |
| Voice agent infrastructure | influence + OpenMuse | ✅ Ready |
| Market intelligence | BigQuery (verticals, pain points, graph) | ✅ Ready |
| Sales scripts | SALES_PLAYBOOK.md | ✅ Ready |

### What needs building

| What | Why | Priority |
|------|-----|----------|
| Meta Business integration | WhatsApp, Facebook, Instagram | P0 |
| Google Business Profile setup | Local discovery | P0 |
| ChatGPT/OpenAI listing optimization | Agentic AI discovery | P0 |
| Website with AI chat | Professional presence | P0 |
| Voice agent for calls | Missed call recovery | P0 |
| Demo workflow | Show prospects what we do | P1 |
| BigQuery dataset | Track installations | P1 |

---

## The Meta Business stack

### What Meta offers businesses

1. **WhatsApp Business API** — customer comms, automated replies
2. **Facebook Business Page** — presence, reviews, marketplace
3. **Instagram Business** — visual presence, DMs
4. **Meta Messenger** — chatbot integration
5. **Meta Ads** — paid promotion (optional)

### What we configure

| Service | What it does | Price |
|---------|--------------|-------|
| WhatsApp Business setup | Professional profile assistance, subject to Meta access, verification, and approval | Separate quote |
| Facebook Business Page | Manual profile completion, subject to customer ownership and approval | Separate quote |
| Instagram Business | Manual profile completion, subject to customer ownership and approval | Separate quote |
| Messenger chatbot | Only with explicit scope, authorization, testing, and supplier charges | Separate quote |
| **Meta Business Stack** | Separate package after access and prerequisites are established | **Separate quote** |

### The AI-native play

When someone asks ChatGPT "find me an electrician in Manchester":

```
ChatGPT searches:
  - Google Business Profile ✓ (we set this up)
  - Facebook Business Page ✓ (we set this up)
  - WhatsApp Business ✓ (we set this up)
  - Website with AI chat ✓ (we set this up)
  - Reviews and ratings ✓ (we help collect these)

Possible outcome: accurate, accessible information may make the business easier for search engines and AI services to understand. No recommendation, ranking, or inclusion is guaranteed.
```

**The current wedge is narrower:** make public information accurate and accessible while preserving the customer’s accounts, permissions, and supplier costs.

---

## The influence connection

### What influence already does

```
stevejobless/SKILL.md — 15-minute onboarding:
  1. Clone kernel (business config)
  2. Register + load
  3. Set autonomy level
  4. Connect WhatsApp
  5. Connect voice (Telnyx + LiveKit)
  6. Connect Google Calendar
  7. Verify first job end-to-end
```

### What we add

```
1. Meta Business Page setup
2. Google Business Profile optimization
3. ChatGPT listing optimization
4. Website with AI chat
5. Voice agent configuration
6. WhatsApp Business setup
7. Training session
8. Handover documentation
```

### The graph per business

Each onboarded business gets a graph:

```json
{
  "business_id": "DEMO-ELEC-MANCHESTER-001",
  "name": "Fictional Manchester Electrical Co.",
  "vertical": "electrician",
  "postcode": "M1 1AA",
  "platforms": {
    "google_business": "assistance-only",
    "whatsapp_business": "separate-deliverable",
    "facebook": "separate-deliverable",
    "instagram": "separate-deliverable",
    "website": "separate-deliverable",
    "chatgpt_listing": "no-guarantee"
  },
  "voice_agent": {
    "status": "separate-deliverable",
    "phone": "+44 7700 900078",
    "answer_rate": null
  },
  "ai_assistant": {
    "status": "demo-only",
    "capabilities": ["quote_drafting", "scheduling_proposal"]
  },
  "installed_at": "DEMO-DATE",
  "installed_by": "ai_onboard"
}
```

---

## The clean service model

### What we charge

```
ONE-OFF SETUP: £499
  - Meta Business Stack (WhatsApp, Facebook, Instagram)
  - Google Business Profile optimization
  - ChatGPT listing optimization
  - Website with AI chat
  - Voice agent for calls
  - Training session (1 hour)
  - Written handover
  - 14 days of fixes

OPTIONAL ADD-ONS (after setup):
  - Lead generation: £149/month
  - Custom integrations: £750+
  - Ongoing consulting: £299/month
```

### What we DON'T charge

- No monthly fees for the basic setup
- No "platform fees"
- No "AI usage fees"
- No hidden costs

### Why this works

1. **Clean pitch**: "We set you up, teach you, leave"
2. **No commitment anxiety**: One payment, done
3. **Word of mouth**: Happy customers tell friends
4. **Upsell naturally**: "Need more? We can help"
5. **No churn**: Can't cancel what you don't subscribe to

---

## The language advantage

### Foreign tradies

Many UK trades businesses are run by people whose first language isn't English. Muse/WhatsApp voice agents can:

- Answer calls in multiple languages
- Translate enquiries
- Draft quotes in the customer's language
- Handle international suppliers

**This is a massive untapped market.** A Polish electrician in Birmingham can now serve English-speaking customers through AI, and vice versa.

### What we offer

| Service | What it does | Price |
|---------|--------------|-------|
| Multi-language voice agent | Answers calls in Polish, Urdu, Arabic, etc | Included in setup |
| Translation service | Translates quotes, invoices | Included |
| Multi-language website | Website in multiple languages | £149 extra |

---

## The agentic AI discovery play

### The problem

Most trades businesses don't appear when AI assistants search for them. They're invisible to:
- ChatGPT
- Google Gemini
- Meta AI
- Apple Intelligence
- Perplexity

### The solution

We optimize their presence across ALL platforms AI assistants check:

| Platform | What we do | Why it matters |
|----------|------------|----------------|
| Google Business Profile | Complete, accurate, reviewed | Google AI uses this |
| Facebook Business Page | Complete, active, reviewed | Meta AI uses this |
| WhatsApp Business | Professional profile, quick replies | Meta AI uses this |
| Website | AI-readable, structured data | ChatGPT/Gemini use this |
| ChatGPT listing | Optimize for OpenAI's directory | ChatGPT uses this |
| Apple Maps | Claimed, complete | Apple Intelligence uses this |

### The pitch

> "When someone asks ChatGPT 'find me an electrician in Manchester',
> will your business appear? We make sure it does."

---

## Peer review: what's missing

### 1. Meta Business API access

**Problem:** We need Meta Business API access to configure WhatsApp Business, Facebook Pages, and Instagram for clients.

**Solution:** 
- Apply for Meta Business Partner status
- Use WhatsApp Cloud API directly
- Use Facebook Graph API for page management
- Document the process for each platform

### 2. ChatGPT listing optimization

**Problem:** ChatGPT doesn't have a formal "business listing" yet. But it does:
- Crawl websites for structured data
- Use Google Business Profile data
- Reference Facebook/LinkedIn profiles
- Use schema.org markup

**Solution:**
- Add structured data to client websites
- Optimize Google Business Profile
- Ensure consistent NAP (Name, Address, Phone) across platforms
- Create content that AI assistants will reference

### 3. Voice agent language support

**Problem:** OpenMuse voice agent currently uses English.

**Solution:**
- Use Telnyx for multi-language telephony
- Use Muse's language capabilities
- Configure language-specific greeting scripts
- Test with real multi-language scenarios

### 4. Demo workflow

**Problem:** We need a working demo to show prospects.

**Solution:**
- Use influence's tradie system
- Create a fictional electrician business
- Show: enquiry → quote → job → invoice
- Run on AI Onboard's own domain

### 5. Security audit

**Problem:** influence has security issues (phone.send without approval).

**Solution:**
- Fix the approval workflow
- Audit multi-tenant isolation
- Test with real customer data
- Document security practices

---

## Immediate next steps

### This week

1. **Apply for Meta Business API access**
2. **Build demo workflow using influence**
3. **Fix influence security issues**
4. **Create first sales email template**
5. **Start calling Greater Manchester prospects**

### This month

1. **Deliver 3 founding-client installations**
2. **Document installation process**
3. **Refine based on feedback**
4. **Build repeatable playbook**
5. **Start charging normal price**

### This quarter

1. **100 installations**
2. **Referral programme live**
3. **Lead generation product launched**
4. **Custom builds pipeline**
5. **Consider Muse connector submission**

---

## The one-liner

> **AI Onboard’s pilot configures authorized workflows, teaches the owner, documents the installation, and leaves. One pilot fee; no outcome guarantees.**
