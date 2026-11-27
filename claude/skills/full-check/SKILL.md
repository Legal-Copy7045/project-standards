---
name: full-check
description: Run the regression and the walkthrough together as one job - every stage plus the walkthrough side by side, all five reviewers in parallel (bugs, claims, exposure, desktop, phone) with a full security audit, both reports published and both logs updated. Use for "/full-check", "regression and walkthrough" or "run everything". For one of the two use /regression or /walkthrough.
---

# /full-check

Read the `regression` and `walkthrough` skills first (`~/.claude/skills/<name>/SKILL.md`); this file only says how
they interleave. Neither run fixes product code; clear fixes follow in the next release. A full check always runs the walkthrough (no skip check) and the full
security audit.

1. **Suite up to date**: regression step 1; commit.
2. **Everything at once** (background): `python3 regression/run.py --with-walkthrough` and
   `python3 regression/run.py brief --full`.
3. **Reviewers**: launch `bugs`, `claims`, `exposure` straight away. When the walkthrough stage has finished (`run.py`
   prints `walkthrough done`), run `python3 regression/run.py brief --walkthrough` and launch `desktop` and `phone`
   (`model: "sonnet"`). All five fresh, read-only, in the background, briefed only with their brief file.
4. **Both reports**: `run.py report` and `run.py report --walkthrough`; publish both to their `published.yaml` URLs;
   `run.py log --full-check` writes both rows, each naming the other report's link.
5. **Commit and tell the owner in one message**: regression totals and failures, findings by severity and the claims
   that did not hold, walkthrough counts and its top three findings, both links; then which findings go into the next release without
   asking and which need the owner's decision (the rule in STANDARD.md 3.6).
