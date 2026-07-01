---
name: completion-report
description: Generates comprehensive completion reports after finishing a phase implementation. Use when a phase is complete, all tests pass, and documentation of what was accomplished is needed.
---
# Phase Completion Report Generator

Generate a comprehensive completion report documenting what was accomplished, lessons learned, deviations from plan, and context for the next phase.

## When to Use

- After all phase tasks are completed
- After all tests are passing
- After deployment (if applicable)
- Before starting the next phase
- When the user explicitly requests implementation documentation

Do not use for small, routine fixes unless explicitly requested.

## Prerequisites

- ✅ Phase implementation is complete
- ✅ All tests are passing
- ✅ Scoped specification exists (`docs/specs/phase-{NN}/`)
- ✅ Implementation plan exists (`docs/plans/phase-{NN}-implementation-plan.md`)
- ✅ Full specification exists (`docs/{project-name}-full-spec.md`)

For non-phase changes, require explicit user request before generating a report.

## Output Location

**File**: `docs/reports/phase-{NN}-completion-report.md`

Use two-digit phase numbers: `01`, `02`, `03`, etc.

## Report Structure

### Header
```markdown
# Completion Report: Phase [N] - [Phase Name]

**Date Completed**: [Current Date]
**Phase**: [Phase Number/Name]
**Status**: ✅ Completed

**Reference Documents:**
- Full Spec: [Link]
- Scoped Spec: [Link to folder]
- Implementation Plan: [Link]
```

### Required Sections

1. **Executive Summary**
   - Phase overview and key deliverables
   - Key achievements (3-5 major accomplishments)
   - Key metrics (duration, tasks completed, test coverage)

2. **What Was Implemented**
   - Database Layer (tables, migrations, ORM models)
   - API Layer (endpoints, auth, error handling)
   - UI Layer (components, pages, navigation)
   - Testing (coverage, test results)
   - Deployment (if applicable)

3. **What Went Well**
   - Technical successes
   - Process successes
   - Tools and technologies that worked well

4. **What Changed vs. Spec**
   - Scope changes (added/removed features)
   - Technical changes (stack, architecture)
   - Database/API/UI changes

5. **Challenges and Solutions**
   - Technical challenges with resolutions
   - Integration challenges
   - Performance/security challenges

6. **Lessons Learned**
   - What to repeat in next phases
   - What to avoid in next phases
   - Process and documentation improvements

7. **Quality Metrics**
   - Code quality (linter, coverage)
   - Performance metrics
   - Security metrics

8. **Known Issues and Technical Debt**
   - Known bugs with severity and workarounds
   - Technical debt items with priority
   - Missing features (deferred)

9. **Recommendations for Next Phase**
   - Technical recommendations
   - Specification improvements
   - Testing/deployment recommendations

10. **Context for Next Phase**
    - Components to build upon
    - Constraints and limitations
    - Dependencies to maintain

11. **Full Spec Updates Required**
    - Sections to update
    - New information to add

12. **Appendices**
    - File structure
    - Dependencies
    - Configuration files
    - Environment variables

## Critical Guidelines

### Completeness
- Be thorough and honest about accomplishments
- Document all deviations, not just successful ones
- Provide specific examples, not generic statements

### Context for Next Phase
- Next phase scoped spec MUST reference this report
- Lessons learned should inform next phase planning
- Known issues should be considered in next phase scope

### Honesty and Accuracy
- Report actual metrics, not ideal metrics
- Document challenges faced, not just successes
- Acknowledge when original plans were incomplete

## Document Flow

```
Full Specification (Overall Vision)
        ↓
Phase N Scoped Spec (Detailed Design)
        ↓
Phase N Implementation Plan (Execution Guide)
        ↓
Phase N Implementation (Actual Work)
        ↓
Phase N Completion Report ← YOU ARE HERE
        ↓
Phase N+1 Scoped Spec (Uses this report as context)
```

This completion report is the bridge between phases, ensuring learning and context flow forward.
