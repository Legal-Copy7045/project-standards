---
name: adopt-standard
description: Bring the current repository to the owner's project standard (CI, releases, deployment, regression/walkthrough/full check, Claude working rules) or set a new project up with it. Use for "/adopt-standard", when starting a new project, when a repository has no regression/profile.yaml or no .github/standard.yaml, or when .github/standard.yaml names an older standard than ~/.claude/standards/VERSION.
---

# /adopt-standard

The standard and its templates are installed at `~/.claude/standards/` (a copy of
github.com/Legal-Copy7045/project-standards; `README.md` there lists every file). Read `STANDARD.md` fully once.

## 1. Gap list first (no changes yet)

The standard is a **baseline, not a ceiling**: its templates and kit are defaults and concepts every project must
have. Where this repository already has a more advanced version of the same concept, keep it (adapt it to answer the
standard's commands and files if needed) and list it under `beyond:` in `.github/standard.yaml`; never replace better
work with a template.

Compare the repository with each section of STANDARD.md and write a short gap list (missing or below baseline only): CI triggers and jobs, `changes`
groups, `ci-result`, pinning and permissions, privacy and gitleaks, CodeQL, Dependabot, VERSION/CHANGELOG/versions
check, release and deployment path for the project's type (section 2.3), the regression contract (section 3), CLAUDE.md
size. Keep what already meets or exceeds the standard (`beyond:`); a project-specific difference that is right stays,
recorded under `exceptions:` in `.github/standard.yaml` with its reason.

## 2. Apply, in one draft PR

- CI: where the existing workflow falls short, start from `~/.claude/standards/templates/.github/workflows/ci.yml`; move the project's existing jobs into it
  (keep job names that people know; `ci-result` becomes the only required check). Copy `changes.py`,
  `check_versions.py`, `dependabot.yml`, `codeql.yml` from `templates/` and fill `changes.yaml`, `versions.yaml`.
  Reusable workflows are referenced by the commit SHA of the standards tag
  (`git ls-remote https://github.com/Legal-Copy7045/project-standards 'refs/tags/v*'`), with a `# v<version>` comment.
- Regression: copy `regression-kit/` into `regression/` for a new project; an existing one keeps its stage runners
  (and any more advanced report or tooling), vendors `standard.py` for whatever it lacks, writes `profile.yaml`, renames stages to the standard names (keeping every existing ID and
  prefix: never renumber), and makes `run.py` answer the standard commands by delegating to `standard.py`.
  Move the project's regression/walkthrough/full-check skill files out of `.claude/skills/` (the global skills replace
  them); project-specific instructions go into `profile.yaml` or `regression/README.md`.
- Write `.github/standard.yaml` (`standard: <version>`, `beyond:`, `exceptions:`).
- Bump VERSION and CHANGELOG. Run `python3 regression/run.py check`, then mark the PR ready.

## 3. After merge

Tell the owner what changed in one overview, any GitHub setting only they can change (branch protection: require
`ci-result`; environments `privacy` and `release-signing` limited to main; CodeQL default setup off), and anything
left as an exception.
