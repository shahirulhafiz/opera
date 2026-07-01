---
name: monitor-business-logic
description: Use when debugging logical errors, business rule violations, or wrong outputs where no crash occurs.
allowed-tools: Read, Grep
---
# Business Logic Interpretation Protocol (Compatibility Router)

This skill is retained for backward compatibility.
For all new workflows, route business-logic analysis to `monitor-logic` to avoid duplicate prompt loading.

## Routing Rule

- If called directly, perform the same analysis protocol as `monitor-logic`.
- Prefer replacing invocation with `monitor-logic` in agents/workflows.