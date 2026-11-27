# External Open-Problem Registry Delta Report (`v2.8.0`)

- **Checked (UTC):** `2026-11-27T04:25:05Z`
- **Mode:** `live`
- **Committed Registries Benchmarked:** `13`
- **Unretired Fall/Nov 2026 AI Claim Targets:** `12` (all remain `ai-claim-under-audit-nov2026`)
- **Epistemic Policy:** Advisory editorial delta only — ZERO automatic problem retirement. Community & primary-registry consensus required.

| Registry | URL | HTTP | Status | Extracted Signals | Editorial Action |
|---|---|---|---|---|---|
| **Clay Mathematics Institute Millennium Prize Problems** | https://www.claymath.org/millennium-problems/ | `200` | `live_checked` | Millennium Prize Problems; Poincaré Conjecture; Poincaré conjecture | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **Erdos Problems Database (Thomas F. Bloom)** | https://www.erdosproblems.com/ | `200` | `live_checked` | 1221 problems; Erdős Problems; Erdős problems | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **ProofAtlas Open Problems Dataset** | https://proofatlas.ai/open-problems/ | `200` | `live_checked` | 500 open problems; Top 500; ProofAtlas | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |

## Reproduction

```bash
python scripts/sync_external_registries.py --live --write-report
```
