# AUTOMATION_PLAYBOOK.md

> Pilot installation notes. Nothing here is production automation yet.

Current canonical offer: `OFFER.md`. Older sections below are implementation research unless they match `OFFER.md`.

Customers must understand which services process their information, which accounts they own, what has been configured for them, and which supplier charges they pay directly.

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
  - pin: "<SECURELY_GENERATED_PIN>"

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
  - callback_url: "https://aionboard.co.uk/webhook/meta"
  - verify_token: "{random_token}"
```

**Status:** Manual/design only. Production WhatsApp/Facebook/Instagram integration is blocked until access, review, business verification, payment terms, and explicit customer authorization are completed.

**Cost:** Supplier charges apply and vary by message category, destination, and usage. AI Onboard does not represent Meta messaging as free.

---

### 2. Google Business Profile

**Status:** Assisted manual setup through Google’s ordinary interface. API automation is not available in this pilot and requires Google approval.

**Manual-first workflow:**
```python
# 1. Get access token
POST https://oauth2.googleapis.com/token
  - code: "{authorization_code}"
  - client_id: "{client_id}"
  - client_secret: "{client_secret}"

# 2. Create or claim location using Google’s ordinary UI
  - Use the current Business Profile field names, including `title`, `websiteUri`, and the primary category object.
  - For a service-area business, do not publicly display a home address.

# 3. Track verification separately
  - Verification uses Google’s separate verification process.
  - Available methods depend on the options Google offers for that location.
  - Keep the task as `pending` until Google confirms verification.

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

**Time:** Assisted setup time varies by business. Verification timing depends on Google, not AI Onboard.
**Cost:** Google does not charge for ordinary Business Profile management here, but customer-owned subscriptions and verification-related costs remain the customer’s responsibility.

---

### 3. Search and AI-readability improvements

**Status:** Accuracy and accessibility work only. AI Onboard cannot guarantee recommendations, ranking, or inclusion.

**What we do:**

```python
# 1. Optionally test an llms.txt file
# Google has said llms.txt does not affect Google Search visibility or ranking.
# Use it only as an optional experiment, not a central deliverable.
write_to_website("/llms.txt", """
# {business_name}

{business_name} provides {services} in {area}.
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

**Time:** Varies by website access and platform.
**Cost:** Customer-owned hosting, domains, and subscriptions remain separate.

---

### 4. Website with AI Chat

**Status:** Separate deliverable. Not included in the standard £499 pilot setup.

**Research notes only:**

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
    "endpoint": "https://api.aionboard.co.uk/chat/{slug}",
    "model": "gpt-4",
    "system_prompt": "You are a helpful assistant for {business_name}..."
})
```

**Time:** Varies by template, content, approvals, and hosting access.
**Cost:** Customer-owned hosting, domains, AI-model usage, and maintenance are separate.

---

### 5. Voice Agent

**Status:** Separate deliverable. Not included in the standard £499 pilot setup.

**Research notes only:**

```python
# 1. Provision phone number
POST https://api.telnyx.com/v2/phone_numbers
  - area_code: "{area_code}"
  - country: "GB"

# 2. Configure voice agent
POST https://api.telnyx.com/v2/call_control/{connection_id}/webhooks
  - webhook_url: "https://api.aionboard.co.uk/voice/{slug}"

# 3. Set up greeting
POST https://api.aionboard.co.uk/voice/{slug}/greeting
  - greeting: "Thank you for calling {business_name}. How can I help?"
  - language: "en"

# 4. Configure SMS fallback
POST https://api.telnyx.com/v2/messages
  - to: "{business_phone}"
  - from: "{telnyx_number}"
  - text: "New enquiry: {caller_name}, {job_description}"
```

**Time:** Varies by telephony access, testing, and monitoring requirements.
**Cost:** Telephone service, compute, speech/model usage, monitoring, and fault handling are separate customer-paid obligations unless explicitly quoted.

---

## Pilot installation checklist

The standard pilot is manual-first. It does not promise automated API provisioning, website creation, live voice service, Meta administration, custom integrations, or lead generation.

1. Record discovery answers and customer authorizations.
2. Configure only the customer-authorized existing email and calendar workflows.
3. Prepare one enquiry-capture workflow using customer-approved contact details.
4. Draft one quotation from the customer-approved price book.
5. Require owner approval before any outbound send.
6. Assist with Google Business Profile through Google’s ordinary interface.
7. Record verification as pending until Google confirms it.
8. Conduct live training.
9. Generate a written handover.
10. Provide fourteen days of fixes for configured workflows.

---

## The graph

Each onboarded business becomes a graph node:

```json
{
  "business_id": "DEMO-ELEC-MANCHESTER-001",
  "name": "Fictional Manchester Electrical Co.",
  "vertical": "electrician",
  "postcode": "M1 1AA",
  "region": "Manchester",
  "installed_at": "DEMO-DATE",
  "package": "ai_business_setup",
  "price": 499,
  
  "platforms": {
    "whatsapp_business": {
      "status": "example",
      "phone": "+44 7700 900077",
      "waba_id": "DEMO-WABA-ID"
    },
    "google_business": {
      "status": "pending",
      "location_id": "DEMO-LOCATION-ID",
      "rating": null,
      "reviews": 0
    },
    "facebook": {
      "status": "example",
      "page_id": "demo-manchester-electrical-co"
    },
    "instagram": {
      "status": "example",
      "username": "@demo.manchester.electrical"
    },
    "website": {
      "status": "separate-deliverable",
      "url": "https://example.com/demo-manchester-electrical",
      "ai_chat": false,
      "schema_markup": false,
      "llms_txt": "optional-experiment"
    },
    "voice_agent": {
      "status": "separate-deliverable",
      "phone": "+44 7700 900078",
      "provider": "unselected"
    }
  },
  
  "ai_optimization": {
    "robots_txt": "optional-experiment",
    "schema_markup": false,
    "llms_txt": "optional-experiment",
    "bing_submitted": false,
    "google_crawlable": "unverified",
    "chatgpt_crawlable": "not-guaranteed"
  },
  
  "lead_generation": {
    "weekly_alerts": false,
    "planning_apps": false,
    "procurement": false
  }
}
```

---

## Customer transparency

Customers receive the implementation state, account ownership, evidence, pending approvals, supplier charges, and revocation instructions in the written handover.

They do not need a line-by-line technical tutorial, but nothing material is concealed:

- Which accounts were configured and who owns them
- Which permissions AI Onboard received and how to revoke them
- Which steps are manual, pending, blocked, or experimentally supported
- Which supplier subscriptions remain the customer’s responsibility

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

### Pilot setup

| Service | Price | Current status |
|---------|-------|----------------|
| Standard AI Setup | £499 | Pilot manual installation described in `OFFER.md` |
| Website development | Separate quote | Separate deliverable |
| Live voice service | Separate quote plus customer-paid telephony/model/monitoring costs | Separate deliverable |
| Meta production integration | Separate quote plus customer-paid Meta charges | Blocked/approval required |
| Custom integrations | Separate quote | Separate deliverable |
| Lead generation | Separate future offering | Not included in pilot |

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
