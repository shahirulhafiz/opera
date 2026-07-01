---
name: validate-full-specs
description: Validates full specifications through simulation testing to identify gaps, vulnerabilities, and ambiguities. Use when reviewing specifications, testing specification quality, or identifying implementation blockers.
---
# Specification Validation & Simulation Testing

Perform comprehensive validation of full specifications through simulation testing to identify gaps, vulnerabilities, and ambiguities before implementation.

## When to Use

- After creating a full specification
- Before starting implementation
- When reviewing specification quality
- To identify potential implementation blockers
- As part of specification sign-off process

## Output Location

**File**: `docs/reports/{spec-name}-validation-report.md`

## Report Structure

### 1. Executive Summary

| Test Category | Pass/Fail/Gap | Critical Issues? |
|---------------|:-------------:|------------------|
| Business Rule Stress Testing | | |
| State Machine Validation | | |
| API & Data Integrity | | |
| Edge Case Simulation | | |
| Integration Failure Handling | | |
| Gaps & Recommendations | | |

> Highlight any showstopper vulnerabilities or design logic bombs.

### 2. Business Rule Stress Testing

Evaluate resilience of business rules through destructive simulation:

- Challenge conflicting business rules
- Attempt boundary exploits, circular logic, invalid orderings
- Document which rules withstand adversarial input
- Identify rules that break or contradict

### 3. State Machine Validation

Map and validate the implied lifecycle:

```
Draft → Submitted → Approved/Rejected
```

- Draw state diagram (markdown or ASCII)
- Simulate invalid transitions:
  - Skipping required states
  - Editing immutable/final states
  - Race conditions (simultaneous actions)
- Summarize where state enforcement is strong/weak

### 4. API & Data Integrity

Review API contracts with adversarial attempts:

- How are malformed/incomplete values handled?
- Is there anti-duplication or replay defense?
- Can orphaned data or broken relationships occur?
- Are null, empty, unexpected values considered?
- Note inconsistencies, ambiguities, missing error handling

### 5. Edge Case & "Chaos" Simulation

Push system boundaries to provoke undefined behavior:

**Temporal Anomalies:**
- Cross-timezone entries
- Server/client date mismatches
- Leap year, DST cutoffs

**Concurrency:**
- Rapid conflicting submissions
- Bulk actions
- Unusual duplicate events

**System Limits:**
- Duration overflow
- Excessive field lengths
- Large data imports

Provide evidence for discovered failures or ambiguities.

### 6. Integration Point Failure

Review behavior when external dependencies fail:

- What if user/employee data cannot be fetched?
- Do DB transaction deadlocks escalate or recover?
- Can system operate if integrations unreachable?
- Summarize gaps in error-handling and fallbacks

### 7. Gaps & Recommendations

For each gap identified:

```markdown
**Gap ID**: [Reference ID]
**Section**: [Spec section reference]

**Description:**
[What the spec says or doesn't say]

**Real-World Risk:**
[Impact if not addressed]

**Recommendation:**
[Actionable fix or clarification needed]

**Priority:** 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low

**Blocking Phase:** [Which phase is blocked, if any]
```

## Validation Categories

### Business Rules
- Conflicting rules
- Boundary conditions
- Circular dependencies
- Invalid state combinations

### State Machines
- Missing states
- Invalid transitions
- Race conditions
- Immutability violations

### Data Integrity
- Malformed input handling
- Duplicate prevention
- Orphan record handling
- Null/empty value handling
- Foreign key enforcement

### Temporal Issues
- Timezone handling
- Date boundary conditions
- Time window overlaps
- Scheduling conflicts

### Concurrency
- Race conditions
- Deadlock potential
- Batch processing limits
- Duplicate submission handling

### Integration
- External system failures
- Timeout handling
- Fallback mechanisms
- Retry strategies

## Critical Blockers

Identify issues that MUST be resolved before implementation:

- [ ] All 🔴 Critical gaps addressed
- [ ] State machine fully defined
- [ ] All API error scenarios documented
- [ ] Data validation rules complete
- [ ] Integration failure handling specified

## Follow-Up Actions

After validation:
1. Create issues clarification document for stakeholder review
2. Update specification with clarified requirements
3. Re-validate after updates
4. Proceed with implementation once critical issues resolved
