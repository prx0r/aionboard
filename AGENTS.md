# AGENTS.md — working in this repo

> Handover doc for incoming agents. Read this first, then `OFFER.md`, then the area you're touching.

## Mission

AI Onboard makes UK trades and beauty businesses AI-native: one-fee setup, owner approval on everything, no credentials held, no subscriptions required. Pilot only — **zero paying customers so far.** Everything unvalidated is marked as such. Keep it that way.

## Repo map

```
aionboard/            Python package (stdlib + cryptography only)
  crm.py              Prospects, contacts, attempts, TPS checks, stack inventory
  businesses.py       Canonical business_id, consents (onboarding/marketing/POW)
  installs.py         Legacy install state machine (electrician-shaped)
  onboarding.py       Package registry (standard-ai-setup, muse-quickstart) + recipes
  integrations.py     Capability inventory with lifecycle states
  manual.py           Customer teaching manual + vertical prompts
  support.py          7-day tickets with guide/human/minutes tracking
  handover.py         Handover generator (rejects secrets)
  security.py         Approvals, isolation, secret scan, audit, rate limiter
  backup.py           Encrypted SQLite backups with restore verify
  privacy.py          Export/delete with suppression tombstones
  compliance.py       Seeds from regulations/registry.json
  buddy.py            Per-business scoped assistant
  graph.py            Global knowledge graph + retrieval
  opportunities.py    Geographic matcher, both directions
  demo.py             Fictional electrician demo
  website.py          Static site generators (index, chat, dashboard)

verticals/            11 packs: manifest + profile + 7 docs each
regulations/          36-rule combined registry (registry.json + README)
mcp/                  Tool contracts (tools.json) — designed, not deployed
connector/            Muse submission pack — draft, not submitted
site/                 Generated static pages (index, chat, dashboard, knowledge)
tests/                119 tests, all must pass
```

## State of the world (honest)

| Area | Status |
|------|--------|
| CRM, installs, onboarding, handover, manual, support | Working code, tested |
| Approvals, isolation, secret scan, audit helpers, rate limiter | Working code, tested — **not deployed as a gateway** |
| Encrypted backups with restore verify | Working code, tested |
| MCP tool contracts | Designed (`mcp/tools.json`), **no server running** |
| Muse connector | Draft manifest, **not submitted** |
| Static site + demo chatbot | Generated, working |
| Customer dashboard | Static mock only, **no backend** |
| Live integrations (OAuth to real tools) | None. Every pipeline step is `manual`. |
| Paying customers | Zero. All economics hypothetical. |

## Security work queue (for the security agent, in order)

1. **Deploy the MCP gateway.** Everything security-related is currently library code with no running enforcement point. Stand up the remote HTTPS server with the `mcp/tools.json` contract: OAuth 2.1 + PKCE, audience-bound tokens, per-tool scopes. Nothing else matters until this exists.
2. **Tenant isolation at the storage layer.** `assert_tenant_rows()` checks result sets; the DB itself has no row-level enforcement. Decide: single-tenant SQLite per customer vs Postgres RLS vs application-level scoping with tests. Document the choice.
3. **Secret store.** Credentials currently live in "customer-owned vaults / OS keychain" by policy only. Integrate a real one (OS keychain for pilot, HashiCorp Vault if multi-operator). No secrets in env files beyond local dev.
4. **Audit pipeline.** `audit_tool_call()` writes to local SQLite. Production needs append-only, tamper-evident storage separate from the monitored system, plus a 90-day retention job.
5. **Approval flow pen-test.** Try to break it: replay tokens, tamper payloads, cross-customer redeem, expired redeem, race two redeems concurrently. The unit tests cover the first four; concurrency and the gateway path are untested.
6. **Rate limiter wiring.** `RateLimiter` exists but isn't attached to anything. Wire per-client + per-tool limits into the gateway with deny-logging.
7. **Influence audit (separate repo).** `/root/influence/dash/mcp.py` has a `phone.send` path without per-message approval. Do not put customers on influence until that's fixed and multi-tenant isolation is verified.
8. **Backup restore drill.** Code exists and is tested. Schedule it: restore monthly, verify integrity, log the drill. Untested restores are wishes.
9. **Incident response rehearsal.** `DATA_POLICY.md` has the procedure. Walk it once with fictional data: revoke, scope, notify, log, fix.

## Conventions (non-negotiable)

1. **Tests must pass before any commit.** `python3 -m unittest discover -s tests -v`. Currently 119.
2. **No secrets in the tree.** Run `grep -rE "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}" --exclude-dir=.git .` before pushing. Test fixtures use obviously-fake values.
3. **Docs stay honest.** Hypotheses marked as hypotheses. No invented case studies, no guaranteed outcomes, no live prices outside `OFFER.md`. Failing tests beat comforting docs.
4. **Stdlib + cryptography only.** No new dependencies without discussion.
5. **Customer data never enters git.** `.gitignore` covers DBs, handovers, env files. Fictional data in tests only.
6. **Manual-first.** No step graduates from `manual` to verified automation without a real customer run and evidence.

## Key docs by role

| You need... | Read |
|-------------|------|
| The offer | `OFFER.md` |
| The threat model | `TRUST_MODEL.md`, `SECURITY_ARCHITECTURE.md` |
| The pilot flow | `CHECKPOINTS.md`, `AUTOMATION_PLAYBOOK.md` |
| Per-vertical intel | `verticals/<slug>/` (profile.json is machine-readable) |
| Regulations | `regulations/registry.json` |
| The funnel | `FUNNEL.md`, `ADDONS.md` |
| Strategy + economics | `STRATEGY.md`, `GEO_OPPORTUNITIES.md` |
| Build history | `BUILD_NOTES.md` |
| Peer critiques | `PEER_REVIEW.md`, `devplan.md` |
