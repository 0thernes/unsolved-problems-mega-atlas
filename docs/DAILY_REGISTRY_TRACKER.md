# Daily External Open-Problem Registry & Left-to-Solve Tracker (`v2.9.0`)

> **Auto-Updated Daily (`06:00 UTC`):** `.github/workflows/daily-registry-sync.yml` · **Last Checked (UTC):** `2026-11-27T05:26:03Z` · **Mode:** `live`

- **Committed Registries Benchmarked:** `16`
- **Live Public Trackers Polled Daily:** `16`
- **Left to Solve Live Fronts (`lefttosolve.com/programs`):** `25` programs (`59,396` targets · `57,410` open · `1,949` Lean-4 formalized open · `1,104` solved-here)
- **Unretired Fall/Nov 2026 AI Claim Targets:** `12` (all remain `ai-claim-under-audit-nov2026`)
- **Epistemic Policy:** Advisory daily telemetry ONLY — ZERO automatic problem retirement. Community & primary-registry consensus required.

## 1. Latest Day-over-Day Changes & Alerts

- lefttosolve_stats.solved_here_total: 1,270 -> 1,322 (+52)
- 0thernes_research_archive HEAD updated: ed2093ed5b15 -> a5ff68ce8dc1 (2026-11-27T05:24:56Z)
- PROGRAM_DELTA [Erdős Problems]: targets 2068->2068, open 837->837, solved_here 699->720
- PROGRAM_DELTA [Wikipedia]: targets 615->615, open 336->336, solved_here 128->135
- PROGRAM_DELTA [OEIS]: targets 461->461, open 394->394, solved_here 59->60
- PROGRAM_DELTA [Green's 100 Open Problems]: targets 285->285, open 128->128, solved_here 72->74
- PROGRAM_DELTA [Papers]: targets 180->180, open 93->93, solved_here 27->29
- PROGRAM_DELTA [arXiv papers]: targets 105->105, open 43->43, solved_here 28->30
- PROGRAM_DELTA [Optimization Constants]: targets 31->31, open 11->11, solved_here 4->5
- PROGRAM_DELTA [Kourovka Notebook]: targets 9->9, open 5->5, solved_here 0->1

## 2. All 16 Daily-Polled Global Open-Problem Registries

| Registry | URL | HTTP | Status | Extracted Signals | Editorial Action |
|---|---|---|---|---|---|
| **Left to Solve Live Catalog Stats API** | https://lefttosolve.com/api/stats | `200` | `live_checked` | total=59,396; lean_open=1,939; unformalized=55,471; solved_here=1,322; live_agents=139 | LIVE_SYNCED: Left to Solve catalog counters updated. |
| **Left to Solve — All 25 Mathematical Programs** | https://lefttosolve.com/programs | `200` | `live_checked` | 25 programs; targets=59,396; open=57,410; solved_here=1,104 | LIVE_SYNCED: Parsed 25 Left to Solve programs. |
| **Google DeepMind formal-conjectures (GitHub)** | https://api.github.com/repos/google-deepmind/formal-conjectures/commits/main | `200` | `live_checked` | sha=ea8e3e198ded; date=2026-11-26T15:20:47Z | LIVE_SYNCED: Upstream commit SHA recorded. |
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
| **0thernes Master Research Archive (GitHub)** | https://api.github.com/repos/0thernes/0thernes-research-archive/commits/main | `200` | `live_checked` | sha=a5ff68ce8dc1; date=2026-11-27T05:24:56Z | LIVE_SYNCED: Upstream commit SHA recorded. |

## 3. All 25 Live Fronts on Left to Solve (`https://lefttosolve.com/programs`)

| # | Program / Front | Lean 4 Formalized | Targets | Open | Solved Here | Live Agents |
|---:|---|---|---:|---:|---:|---:|
| 1 | [MathOverflow (not formalized)](https://lefttosolve.com/programs/MathOverflow%20(not%20formalized)) | No | 35,783 | 35,783 | 0 | 1 |
| 2 | [OEIS conjectures (not formalized)](https://lefttosolve.com/programs/OEIS%20conjectures%20(not%20formalized)) | No | 18,441 | 18,441 | 0 | 3 |
| 3 | [Erdős Problems](https://lefttosolve.com/programs/Erd%C5%91s%20Problems) | Yes | 2,068 | 837 | 720 | 72 |
| 4 | [Wikipedia](https://lefttosolve.com/programs/Wikipedia) | Yes | 615 | 336 | 135 | 12 |
| 5 | [OEIS](https://lefttosolve.com/programs/OEIS) | Yes | 461 | 394 | 60 | 13 |
| 6 | [Mathematics Stack Exchange (not formalized)](https://lefttosolve.com/programs/Mathematics%20Stack%20Exchange%20(not%20formalized)) | No | 395 | 395 | 0 | 0 |
| 7 | [Wikipedia list (not formalized)](https://lefttosolve.com/programs/Wikipedia%20list%20(not%20formalized)) | No | 366 | 366 | 0 | 3 |
| 8 | [Open Problem Garden](https://lefttosolve.com/programs/Open%20Problem%20Garden) | No | 316 | 316 | 0 | 0 |
| 9 | [Green's 100 Open Problems](https://lefttosolve.com/programs/Green&#x27;s%20100%20Open%20Problems) | Yes | 285 | 128 | 74 | 4 |
| 10 | [Papers](https://lefttosolve.com/programs/Papers) | Yes | 180 | 93 | 29 | 6 |
| 11 | [Erdős Problems (not formalized)](https://lefttosolve.com/programs/Erd%C5%91s%20Problems%20(not%20formalized)) | No | 116 | 116 | 0 | 0 |
| 12 | [arXiv papers](https://lefttosolve.com/programs/arXiv%20papers) | Yes | 105 | 43 | 30 | 4 |
| 13 | [Wikipedia (not formalized)](https://lefttosolve.com/programs/Wikipedia%20(not%20formalized)) | No | 44 | 44 | 0 | 0 |
| 14 | [Open Quantum Problems](https://lefttosolve.com/programs/Open%20Quantum%20Problems) | Yes | 32 | 28 | 4 | 0 |
| 15 | [Optimization Constants](https://lefttosolve.com/programs/Optimization%20Constants) | Yes | 31 | 11 | 5 | 0 |
| 16 | [Written on the Wall II](https://lefttosolve.com/programs/Written%20on%20the%20Wall%20II) | Yes | 31 | 11 | 20 | 3 |
| 17 | [Other](https://lefttosolve.com/programs/Other) | Yes | 29 | 17 | 6 | 1 |
| 18 | [Books](https://lefttosolve.com/programs/Books) | Yes | 26 | 11 | 6 | 1 |
| 19 | [MathOverflow](https://lefttosolve.com/programs/MathOverflow) | Yes | 21 | 9 | 10 | 0 |
| 20 | [Millennium Prize](https://lefttosolve.com/programs/Millennium%20Prize) | Yes | 21 | 12 | 2 | 1 |
| 21 | [Kourovka Notebook](https://lefttosolve.com/programs/Kourovka%20Notebook) | Yes | 9 | 5 | 1 | 0 |
| 22 | [Hilbert's Problems](https://lefttosolve.com/programs/Hilbert&#x27;s%20Problems) | Yes | 8 | 2 | 1 | 0 |
| 23 | [Open problems in information theory (gokhanmergen)](https://lefttosolve.com/programs/Open%20problems%20in%20information%20theory%20(gokhanmergen)) | Yes | 7 | 7 | 0 | 0 |
| 24 | [Conjectures of Luc Gillibert](https://lefttosolve.com/programs/Conjectures%20of%20Luc%20Gillibert) | Yes | 3 | 3 | 0 | 0 |
| 25 | [Litt's Problems](https://lefttosolve.com/programs/Litt&#x27;s%20Problems) | Yes | 3 | 2 | 1 | 0 |
| — | **Total (25 Programs)** | — | **59,396** | **57,410** | **1,104** | **124** |

## 4. Manual / Local Reproduction

```bash
python scripts/sync_external_registries.py --live --write-daily
# Or via justfile:
just sync-registries
```
