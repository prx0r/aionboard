# DEMO_SPEC.md

> What we build and show to convert prospects into customers.

## The demo principle

**Don't tell them what it does. Show them their own business running on it.**

Every demo is personalised:
- Their business name
- Their services and prices
- Their Google rating and reviews
- Their local area leads
- Their AI visibility status

---

## Demo 1: Website + chatbot (buildable NOW)

### What we show

A working website with their business data, featuring an AI chatbot that answers questions.

### How to build it

1. **Collect data** (from intake form):
   - Business name, phone, email, address
   - Services offered + prices
   - Opening hours
   - Photos (if available)

2. **Generate knowledge bundle**:
   ```python
   # From intake form data
   knowledge = {
       "business": "Yulia Hamilton Nails & Beauty",
       "services": ["gel manicure £35", "acrylic full set £55", "pedicure £40"],
       "hours": "Tue-Sat 9am-6pm",
       "address": "40 Laystall St, Manchester M1 2JQ",
       "phone": "07858 358562",
       "reviews": "4.8★ from 686 reviews"
   }
   ```

3. **Generate website**:
   - One page with services, prices, reviews, contact
   - Inline chatbot that answers from knowledge bundle
   - Booking link to their existing system
   - Mobile responsive

4. **Deploy to Cloudflare Pages**:
   - Free hosting
   - Custom domain (or subdomain of aionboard.co.uk)
   - SSL included

### Demo flow

> "Here's your website. See the chatbot in the bottom right? Ask it anything about your business."

[Customer types: "How much for a gel manicure?"]

[Chatbot: "A gel manicure at Yulia Hamilton Nails & Beauty costs £35. The appointment takes about 45 minutes. Would you like to book? Here's the link: [booking link]"]

> "This works 24/7. When someone finds you on Google at 11pm, they get an instant answer instead of waiting until morning."

### Tech stack

| Component | Tech | Cost |
|-----------|------|------|
| Website | Static HTML + CSS | £0 |
| Chatbot | Token overlap matching | £0 |
| Hosting | Cloudflare Pages | £0 |
| Domain | aionboard.co.uk subdomain | £0 |
| SSL | Cloudflare | £0 |

**Total cost to deliver: £0** (after initial build)

---

## Demo 2: Google Maps optimisation

### What we show

Before/after of their Google Business Profile with predicted traffic increase.

### How to build it

1. **Audit current profile**:
   - Check all fields completed
   - Count photos
   - Check review responses
   - Verify NAP consistency

2. **Generate improvement report**:
   ```
   Current score: 45/100
   - Missing: service menu (0/10 services listed)
   - Missing: photos (2 of recommended 10+)
   - Missing: review responses (0 of 47 reviews responded to)
   - Missing: weekly posts (0 in last 30 days)
   
   After optimisation: 85/100
   Expected traffic increase: +40%
   ```

3. **Show before/after**:
   - Before: incomplete profile, no photos, no responses
   - After: complete profile, 10+ photos, all reviews responded to, weekly posts

### Demo flow

> "I audited your Google Business Profile. Here's what I found."

[Show audit report]

> "Your profile is 45% complete. Your competitor at 4.5★ is at 85%. That's why they show up first."

> "After we optimise it, you'll be at 85% — and here's the expected traffic increase."

### What we need

- Google Business Profile API access (needs billing)
- Or: manual optimisation via Google Business Profile dashboard

---

## Demo 3: AI visibility (ChatGPT/Perplexity)

### What we show

Ask ChatGPT/Perplexity a question about their business — and show them whether they appear.

### How to build it

1. **Test current visibility**:
   - Ask ChatGPT: "Find me a [vertical] in [city]"
   - Ask Perplexity: same
   - Ask Google AI Overview: same
   - Record whether they appear

2. **Implement fixes**:
   - Add schema markup to their website
   - Add llms.txt
   - Add robots.txt allowing AI crawlers
   - Ensure NAP consistency

3. **Re-test after fixes**:
   - Ask again
   - Show improvement

### Demo flow

> "Let me ask ChatGPT: 'Find me a nail tech in Manchester.'"

[ChatGPT response — business not mentioned]

> "See? You're not in the answer. But your competitor is. Let me show you why."

> "Here's what we fix: schema markup, llms.txt, robots.txt. After we implement these, ChatGPT will find you."

> "We also add your business to Bing Webmaster Tools, which feeds into ChatGPT's search."

### What we need

- Schema markup generator (buildable now)
- llms.txt generator (buildable now)
- robots.txt template (buildable now)
- Bing Webmaster submission (free)

---

## Demo 4: Local lead generation

### What we show

A list of people in their area who need their services RIGHT NOW.

### How to build it

1. **Find demand signals**:
   - Planning applications (extensions, renovations → need electrician/plumber)
   - OZEV grants (EV charger → need electrician)
   - New pet registrations (→ need groomer)
   - New property sales (→ need cleaner/gardener)
   - Wedding venue bookings (→ need photographer)

2. **Score leads**:
   - Urgency (how soon do they need it?)
   - Budget (can they afford it?)
   - Location (in their service area?)

3. **Present leads**:
   ```
   This week's leads for Yulia Hamilton Nails:
   
   1. "Looking for a nail tech in Manchester for my wedding" — Instagram, 2 days ago
   2. "Any recommendations for gel nails near Deansgate?" — Reddit, 1 day ago
   3. "Prom season! Need nails done Saturday" — TikTok, today
   ```

### Demo flow

> "Here are 5 people in Manchester who need a nail tech this week — from Instagram, Reddit, and TikTok."

[Show lead list with sources]

> "We send these to you every week. You just reply and book them."

### What we need

- Instagram/TikTok search (manual or API)
- Reddit search (API available)
- Google Alerts for local demand
- Planning application data (we have this)

---

## Demo 5: Full package (combined)

### What we show

Everything together: website, Google Maps, AI visibility, leads — all working.

### Demo flow (15 minutes)

**Minute 1-3: The problem**
> "I searched for your business on Google, ChatGPT, and Instagram. Here's what I found — and here's what's missing."

**Minute 4-7: The website**
> "Here's your new website with an AI assistant. Ask it anything."

[Demo chatbot]

**Minute 8-10: Google Maps**
> "Here's your Google profile after optimisation — 85% complete with photos, service menu, and booking link."

**Minute 11-13: AI visibility**
> "Ask ChatGPT 'find me a [vertical] in [city]' — with our optimisation, you now appear."

**Minute 14-15: Close**
> "All of this for £40 bundle or £50/month. Want to try it free for 4 weeks?"

---

## What we need to build (priority order)

### Week 1: Website + chatbot
- [ ] Per-vertical website template (HTML/CSS)
- [ ] Knowledge bundle builder (from intake data)
- [ ] Chat interface (reuse site/chat.html)
- [ ] Deploy to Cloudflare Pages

### Week 2: Google Maps + AI visibility
- [ ] GBP audit tool
- [ ] Schema markup generator
- [ ] llms.txt generator
- [ ] robots.txt template

### Week 3: Lead generation
- [ ] Instagram/TikTok demand scanner
- [ ] Reddit demand scanner
- [ ] Planning application monitor
- [ ] Lead scoring system

### Week 4: Combined demo
- [ ] End-to-end demo script
- [ ] Personalisation engine
- [ ] Metrics tracking
- [ ] Customer dashboard

---

## Success metrics

| Metric | Target | How we measure |
|--------|--------|---------------|
| Demo → trial conversion | >30% | Track signups |
| Trial → paid conversion | >50% | Track payments |
| Website chatbot response rate | >90% | Chat logs |
| Google profile completeness | >80% | GBP audit |
| AI visibility improvement | >50% | Before/after tests |
| Lead quality (response rate) | >20% | Customer feedback |

---

## The one-liner

> "We don't sell software. We make your business visible to humans and AI — and find you customers while you sleep."
