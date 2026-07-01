---
name: execute-plan
description: Systematically executes implementation plans phase by phase with validation at each step. Use when implementing a phase, executing tasks from an implementation plan, or building features according to specifications.
---
# Implementation Plan Execution

Systematically execute an implementation plan phase by phase, task by task, ensuring thorough completion with proper testing and documentation.

## When to Use

- When starting phase implementation
- When executing tasks from an implementation plan
- When building features according to specifications

## Prerequisites

- ✅ Scoped specification exists (`docs/specs/phase-{NN}/`)
- ✅ Implementation plan exists (`docs/plans/phase-{NN}-implementation-plan.md`)
- ✅ Full specification exists (`docs/{project-name}-full-spec.md`)
- ✅ Development environment is set up
- ✅ Version control initialized with clean working directory

## Scoped Specification Files

Use staged loading from `docs/specs/phase-{NN}/` instead of reading everything up front:
- `00-overview.md` - Phase overview & context
- `01-ui-design.md` - UI/UX specifications
- `02-api-design.md` - API endpoints & contracts (🔒 LOCKED)
- `03-database-design.md` - Database schema (🔒 LOCKED)
- `04-integrations.md` - Integration points
- `05-testing.md` - Testing requirements
- `06-non-functional.md` - NFRs, security, performance
- `07-checklist.md` - Implementation checklist

### Minimum Initial Read Set
- `00-overview.md`
- `07-checklist.md`
- `docs/plans/phase-{NN}-implementation-plan.md`

### Stage-Based Reads
- Database stage: add `03-database-design.md`
- API stage: add `02-api-design.md`
- Frontend stage: add `01-ui-design.md`
- Integration stage: add `04-integrations.md`
- Test/quality stage: add `05-testing.md`, `06-non-functional.md`

If requirements are ambiguous, escalate by loading the next relevant spec file, not all files.

## Execution Phases

### 1. Preparation Phase
- Read minimum initial set
- Review the entire implementation plan
- Understand technology stack and tools
- Note all dependencies and versions

### 2. Execution Phase - Work Sequentially

**Stage Order:**
1. **Database** (DB-1 → DB-2 → DB-3 → DB-4)
2. **API Foundation** (API-1 → API-4, API-5)
3. **Authentication** (API-2)
4. **API Endpoints** (API-3+)
5. **Frontend Foundation** (UI-1 → UI-2)
6. **Frontend Features** (UI-3 → UI-5 → UI-4)
7. **Integration Testing** (INT-1 → INT-2 → INT-3)
8. **Performance & Security** (PERF-1, PERF-2, SEC-1)
9. **Deployment** (DEP-1 → DEP-2 → DEP-3)

**For Each Task:**
1. Read all sections (Description, Steps, Implementation Details)
2. Refer to the stage-relevant scoped spec files for context
3. Write complete, production-ready code (no placeholders)
4. Include all error handling
5. Add appropriate comments
6. Create all files listed in "Files to Create"
7. Run all validation steps
8. Verify all acceptance criteria are met
9. Mark task as complete

### 3. Integration Phase
- Run integration tests after completing feature tasks
- Verify components work together
- Fix any integration issues

### 4. Quality Phase
- Run performance tests
- Run security tests
- Optimize as needed
- Verify all quality metrics

### 5. Completion Phase
- Deploy (if applicable)
- Run smoke tests
- Write completion report

## Critical Guidelines

| Guideline | Description |
|-----------|-------------|
| **Be Complete** | Write full, working code - no "TODO" or placeholder comments |
| **Follow Specs Exactly** | Implement what's specified, nothing more or less |
| **Test Everything** | Run validation steps after every task |
| **Handle Errors** | Every function should handle potential errors |
| **Use Latest Stable** | Install latest stable versions of packages |
| **Document Clearly** | Update README, add code comments, document APIs |
| **Stay Sequential** | Respect dependencies, complete tasks in order |

## Common Pitfalls to Avoid

- ❌ Skipping validation steps
- ❌ Starting UI before API is done
- ❌ Skipping tests
- ❌ Adding features not in scoped spec
- ❌ Poor error handling
- ❌ Inadequate documentation
- ❌ Not testing integrations
- ❌ Hardcoding values (use environment variables)
- ❌ Creating placeholder code

## Definition of Done

### Task Level
- [ ] Code written and follows standards
- [ ] Unit tests written and passing
- [ ] No linter errors
- [ ] Documentation updated
- [ ] Validation steps completed
- [ ] All acceptance criteria met

### Phase Level
- [ ] All features completed
- [ ] All tests passing (>80% coverage)
- [ ] Performance requirements met
- [ ] Security audit passed
- [ ] Documentation complete
- [ ] Completion report written
