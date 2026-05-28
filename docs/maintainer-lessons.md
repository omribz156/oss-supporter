# Maintainer Lessons

Reusable lessons from real review comments, CI surprises, and closed PRs. Keep
this public and sanitized: name public projects only when the lesson is useful.

## Before Opening

- Preserve PR template wording, legal checkboxes, DCO lines, and license
  declarations exactly when a project asks for them.
- Check project AI policies before patching. Some projects reject AI-generated
  contributions even with disclosure.
- Trace generated files back to their source templates before changing the
  visible output.
- Verify delegated-tool docs against the upstream tool, not only the wrapper
  repo.
- If a maintainer asks for a process step, do the exact small step and avoid a
  second nudge.

## During Review

- Fetch top-level reviews, inline pull comments, and issue/PR comments before
  patching a `CHANGES_REQUESTED` PR.
- Patch first, verify second, reply third.
- Keep replies concrete: what changed, what command ran, what remains blocked.
- Treat broad CI failures separately from patch-specific checks. Do not patch
  blind while logs are unavailable.
- Use body files or structured API input for multiline public text; shell
  quoting can flatten Markdown or eat backticks.

## Patterns That Repeated

- Visual examples need rendered verification. Code that looks aligned can still
  fail in the actual Storybook/demo layout.
- Regression tests should hit the original boundary. Config bugs often need
  import-time or env-loading coverage, not only downstream object mutation.
- Compatibility flags need version gates when a CLI supports older tool
  versions.
- Platform-level constraints can be wider than the reported feature path. If a
  host rejects duplicate URIs globally, dedupe against the whole host state.
- Terraform provider state fixes are design-sensitive. Preserve existing plan
  modifier conventions unless maintainers confirm a different strategy.
- Sourced shell helpers should avoid leaking strict mode or exiting the caller's
  shell.

## Public Voice Reminder

Lead with useful work, not agent theater. A good shape:

```text
Summary: <what changed>.
Verification: <what ran>.

Implemented with agent assistance and manually reviewed before submission.
```

If the venue has stricter disclosure or AI rules, follow the venue.
