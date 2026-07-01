---
name: check-phase
description: Verifies phase completion reports against scoped specifications and validates readiness for the next phase. Use when reviewing a completed phase, checking phase completion status, or validating next phase prerequisites.
---
# Phase Completion Verification

Verify that a phase completion report satisfies all requirements from its scoped specification and confirms readiness for the next phase based on the full specification.

## When to Use

- After a phase implementation is complete
- Before starting a new phase
- When reviewing completion report quality
- To validate readiness for next phase

## Instructions

When verifying phase completion (e.g., for Phase 01), perform the following:

### Step 1: Load Required Documents

Read these documents in order:

1. **Full Specification**: `docs/{project-name}-full-spec.md`
   - Extract phase definitions from Section 4 "Phases Breakdown"
   - Identify current phase goals, UI/API/Database requirements
   - Identify next phase prerequisites and dependencies

2. **Scoped Specification**: `docs/specs/phase-{NN}/` (folder, staged loading)
   - Start with:
     - `00-overview.md` - Phase goals and success criteria
     - `07-checklist.md` - Checklist items and deliverables
   - Load additional files only when verifying their area:
     - `01-ui-design.md` - UI screens/components
     - `02-api-design.md` - API endpoints
     - `03-database-design.md` - Database tables
     - `04-integrations.md` - Integration requirements
     - `05-testing.md` - Testing requirements
     - `06-non-functional.md` - NFR requirements

3. **Completion Report**: `docs/reports/phase-{NN}-completion-report.md`
   - What was actually implemented
   - Deferred items or scope changes
   - Known issues and technical debt
   - Recommendations for next phase

### Step 2: Verify Scoped Spec Satisfaction

Create a verification checklist comparing the Scoped Spec against the Completion Report:

#### 2.1 Success Criteria Verification
For each success criterion:
- ✅ SATISFIED if explicitly confirmed in completion report
- ⚠️ PARTIAL if partially implemented with noted limitations
- ❌ NOT MET if missing or explicitly deferred

#### 2.2 Deliverables Verification
- Verify each deliverable exists in "What Was Implemented" section
- Note any scope changes or modifications

#### 2.3 API/Database/UI Verification
- Verify all specified endpoints, tables, and components are implemented
- Note any changes or additions

### Step 3: Verify Next Phase Prerequisites

Check the Full Specification for Phase {NN+1} requirements:

- All database tables required by next phase exist
- All API endpoints required by next phase are available
- All UI components required by next phase are ready
- No blocking technical debt for next phase

### Step 4: Generate Verification Report

Output a structured report:

```markdown
# Phase {NN} Completion Verification Report

**Verification Date**: {current date}
**Phase**: {NN} - {Phase Name}
**Status**: ✅ READY FOR NEXT PHASE | ⚠️ CONDITIONAL PASS | ❌ BLOCKING ISSUES

## 1. Scoped Specification Compliance

### Success Criteria
| Criterion | Status | Notes |
|-----------|--------|-------|
| {criterion} | ✅/⚠️/❌ | {notes} |

**Compliance Score**: X/Y criteria met (Z%)

### Deliverables
| Deliverable | Status | Notes |
|-------------|--------|-------|
| {deliverable} | ✅/⚠️/❌ | {notes} |

## 2. Next Phase Readiness (Phase {NN+1})

### Prerequisites Check
| Prerequisite | Status | Blocking? |
|--------------|--------|-----------|
| {prereq} | ✅/❌ | Yes/No |

## 3. Summary

### What's Ready
- {list of ready items}

### What Needs Attention
- {list of items needing attention}

### Recommendations Before Starting Phase {NN+1}
1. {recommendation}

## 4. Verdict

**Phase {NN} Completion Status**: {COMPLETE/INCOMPLETE}
**Ready for Phase {NN+1}**: {YES/CONDITIONAL/NO}
```

### Step 5: Provide Actionable Next Steps

Based on the verification:
1. **If READY**: Suggest starting Phase {NN+1} scoped spec creation
2. **If CONDITIONAL**: List specific items to address before proceeding
3. **If BLOCKING**: Identify critical fixes needed

## Notes

- Always use two-digit phase numbers (01, 02, etc.)
- If scoped spec folder doesn't exist, report that verification cannot proceed
- If completion report doesn't exist, report phase is not yet complete
- Cross-reference with full spec for overall project vision alignment
