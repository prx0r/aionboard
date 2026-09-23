# AI Onboard — UK competitive research and full development brief

Research and repository review: 23 September 2026

The opportunity is not to invent business software for nail technicians, cleaners or tradespeople. It is to make the software they already have genuinely usable through an AI assistant, configure it securely, and teach them how to operate it for a small one-off fee.

The competitive research makes the £20 offer more compelling as an installation and education service, but less compelling as a custom integration service. Established platforms already provide booking, reminders, deposits and client management. You need to configure these capabilities, not reproduce them.

There is one immediate constraint: Meta's official September 8 announcement describes Muse as rolling out in the US, and its connector platform requires functional, security and legal review. Don't market unrestricted UK access or universal app integration until those are actually available. Build the same onboarding workflow so it can operate with Muse when eligible, with a clearly identified alternative or waiting-list option beforehand.

![](https://www.google.com/s2/favicons?domain=https://about.fb.com&sz=32)

about.fb.com

+1

## 1. What you're competing against

|
Competitor

|

Verified offering

|

Implication for AI Onboard

|
| --- | --- | --- |
|

Square Appointments

|

UK free plan with booking site, automated reminders and payments

|

Don't rebuild bookings; configure a customer's account.

|
|

Booksy

|

£40/month plus VAT in the UK, with booking, marketing, client management and payments

|

Sell assisted setup of existing features, not generic booking automation.

|
|

Fresha

|

Booking, deposits, client records, reminders, marketplace discovery and existing social integrations

|

Be platform-neutral; don't force a migration.

|
|

Manychat

|

Free limited social automation; paid plans with additional channels and AI features

|

Its AI messaging overlaps heavily with a future advanced onboarding offer.

|
|

ZenMaid

|

Scheduling, automated communication, invoicing and payments

|

Configure workflows for cleaners already using it.

|
|

CleanerPlanner

|

UK round-management software from £19/month

|

Window cleaners with established rounds may already have most of the necessary functionality.

|

The vendor pages confirm that Square's free UK tier includes automatic email and text reminders; Booksy includes unlimited bookings and marketing tools; and Manychat's free tier permits two eligible social channels and four active automations, but not WhatsApp. CleanerPlanner's £19/month entry tier already provides unlimited rounds and jobs.

![](https://www.google.com/s2/favicons?domain=https://squareup.com&sz=32)

Square Appointments

+5

The service you're building is therefore a cross-platform onboarding, security and AI-training layer, rather than a competitor to those providers. That is also the correct architecture for your longer-term opportunity network: the customer continues using their familiar systems, while AI Onboard understands which capabilities they have and which POW services might subsequently be useful.


### The most relevant new development: Meta has its own WhatsApp setup tools

Meta is introducing a WhatsApp Business Tools MCP that lets supported AI coding agents assist with setting up business accounts, numbers, message templates and test messaging. It is rolling out gradually and is currently aimed at development and testing. This could remove considerable work from your eventual advanced WhatsApp installations. It does not mean every customer can already connect their personal Muse to every WhatsApp Business feature.

![](https://www.google.com/s2/favicons?domain=https://developers.meta.com&sz=32)

Meta for Developers

+1

There are two other competitors worth designing around: Manychat's current paid plans start at $14/month for expanded social automation and $29/month for Pro with WhatsApp and AI features, while ZenMaid has a $19/month entry plan for cleaners. Neither prevents you from selling a £20 one-time configuration, but both make it important to disclose when your proposed workflow would require paid software.

![](https://www.google.com/s2/favicons?domain=https://manychat.com&sz=32)

manychat.com

+1

One important UK demand indicator: the government's 2025 estimate identified approximately 3.2 million sole proprietorships, which underlines why a Companies House-only acquisition system would miss so many potential customers.

![](https://www.google.com/s2/favicons?domain=https://www.gov.uk&sz=32)

GOV.UK


## 2. Detailed onboarding specification for the five launch markets

The five campaigns can share three technical workflows: appointment-based businesses, recurring local services and quotation-based mobile services. Each business gets a different discovery questionnaire and manual, but the underlying engine stays the same.

### A. Nail technicians and lash artists

First pilot template

Existing competition: Square, Booksy, Fresha and Manychat. Booksy already offers automated return-visit reminders and free bookings through a customer's own booking link. Fresha already handles appointments, deposits and client information. There is no reason for your £20 service to duplicate those capabilities.

![](https://www.google.com/s2/favicons?domain=https://biz.booksy.com&sz=32)

Get more visibility and more bookings

+1

Customer discovery: Ask which booking platform they use, where enquiries arrive, their services and prices, typical appointment duration, deposit and cancellation policies, and whether they maintain separate personal and business accounts.

Installation procedure:

1. Check Muse eligibility and identify which connections are actually available on that customer's account.

2. Have the customer sign in to their existing booking platform. If they have none, offer to configure a free or low-cost option, showing the supplier's charges first.

3. Verify their public booking link, business hours, service menu, appointment durations, buffer times and approved deposit policy.

4. Add the booking link to their Instagram or TikTok profile where supported.

5. Configure WhatsApp Business quick replies and an appropriate away message. This is manual app configuration unless an approved integration genuinely supports it.

6. Create a small business-knowledge pack containing public services, prices, hours, booking instructions and the owner's preferred communication style.

7. Teach the assistant to draft replies, prepare content and help review the diary, without giving it blanket access to customer conversations.

Acceptance test: A fictional customer asks about an infill appointment. The system produces the correct price and booking instructions without inventing availability, changing a deposit or sending an unapproved message.

Industry-specific safety: Beauty products can present chemical and respiratory hazards, and some treatments may require local authority premises licensing. The owner remains responsible for relevant treatment checks and safety procedures. Do not let an AI agent make allergy or treatment-suitability decisions.

![](https://www.google.com/s2/favicons?domain=https://www.gov.uk&sz=32)

GOV.UK

+1

Health information, including some allergy and treatment records, may be special-category personal data. Keep it inside the customer's appropriate treatment-management system. Do not put it in a general-purpose Muse instruction pack or routinely transmit it to AI Onboard.

![](https://www.google.com/s2/favicons?domain=https://ico.org.uk&sz=32)

ICO

+1

### B. Mobile hairdressers and braiders

Appointment template with travel

These customers resemble nail technicians but need more careful handling of service locations, travel charges, preparation times and appointment lengths.

The installation should capture service areas, accepted travel distances, minimum appointment values, travel fees and the owner's actual treatment menu. Connect an existing booking tool where available, create approved replies for common Instagram and WhatsApp questions, and teach the assistant how to prepare estimates without promising a final price.

A useful manual prompt is: “Help me prepare a response to this bridal-hair enquiry using my approved price list, travel area and availability. Ask me to approve the final quotation.”

Acceptance test: A fictional customer requests an appointment outside the usual travel area. The workflow identifies the exception and asks the business owner to confirm travel availability and charges.

Do not automate chemical-treatment suitability or patch-test decisions. HSE guidance identifies dermatitis and respiratory risks associated with common hairdressing substances. The onboarding pack can remind the owner to follow their established safety procedures; it should not attempt to certify that those procedures have been followed.

![](https://www.google.com/s2/favicons?domain=https://www.hse.gov.uk&sz=32)

COSHH

### C. Domestic cleaners

Recurring-service template

Existing competition: ZenMaid and other specialist cleaning platforms already handle recurring bookings, automated messages and payments. ZenMaid's published entry plan is $19/month, with charges in US dollars.

![](https://www.google.com/s2/favicons?domain=https://get.zenmaid.com&sz=32)

get.zenmaid.com

Customer discovery: Establish whether the business is a solo cleaner or employs staff, which towns it serves, whether appointments are weekly or fortnightly, how quotations are calculated, and which scheduling and payment systems are already in use.

The £20 installation should concentrate on an approved service menu, a repeat-booking workflow and consistent enquiry handling. Configure the customer's current calendar or cleaning application. If they use WhatsApp informally, prepare quick replies for availability, first-clean enquiries and rescheduling.

Keep client addresses, keys, alarm instructions and property-access details outside the general AI knowledge pack. These are operationally sensitive even where they do not fall into a special data category.

Acceptance test: The owner demonstrates scheduling a fictional fortnightly clean, skipping one occurrence and drafting an appropriate customer notification without accidentally cancelling the whole recurring arrangement.

Advanced installation: Staff scheduling, access instructions, recurring payments and automatic customer communications need more granular permissions. They should not be included indiscriminately in a £20 setup.

### D. Mobile car detailers

Quotation-based mobile template

Car detailing is a good fit for a simple enquiry workflow because customers frequently need to communicate vehicle information, service requirements and location before receiving a quote. Existing detailing businesses already use platforms such as Fresha for mobile-service bookings, so start with the customer's actual tools rather than prescribing a new one.

![](https://www.google.com/s2/favicons?domain=https://www.fresha.com&sz=32)

Fresha

Capture approved service packages, vehicle-size categories, travel area, minimum prices, working hours and weather-related scheduling restrictions. Set up a structured enquiry template asking about the vehicle, requested service, location and relevant photographs.

Muse can help organise this information and prepare a quotation for approval. It must not independently assess paint condition, guarantee restoration outcomes or promise a price unsupported by the owner's assessment.

Acceptance test: A customer requests a ceramic-coating service but hasn't provided enough condition information. The assistant asks for the missing information rather than issuing a final quote.

Add a practical compliance reminder for mobile washing. Government pollution guidance requires businesses to prevent contaminated wastewater from entering surface-water drains; acceptable disposal arrangements depend on the circumstances and may require permission from the relevant water company. This is a checklist for the operator, not something the assistant can verify remotely.

![](https://www.google.com/s2/favicons?domain=https://www.gov.uk&sz=32)

GOV.UK

### E. Window cleaners and gardeners

Round-management template

This market has particularly direct follow-on opportunities for POW UK, including commercial property maintenance, public procurement and appropriately matched local work.

Existing competition: CleanerPlanner already provides round management, invoicing and support. Its published UK plans start at £19/month for a single user, while its £29/month plan adds integrations including GoCardless. It also supports importing data from several existing round-management systems.

![](https://www.google.com/s2/favicons?domain=https://www.cleanerplanner.com&sz=32)

cleanerplanner.com

+1

Begin with the simplest possible installation: organise the existing round or repeat-service schedule, prepare enquiry templates, configure approved appointment reminders and create a weekly administrative checklist. If the customer's current software already handles invoicing and collections, leave those functions where they are.

For gardeners, separately capture service types, seasonal availability, green-waste arrangements and travel coverage. Do not treat gardening and window cleaning as interchangeable when generating quotations or assessing operational requirements.

Acceptance test: A fictional customer skips one visit, requests another date and asks about an outstanding invoice. The assistant identifies the relevant record, proposes appropriate updates and requests approval before changing the schedule or sending a payment reminder.

For window cleaning, the assistant must not decide that a job at height is safe. HSE requires appropriate planning, competence and equipment, with avoidance of work at height where reasonably practicable. Gardening businesses transporting waste may also need registration; the rules vary by UK nation and type of waste.

![](https://www.google.com/s2/favicons?domain=https://www.hse.gov.uk&sz=32)

HSE

+1

## 3. Shared UK security and legal requirements

These are launch requirements, not optional improvements to make after the first substantial customer-data import.

|
Area

|

Requirement

|

Engineering implementation

|
| --- | --- | --- |
|

Customer ownership

|

The customer owns and controls their accounts.

|

Delegated access, explicit scopes, revocation instructions and no shared master login.

|
|

Data protection

|

Distinguish your purposes from processing carried out on clients' instructions.

|

Separate CRM and client-workflow data, appropriate contracts and processing records.

|
|

Marketing

|

A customer purchasing onboarding hasn't automatically consented to later sales messages.

|

Channel-specific preferences, source records and suppression enforcement.

|
|

AI access

|

Muse can only operate through capabilities genuinely available to that customer.

|

Tested capability registry and least-privilege permissions.

|
|

Consequential actions

|

Quotes, financial actions and sensitive communications require appropriate controls.

|

Exact-action approvals, audit receipts and configurable automation limits.

|
|

Security operations

|

Protect information during storage, backup, support and deletion.

|

Encrypted storage, access controls, incident response and tested restoration.

|

### Controller and processor separation

AI Onboard is likely to act as a controller for its own customer relationships, billing and legitimate business-development records. When processing a client's end-customer information solely to configure and operate that client's systems, it may act as a processor. The exact role depends on who determines the processing purposes and means.

Where AI Onboard is a processor, use a written agreement covering documented instructions, security, sub-processors, confidentiality, assistance with individual rights, breaches and deletion or return of data. The ICO sets out these contractual requirements under Article 28.

![](https://www.google.com/s2/favicons?domain=https://ico.org.uk&sz=32)

ICO

+1

Do not quietly reuse a client's appointment history or customer messages for POW intelligence. Ask separately for any proposed use of customer-specific business outcomes, define exactly what may be shared, and prefer aggregate or genuinely anonymised findings where sufficient.

### Marketing permission

This matters particularly for the sole-trader strategy. Under PECR, sole traders and certain partnerships are individual subscribers. Unsolicited promotional emails, WhatsApp messages and social-media DMs generally require consent unless an applicable exception, such as a valid soft opt-in, is established. Corporate-subscriber marketing has different PECR rules, but UK GDPR can still apply to named contacts.

![](https://www.google.com/s2/favicons?domain=https://ico.org.uk&sz=32)

ICO

+1

Implement separate choices for essential service messages, seven-day support, optional product updates and paid opportunity alerts. No pre-ticked marketing boxes and no automatic inclusion in a POW mailing list.

### Financial integration

The £20 service should start by helping customers use their existing invoicing or accounting application. For the initial version, restrict AI access to appropriately minimised information and prepare drafts or summaries for human review.

Do not directly aggregate bank accounts or initiate payments as an unregulated service. The FCA regulates account-information and payment-initiation services; use an appropriately authorised provider where those capabilities are required.

![](https://www.google.com/s2/favicons?domain=https://www.fca.org.uk&sz=32)

FCA

For sole traders, the relevant Making Tax Digital qualifying-income thresholds are more than £50,000 from April 2026, more than £30,000 from April 2027 and more than £20,000 from April 2028. Qualifying income is gross self-employment and property income before expenses. Muse is not a substitute for compatible MTD software.

![](https://www.google.com/s2/favicons?domain=https://www.gov.uk&sz=32)

GOV.UK

+1

The standard UK VAT-registration threshold is £90,000 of taxable turnover over a rolling 12 months. Non-established businesses supplying the UK can have different registration obligations, so review AI Onboard's own establishment and VAT position before taking payments at scale.

![](https://www.google.com/s2/favicons?domain=https://www.gov.uk&sz=32)

GOV.UK

### International access and incident response

Because your implementation work may be carried out outside the UK, document where each customer's information is hosted and who can access it. The ICO explains that making personal data accessible to a separate overseas organisation can constitute a restricted transfer, whereas access by an employee of the same legal entity is treated differently. Establish the actual legal and contractual arrangement before handling live records.

![](https://www.google.com/s2/favicons?domain=https://ico.org.uk&sz=32)

ICO

+1

Correct the current repository's breach policy. A processor must inform its controller without undue delay. A controller must assess whether a breach is reportable to the ICO, generally within 72 hours of awareness where the notification threshold is met, and inform affected people without undue delay where the risk is high. Document every breach, including those not requiring external notification.

![](https://www.google.com/s2/favicons?domain=https://ico.org.uk&sz=32)

ICO

For remote £20 setups, keep live customer data out of your support recordings by default. Prefer customer-controlled login and screen-sharing workflows, fictional test records and temporary delegated access over taking permanent copies of entire inboxes.

## 4. Complete development instructions for `prx0r/aionboard`

Repository baseline reviewed: [7151634](https://github.com/prx0r/aionboard/commit/7151634e4be62a1e4bc1200facfeb510947b0722) . The current README reports 32 tests, but the integration pipelines are explicitly manual and no paying installation is recorded.

### Checkpoint A — Establish the new product contract

Retain `standard-ai-setup` at £499 for bespoke electrician installations and more complex businesses. Introduce `muse-quickstart` as a separate £20 package, with seven days of support and strictly limited technical scope.

Define successful Quickstart delivery as one agreed workflow being configured and demonstrated, an accurate personalised manual being supplied, and the customer understanding what they have connected. Do not make a universal live AI receptionist, website build, accounting migration or WhatsApp Cloud API deployment part of £20.

Make the contract explicit about the included support allowance. Unlimited automated help can be offered with sensible abuse limits, while human calls should have a documented allowance and a separate escalation path for a failure of the agreed installation. Measure delivery and support before expanding the allowance.

Update `OFFER.md`, `CHECKPOINTS.md`, the public website and every affected vertical manifest from one canonical package definition. Older £249–£349 niche pricing hypotheses should not accidentally appear as live checkout prices.

### Checkpoint B — Replace the company-only CRM identity

Your `crm.py` currently requires `company_number` for every prospect. Introduce a stable internal `business_id` that supports sole traders, partnerships and incorporated businesses. A Companies House number should be an optional external identifier, not the primary key.

Implement distinct records for business identity, owner contacts, existing software, authorised integrations, installations, support cases, marketing preferences and opportunity subscriptions.

A proposed core customer record:

JSON

```
{
  "business_id": "generated-uuid",
  "legal_form": "sole_trader",
  "company_number": null,
  "vertical": "nails",
  "trading_name": "Example Nails",
  "operating_region": "Greater Manchester",
  "service_areas": [],
  "existing_stack": [],
  "package": "muse-quickstart",
  "marketing_preferences": {
    "service_messages": true,
    "email_marketing": false,
    "whatsapp_marketing": false,
    "pow_opportunities": false
  }
}
```

Treat this as the application's own customer-profile design, not a complete permission or identity-verification record. Record the provenance, time and version of each actual permission separately.

Migrate existing electrical-business prospects without losing their source information or accidentally granting marketing permission.

### Checkpoint C — Build a real app capability registry

Each advertised connection must distinguish the platform's general functionality from what the specific customer can actually use.

A capability record needs the supplier, supported region, eligible account type, required plan, authorised scopes, official connection method, recurring charges, last documentation review and observed installation result.

Use states such as `not_supported`, `eligibility_unknown`, `available`, `authorization_pending`, `connected`, `verified`, `blocked` and `revoked`.

For WhatsApp, distinguish the ordinary WhatsApp Business App, the Cloud API, any supported coexistence arrangement, Meta's new developer MCP and Muse's own approved integrations. These are not the same product. Meta has published a unified onboarding approach for business messaging, but platform eligibility and access still need checking for each intended deployment.

![](https://www.google.com/s2/favicons?domain=https://developers.meta.com&sz=32)

Meta Horizon OS Developers

+1

A customer's inability to connect an app should produce a documented manual route, not an invisible failed automation or a misleading success indicator.

### Checkpoint D — Implement the onboarding engine

Turn the current vertical JSON files into executable installation recipes. Separate shared tasks from package-specific and vertical-specific tasks, rather than expanding the existing electrician checklist indefinitely.

```
Customer selects vertical
  ↓
Package and Muse eligibility checks
  ↓
Customer pays and accepts service terms
  ↓
Capture existing software and business profile
  ↓
Customer authorises eligible connections
  ↓
Generate vertical-specific installation plan
  ↓
Execute supported automated steps
  ↓
Guide customer through unsupported manual steps
  ↓
Run fictional-data acceptance test
  ↓
Generate personalised manual
  ↓
Activate seven-day support
  ↓
Record outcome and optional future-service preferences
```

Each task requires an owner, authorisation method, prerequisites, execution method, verification procedure, evidence, completion state and safe recovery action.

For example, the nail-booking recipe should check whether the approved booking link actually resolves and presents the correct services. A configuration screenshot alone does not prove that a customer can successfully book.

Write Q&A pairs that explain the reasoning behind each procedure, define potentially obscure terms and identify product or legal questions that should be resolved before the project can proceed.

For example, the nail-booking recipe should check whether the approved booking link actually resolves and presents the correct services. A configuration screenshot alone does not prove that a customer can successfully book.

Maintain idempotency so an interrupted setup can be rescheduled without creating duplicate reminders, duplicate business accounts or repeated customer messages.

### Checkpoint E — Establish the security boundary

The current `security.py` contains useful dry-run approval and isolation helpers. It does not yet authenticate real approvers or enforce production tenant isolation.

Before real customer integrations, implement authenticated identities, tenant-scoped database access, scoped delegated credentials, an encrypted secrets store, audit records and short-lived, single-use approvals for consequential actions.

Approval receipts should bind the customer, specific action, target, exact proposed payload, expiry and authenticated approver. Test that a modified quotation or destination invalidates the original approval.

Don't rely on prompt instructions such as “never send messages without asking” as the only control. The backend must independently enforce the rule.

For recurring reminders, the owner may explicitly approve a narrowly defined automation policy rather than approving every identical operational reminder. Promotional broadcasts, changes to payment terms, unusual quotations and other higher-risk actions should require stronger approval.

Review uploaded files, third-party messages and imported text as untrusted material. Prevent instructions inside a customer email or external document from becoming tool-execution instructions.

### Checkpoint F — Fix persistence and backups

SQLite is acceptable for a single-operator pilot, but the current schema and storage checks are not sufficient evidence of safe multi-tenant production operation.

Make the customer boundary enforceable in storage and application queries. Once multiple operators or a remote customer-facing MCP gateway are involved, introduce the necessary production database access controls.

Replace direct SQLite file copies with its online backup API. Run integrity checks, encrypt backups and test restoring them. SHA-256 checksums provide integrity verification, not encryption.

Design deletion and export procedures that address the operational database, object storage, backups and connected third-party accounts. Suppression records may need limited retention to prevent further unwanted marketing, but don't describe every suppression record as automatically requiring indefinite retention regardless of circumstances.

### Checkpoint G — Generate the customer manual and prompt pack

This should be the most polished output of the entire £20 experience.

Extend `handover.py` to produce a plain-English customer pack containing the business's verified configuration, working and unsupported capabilities, account ownership, relevant supplier charges, safe operating instructions and troubleshooting steps.

Generate separate reusable prompts for the customer's selected workflow. A nail technician gets booking and social-content prompts; a cleaner gets recurring-appointment and administrative prompts; a car detailer gets enquiry and quotation-preparation prompts.

Every prompt should be written against the customer's actual confirmed capabilities. If the assistant cannot read Booksy appointments, its instructions must not imply that it can.

The handover must never include passwords, tokens, unnecessary end-customer information or unsupported guarantees about what Muse can do. Offer a non-sensitive version that customers can upload to an assistant and a private account-and-permissions record kept separately.

### Checkpoint H — Build the seven-day support engine

Create support cases linked to the installation, capability and attempted task. Let the customer ask unlimited reasonable questions through the automated guide during the seven-day period, escalating failures or situations that cannot be resolved safely.

Capture issue categories, relevant error codes, resolution, time spent, whether a human intervened and whether a reusable onboarding improvement was identified. Avoid retaining complete sensitive chats where a short diagnostic description is sufficient.

The goal is to discover which manual steps can safely become automated. A recurring support question is a signal to improve the recipe, not evidence that you should build an entirely new application.

### Checkpoint I — Implement compliance as data, not scattered prose

Create a versioned compliance-rules registry. Each rule needs jurisdiction, industry, source URL, review date, applicability conditions, required owner action and escalation guidance.

For example, beauty packs should link to the relevant HSE information and local council licensing checks; window cleaning packs should include work-at-height safety reminders; and mobile detailing should include the relevant pollution-prevention guidance.

These are reminders for the responsible business operator. Do not have AI Onboard issue legal certification, determine technical competence or automatically represent that a customer's business meets requirements it has not verified.

Create a separate legal-review queue for activities that materially increase risk: storing allergy records, importing complete customer databases, accessing bank accounts, initiating payments, recording calls or deploying autonomous customer-facing voice agents.

### Checkpoint J — End-to-end acceptance tests

The next milestone is not another passing schema-validation test. It is five repeatable fictional installations followed by a tightly controlled real-customer pilot.

|
Test

|

Required evidence

|
| --- | --- | --- |
|

Sole trader without company number

|

Can purchase, onboard and receive a manual

|
|

Existing Booksy customer

|

No unnecessary migration; correct link and service-menu verification

|
|

Unsupported Muse connector

|

Marked unsupported; honest manual alternative supplied

|
|

Failed authorisation

|

No false success, no credential leakage and safe recovery

|
|

Different customer tenants

|

Cross-customer reads and writes denied

|
|

Modified quotation

|

Existing action approval rejected

|
|

Financial workflow

|

Draft or approved operation only; no unauthorised payment

|
|

Marketing refusal

|

Doesn't affect onboarding or future service eligibility

|
|

Data export and revocation

|

Customer can retrieve their information and remove access

|
|

Interrupted setup

|

Resumes without duplicate external actions

|
|

Backup restoration

|

Consistent restored records and successful integrity check

|
|

Seven-day support

|

Appropriate escalation, closure and retention behaviour

|

Retain the existing unit tests and CI, but add integration tests against documented vendor test environments where available. Use fictional customer information for automated tests. A real-world platform feature must not be promoted from manual to verified automation solely because a mock test passed.

## 5. Commercial deployment checkpoints

Checkpoint 1

## Five verified fictional installs

One representative for each launch market. Produce a valid manual and fully tested workflow for each, with no live customer data.

Checkpoint 2

## Five to ten paying pilot customers

Record actual setup duration, support usage, failed connections, customer comprehension, refunds and operating costs. Use assisted rather than fully autonomous delivery initially.

Checkpoint 3

## Automate only repeated successes

Convert successful, documented manual procedures into verified automation one capability at a time. Don't automate a workflow that still regularly needs human diagnosis.

Checkpoint 4

## Launch optional POW opportunities

Offer relevant local opportunities to customers who explicitly opt in. Charge separately only after proving the alerts are useful and sufficiently accurate.

At £20, the business depends on low delivery costs and minimal support escalation. Don't assume that later upsells will subsidise a loss-making acquisition process before customers demonstrate any interest in buying them. Measure the standalone economics as well as subsequent revenue.

The latest repository's `CHECKPOINTS.md` correctly distinguishes the first verified paying installation from later retention services. Keep that discipline as you introduce Quickstart. The new £20 product is a promising distribution strategy, but its first defensible achievement will be a repeatable, secure installation that a nontechnical customer can use independently.
