# Validation Gates

Run these before cloning deeply, installing dependencies, commenting, or opening
a PR.

## Hard Reject

- repo is archived or read-only
- issue is closed
- duplicate PR already covers it
- repo has no recent maintenance signal
- issue is crowded with drive-by comments
- issue is vague, huge, or product-directional
- project rejects AI-assisted contributions
- task requires live security probing without authorization
- useful action would mostly serve your contribution graph

## Quarantine

Proceed slowly or skip when:

- maintainer activity is unclear
- setup is heavy for a tiny patch
- issue is labeled easy but underspecified
- generated docs require source tracing
- CI is already broadly failing
- stale project has a fresh-looking issue but no maintainer replies

## Proceed

Good signs:

- current issue, clear expected behavior
- no duplicate PR
- maintainers welcome contributions
- scope is narrow
- local or source-backed verification is realistic
- patch/comment will reduce maintainer effort

## Minimum Evidence

Before public action, know:

- target link
- current issue/PR state
- duplicate search result
- intended help type
- validation result
- verification plan
- disclosure text
