# Cloudflare onboarding — runbook

> Goal: every customer domain managed from one place (DNS, bots, access),
> ownership always with the customer. Status: tracker shipped
> (`aionboard/cloudflare.py`); live API provisioning needs a token model
> decision (below).

## What we manage vs what they own

| Item | Owner | Us |
|------|-------|----|
| Domain registration | Customer, always | Never transfer to us |
| DNS records | Customer delegates (Cloudflare partner / scoped token) | Manage day-to-day |
| Turnstile widgets | Us (per-environment) | Create, monitor |
| Access rules | Us | Configure, review quarterly |
| Analytics | Us reads, customer sees | Weekly summary option |

Revocation: customer removes our access in Cloudflare dashboard or tells
us; we confirm removal within 1 business day and hand over a records
export. Tracked as a support task, not a handshake promise.

## Per-business steps (tracked in cloudflare.py)

1. **dns** — domain delegated or scoped token issued. Verify with a
   TXT record the customer adds (proves control).
2. **turnstile** — widgets for enquiry/booking forms (see aocsec
   docs/form-defense.md). Verify a challenge blocks a test bot POST.
3. **access_rules** — WAF basics, bot fight mode per plan, no
   over-blocking (test the booking flow after enabling).
4. **analytics** — weekly visits/chats summary wired to the customer
   dashboard. Read-only.

## Token model (decision needed before live provisioning)

- Option A: customer-scoped API tokens per business (most isolated,
  most setup friction).
- Option B: our partner token with per-customer audit scope (simplest,
  concentrates risk — requires the audit log to be airtight).
- Recommendation: A for paying customers, B never without written
  consent + IP-allowlisted token + expiry.

Until decided: tracker runs in planning mode (records intent and
manual actions). No code path provisions anything automatically.
