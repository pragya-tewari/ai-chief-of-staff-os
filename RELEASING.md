# Releasing

The release process for a maintainer. Kept short and honest.

## Before you tag a release

Run the same checks CI runs, plus the human ones:

- [ ] `bash scripts/check.sh` passes (links, schemas, capabilities,
      credential/email/phone/forbidden-term scans, full-history scan, sample
      references and sample index coverage).
- [ ] `bash setup/install.sh` works end to end into a throwaway workspace on a
      clean checkout, and `setup/doctor.sh` passes.
- [ ] The sample company runs: the `meeting-to-tasks` demo produces what
      `example-company/EXPECTED-STATE.md` says, and the injection line is quoted,
      not obeyed.
- [ ] Rerun recovery is exercised: a succeeded action is not repeated, a failed
      local action resumes alone, and an external action left `in-progress`
      becomes `needs-verification` rather than being sent/created again.
- [ ] Human semantic review confirms that no real names, confidential amounts,
      workspace IDs, internal slugs or distinctive real-world fact combinations
      remain. CI assists with patterns; it cannot classify fictional names and
      amounts by itself.
- [ ] GitHub private vulnerability reporting is enabled under repository
      Settings → Security before `SECURITY.md` points users to it.
- [ ] `git log --oneline` shows only the intended clean public history; no earlier
      real-derived sample is reachable from any branch or tag.
- [ ] `README.md` job list matches what actually ships this release.
- [ ] `CHANGELOG.md` has a dated section for this version.

## If the release includes anything built from real data

Never publish a scrub of a private file in place — git history keeps the original.
Rebuild it into a **fresh repo with no history**, and re-run `scripts/check.sh`
against that fresh tree.

## Tag it

1. Move the `[Unreleased]` changelog entries under a dated `vX.Y.Z` heading.
2. Commit.
3. Tag: `git tag vX.Y.Z && git push --tags`.
4. Cut the GitHub release from the tag, pasting the changelog section.

## Versioning

Semantic-ish: patch for fixes, minor for new jobs/connections, and a `SPEC-VERSION`
bump only when the file format changes in a way that affects existing workspaces —
which ships with a migration note in the changelog.
