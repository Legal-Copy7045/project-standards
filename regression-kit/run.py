#!/usr/bin/env python3
"""Regression runner (the standard's command set; see regression/README.md and profile.yaml).

    python3 regression/run.py check                 ci + unit, quiet: run before marking a PR ready
    python3 regression/run.py                       every stage but walkthrough
    python3 regression/run.py --with-walkthrough    every stage and the walkthrough
    python3 regression/run.py --stage unit          one stage (repeatable)
    python3 regression/run.py brief|report|log|summary|manual|schema|walkthrough-due ...   (standard.py)

This template runs the command stages defined in profile.yaml. A project with its own stage code keeps it here and
calls standard.write_stage() for each stage's results; everything after the stages stays in standard.py.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import standard  # noqa: E402

TOOLING = {"brief", "report", "log", "summary", "manual", "schema", "walkthrough-due"}


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in TOOLING:
        return standard.main(sys.argv[1:])
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("mode", nargs="?", choices=["check"], help="ci + unit, quiet")
    ap.add_argument("--stage", action="append", help="run only this stage (repeatable)")
    ap.add_argument("--with-walkthrough", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    standard.OUT.mkdir(exist_ok=True)
    if a.mode == "check":
        return standard.run_stages(["ci", "unit"], quiet=True)
    return standard.run_stages(a.stage, with_walkthrough=a.with_walkthrough, quiet=a.quiet)


if __name__ == "__main__":
    sys.exit(main())
