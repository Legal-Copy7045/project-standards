# CLAUDE.md (project-standards)

The owner's standard for every project: STANDARD.md (the rules), templates/ and regression-kit/ (what projects copy),
.github/workflows/ (reusable workflows projects call by commit SHA), claude/ (the owner-defaults block and global
skills that install.sh puts in ~/.claude), maintenance/ (the weekly maintenance repo list and log), tools/.

- This repository is public: no names, places, addresses, coordinates, device IDs, hostnames, emails or credentials of
  the owner, his family or his home. Examples use made-up values (Morgan, Casey, Lakeview, Hillcrest).
- Commit as `Legal-Copy7045 <323378128+Legal-Copy7045@users.noreply.github.com>`.
- A change to the standard: bump VERSION (MINOR for new rules, PATCH for fixes, MAJOR when projects must change),
  add the CHANGELOG section, tag v<VERSION> after merging. Projects pin reusable workflows by that tag's commit.
- `bash tests/run.sh` tests the kit and the scripts; run it before marking a PR ready.
- The weekly maintenance session may commit maintenance/WEEKLY.md and maintenance/published.yaml straight to main;
  every other change goes through a pull request.
