# Operating Model

OSS Supporter is a small-loop workflow for agent-assisted open source help.
It works with any model, shell, editor, operating system, or hosting platform.

## Roles

- Operator: the person accountable for judgment and public action.
- Agent: any assistant or automation helping inspect, patch, test, or summarize.
- Scout: a narrow research pass that finds candidates or checks status.
- Maintainer: the project owner/reviewer whose time we are trying to save.

## Loop

1. Scout for a lead.
2. Run reject checks before heavy work.
3. Claim the lead in the private workbench.
4. Create a work slice.
5. Reproduce or source-check the issue.
6. Patch or comment only if it reduces maintainer burden.
7. Verify at a depth matching the risk.
8. Publish with clear scope and disclosure.
9. Watch review and CI.
10. Record outcomes and reusable lessons.

## Work Types

- Comment: source-backed triage, reproduction, duplicate trace, or support note.
- Docs: focused correction or missing workflow detail.
- Test: narrow regression or coverage for an accepted behavior.
- CI: small broken workflow or lint fix.
- Code: low-risk behavior fix with focused tests.

## Relationship Projects

Balance one-shot help with a small set of relationship projects. These are repos
where repeated useful help is welcome and setup cost drops over time.

Rules:

- still run validation gates
- still disclose assistance
- still keep patches scoped
- do not assume trust means product-direction freedom

## Stop Conditions

Stop or ask before:

- legal/account actions
- live security probing
- paid/commercial scope
- large refactors
- product decisions
- private maintainer contact
- heavy setup for tiny value
