# AUTOMATION_PLAYBOOK.md

> Pilot installation process. Customer-led at every step; trust guarantees in `TRUST_MODEL.md`.

Current canonical offer: `OFFER.md`. This file describes the general process for each area — what the customer does, what we do, and how it stays secure — not exact API automation.

## Process cards

Each card follows the same shape: goal, customer action, our action, what we see, what we never touch, how to revoke, and what happens if blocked.

### 1. WhatsApp Business (free app)

**Goal:** Professional presence, quick replies, labels, greeting and away messages.

- **Customer does:** Installs the free WhatsApp Business app, verifies their own number, completes the business profile.
- **We do:** Guide the setup over screen share; draft quick replies and greeting text for approval; verify the profile together.
- **What we see:** Screenshots the customer shares; message templates they approve.
- **What we never touch:** Their phone, their SIM, their personal chats, their password.
- **How to revoke:** Uninstall the app or remove our guidance access; nothing of ours remains.
- **If blocked:** Fall back to SMS templates and a documented manual routine.

Production Cloud API integration is a separate deliverable with separate Meta charges.

### 2. Google Business Profile

**Goal:** Complete, accurate listing the customer owns.

- **Customer does:** Claims or creates the listing in their own Google account; completes verification when Google offers a method.
- **We do:** Prepare categories, services, hours, and description text; guide field-by-field entry; track verification as pending until Google confirms.
- **What we see:** Screenshots and the public listing.
- **What we never touch:** Their Google password; we never claim ownership.
- **How to revoke:** Remove any granted manager role in Google Business settings.
- **If blocked:** Record `blocked` with Google's stated reason; verification is never marked complete on our word alone.
- **Service-area note:** Mobile trades list service areas, not home addresses.

### 3. Booking platform (Booksy, Fresha, Square, or existing)

**Goal:** Deposits, reminders, and booking links working in the tool they already use.

- **Customer does:** Logs in themselves; enables deposit and reminder settings we recommend; confirms the booking link.
- **We do:** Prepare the exact settings to change; verify the public booking link resolves with correct services; document refund and cancellation rules.
- **What we see:** Settings screens they share; the public booking page.
- **What we never touch:** Their login, their customer list exports beyond what they explicitly share, their payout settings.
- **How to revoke:** Change nothing — we never held access. Disable any reminder we configured, in their own dashboard.
- **If blocked:** Documented manual routine (e.g. card-on-file at first visit, manual confirmation messages).

### 4. Search and AI-readability

**Goal:** Accurate, accessible public information. No ranking or recommendation guarantees.

- **Customer does:** Approves business description, services, prices, and photos.
- **We do:** Add structured data where they own the website; check consistent name/address/phone across listings; submit sitemap to Bing Webmaster Tools on request.
- **What we see:** Public pages only.
- **What we never touch:** Anything requiring guarantees. `llms.txt` is an optional experiment.
- **If blocked:** Ship without it; record as pending, not failed.

### 5. Website with AI chat (separate deliverable)

Not in either pilot package. Quoted separately with customer-paid hosting, domains, and model usage.

### 6. Voice agent (separate deliverable)

Not in either pilot package. Quoted separately with customer-paid telephony, compute, and monitoring. Multi-language support is configured per customer, never assumed.

---

## Pilot installation checklist

The standard pilot is manual-first:

1. Record discovery answers and customer authorizations.
2. Configure only the customer-authorized existing email and calendar workflows.
3. Prepare one enquiry-capture workflow using customer-approved contact details.
4. Draft one quotation from the customer-approved price book.
5. Require owner approval before any outbound send.
6. Assist with Google Business Profile through Google's ordinary interface.
7. Record verification as pending until Google confirms it.
8. Conduct live training.
9. Generate a written handover.
10. Provide fixes within the support window (14 days standard, 7 days quickstart).

---

## The graph

Each onboarded business becomes a graph node (fictional example):

```json
{
  "business_id": "DEMO-ELEC-MANCHESTER-001",
  "name": "Fictional Manchester Electrical Co.",
  "vertical": "electrician",
  "postcode": "M1 1AA",
  "installed_at": "DEMO-DATE",
  "package": "muse-quickstart",
  "price": 20,

  "platforms": {
    "whatsapp_business": {"status": "configured-in-customer-app"},
    "google_business": {"status": "pending"},
    "booking_platform": {"status": "configured", "provider": "customer-owned"},
    "website": {"status": "separate-deliverable"},
    "voice_agent": {"status": "separate-deliverable"}
  },

  "trust": {
    "passwords_held": 0,
    "payment_capability_connected": false,
    "outbound_requires_approval": true,
    "revocation_documented": true
  }
}
```

---

## Customer transparency

Customers receive the implementation state, account ownership, evidence, pending approvals, supplier charges, and revocation instructions in the written handover:

- Which accounts were configured and who owns them
- Which permissions AI Onboard received and how to revoke them
- Which steps are manual, pending, blocked, or experimentally supported
- Which supplier subscriptions remain the customer's responsibility

---

## Revenue model

| Service | Price | Current status |
|---------|-------|----------------|
| Basic Onboarding | £20 one-off | Pilot manual installation per `OFFER.md` |
| Add-ons | £5-10 each | Per `ADDONS.md` |
| Integrated Package | £50/month | Monitoring, support, consulting |
| Website development | Separate quote | Separate deliverable |
| Live voice service | Separate quote plus customer-paid costs | Separate deliverable |
| Meta production integration | Separate quote plus customer-paid Meta charges | Blocked/approval required |
| Custom integrations | Separate quote | Separate deliverable |
| Lead generation | Separate future offering | Not included in pilot |

**One fee per package. No subscription. No bullshit.**

> "We set you up, teach you how to use it, and leave. If you need more later, we're here."

---

## Next steps

1. Validate one manual electrician installation.
2. Validate one £20 nail-tech quickstart and measure support minutes.
3. Promote one manual step to verified automation only with customer evidence.
4. Deliver 3 founding-client installations.
5. Refine from measured results, not assumptions.
