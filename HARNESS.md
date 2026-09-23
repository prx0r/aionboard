# HARNESS.md

> How AI Onboard reuses the pi harness and dashboard pattern — and where the onboard buddy sits next to Muse.

## The reused pattern (from influence)

Three ideas, copied deliberately:

1. **Per-business kernel.** Influence keeps one YAML per business driving voice + tradie state. We keep one graph per business: vertical pack + configured stack + install state (`build_business_graph()`).
2. **Read-only tools, gated writes.** Influence's MCP surface can never spend, send, or mutate; writes stay behind a decide gate. Our `mcp/tools.json` copies the contract: 5 read tools, 4 approval-gated writes.
3. **Autonomy levels + retention.** Influence defaults to observe, escalates to semi/full auto, sweeps transcripts quarterly. Our install states (`not_started` → `verified`) and 90-day transcript default follow the same discipline.

What we don't copy: influence's known approval-path gaps. Our approvals are customer-bound, payload-hashed, expiring, and one-time-use from day one.

## The onboard buddy

Every installed business gets a free buddy: an assistant scoped to exactly one business graph.

```
Customer question
        ↓
buddy_ask(business_graph, question)
        ↓
Vertical pains + stack + install state (this business only)
        ↓
Cited answer or honest ignorance
```

Rules the buddy follows:

- Answers only from the business's own graph. Unknown questions get "I don't have verified information," never invention.
- Every answer cites its source file or installation record.
- Cannot see other businesses. Tenant scoping enforced before every answer.
- Cannot send, book, pay, or change anything. Drafts go through owner approval like everything else.
- No passwords, no credentials, no customer PII beyond what the customer approved for the manual.

## Buddy vs Muse: complement, not competition

| | Onboard buddy | Meta Muse |
|---|---|---|
| Scope | One business, deeply | Everything, generally |
| Knows | Services, prices, workflows, rules | The whole internet + connected apps |
| Runs on | Our harness, customer-approved data | Meta's cloud, US-only for now |
| Costs customer | Free with setup | Meta's pricing, when available in UK |
| Sees customer PII | Only what the install recorded | Whatever the customer connects |

The positioning: **the buddy knows your business; Muse knows everything else.** They don't overlap because the buddy's knowledge (price book, workflows, install state) lives outside Meta, and Muse's generality lives outside any single business.

When Muse reaches the UK, the buddy becomes the trusted on-ramp: it holds the verified business profile, price book, and approval rules that a Muse connector would need — already structured, already permissioned. Until then, the buddy works standalone over WhatsApp, email, and the dashboard.

We do not compete with Muse. We make businesses ready for it — and useful without it.
