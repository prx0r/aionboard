# AUTOMATION_PLAYBOOK.md

> How to automate AI Onboard installations without clients realizing.

---

## The key insight

We can automate 80% of the setup. The client thinks we're doing magic. We're just connecting APIs.

```
CLIENT THINKS:
  "They set up my WhatsApp, website, Google, and AI in an hour"
  "Incredible service, worth every penny"

WHAT WE ACTUALLY DO:
  1. Run automated scripts
  2. Connect to APIs
  3. Configure settings
  4. Verify everything works
  5. Hand over login details
```

---

## What we automate

### 1. Meta Business Stack (WhatsApp, Facebook, Instagram)

**API:** WhatsApp Cloud API + Facebook Graph API

**Automated steps:**
```python
# 1. Create WhatsApp Business account
POST https://graph.facebook.com/v23.0/<PORTFOLIO_ID>/whatsapp_business_accounts
  - name: "{business_name}"
  - currency: "GBP"

# 2. Register phone number
POST https://graph.facebook.com/v23.0/<PHONE_ID>/register
  - messaging_product: "whatsapp"
  - pin: "123456"

# 3. Set up business profile
POST https://graph.facebook.com/v23.0/<PHONE_ID>/whatsapp_business_profile
  - description: "{business_description}"
  - websites: ["{website_url}"]
  - profile_picture_url: "{logo_url}"

# 4. Create message templates
POST https://graph.facebook.com/v23.0/<WABA_ID>/message_templates
  - name: "quote_followup"
  - language: "en"
  - category: "MARKETING"

# 5. Configure webhook
POST https://graph.facebook.com/v23.0/<APP_ID>/subscriptions
  - object: "whatsapp_business_account"
  - callback_url: "https://ai-onboard.co.uk/webhook/meta"
  - verify_token: "{random_token}"
```

**Time:** 5 minutes (automated)
**Cost:** £0 (Meta provides 1,000 free conversations/month)

---

### 2. Google Business Profile

**API:** My Business Business Information API

**Automated steps:**
```python
# 1. Get access token
POST https://oauth2.googleapis.com/token
  - code: "{authorization_code}"
  - client_id: "{client_id}"
  - client_secret: "{client_secret}"

# 2. Create location
POST https://mybusinessbusinessinformation.googleapis.com/v1/{parent=accounts/*}/locations
  - locationName: "{business_name}"
  - address: { ... }
  - phoneNumbers: { primaryPhone: "{phone}" }
  - websiteUrl: "{website_url}"
  - categories: [{ displayName: "Electrician" }]

# 3. Verify location
POST https://mybusinessbusinessinformation.googleapis.com/v1/{name=locations/*}:verify
  - method: "PHONE" or "POSTCARD"

# 4. Set attributes
PATCH https://mybusinessbusinessinformation.googleapis.com/v1/{name=locations/*/attributes}
  - attributes: [
      { name: "opening_hours", value: "..." },
      { name: "service_area", value: "..." }
    ]

# 5. Create service list
PATCH https://mybusinessbusinessinformation.googleapis.com/v1/{name=locations/*/serviceList}
  - services: [
      { name: "EV Charger Installation", price: "..." },
      { name: "Consumer Unit Replacement", price: "..." }
    ]
```

**Time:** 10 minutes (automated, verification takes 24-48h)
**Cost:** £0

---

### 3. ChatGPT/AI Optimization

**What we do:**

```python
# 1. Create llms.txt file
write_to_website("/llms.txt", """
# {business_name}

{business_name} provides {services} in {area}.

## Services
- {service_1}: {description}
- {service_2}: {description}

## Contact
- Phone: {phone}
- Email: {email}
- Website: {website}
""")

# 2. Add schema markup to website
add_schema_markup({
    "@context": "https://schema.org",
    "@type": "Electrician",
    "name": "{business_name}",
    "address": { ... },
    "telephone": "{phone}",
    "areaServed": "{area}",
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Electrical Services",
        "itemListElement": [...]
    }
})

# 3. Configure robots.txt
write_to_website("/robots.txt", """
User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: *
Allow: /
""")

# 4. Submit to Bing Webmaster Tools
POST https://www.bing.com/webmaster/api.svc/json/SubmitUrl
  - url: "{website_url}"
  - apiKey: "{bing_api_key}"
```

**Time:** 15 minutes (automated)
**Cost:** £0

---

### 4. Website with AI Chat

**Using OpenMuse or custom solution:**

```python
# 1. Create website from template
generate_website({
    "template": "trades/electrician",
    "business_name": "{name}",
    "services": [...],
    "contact": { ... },
    "ai_chat": True
})

# 2. Deploy to Cloudflare Pages
deploy_to_cloudflare({
    "project": "aionboard-{slug}",
    "source": "./generated/{slug}"
})

# 3. Configure AI chat widget
configure_ai_chat({
    "endpoint": "https://api.ai-onboard.co.uk/chat/{slug}",
    "model": "gpt-4",
    "system_prompt": "You are a helpful assistant for {business_name}..."
})
```

**Time:** 20 minutes (automated)
**Cost:** £0 (Cloudflare Pages free tier)

---

### 5. Voice Agent

**Using Telnyx + LiveKit (from influence):**

```python
# 1. Provision phone number
POST https://api.telnyx.com/v2/phone_numbers
  - area_code: "{area_code}"
  - country: "GB"

# 2. Configure voice agent
POST https://api.telnyx.com/v2/call_control/{connection_id}/webhooks
  - webhook_url: "https://api.ai-onboard.co.uk/voice/{slug}"

# 3. Set up greeting
POST https://api.ai-onboard.co.uk/voice/{slug}/greeting
  - greeting: "Thank you for calling {business_name}. How can I help?"
  - language: "en"

# 4. Configure SMS fallback
POST https://api.telnyx.com/v2/messages
  - to: "{business_phone}"
  - from: "{telnyx_number}"
  - text: "New enquiry: {caller_name}, {job_description}"
```

**Time:** 10 minutes (automated)
**Cost:** £1/month (Telnyx)

---

## The one-hour installation

### Minute 0-5: Discovery
- Ask for business name, address, phone, email
- Ask for current software (Tradify, Xero, etc.)
- Ask for services and pricing

### Minute 5-10: Meta Business
- Create WhatsApp Business account
- Register phone number
- Set up business profile
- Create message templates

### Minute 10-20: Google Business
- Create/claim Google Business Profile
- Set categories, services, hours
- Add photos (use AI-generated if none)
- Submit for verification

### Minute 20-30: Website
- Generate website from template
- Deploy to Cloudflare
- Add schema markup
- Configure robots.txt for AI crawlers

### Minute 30-40: AI Chat
- Configure AI chat widget
- Set up system prompt
- Test with sample questions

### Minute 40-50: Voice Agent
- Provision phone number
- Configure greeting
- Set up SMS fallback
- Test call

### Minute 50-60: Training
- Show WhatsApp interface
- Show Google Business Profile
- Show website and AI chat
- Show voice agent
- Hand over login details

---

## The graph

Each onboarded business becomes a graph node:

```json
{
  "business_id": "aionboard-elec-manchester-001",
  "name": "WN Networks Ltd",
  "vertical": "electrician",
  "postcode": "S5 9LG",
  "region": " Sheffield",
  "installed_at": "2026-09-23",
  "package": "ai_business_setup",
  "price": 499,
  
  "platforms": {
    "whatsapp_business": {
      "status": "active",
      "phone": "+44 114 123 4567",
      "waba_id": "123456789"
    },
    "google_business": {
      "status": "verified",
      "location_id": "abc123",
      "rating": 4.8,
      "reviews": 12
    },
    "facebook": {
      "status": "active",
      "page_id": "wn-networks-ltd"
    },
    "instagram": {
      "status": "active",
      "username": "@wnnetworks"
    },
    "website": {
      "status": "live",
      "url": "https://wn-networks.co.uk",
      "ai_chat": true,
      "schema_markup": true,
      "llms_txt": true
    },
    "voice_agent": {
      "status": "active",
      "phone": "+44 114 987 6543",
      "provider": "telnyx"
    }
  },
  
  "ai_optimization": {
    "robots_txt": true,
    "schema_markup": true,
    "llms_txt": true,
    "bing_submitted": true,
    "google_crawlable": true,
    "chatgpt_crawlable": true
  },
  
  "lead_generation": {
    "weekly_alerts": false,
    "planning_apps": false,
    "procurement": false
  }
}
```

---

## What clients don't see

### The automation layer

```
CLIENT SEES:
  "Your WhatsApp is set up"
  "Your Google profile is live"
  "Your website is ready"

WE ACTUALLY DO:
  - Call Meta API
  - Call Google API
  - Generate HTML
  - Deploy to Cloudflare
  - Configure AI models
  - Set up webhooks
  - Verify everything works
```

### The ongoing intelligence

```
CLIENT SEES:
  "Here are 5 potential jobs this week"

WE ACTUALLY DO:
  - Query powuk for planning apps
  - Query BigQuery for procurement
  - Score by relevance
  - Format as email digest
  - Send via our platform
```

---

## Revenue model (revised)

### One-time setup

| Service | Price | What we automate |
|---------|-------|------------------|
| AI Business Setup | £499 | Meta, Google, website, voice, training |
| Meta Business Stack | £399 | WhatsApp, Facebook, Instagram |
| Website + AI Chat | £249 | Template site + AI widget |
| Voice Agent Setup | £149 | Telnyx + greeting |
| **Bundle (all above)** | **£499** | **Everything** |

### Optional add-ons

| Service | Price | What it is |
|---------|-------|------------|
| Lead Generation | £149/mo | Weekly leads from powuk |
| Custom Integrations | £750+ | Xero, Tradify, custom workflows |
| Consulting | £299/mo | Legal, advertising, strategy |
| Multi-language | £149 extra | Voice agent in Polish, Urdu, etc. |

### The key insight

**One fee. No subscription. No bullshit.**

> "We set you up, teach you how to use it, and leave. If you need more later, we're here."

This is the opposite of SaaS. It's a service, not a product.

---

## Next steps

1. Apply for Meta Business API access
2. Apply for Google Business Profile API access
3. Set up Telnyx account
4. Build demo installation
5. Test with fictional business
6. Deliver 3 founding-client installations
7. Refine automation based on feedback
