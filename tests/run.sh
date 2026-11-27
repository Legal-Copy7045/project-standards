#!/usr/bin/env bash
# Tests the regression kit and the template scripts on throwaway repositories.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
t="$(mktemp -d)"; trap 'rm -rf "$t"' EXIT
g() { git -c user.email=t@example.invalid -c user.name=t "$@"; }

# kit
mkdir -p "$t/kit/tests" && cd "$t/kit" && git init -q
cp -r "$root/regression-kit" regression && echo 1.0.0 > VERSION
printf 'def test_ok(): assert True\ndef test_bad(): assert False\n' > tests/test_a.py
cat > regression/profile.yaml <<'Y'
name: Kit test
type: library
ui: false
stages:
  ci: {prefix: CI, commands: [{key: ok, run: "true"}]}
  unit: {prefix: UNIT, commands: [{key: pytest, run: "python3 -m pytest -q -p no:cacheprovider tests --junitxml={junit}", junit: true}]}
  manual: {prefix: MAN}
Y
g add -A && g commit -qm init
python3 regression/run.py check >/dev/null && { echo "check should fail"; exit 1; } || true
grep -q '"UNIT-0002": ' <(python3 -c "import yaml,json;print(json.dumps(yaml.safe_load(open('regression/ids/unit.yaml'))))")
python3 regression/run.py >/dev/null || true
python3 regression/run.py brief | grep -q "audit: full"
python3 regression/run.py report >/dev/null && python3 regression/run.py log >/dev/null
grep -q "| full |" regression/RUNS.md
echo x >> tests/test_a.py && g commit -qam c2
python3 regression/run.py brief | grep -q "audit: delta"
python3 regression/run.py summary | grep -q "Failing (1)"
echo "kit ok"

# template scripts
mkdir -p "$t/tpl" && cd "$t/tpl" && git init -q -b main && cp -r "$root/templates/.github" .
echo 1.0.0 > VERSION && echo '{"version":"1.0.0"}' > package.json
printf '# Changelog\n\n## [1.0.0] - 2026-11-27\n### Added\n- x\n' > CHANGELOG.md
mkdir -p src docs && touch src/a.py docs/b.md && g add -A && g commit -qm a && g checkout -qb f
echo >> docs/b.md && g commit -qam d
EVENT=pull_request BASE=main HEAD=HEAD python3 .github/scripts/changes.py | grep -q "app=false"
echo >> src/a.py && g commit -qam s
EVENT=pull_request BASE=main HEAD=HEAD python3 .github/scripts/changes.py | grep -q "app=true"
python3 .github/scripts/check_versions.py v1.0.0 >/dev/null
python3 .github/scripts/release_notes.py 1.0.0 | grep -q "### Added"
echo '{"version":"0.9.0"}' > package.json && ! python3 .github/scripts/check_versions.py >/dev/null
echo "templates ok"
python3 -m py_compile "$root"/tools/*.py "$root"/regression-kit/*.py "$root"/templates/.github/scripts/*.py
echo "all ok"
