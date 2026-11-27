#!/usr/bin/env python3
"""Checks a repository's .github/upstreams.yaml for newer releases (versions Dependabot doesn't track).

    python3 upstreams.py <repo dir> [--json]

track: "16" (optional) stays on that release line.
source: pypi:<name> | npm:<name> | github:<owner>/<repo> (semver tags, via git) | docker:<namespace/image> (Docker Hub)
Prints one line per upstream: name, current, latest, kind of update (major/minor/patch/none/unknown).
"""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

SEMVER = re.compile(r"^v?(\d+)\.(\d+)(?:\.(\d+))?$")


def parse(v: str):
    m = SEMVER.match(v.strip())
    return tuple(int(x or 0) for x in m.groups()) if m else None


def fetch(url: str):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "upstreams-check"}), timeout=20) as r:
        return json.load(r)


def best(tags, track: str = "") -> str:
    ok = [t for t in tags if parse(t) and (not track or t.lstrip("v").startswith(track.rstrip(".") + "."))]
    return max(ok, key=parse)


def latest(source: str, track: str = "") -> str:
    kind, _, name = source.partition(":")
    if kind == "pypi":
        data = fetch(f"https://pypi.org/pypi/{name}/json")
        return best(data["releases"], track) if track else data["info"]["version"]
    if kind == "npm":
        return fetch(f"https://registry.npmjs.org/{name}/latest")["version"]
    if kind == "github":
        out = subprocess.run(["git", "ls-remote", "--tags", "--refs", f"https://github.com/{name}"],
                             capture_output=True, text=True, timeout=60, check=True).stdout
        tags = [t.rsplit("/", 1)[-1] for t in out.split()[1::2]]
        return best(tags, track)
    if kind == "docker":
        ns = name if "/" in name else f"library/{name}"
        tags = [t["name"] for t in fetch(f"https://hub.docker.com/v2/repositories/{ns}/tags?page_size=100")["results"]]
        return best(tags, track)
    raise ValueError(f"unknown source {source}")


def kind_of(cur: str, new: str) -> str:
    a, b = parse(cur), parse(new)
    if not a or not b:
        return "unknown" if cur != new else "none"
    if b <= a:
        return "none"
    return "major" if b[0] > a[0] else "minor" if b[1] > a[1] else "patch"


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    f = repo / ".github" / "upstreams.yaml"
    items = yaml.safe_load(f.read_text()) if f.is_file() else []
    rows = []
    for it in items or []:
        try:
            new = latest(it["source"], str(it.get("track", "")))
            rows.append({**it, "latest": new, "update": kind_of(str(it["current"]), new)})
        except Exception as e:  # noqa: BLE001
            rows.append({**it, "latest": "?", "update": "unknown", "error": str(e)[:120]})
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=1))
    else:
        for r in rows:
            print(f"{r['name']}: {r['current']} -> {r['latest']} ({r['update']}){'  ' + r['error'] if 'error' in r else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
