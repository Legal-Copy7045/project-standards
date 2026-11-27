# project-standards

One standard for every project: how CI runs (economically, the same for public and private repositories), how
releases and deployments happen, how the regression, walkthrough and full check work, how each project keeps itself
up to date every week, and how Claude Code sessions work in them. Read **[STANDARD.md](STANDARD.md)**.

| Path | What |
|---|---|
| `STANDARD.md` | The rules. |
| `.github/workflows/` | Reusable workflows: `privacy.yml`, `gitleaks.yml`, `codeql.yml`, `release.yml`, `dependabot-automerge.yml`. Call them by the commit SHA of a `v*` tag. |
| `templates/.github/` | What a project copies: `ci.yml`, `codeql.yml`, `dependabot-automerge.yml`, `dependabot.yml`, `changes.yaml`, `versions.yaml`, `upstreams.yaml`, `standard.yaml`, and the scripts `changes.py`, `check_versions.py`, `release_notes.py`, `privacy_guard.py`. |
| `regression-kit/` | A project's `regression/` starter: `standard.py` (shared tooling, vendored unchanged), `run.py`, `profile.yaml`, catalogue, claims, manual, schemas. |
| `claude/` | The owner-defaults block for `~/.claude/CLAUDE.md` and the global skills `/regression`, `/walkthrough`, `/full-check`, `/adopt-standard`, `/weekly-maintenance`. |
| `install.sh` | Installs `claude/` and a copy of this repository into `~/.claude` (the cloud environment's setup script runs it for every new session). |
| `maintenance/` | The repositories the weekly maintenance covers, its log and its report link. |
| `tools/upstreams.py` | Newer releases of versions Dependabot doesn't track. |

New project: open a Claude session in it and run `/adopt-standard`.
