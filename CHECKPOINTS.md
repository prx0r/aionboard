# CHECKPOINTS.md

> What "done" means at each stage. Checkpoint 1 is the pilot. Checkpoint 2 is retention.

## Checkpoint 1: narrow pilot install (current)

**Goal:** One verified paying installation, delivered manually, with evidence.

**In scope:**
- Standard £499 setup per `OFFER.md`
- Existing-stack capture (integrate/import, never replace unnecessarily)
- Owner approval before every outbound action
- Written handover with working/pending/blocked items
- 14 days of fixes

**Evidence required:**
- Completed install checklist (all required tasks `verified`)
- Handover document with revocation instructions
- Measured delivery hours
- Customer permission before any case study

**Explicitly out of scope:**
- Live voice service
- Meta/WhatsApp production integration
- Website builds
- Custom integrations
- Lead generation
- Ongoing subscriptions

**Status:** 0 completed installations. All integration pipeline steps are `manual`.

## Checkpoint 2: retention wedge (future)

**Goal:** Give customers a reason to stay after setup.

**Candidates (all unbuilt, all require separate consent and pricing):**
- Opportunity alerts (planning apps, procurement, labour demand from powuk)
- Group-message broadcasts via approved channels (opt-in lists only)
- Scheduled check-in calls
- Review and rebooking automation
- Custom integrations

**Gates before building any of these:**
1. Checkpoint 1 complete with measured delivery time
2. Customer explicitly opts in (separate agreement, separate price)
3. Supplier access, verification, and payment terms established
4. Approval and audit model extended to the new channel
5. No customer PII flows into POW without explicit opt-in

## What "automated onboarding pipeline" means here

Today the pipeline is **manual steps tracked by code**: the install state machine records owner, authorization, action, verification, and evidence per task. Automation means replacing individual manual steps with verified integrations — one tool, one vertical, one evidence trail at a time. No step is marked `automated` until it has run successfully for a real customer.
