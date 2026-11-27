# Changelog

## [1.2.2] - 2026-11-27
### Security
- gitleaks.yml: the image is pinned by digest (new input `image`, must be tag@sha256:...), and `.gitleaks.toml` is
  always read from the default branch, so a pull request can't allowlist its own leak; the checkout is mounted read-only.
- STANDARD.md 1.5: container images run from workflow steps are pinned by digest and listed in `.github/upstreams.yaml`.

## [1.2.1] - 2026-11-27
### Fixed
- gitleaks.yml: findings are listed in the step summary (rule, file, line, commit; secrets redacted) with a redacted
  JSON report kept 3 days, instead of only "leaks found: N".

## [1.2.0] - 2026-11-27
### Changed
- Findings (STANDARD.md 3.6, owner defaults, regression/walkthrough/full-check/weekly-maintenance skills): the run
  stays an independent, read-only check; afterwards every finding with a clear fix goes into the next release without
  asking. The owner is asked only when a fix is uncertain, weakens a security setting, changes a legal or governance
  rule, or merges or removes pages. Summaries say which findings will be fixed and which need the owner.
- HOA-Portal is public; the maintenance list no longer marks it private.

### Fixed
- regression-kit standard.py 1.2.0: `log` never adds a second row for the same commit (with --full-check, projects
  that write their own walkthrough row got two).

## [1.1.0] - 2026-11-27
### Changed
- The standard is a baseline, not a ceiling: a project keeps a more advanced version of any concept and lists it
  under `beyond:` in .github/standard.yaml (STANDARD.md, adopt-standard, owner defaults, standard.yaml template).

### Added
- watchgrapher and open-pitmaster in the weekly maintenance (Sunday 03:47 UTC CI slot).

## [1.0.0] - 2026-11-27
### Added
- The project standard (STANDARD.md): one CI profile for public and private repositories, releases from a merged
  VERSION bump, deployment per project type, the regression/walkthrough/full-check contract, working rules for Claude
  sessions, weekly maintenance with a weekly report for the owner.
- Reusable workflows: privacy guard, gitleaks, CodeQL, release, Dependabot auto-merge.
- Templates: ci.yml, codeql.yml, dependabot-automerge.yml, dependabot.yml, changes.py, check_versions.py,
  release_notes.py, privacy_guard.py and their config files.
- Regression kit: standard.py (briefs, full/delta security audit, reports, logs, summary, manual results), run.py
  for command-based stages, profile, catalogue, claims and manual examples, findings schemas.
- Global Claude skills: regression, walkthrough, full-check, adopt-standard, weekly-maintenance; install.sh.
- tools/upstreams.py: newer releases of versions Dependabot doesn't track.
