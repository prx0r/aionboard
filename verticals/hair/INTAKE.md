# Hairdresser intake form

> The entry point. If we can't define intake as a form, the unit isn't clear enough.

## The form (5 fields)

```
1. Business name + postcode
2. Phone number + email
3. Services offered (checkboxes)
4. Current booking method
5. Upload your price book (photo or PDF)
```

### Field 1: Business name + postcode

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Business name | text | yes | As the customer wants it displayed |
| Postcode | text | yes | Used for service-area matching and geographic intel |

### Field 2: Phone number + email

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Phone | phone | yes | Primary contact; must be TPS-screened before any outbound call |
| Email | email | yes | For handover, support, and booking confirmations |

### Field 3: Services offered

Checkboxes. Customer ticks what they do:

- [ ] Haircut (wash & cut)
- [ ] Haircut (dry cut)
- [ ] Blow-dry
- [ ] Blow-dry & style
- [ ] Hair colour (full)
- [ ] Hair colour (roots only)
- [ ] Highlights / balayage / ombre
- [ ] Toner / gloss
- [ ] Bleach
- [ ] Perm / relaxer
- [ ] Braids (box braids)
- [ ] Braids (cornrows / feed-in)
- [ ] Braids (other — text field)
- [ ] Extensions (weave)
- [ ] Extensions (micro-ring / fusion)
- [ ] Deep conditioning / treatment
- [ ] Hair-up / occasion styling
- [ ] Men's cut
- [ ] Children's cut
- [ ] Other (text field)

**Why this matters:** The AI only references services the customer actually offers. Never promise a service that isn't in this list. The rulebook (RULEBOOK.md #9) says: "Price quote doesn't match actual service" — this field prevents it.

### Field 4: Current booking method

Dropdown or radio:

- Booksy
- Fresha
- Square Appointments
- Mangomint
- Google Calendar
- Instagram DMs only
- WhatsApp only
- Phone calls only
- Mix of the above (text field: "which ones?")
- Nothing — I manage manually

**Why this matters:** This determines the onboarding recipe. Booksy user gets deposit + reminder setup. WhatsApp-only user gets quick-reply + booking-link setup. The onboarding engine (onboarding.py) uses this to select tasks.

### Field 5: Upload your price book

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Price book | file (image or PDF) | yes | Photo of printed price list, screenshot of digital prices, or PDF |

**Why this matters:** The AI quotes from the customer's own prices. Never invent prices. The rulebook (RULEBOOK.md #36) says: "Price book outdated" — this field plus monthly verification prevents it.

If the customer doesn't have a price book, stop. Help them create one first. The onboarding cannot proceed without approved prices.

---

## What happens after intake

1. **Import to CRM** (`crm.py`): business name, postcode, phone, email, services, booking tool. Provenance: intake-form.
2. **Select recipe** (`onboarding.py`): booking tool → which tasks apply.
3. **Generate quote draft** from uploaded price book. Owner approves before any send.
4. **Schedule onboarding session** (1 hour, live training + setup).

## Intake rules

- No passwords collected at intake. Ever.
- No payment taken at intake. Payment is after onboarding session.
- Customer can withdraw at any point. Data deleted per DATA_POLICY.md.
- All data is customer-owned. We are processor, not controller, for their client data.

### Optional: Add-ons interested in

- [ ] Website + AI Chatbot (£199)
- [ ] Google Business Profile Optimisation (£99)
- [ ] AI Visibility Package (£149)
- [ ] Social Media Bio Optimisation (£49)
- [ ] Full Digital Footprint Audit (£79)
- [ ] Not sure — include in consultation
