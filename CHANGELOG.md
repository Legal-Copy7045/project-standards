# Changelog

## [1.1.0] - 2026-11-27
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
