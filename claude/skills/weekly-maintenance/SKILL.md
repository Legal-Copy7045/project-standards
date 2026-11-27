---
name: weekly-maintenance
description: The weekly maintenance run across all the owner's projects - checks what Dependabot merged and left open, the weekly CI and CodeQL results, vulnerabilities and upstream versions; cuts maintenance releases for merged dependency updates; publishes one weekly summary report and says what needs the owner. Use for "/weekly-maintenance" or the weekly scheduled task.
---

# /weekly-maintenance

Standard: `~/.claude/standards/STANDARD.md` section 5. Repositories: `~/.claude/standards/maintenance/repos.yaml`.
Keep it frugal: GitHub MCP list calls with small pages (`perPage` 10-30, `minimal_output` where offered), read job
logs only for a failed job, never run a project's full test suite (CI already did).

## 1. Gather, per repository (last 7 days)

Attach each with `add_repo` (`access: push`) and clone shallowly (depth 50). Then:
- **Dependabot**: PRs merged (what, from -> to), PRs open (why: failing `ci-result`, `major-update` label, conflict).
- **Weekly CI** (`schedule` run of `ci.yml`) and **CodeQL** (`codeql.yml`): conclusion; for a failure, the failing
  job and the first error lines; CodeQL finding count from the step summary or job log.
- **Vulnerabilities**: audit and image-scan steps of the weekly run (pip-audit, npm audit, Trivy), and open Dependabot
  security PRs. Note which have a fix available.
- **Upstreams**: `python3 ~/.claude/standards/tools/upstreams.py <clone>` (versions Dependabot doesn't track).
- **Release state**: latest `v*` tag vs `main`; commits on main since the tag (dependency merges don't release).

## 2. Act (these; anything uncertain goes in "needs the owner")

Each change goes through a PR per the standard (draft, `regression/run.py check` where it runs quickly, ready, merge
when `ci-result` is green). Commit as the owner's no-reply identity; follow each repository's CLAUDE.md privacy rules.

1. **Upstream patch/minor updates** in `.github/upstreams.yaml` (and the pins they describe): one PR per repository.
2. **Major Dependabot updates**: read the upstream release notes. Merge only when `ci-result` is green and nothing in
   the notes breaks how this project uses it; otherwise leave it open with a one-line recommendation for the owner.
3. **Maintenance release**: when `main` has commits since the latest tag (dependency or upstream updates), one PR:
   PATCH bump of `VERSION` (and every place in `.github/versions.yaml`) and a CHANGELOG section with
   `### Dependencies` (and `### Security` for vulnerability fixes). Merging it releases (section 2.2). Skip it when the
   repository already has an open release PR of its own.
4. **A failing weekly run** caused by an update merged this week: revert that update in a PR (and say so). Other
   failures and CodeQL findings with a clear fix: fix them in a PR that joins the maintenance release (STANDARD.md
   3.6). Ask the owner ("Needs you") when the fix is uncertain, weakens security, changes a legal or governance rule
   or merges or removes pages; vulnerabilities without a fix are reported.

## 3. Report

Write one self-contained HTML page (theme tokens with a dark mode, phone-friendly): a top line ("All quiet" or
"N things need you"), then **Needs you** (each: repo, what, why, the one action), then per repository: updates
merged, releases cut (with what that means: `deploy` in repos.yaml), vulnerabilities (open / fixed), weekly CI and
CodeQL status, upstreams, open PRs. Publish it as a private artifact (icon `calendar`), republished to the `report:`
URL in `maintenance/published.yaml` of the standards repository (read it first); record a new URL there.

Add the row to `maintenance/WEEKLY.md` and commit both files straight to `main` of
Legal-Copy7045/project-standards (the only direct push this run makes; nothing else in that repository changes).

## 4. Tell the owner

A push notification (`PushNotification`, proactive): the top line and up to three "needs you" items, with the report
link. Finish with the same summary as the session's last message.
