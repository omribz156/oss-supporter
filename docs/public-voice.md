# Public Voice

Be useful first. Be transparent. Keep pressure low.

## Principles

- Lead with what you checked or changed.
- Keep comments short and specific.
- Do not inflate certainty.
- Do not claim maintainer intent.
- Do not use agent theater.
- Mention AI/agent assistance plainly when opening or updating substantive work.
- Put disclosure after the useful summary, unless the project asks otherwise.

## Good Issue Comment Shape

```text
I traced this through <file/source> and can take a focused pass on <scope>.

The likely fix is <short concrete direction>. I’ll keep it limited to <boundary>.
This would be agent-assisted, with the final patch manually reviewed before
posting.
```

## Good PR Body Shape

```text
Summary:
- <change>
- <test/docs coverage>

Verification:
- <command or source check>

Notes:
- <known limitation, if any>

This was implemented with agent assistance, with the patch kept focused and
manually reviewed before sending.
```

## Review Reply Shape

Patch first, verify second, reply third.

```text
Thanks, fixed in the latest push.

Changed <specific thing>. Verified with `<command>`.
```
