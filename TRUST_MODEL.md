# TRUST_MODEL.md

> Why a customer can let us in without handing over the keys.

## The core promise

The customer keeps their accounts, their passwords, and their money. We configure, guide, and verify — we never take control.

## The five guarantees

### 1. No passwords, ever

- The customer logs in themselves, on their own device, or shares their screen.
- Where OAuth exists, they grant scoped access and can revoke it in one click.
- Where no OAuth exists, they perform the clicks while we guide.
- We never ask for, receive, or store passwords.

### 2. No money movement

- No payment capability is ever connected.
- Quotes are drafts until the owner taps approve.
- Invoices are prepared, never sent, never paid by us.
- Deposits, refunds, and payment links are configured in the customer's own accounts.

### 3. No silent sends

- Every outbound message — quote, booking, reminder, review request — needs explicit owner approval first.
- Approval is bound to the exact content: a changed quote invalidates the approval.
- The customer can see everything queued before anything goes out.

### 4. Revocable everything

- Every grant lists how to revoke it.
- The written handover includes step-by-step revocation for each connected app.
- Revocation takes effect immediately; no call, no notice period, no retention.

### 5. Minimal data

- We record configuration and evidence, not customer conversations.
- Allergy records, key codes, alarm details, and full customer databases stay in the customer's own systems.
- Support uses fictional test records and short diagnostic descriptions, never inbox copies.

## What we see vs what we never see

| We see (with permission) | We never see |
|--------------------------|--------------|
| Booking settings screens | Passwords |
| Service menus and prices | Bank credentials |
| Public business profiles | Full customer databases |
| Approval receipts | Payment instruments |
| Diagnostic descriptions | Raw inbox contents |

## If something goes wrong

1. The customer revokes access (documented in handover).
2. We confirm deletion of our configuration copies.
3. The incident is logged with scope and time window.
4. No customer data is needed to fix our side — configuration is reproducible from the handover.
