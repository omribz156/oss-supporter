# Lifecycle Case Study: VS Code DocumentDB

Public example of the OSS Supporter loop. This is a sanitized case study built
from public GitHub state, not private transcripts.

## 1. Scout

The target was a focused bug in
[`microsoft/vscode-documentdb#660`](https://github.com/microsoft/vscode-documentdb/issues/660):
new playground documents could collide on file names.

Why it survived validation:

- active Microsoft OSS repo
- concrete user-facing bug
- small implementation boundary
- normal public PR path
- no duplicate PR covering the same fix

## 2. Slice

The work was recorded privately as a small slice with:

- target links
- intended help
- validation notes
- verification commands
- public-action receipt

The slice was not published directly because it contained local workbench paths
and private operator notes.

## 3. Patch

The PR added duplicate-name handling where playground documents are created.

Public PR:
[`microsoft/vscode-documentdb#664`](https://github.com/microsoft/vscode-documentdb/pull/664)

## 4. Review

Maintainers accepted the core direction, then pushed follow-up commits expanding
the fix to cover all open text documents and another playground entry point.

Lesson:

> Filename/URI collision fixes must cover the host boundary, not only the
> feature-specific path that exposed the bug.

## 5. Outcome

The PR merged on 2026-05-27. The maintainer follow-up made the fix broader than
the first patch, which is a good outcome: the original support reduced the
maintainer's search space, and the maintainer landed the product-correct shape.

## 6. Reusable Pattern

For editor/tooling bugs:

- identify the host-level invariant
- search sibling entry points
- avoid assuming the failing feature owns the whole constraint
- keep verification honest when only part of the platform is locally runnable
