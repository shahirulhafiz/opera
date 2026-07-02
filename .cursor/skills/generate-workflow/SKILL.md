---
name: generate-workflow
description: Create and generate new orchestration workflows for the .claude harness. Scaffolds a workflow YAML from the template, validates it, and registers it in registry.yml. Use when the user asks to create, generate, add, or edit a workflow, cycle, pipeline, route, or the registry.
---

# Generate Workflow

Guide the user to create a runnable **workflow** for the orchestration harness. A
workflow is **one YAML file** in `.claude/workflows/` plus **one route** in
`.claude/workflows/registry.yml`. No orchestrator code changes are needed.

Canonical terms live in `.claude/GLOSSARY.md` — **workflow** is the noun;
"cycle"/"pipeline" are human synonyms only (fine as `match.intent` keywords).

## Quick Start

Copy this checklist and track progress:

```
Workflow Progress:
- [ ] Step 1: Gather intent (keywords + ordered steps + gates)
- [ ] Step 2: Scaffold {id}.yml from the template
- [ ] Step 3: Validate the new file (must exit 0)
- [ ] Step 4: Register the route in registry.yml (upsert)
- [ ] Step 5: Re-validate the full config (must exit 0)
- [ ] Step 6: Report the route, file path, and validator output
```

## Step 1: Gather Intent

Ask (or infer) these before writing anything:

- **Trigger keywords** → `match.intent` (the words that route a request here).
- **Ordered steps** → each step's `agent` and optional `skill`.
- **Gates** → any step whose next step depends on a verdict (approve/revise).

Every step's `agent` and `skill` must **already exist** under `.claude/agents/`
and `.claude/skills/`. If a needed capability is missing, say so — do not invent
a route that cannot run.

## Step 2: Scaffold

Copy `.claude/workflows/_template.yml` to `.claude/workflows/{id}.yml` and fill
in `match`, `steps`, and any gates. Use the template's shape:

```yaml
name: My Workflow
description: One-line summary of what this workflow accomplishes.

match:
  intent: [keyword, another-keyword]
  priority: 50

steps:
  - id: build
    type: agent                 # optional; `agent` is the default step type
    agent: implementer          # required for agent steps; must exist under .claude/agents/
    skill: execute-plan         # optional; must exist under .claude/skills/
    action: Do the first thing.
    mandatory: true

  - id: review
    agent: code-reviewer
    requires: [build]
    verdict_contract: ["APPROVE", "REVISE"]   # exact tokens the agent emits
    max_retries: 2
    on_complete:
      APPROVE: { next: done }
      REVISE: { next: build }

  - id: done
    agent: test-expert
    requires: [review]
```

**Step types** (`type`, default `agent`): use `type: manual` for a step that
**escalates to the user** (decision/approval) instead of spawning an agent.

Rules for gated steps: every `on_complete` **requires** a `verdict_contract`
(the exact `VERDICT: <token>` tokens the step's agent emits) and `max_retries`.

## Step 3: Validate (incremental)

Run the validator on the new file only. Proceed **only on exit 0**:

```bash
python .claude/skills/validate-config/scripts/validate_config.py .claude/workflows/{id}.yml
```

Never register a file that fails validation.

## Step 4: Register (upsert)

Add an `enabled` route to `.claude/workflows/registry.yml`. If a route with the
same `id` already exists, **edit it in place** — never duplicate:

```yaml
routes:
  - id: my-workflow
    workflow: my-workflow.yml
    description: What this workflow does
    match: { intent: [keyword, another-keyword], priority: 50 }
    enabled: true
```

## Step 5: Re-validate (full)

Run the validator with no argument and expect exit 0:

```bash
python .claude/skills/validate-config/scripts/validate_config.py
```

## Step 6: Report

Report the new/updated route, the workflow file path, and the validator output.

## Hard Rules

- **Validate before registering.** Only exit 0 proceeds.
- **Upsert, never duplicate** a route id in `registry.yml`.
- **Recursion guard:** a workflow step may never spawn `orchestrator` or
  `workflow-author`.
- **Only real capabilities:** every `agent`/`skill` referenced must already exist.
- `_`-prefixed files (e.g. `_template.yml`) are non-routable templates — never add
  them to `registry.yml`.
