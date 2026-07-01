---
name: review-plan
description: Audits an implementation plan against its source specification before execution. Use when reviewing a drafted plan, gating a plan for approval, or validating readiness for task breakdown.
allowed-tools: Read, Grep, Glob
---
# Implementation Plan Review

Audit a drafted implementation plan for completeness, feasibility, and alignment with its source specification. This is a read-only gate that runs after planning and before task breakdown or execution.

## When to Use

- After `implementation-plan` produces a plan draft
- Before breaking the plan into detailed tasks
- Before an implementer starts executing
- When a plan changed materially and needs re-approval

## Inputs

- Plan under review: `docs/plans/phase-{NN}-implementation-plan.md`
- Source spec: `docs/specs/phase-{NN}/` and/or `docs/{project-name}-full-spec.md`

Load spec files on demand (overview + checklist first, then targeted sections) rather than reading everything up front.

## Review Checklist

### 1. Spec Coverage
- [ ] Every spec requirement maps to at least one task
- [ ] No task introduces scope not present in the spec
- [ ] 🔒 LOCKED API/DB designs are respected, not silently changed

### 2. Task Quality
- [ ] Each task has a clear description and component/layer
- [ ] Each task has concrete, testable acceptance criteria
- [ ] Each task lists files to create/modify
- [ ] Validation steps are defined per task

### 3. Sequencing & Dependencies
- [ ] Dependencies are explicit and acyclic
- [ ] No task depends on a later task
- [ ] Stage order is respected (DB → API → UI → Integration → Quality → Deploy)

### 4. Risk & Testability
- [ ] Cross-module, migration, security, and integration risks are flagged
- [ ] Test strategy exists for each deliverable (unit / integration / e2e)
- [ ] Non-functional requirements (perf, security) have owning tasks

## Output

Produce an inline review report (do not edit the plan):

```markdown
# Plan Review: Phase {NN}

**Verdict**: APPROVE | APPROVE WITH CHANGES | REVISE

## 🔴 Blockers
- [TASK-ID] <what is missing/broken and why it blocks execution>

## 🟡 Concerns
- [TASK-ID] <what should improve>

## 🟢 Strengths
- <well-formed parts worth keeping>

## Coverage Gaps
- <spec requirements with no owning task>
```

## Verdict Rules

- **APPROVE** — No blockers, coverage complete, acceptance criteria testable.
- **APPROVE WITH CHANGES** — Only concerns; safe to proceed after minor edits.
- **REVISE** — One or more blockers, or unmapped spec requirements. Return to `planner`.

## Critical Rules

- Read-only: never modify the plan; hand findings back to the planner.
- Reference specific task IDs for every finding.
- Do not approve a plan with unmapped requirements or ambiguous acceptance criteria.
