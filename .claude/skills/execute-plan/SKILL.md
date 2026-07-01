---
name: execute-plan
description: Systematically implements a change task by task with validation at each step. Works from an explicit plan when one exists, or directly from the request. Use when building or changing features.
---
# Execute Plan

Implement work systematically, one task at a time, with validation and tests at
each step. This skill is self-contained: it works whether or not a formal plan
document exists.

## When to Use

- Building a new feature or making a change.
- Executing tasks from a plan, task list, or issue.
- Running the `execute` step of a workflow or the ad-hoc route.

## Inputs (use whatever is available)

- An explicit plan / task breakdown, if one was provided.
- Otherwise, the user's request plus the current state of the codebase.
- Relevant existing code, tests, and conventions (read on demand, not all up front).

If requirements are ambiguous, resolve the smallest next unknown by reading the
relevant file — don't stall, and don't invent scope that wasn't asked for.

## Execution Loop

1. **Scope** — restate the goal and list the concrete tasks in dependency order.
   For a small change this may be a single task.
2. **Implement** — for each task:
   - Read the code you're about to change and its immediate neighbors.
   - Write complete, production-ready code — no placeholders or `TODO`s.
   - Handle errors; don't hardcode secrets/config (use env vars).
   - Match the existing style and conventions of the file/project.
3. **Validate** — run the build/linter and the relevant tests after each task.
   Fix what you broke before moving on.
4. **Verify** — confirm the task's acceptance criteria (or the request's intent)
   are actually met.
5. **Repeat** in order, respecting dependencies.

## Definition of Done

- [ ] Code written, complete, and consistent with project conventions
- [ ] Errors handled; no hardcoded secrets/config
- [ ] Relevant tests written/updated and passing
- [ ] No linter/build errors
- [ ] Acceptance criteria / request intent satisfied
- [ ] Docs or comments updated where behavior changed

## Pitfalls to Avoid

- ❌ Placeholder code or `TODO`s left behind
- ❌ Skipping validation or tests
- ❌ Adding features not requested
- ❌ Poor error handling or hardcoded values
- ❌ Reading the whole codebase up front instead of on demand
