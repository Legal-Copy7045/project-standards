---
name: walkthrough
description: Run the project's independent walkthrough of every function on desktop and phone - signs in as every role, records every menu and page with screenshots, runs the automated UX checks, has two fresh reviewers (desktop, phone) write a streamlining report, publishes it and logs it in WALKTHROUGHS.md. Use for "/walkthrough" or a usability or streamlining review. Projects with a UI only. Fixes nothing.
---

# /walkthrough

Standard: `~/.claude/standards/STANDARD.md` section 3.5. Read `regression/profile.yaml` (`ui`, `roles`, `walkthrough`)
and `regression/README.md`. If `ui` is false, say the project has no walkthrough and stop.

**Skip check.** Unless the owner asked for it explicitly or `/full-check` called it: if no file matching
`walkthrough.ui_paths` in `profile.yaml` changed since the commit of the newest `regression/WALKTHROUGHS.md` row,
say so with that row's report link and stop.

## 1. Run the stage (background)

```bash
python3 regression/run.py --stage walkthrough
```

Output: `regression/out/walkthrough.json` (role -> desktop|phone -> menu and pages), screenshots under
`regression/out/walkthrough/`, and the `WALK-` checks in `regression/out/walkthrough-checks.json`. A `WALK-RUN`
failure means the stage broke: fix the environment and run it again. Commit new IDs in `regression/ids/`.

## 2. Two reviewers, in parallel (after the stage)

`python3 regression/run.py brief --walkthrough` writes `out/briefs/desktop.md` and `out/briefs/phone.md`. Launch two
fresh `general-purpose` agents with `model: "sonnet"`, `run_in_background: true`, each with its brief as the whole
prompt. They read files and screenshots only and return JSON per `regression/standard.py schema walkthrough`.
Save to `regression/out/findings/walkthrough-<desktop|phone>.json` (failed reviewer: `status: failed`, as in /regression).

## 3. Report, publish, log, commit

```bash
python3 regression/run.py report --walkthrough   # out/walkthrough.html
```

Publish `regression/out/walkthrough.html` privately (icon `layout`), to the `walkthrough:` URL in
`regression/published.yaml` if there is one (read it first), else new and record it. `python3 regression/run.py log
--walkthrough`, commit the records, push to the working branch.

Tell the owner: roles and page counts, failing UX checks by kind, the findings by group with the three most valuable
in one sentence each, and the link. Fix nothing.
