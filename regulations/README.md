# regulations/

Combined regulations source. Everything AI-agent related, tax, finance, security, voice, marketing, trade, employment, consumer, and data — in one machine-readable registry that every vertical pack, manual, and prompt can read from.

## Files

- `registry.json` — 36 rules. Each rule carries `id`, `domain`, `jurisdiction`, `industries`, `law`, `detail`, `citation`, `source_url`, `basis`, `failure_mode`, `applies_when`, `owner_action`, `escalation`, `review_date`, and `source`.
- `README.md` — this file.

## Sources

- 26 entries imported from `cgraphuk/graph/law/legislation.json` (marked `"source": "cgraphuk/..."`).
- 10 entries added by aionboard research: VAT, Corporation Tax, payroll/NICs, FCA payment rules, PECR marketing, call recording, secrets handling, tenant isolation, Muse availability, ChatGPT MCP gating (marked `"source": "aionboard-research"`).

## Domains

`ai-agent`, `consumer`, `data`, `employment`, `finance`, `marketing`, `security`, `tax`, `trade`, `voice`.

## Review policy

Every entry carries `review_date`. Entries past their review date are **stale**: re-verify before use, never silently trust. `stale_rules()` in `aionboard/compliance.py` lists them.

## Honesty rules

- Entries marked `template-analysis` or with `(DESIGN RULE, not legislation)` in the law field are **our invariants, not statutes**. Never present them as law.
- Platform entries (`AI-MUSE-UK`, `AI-CHATGPT-MCP`) describe platform reality at review time. Platforms shift — re-check before selling access.
- These are reminders for the responsible business operator. AI Onboard does not issue legal certification, determine competence, or represent that a business meets requirements it has not verified.

## How others read from it

```python
from aionboard.compliance import init_compliance_tables, rules_for_industry

init_compliance_tables(connection)          # seeds SQLite from registry.json
rules_for_industry(connection, "nails")     # beauty + universal rules
```

Vertical `profile.json` `legal[]` entries reference registry IDs. Tests enforce that every referenced ID exists in the registry.
