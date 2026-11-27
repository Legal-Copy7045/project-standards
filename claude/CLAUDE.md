# Owner's defaults for every project (a project's own CLAUDE.md wins where they differ)

The full standard is `~/.claude/standards/STANDARD.md` (from github.com/Legal-Copy7045/project-standards). Read the
section a task needs. It is a baseline, not a ceiling: every project must have each concept, and a project
that already has a more advanced version of one keeps it (listed under `beyond:` in .github/standard.yaml). The essentials:

## Build pipeline (STANDARD.md section 1)
- One CI workflow: pull requests only and never drafts; push to main only releases (when VERSION has no tag); a weekly
  full run and workflow_dispatch. A `changes` job starts each slow group only when the PR touches its files.
- `ci-result` is the only required check. Every job has a timeout and least permissions; actions pinned by commit with
  a `# vX` comment; at most 2 test shards; one image build per run; artifacts kept 3 days.
- CodeQL weekly and on demand only; Dependabot weekly (Sunday), grouped minor/patch PRs merge themselves when CI passes.
  Same rules for public and private repos.

## Releases (section 2)
- VERSION (MAJOR.MINOR.PATCH) and a newest-first CHANGELOG.md section with every merge to main; a merged version bump
  is the release (tag v<VERSION>, GitHub Release, deploy). Nothing deploys from an unreleased commit.
- Merge your own PR when ci-result is green, unless the project says otherwise.

## Regression, walkthrough and full check (section 3)
- Every project keeps `regression/` per the standard (profile.yaml, run.py, standard.py, ids, catalogue, claims,
  manual, RUNS.md, WALKTHROUGHS.md, published.yaml). `/regression`, `/walkthrough` and `/full-check` are global skills;
  `/adopt-standard` sets a project up or brings it to the current standard.
- A run fixes no product code; every regression includes the security audit; fix every finding with a clear fix in the
  next release unasked; ask the owner only when a fix is uncertain, weakens security, changes a legal or governance
  rule, or merges or removes pages.

## Weekly maintenance (section 5)
- A Monday scheduled session runs `/weekly-maintenance` across all projects: maintenance releases, upstream pins,
  major updates judged, one weekly report for the owner. Keep `.github/upstreams.yaml` current in every project.

## Working style (section 4)
- Open PRs as drafts; mark ready only after `python3 regression/run.py check` passes; then push again only to fix CI.
- Keep CLAUDE.md short; reference material in docs/claude/<topic>.md. Read summaries, not logs.
- Overview-level updates. Fictional data only; secrets only through guided server scripts, never chat or the web app.
