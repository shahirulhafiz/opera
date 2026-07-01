---
name: implementation-plan
description: Creates detailed implementation plans from scoped specifications with task breakdowns and dependencies. Use when creating a phase implementation plan, planning development tasks, or preparing for phase execution.
---
# Implementation Plan Generator

Generate a detailed, actionable implementation plan for a specific phase based on the scoped specification. The plan breaks down UI, API, and Database designs into concrete tasks with sequences, dependencies, and acceptance criteria.

## When to Use

- After scoped specification is complete
- Before starting phase implementation
- When planning development tasks
- Preparing for AI-autonomous implementation

## Prerequisites

- ✅ Full specification exists (`docs/{project-name}-full-spec.md`)
- ✅ Scoped specification complete (`docs/specs/phase-{NN}/`)
- ✅ Development environment requirements specified
- ✅ Dependencies and versions identified

## Output Location

**File**: `docs/plans/phase-{NN}-implementation-plan.md`

Use two-digit phase numbers: `01`, `02`, `03`, etc.

## Plan Structure

### Header Information
```markdown
# Implementation Plan: Phase [N] - [Phase Name]

**Date**: [Current Date]
**Phase**: [Phase Number/Name]
**Status**: Draft/Ready/In Progress/Completed
**Implementation Mode**: AI-Autonomous

**Reference Documents:**
- Full Spec: [Link]
- Scoped Spec: [Link to folder]
```

### Required Sections

#### 1. Implementation Overview
- Phase goals (from scoped spec)
- Implementation scope (DB, API, UI, Testing)
- Development environment details
- Required tools and versions

#### 2. Database Implementation Plan
Tasks: DB-1 → DB-2 → DB-3 → DB-4

| Task | Description | Complexity |
|------|-------------|------------|
| DB-1 | Environment Setup | Low |
| DB-2 | Migration Scripts | Medium |
| DB-3 | Seed Data | Low |
| DB-4 | Data Access Layer | Medium-High |

#### 3. API Implementation Plan
Tasks: API-1 → API-4/5 → API-2 → API-3+

| Task | Description | Complexity |
|------|-------------|------------|
| API-1 | Project Setup | Medium |
| API-2 | Auth System | High |
| API-3 | Endpoints | Medium |
| API-4 | Error Handling | Medium |
| API-5 | Security | Medium |

#### 4. UI Implementation Plan
Tasks: UI-1 → UI-2 → UI-3 → UI-5 → UI-4

| Task | Description | Complexity |
|------|-------------|------------|
| UI-1 | Project Init | Medium |
| UI-2 | Design System | High |
| UI-3 | Auth UI | High |
| UI-4 | Features | Medium-High |
| UI-5 | Navigation | Medium |
| UI-6 | Error Handling | Medium |

#### 5. Integration & Testing Plan
- INT-1: API-Database integration
- INT-2: UI-API integration
- INT-3: End-to-end testing
- PERF-1/2: Performance testing
- SEC-1: Security audit

#### 6. Deployment Plan
- DEP-1: Database deployment
- DEP-2: API deployment
- DEP-3: UI deployment
- POST-1: Monitoring setup
- POST-2: Smoke tests

## Task Structure Template

For each task include:

```markdown
#### Task [ID]: [Name]
- **Description**: What this task accomplishes
- **Component**: Which layer/system
- **Estimated Complexity**: Low/Medium/High
- **Dependencies**: Which tasks must complete first
- **Reference**: Scoped Spec section reference

**Steps:**
1. Step with exact details
2. Step with exact details

**Files to Create:**
- File paths with purpose

**Implementation Details:**
- Specific technical details
- Configuration requirements

**Validation Steps:**
1. How to verify this works
2. Commands to run

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
```

## Implementation Sequence

```
Stage 1: Database      [DB-1 → DB-4]
Stage 2: API Base      [API-1 → API-4, API-5]
Stage 3: Auth          [API-2]
Stage 4: API Endpoints [API-3+]
Stage 5: Frontend Base [UI-1 → UI-2]
Stage 6: Frontend Full [UI-3 → UI-6]
Stage 7: Integration   [INT-1 → INT-3]
Stage 8: Perf/Security [PERF-1, PERF-2, SEC-1]
Stage 9: Deployment    [DEP-1 → DEP-3]
```

**Critical Path**: DB → API Base → Auth → Endpoints → Frontend → Integration → Testing → Deployment

## Quality Standards

### Testing Requirements
- Unit Tests: >80% coverage
- Integration Tests: All API endpoints
- E2E Tests: All critical user flows

### Success Metrics
- Code coverage > 80%
- API response time < 200ms (p95)
- Page load time < 3s
- Lighthouse score > 90
- Zero critical security vulnerabilities

## Definition of Done

### Task Level
- [ ] Code follows standards
- [ ] Tests passing
- [ ] No linter errors
- [ ] Documentation updated
- [ ] Acceptance criteria met

### Phase Level
- [ ] All features completed
- [ ] All tests passing
- [ ] Performance met
- [ ] Security audit passed
- [ ] Completion report written
