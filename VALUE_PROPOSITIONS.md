# VALUE_PROPOSITIONS.md

> What we actually deliver for each vertical. Not just "set up WhatsApp" — real value that makes money.

## The problem we solve

Every small business has the same problem: **they're invisible online and lose customers to competitors who show up first.**

- 40% of sole traders use AI but only 18% have it integrated (DSIT 2026)
- 91% of SMBs score below 60/100 in AI visibility
- 35% of construction businesses don't even have a website
- Most businesses don't appear when people ask ChatGPT, Perplexity, or Google AI

**We fix all of this.** Not with a SaaS tool — with a done-for-you service.

---

## The 4 things we deliver

### 1. Find them customers (lead generation)

**What we do:** Use government data, planning applications, procurement contracts, and directory listings to find people who need their services RIGHT NOW.

**How it works:**

| Vertical | Lead source | What we find | How often |
|----------|------------|-------------|-----------|
| Nails | Instagram/TikTok local hashtags | People posting "looking for nail tech" | Daily |
| Electrician | Planning applications, OZEV grants, EICR expiries | Properties that need electrical work | Weekly |
| Dog groomers | New pet registrations, vet referrals | New dog owners in their area | Weekly |
| Cleaners | Letting agent listings, move-in dates | New tenants needing cleaning | Weekly |
| Hair | Local event listings, wedding season | Events requiring hair services | Weekly |
| Beauty | Seasonal trends, local events | People searching for treatments | Weekly |
| Lashes | Wedding season, prom season, events | High-intent demand periods | Seasonal |
| Car detailers | New car registrations, MOT reminders | Cars needing detailing | Monthly |
| Driving instructors | Pass rates by area, theory test bookings | Learners in their area | Weekly |
| Gardeners | Seasonal demand, property sales | New homeowners needing garden work | Weekly |
| Weddings | Venue bookings, engagement season | Engaged couples in their area | Weekly |

**Demo we can show:** "Here are 15 people in Manchester who need an electrician this week — from planning applications and OZEV grants."

**Tech needed:**
- Planning applications API (we have this in powuk)
- OZEV grant data (we have this)
- Instagram/TikTok search (manual or API)
- Letting agent data (public listings)
- Google Alerts for local demand

---

### 2. Make them show up (Google Maps + SEO)

**What we do:** Optimise their Google Business Profile, add photos, complete all fields, set up service menus, and ensure consistent NAP (Name, Address, Phone) across all platforms.

**How it works:**

| Step | What we do | Time | Impact |
|------|-----------|------|--------|
| 1 | Complete Google Business Profile | 30 min | +40% visibility |
| 2 | Add service menu with prices | 15 min | +25% enquiry rate |
| 3 | Add 10+ photos | 15 min | +35% click-through |
| 4 | Set up Q&A with AI answers | 15 min | +20% trust |
| 5 | Configure booking link | 10 min | Direct conversions |
| 6 | Add posts weekly | 5 min/week | Ongoing visibility |
| 7 | Respond to every review | 5 min/review | +15% conversion |

**Demo we can show:** "Your Google profile is 40% complete. Here's what it looks like after we optimise it — and here's the expected traffic increase."

**Tech needed:**
- Google Business Profile API (needs billing enabled)
- Photo generation/optimisation
- Review response templates
- NAP consistency checker

---

### 3. Build them a website (AI-native)

**What we do:** Build a one-page website with an inline AI chatbot that answers questions, quotes prices, and books appointments — all from their knowledge base.

**How it works:**

| Component | What it does | Tech |
|-----------|-------------|------|
| One-page site | Shows services, prices, reviews, contact | Static HTML + CSS |
| AI chatbot | Answers questions 24/7 | Knowledge bundle + token overlap |
| Booking link | Direct to their booking tool | Link in bio |
| Review display | Shows Google reviews | Google Places API |
| Service menu | Lists all services with prices | From intake form |
| Contact form | Captures enquiries | Email forwarding |

**Demo we can show:** "Here's your website with an AI assistant that knows your services, prices, and availability. Ask it anything."

**Tech needed:**
- Static site generator (we have this in website.py)
- Knowledge bundle builder (we have this in graph.py)
- Chat interface (we have this in site/chat.html)
- Cloudflare Pages hosting (free)

---

### 4. Make them visible to AI (ChatGPT/Perplexity/Gemini)

**What we do:** Add structured data, schema markup, llms.txt, and ensure consistent information across all platforms so AI assistants can find and recommend them.

**How it works:**

| Platform | What we do | Impact |
|----------|-----------|--------|
| Schema.org markup | LocalBusiness, Service, FAQPage | Shows in Google AI Overviews |
| llms.txt | AI-readable business summary | Shows in ChatGPT/Perplexity |
| robots.txt | Allow AI crawlers | Indexable by all AI systems |
| NAP consistency | Same name/address/phone everywhere | Trust signal for AI ranking |
| Google Business Profile | Complete, active, reviewed | Primary data source for AI |
| Bing Webmaster Tools | Submit sitemap | Shows in Bing/Copilot |

**Demo we can show:** "Ask ChatGPT 'find me a nail tech in Manchester' — your business now appears in the answer."

**Tech needed:**
- Schema markup generator
- llms.txt generator
- NAP consistency checker
- Bing Webmaster submission

---

## What we charge

| Service | Price | What they get |
|---------|-------|--------------|
| Basic onboarding | £20 one-off | Meta Business Agent setup |
| Website + chatbot | £10 one-off | One-page site with AI assistant |
| Google Maps optimisation | £10 one-off | Full GBP completion |
| AI visibility package | £10 one-off | Schema, llms.txt, robots.txt |
| Lead generation | £10 one-off | First batch of local leads |
| **Starter bundle** | **£40 one-off** | Website + GBP + AI visibility + leads |
| **Integrated package** | **£50/month** | Ongoing monitoring + support + monthly leads |

**The pitch:** "£20 to get started. £10 for a website. £10 to show up on Google. £10 to show up in ChatGPT. £10 for leads. £50/month to keep it all running. Less than a single day of a social media manager."

---

## What we build first (MVP)

### Priority 1: Website + chatbot (buildable NOW)

We already have:
- Static site generator (`website.py`)
- Knowledge bundle builder (`graph.py`)
- Chat interface (`site/chat.html`)
- Vertical profiles with services and prices

**What to build:**
1. Per-vertical website template (different layouts for different businesses)
2. Knowledge bundle from intake form data
3. Inline chatbot that answers from the knowledge base
4. Deploy to Cloudflare Pages (free)

### Priority 2: Google Maps optimisation (needs API billing)

We need:
- Google Business Profile API access
- Photo upload capability
- Review response system

**What to build:**
1. GBP audit tool (check completeness)
2. Photo upload workflow
3. Review response templates
4. NAP consistency checker

### Priority 3: AI visibility (buildable NOW)

We already have:
- Schema markup knowledge
- llms.txt format
- robots.txt format

**What to build:**
1. Schema markup generator per vertical
2. llms.txt generator from knowledge bundle
3. robots.txt template
4. Bing Webmaster submission helper

### Priority 4: Lead generation (needs data sources)

We have:
- powuk data (planning applications, procurement)
- SerpAPI (Google Maps search)
- Companies House (business verification)

**What to build:**
1. Planning application monitor (weekly)
2. OZEV grant tracker
3. Instagram/TikTok demand scanner
4. Letting agent listing monitor

---

## Demo script (15 minutes)

### Minute 1-3: Show the problem
> "I searched for 'nail tech Manchester' on ChatGPT. Here's what it said — your business isn't mentioned. But your competitor at 4.5★ is. Let me show you why."

### Minute 4-7: Show the solution
> "Here's what we build for you: a website with an AI assistant that knows your services, prices, and availability. Ask it anything."

[Demo the chatbot answering questions]

> "Here's your Google Business Profile after we optimise it — complete with service menu, photos, and booking link."

### Minute 8-10: Show the leads
> "Here are 15 people in Manchester who need a nail tech this week — from Instagram posts and local searches. We send these to you automatically."

### Minute 11-13: Show the AI visibility
> "Ask ChatGPT 'find me a nail tech in Manchester' — with our optimisation, your business now appears in the answer."

### Minute 14-15: Close
> "All of this for £20 to start, £10 for the website, £10 for Google, £10 for AI visibility, £10 for leads. Or £40 for the bundle. Want to try it free for 4 weeks?"

---

## Tech stack (what we build)

### Existing (already have)
- `website.py` — static site generator
- `graph.py` — knowledge bundle builder
- `site/chat.html` — chat interface
- `verticals/*/profile.json` — services, prices, pain points
- `pipeline/` — outreach tracking
- `prospects.py` — prospect scoring

### Need to build
1. **Website template engine** — per-vertical layouts with customisable branding
2. **Knowledge bundle builder** — auto-generate from intake form data
3. **Google Business Profile auditor** — check completeness, suggest improvements
4. **Schema markup generator** — LocalBusiness, Service, FAQPage per vertical
5. **llms.txt generator** — AI-readable business summary
6. **Lead monitor** — planning applications, OZEV grants, Instagram demand
7. **Review request system** — automated post-service Google review requests
8. **NAP checker** — verify consistency across platforms

### Timeline
- **Week 1:** Website template + knowledge bundle builder
- **Week 2:** Chat interface + deploy to Cloudflare
- **Week 3:** GBP auditor + schema generator
- **Week 4:** Lead monitor + review system

---

## Revenue model

### Per customer

| Revenue stream | Price | Frequency | Margin |
|---------------|-------|-----------|--------|
| Basic onboarding | £20 | One-off | 90% |
| Website + chatbot | £10 | One-off | 85% |
| GBP optimisation | £10 | One-off | 80% |
| AI visibility | £10 | One-off | 85% |
| Lead generation | £10 | One-off | 70% |
| Integrated support | £50/month | Monthly | 80% |
| **Total per customer** | **£110 + £50/mo** | | |

### At scale (100 customers)

| Metric | Value |
|--------|-------|
| One-off revenue | £11,000 |
| Monthly recurring | £5,000 |
| Annual recurring | £60,000 |
| Total year 1 | £71,000 |
| Cost to deliver | ~£10,000 |
| **Gross profit** | **~£61,000** |

---

## What makes this defensible

1. **The rulebook** — 370+ failure modes across 11 verticals. A competitor can copy our tools; they can't copy our mistakes-and-fixes list.

2. **The data** — 1,500+ prospects, planning applications, OZEV grants, Companies House data. We know who needs what, when.

3. **The vertical depth** — We don't do "generic AI for businesses." We do "AI for nail techs that knows gel vs acrylic timing."

4. **The done-for-you model** — We don't sell software. We sell the outcome. The customer never touches a dashboard.

5. **The referral engine** — Every happy customer refers one more. The network compounds.
