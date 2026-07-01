---
name: issues-clarification
description: Extracts issues and ambiguities from validation reports and creates structured clarification documents. Use when processing validation reports, creating clarification requests, or documenting specification gaps.
---
# Issues Clarification Document Generator

Extract all issues, gaps, and ambiguities from validation reports and create structured clarification documents for stakeholder review.

## When to Use

- After running specification validation
- When gaps or ambiguities are identified
- Before implementation to resolve unclear requirements
- When stakeholder input is needed on design decisions

## Output Structure

### Header Section
```markdown
# Clarification Request: [Specification Name]

**Document Type**: Clarification Request
**Created Date**: [TODAY]
**Source**: [VALIDATION_REPORT_PATH]
**Status**: Pending User Response
```

### Purpose Statement
Brief explanation that this document lists gaps requiring stakeholder clarification before implementation.

### Issue Priority Levels

| Priority | Emoji | Criteria | Action Required |
|----------|-------|----------|-----------------|
| Critical | 🔴 | Blocks implementation | Must resolve before that phase |
| High | 🟠 | Causes ambiguity/bugs | Should resolve before implementation |
| Medium | 🟡 | Documentation issue | Can decide during implementation |
| Low | 🟢 | Nice-to-have clarification | Optional |

### Issue Format

For each issue include:

```markdown
**Issue #[N]: [Descriptive Title]**

**Priority:** 🔴 CRITICAL / 🟠 HIGH / 🟡 MEDIUM ([Impact])
**Gap ID:** [Reference from validation report]

**Current Situation:**
[What the spec currently says or doesn't say]

**Questions for Clarification:**
[Numbered questions with checkbox options]

- [ ] Option A: [Description]
- [ ] Option B: [Description]
- [ ] Option C: [Description]
- [ ] Other: _______________

**Proposed Solution (if applicable):**
[Recommended approach if clear best practice exists]

**Risk if Not Addressed:**
[Business impact of leaving undefined]

**Example Scenario (if helpful):**
[Real-world example illustrating the issue]
```

### Summary Response Form

```markdown
| Issue # | Priority | Your Decision | Notes |
|---------|----------|---------------|-------|
| #1 - [Title] | [Priority] | | |
| #2 - [Title] | [Priority] | | |
```

### Next Steps Section
1. Stakeholders review and provide decisions
2. Update specification with clarified requirements
3. Re-validate specification after updates
4. Proceed with implementation once critical issues resolved

## Issue Categories to Look For

1. **State Machine Gaps** - Missing states, undefined transitions
2. **Business Rule Ambiguity** - Vague rules, undefined boundaries
3. **Validation Rules** - Unclear input handling, edge cases
4. **Data Integrity** - Duplicate handling, FK validation, orphaned data
5. **Temporal Issues** - Timezone, date boundaries, time windows
6. **Concurrency** - Race conditions, batch limits
7. **Integration** - External system failures, fallback behavior
8. **Error Handling** - Missing error codes, retry strategies
9. **Performance** - Rate limits, batch sizes, timeouts

## Formatting Rules

- Use horizontal rules (---) between major sections
- Use checkboxes [ ] for all options
- Include "Other: _______________" option where appropriate
- Add blank lines for readability
- Use emoji indicators for priority levels
- Keep questions clear and actionable

## Completion Checklist

- [ ] All gaps from validation report are included
- [ ] Each issue has clear questions with options
- [ ] Priority levels assigned correctly
- [ ] Blocking relationships to implementation phases noted
- [ ] Summary table includes all issues
- [ ] Next steps section included
- [ ] Document formatted consistently
