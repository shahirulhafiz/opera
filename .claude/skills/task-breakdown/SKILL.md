---
name: task-breakdown
description: Expands an approved implementation plan into granular, execution-ready tasks with atomic steps, file targets, and per-task acceptance criteria. Use after a plan is approved and before implementation.
---
# Task Breakdown

Decompose an approved implementation plan into granular, execution-ready tasks. Each task should be small enough to implement and verify in a single focused pass. This runs after plan review approval and before execution.

## When to Use

- After `review-plan` returns APPROVE or APPROVE WITH CHANGES
- Before `execute-plan` begins implementation
- When a high-level plan item is too coarse to implement directly

## Inputs

- Approved plan: `docs/plans/phase-{NN}-implementation-plan.md`
- Plan review verdict (blockers resolved)

## Output Location

**File**: `docs/plans/phase-{NN}-task-breakdown.md`

Use two-digit phase numbers: `01`, `02`, etc.

## Granularity Rules

- One task = one coherent, independently verifiable unit of work.
- Split any plan item that touches multiple layers or has more than one acceptance criterion.
- Prefer tasks that can be completed and tested without waiting on unfinished work.
- Preserve the plan's stage order and task ID prefixes (DB-, API-, UI-, INT-, PERF-, SEC-, DEPLOY-).

## Per-Task Template

```markdown
#### Task [ID]: [Name]
- **Parent plan item**: [Plan task ID]
- **Layer**: DB | API | UI | Integration | Quality | Deploy
- **Depends on**: [Task IDs] (or "none")
- **Estimated complexity**: Low | Medium | High

**Atomic steps:**
1. <single concrete action>
2. <single concrete action>

**Files to create/modify:**
- `path/to/file` — <purpose>

**Acceptance criteria:**
- [ ] <observable, testable condition>

**Verification:**
- <command or check that proves the task is done>
```

## Sequencing Output

End the document with an ordered execution list and a dependency note, so `execute-plan` can proceed top-to-bottom:

```
Execution order: DB-1 → DB-2 → API-1 → API-2 → ...
Parallelizable: [UI-1, UI-2] once API-1 is done
```

## Definition of Done (for the breakdown itself)

- [ ] Every approved plan item maps to one or more atomic tasks
- [ ] Each task has depends-on, files, acceptance criteria, and verification
- [ ] No task depends on a later task
- [ ] Execution order is explicit

## Critical Rules

- Do not introduce scope beyond the approved plan.
- Do not implement here — this step only produces the task list.
- If breakdown surfaces a plan gap or contradiction, stop and route back to `planner` / `plan-reviewer`.
