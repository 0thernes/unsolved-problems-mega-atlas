## Summary of Changes

- Affected Problem ID(s) / Module(s):
- Motivation & primary sources (DOI / arXiv / ProofAtlas / Erdős DB / Clay CMI):

## Verification Checklist (Required)

- [ ] `python src/v2_export_all.py` completed cleanly
- [ ] `cd lean && lake build` passed with **0 `sorry`**, **0 `admit`**, **0 `native_decide`**, and axioms strictly within `[propext, Quot.sound]`
- [ ] `python scripts/audit_atlas.py --sync-checksums --check-lean` passed
- [ ] `pytest -v` passed 100%
- [ ] Any new score changes are justified transparently as falsifiable editorial estimates
- [ ] No unverified AI proof claim is prematurely marked as retired/solved

## Licensing Confirmation

I confirm that data/prose contributions are submitted under **CC BY 4.0** (`LICENSE`) and code/schema/Lean contributions under **MIT** (`LICENSE-CODE`).
