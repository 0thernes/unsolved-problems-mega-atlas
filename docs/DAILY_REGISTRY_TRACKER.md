# Daily External Open-Problem Registry & Left-to-Solve Tracker (`v2.10.0`)

> **Auto-Updated Daily (`06:00 UTC`):** `.github/workflows/daily-registry-sync.yml` · **Last Checked (UTC):** `2026-11-27T16:30:38Z` · **Mode:** `live`

- **Committed Registries Benchmarked:** `16`
- **Live Public Trackers Polled Daily:** `16`
- **Left to Solve Live Fronts (`lefttosolve.com/programs`):** `26` programs (`62,790` targets · `60,804` open · `1,949` Lean-4 formalized open · `1,706` solved-here)
- **Unretired Fall/Nov 2026 AI Claim Targets:** `12` (all remain `ai-claim-under-audit-nov2026`)
- **Epistemic Policy:** Advisory daily telemetry ONLY — ZERO automatic problem retirement. Community & primary-registry consensus required.

## 1. Latest Day-over-Day Changes & Alerts

- lefttosolve_stats.total: 62,765 -> 62,790 (+25)
- lefttosolve_stats.solved_here_total: 2,356 -> 2,662 (+306)
- lefttosolve_stats.catalog.open: 2,208 -> 2,549 (+341)
- lefttosolve_stats.catalog.unformalized: 58,571 -> 58,255 (-316)
- deepmind_formal_conjectures HEAD updated: 023c8018c82b -> f606af160664 (2026-11-27T14:03:49Z)
- 0thernes_research_archive HEAD updated: 5bb57cbf9027 -> e60a7458abdd (2026-11-27T15:54:47Z)
- PROGRAM_DELTA [MathOverflow (not formalized)]: targets 35783->35783, open 35783->35783, solved_here 7->16
- PROGRAM_DELTA [OEIS conjectures (not formalized)]: targets 18441->18451, open 18441->18451, solved_here 48->119
- PROGRAM_DELTA [arXiv abstracts (not formalized)]: targets 3368->3368, open 3368->3368, solved_here 3->5
- PROGRAM_DELTA [Erdős Problems]: targets 2068->2068, open 837->837, solved_here 957->995
- PROGRAM_DELTA [Wikipedia]: targets 615->615, open 336->336, solved_here 176->186
- PROGRAM_DELTA [OEIS]: targets 461->461, open 394->394, solved_here 82->85
- PROGRAM_DELTA [Mathematics Stack Exchange (not formalized)]: targets 395->395, open 395->395, solved_here 1->3
- PROGRAM_DELTA [Open Problem Garden]: targets 316->316, open 316->316, solved_here 1->6
- PROGRAM_DELTA [Green's 100 Open Problems]: targets 285->285, open 128->128, solved_here 112->120
- PROGRAM_DELTA [Papers]: targets 180->180, open 93->93, solved_here 36->39
- PROGRAM_DELTA [Wikipedia (not formalized)]: targets 45->60, open 45->60, solved_here 0->0

## 2. All 16 Daily-Polled Global Open-Problem Registries

| Registry | URL | HTTP | Status | Extracted Signals | Editorial Action |
|---|---|---|---|---|---|
| **Left to Solve Live Catalog Stats API** | https://lefttosolve.com/api/stats | `200` | `live_checked` | total=62,790; lean_open=2,549; unformalized=58,255; solved_here=2,662; live_agents=194 | LIVE_SYNCED: Left to Solve catalog counters updated. |
| **Left to Solve — All 25 Mathematical Programs** | https://lefttosolve.com/programs | `200` | `live_checked` | 26 programs; targets=62,790; open=60,804; solved_here=1,706 | LIVE_SYNCED: Parsed 26 Left to Solve programs. |
| **Google DeepMind formal-conjectures (GitHub)** | https://api.github.com/repos/google-deepmind/formal-conjectures/commits/main | `200` | `live_checked` | sha=f606af160664; date=2026-11-27T14:03:49Z | LIVE_SYNCED: Upstream commit SHA recorded. |
| **Terence Tao / Thomas Bloom erdosproblems (GitHub)** | https://api.github.com/repos/teorth/erdosproblems/commits/main | `200` | `live_checked` | sha=3d9fd1caec27; date=2026-11-24T14:42:43Z | LIVE_SYNCED: Upstream commit SHA recorded. |
| **Clay Mathematics Institute Millennium Prize Problems** | https://www.claymath.org/millennium-problems/ | `200` | `live_checked` | Millennium Prize Problems; Poincaré Conjecture; Poincaré conjecture | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **Erdős Problems Database (Thomas F. Bloom)** | https://www.erdosproblems.com/ | `200` | `live_checked` | 1221 problems; Erdős Problems; Erdős problems | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **ProofAtlas Open Problems Dataset** | https://proofatlas.ai/open-problems/ | `200` | `live_checked` | 500 open problems; Top 500; ProofAtlas | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **Open Problem Garden** | https://www.openproblemgarden.org/ | `200` | `live_checked` | Open Problem Garden | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **Wikipedia: List of Unsolved Problems in Mathematics** | https://en.wikipedia.org/api/rest_v1/page/summary/List_of_unsolved_problems_in_mathematics | `200` | `live_checked` | rev=1386859731; updated=2026-11-21T01:55:17Z | LIVE_SYNCED: Wikipedia revision tracked. |
| **Wikipedia: List of Unsolved Problems in Physics** | https://en.wikipedia.org/api/rest_v1/page/summary/List_of_unsolved_problems_in_physics | `200` | `live_checked` | rev=1387943544; updated=2026-11-26T03:04:46Z | LIVE_SYNCED: Wikipedia revision tracked. |
| **Wikipedia: List of Unsolved Problems in Computer Science** | https://en.wikipedia.org/api/rest_v1/page/summary/List_of_unsolved_problems_in_computer_science | `200` | `live_checked` | rev=1388116134; updated=2026-11-26T17:47:23Z | LIVE_SYNCED: Wikipedia revision tracked. |
| **The Busy Beaver Challenge (BB(6) / Antihydra)** | https://bbchallenge.org/ | `200` | `live_checked` | BB(5) = 47,176,870; bbchallenge; busy beaver | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **Kourovka Notebook (arXiv:1401.0300)** | https://arxiv.org/abs/1401.0300 | `200` | `live_checked` | [v1]; [v2]; [v3]; [v4]; [v5]; [v6]; [v7]; [v8]; [v9]; [v10] | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **IQOQI Vienna Open Quantum Problems** | https://oqp.iqoqi.oeaw.ac.at/ | `200` | `live_checked` | Open Quantum Problems | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **Lean FRO & Mathlib Initiative RH Verification Statement** | https://leanprover-community.github.io/blog/posts/riemann-hypothesis/ | `200` | `live_checked` | Riemann Hypothesis; Mathlib; Lean FRO | NO_RETIREMENT_DETECTED: committed baseline remains consistent. |
| **0thernes Master Research Archive (GitHub)** | https://api.github.com/repos/0thernes/0thernes-research-archive/commits/main | `200` | `live_checked` | sha=e60a7458abdd; date=2026-11-27T15:54:47Z | LIVE_SYNCED: Upstream commit SHA recorded. |

## 3. All 26 Live Fronts on Left to Solve (`https://lefttosolve.com/programs`)

| # | Program / Front | Lean 4 Formalized | Targets | Open | Solved Here | Live Agents |
|---:|---|---|---:|---:|---:|---:|
| 1 | [MathOverflow (not formalized)](https://lefttosolve.com/programs/MathOverflow%20(not%20formalized)) | No | 35,783 | 35,783 | 16 | 2 |
| 2 | [OEIS conjectures (not formalized)](https://lefttosolve.com/programs/OEIS%20conjectures%20(not%20formalized)) | No | 18,451 | 18,451 | 119 | 33 |
| 3 | [arXiv abstracts (not formalized)](https://lefttosolve.com/programs/arXiv%20abstracts%20(not%20formalized)) | No | 3,368 | 3,368 | 5 | 4 |
| 4 | [Erdős Problems](https://lefttosolve.com/programs/Erd%C5%91s%20Problems) | Yes | 2,068 | 837 | 995 | 51 |
| 5 | [Wikipedia](https://lefttosolve.com/programs/Wikipedia) | Yes | 615 | 336 | 186 | 5 |
| 6 | [OEIS](https://lefttosolve.com/programs/OEIS) | Yes | 461 | 394 | 85 | 10 |
| 7 | [Mathematics Stack Exchange (not formalized)](https://lefttosolve.com/programs/Mathematics%20Stack%20Exchange%20(not%20formalized)) | No | 395 | 395 | 3 | 0 |
| 8 | [Wikipedia list (not formalized)](https://lefttosolve.com/programs/Wikipedia%20list%20(not%20formalized)) | No | 366 | 366 | 0 | 1 |
| 9 | [Open Problem Garden](https://lefttosolve.com/programs/Open%20Problem%20Garden) | No | 316 | 316 | 6 | 0 |
| 10 | [Green's 100 Open Problems](https://lefttosolve.com/programs/Green%27s%20100%20Open%20Problems) | Yes | 285 | 128 | 120 | 4 |
| 11 | [Papers](https://lefttosolve.com/programs/Papers) | Yes | 180 | 93 | 39 | 5 |
| 12 | [Erdős Problems (not formalized)](https://lefttosolve.com/programs/Erd%C5%91s%20Problems%20(not%20formalized)) | No | 116 | 116 | 1 | 0 |
| 13 | [arXiv papers](https://lefttosolve.com/programs/arXiv%20papers) | Yes | 105 | 43 | 50 | 4 |
| 14 | [Wikipedia (not formalized)](https://lefttosolve.com/programs/Wikipedia%20(not%20formalized)) | No | 60 | 60 | 0 | 0 |
| 15 | [Open Quantum Problems](https://lefttosolve.com/programs/Open%20Quantum%20Problems) | Yes | 32 | 28 | 4 | 1 |
| 16 | [Optimization Constants](https://lefttosolve.com/programs/Optimization%20Constants) | Yes | 31 | 11 | 10 | 1 |
| 17 | [Written on the Wall II](https://lefttosolve.com/programs/Written%20on%20the%20Wall%20II) | Yes | 31 | 11 | 25 | 1 |
| 18 | [Other](https://lefttosolve.com/programs/Other) | Yes | 29 | 17 | 8 | 2 |
| 19 | [Books](https://lefttosolve.com/programs/Books) | Yes | 26 | 11 | 14 | 0 |
| 20 | [MathOverflow](https://lefttosolve.com/programs/MathOverflow) | Yes | 21 | 9 | 11 | 1 |
| 21 | [Millennium Prize](https://lefttosolve.com/programs/Millennium%20Prize) | Yes | 21 | 12 | 2 | 1 |
| 22 | [Kourovka Notebook](https://lefttosolve.com/programs/Kourovka%20Notebook) | Yes | 9 | 5 | 2 | 0 |
| 23 | [Hilbert's Problems](https://lefttosolve.com/programs/Hilbert%27s%20Problems) | Yes | 8 | 2 | 3 | 0 |
| 24 | [Open problems in information theory (gokhanmergen)](https://lefttosolve.com/programs/Open%20problems%20in%20information%20theory%20(gokhanmergen)) | Yes | 7 | 7 | 0 | 1 |
| 25 | [Conjectures of Luc Gillibert](https://lefttosolve.com/programs/Conjectures%20of%20Luc%20Gillibert) | Yes | 3 | 3 | 1 | 0 |
| 26 | [Litt's Problems](https://lefttosolve.com/programs/Litt%27s%20Problems) | Yes | 3 | 2 | 1 | 0 |
| — | **Total (26 Programs)** | — | **62,790** | **60,804** | **1,706** | **127** |

## 4. Manual / Local Reproduction

```bash
python scripts/sync_external_registries.py --live --write-daily
# Or via justfile:
just sync-registries
```
