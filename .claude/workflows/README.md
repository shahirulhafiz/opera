# Workflow Definitions

This directory contains YAML workflow definitions that describe agent orchestration patterns for the project.

## Purpose

Workflows define:
- **Step sequences** - Ordered steps with dependencies
- **Agent assignments** - Which agent handles each step
- **Auto-continuation** - Steps that run automatically after others
- **Triggers** - Events that invoke workflows or steps
- **Output locations** - Where artifacts are created

## Schema Reference

### Workflow File Structure

```yaml
# workflow-name.yml
name: Human-readable workflow name
description: Brief description of what this workflow accomplishes
version: "1.0"

# Define the steps in this workflow
steps:
  - id: unique-step-id
    name: Human-readable step name
    agent: agent-name           # Which agent executes this step
    skill: skill-name           # Optional: specific skill to use
    action: "Description of what to do"
    type: auto | manual         # Default: auto. Manual requires user action
    requires: [step-id, ...]    # Steps that must complete first
    auto_continues: [step-id]   # Steps that auto-run after this one
    input: "path/to/input"      # Input file or resource
    output: "path/to/output"    # Output file or resource
    mandatory: true | false     # Whether this step can be skipped

# Define event-based triggers
triggers:
  trigger_name:
    event: after_implementation | after_fix | on_error | ...
    agent: agent-name
    skill: skill-name
    mandatory: true | false
    description: "When and why this triggers"

# Define execution rules
rules:
  - id: rule-id
    description: "Rule explanation"
    condition: "When this applies"
    action: "What must happen"
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable workflow name |
| `description` | string | Yes | What the workflow accomplishes |
| `version` | string | No | Semantic version for tracking changes |
| `steps` | array | Yes | Ordered list of workflow steps |
| `triggers` | object | No | Event-based automatic invocations |
| `rules` | array | No | Behavioral rules and constraints |

### Step Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (kebab-case) |
| `name` | string | Yes | Human-readable name |
| `agent` | string | Yes* | Agent that executes this step |
| `skill` | string | No | Specific skill to invoke |
| `action` | string | No | Description of the action |
| `type` | string | No | `auto` (default) or `manual` |
| `requires` | array | No | Step IDs that must complete first |
| `auto_continues` | array | No | Steps that auto-run after completion |
| `input` | string | No | Input file path (supports `{placeholders}`) |
| `output` | string | No | Output file path (supports `{placeholders}`) |
| `mandatory` | boolean | No | Whether step can be skipped |

*Not required for `type: manual` steps

### Path Placeholders

Use placeholders in `input` and `output` paths:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{project-name}` | Current project name | `novelist` |
| `{NN}` | Two-digit phase number | `01`, `02` |
| `{name}` | Dynamic name from context | `auth-module` |

## Available Workflows

| File | Purpose |
|------|---------|
| `project-lifecycle.yml` | **Source of truth** - Agent definitions + project workflow |
| `full-spec-pipeline.yml` | Specification creation with auto-validation |
| `implementation-stages.yml` | Code implementation execution order |
| `completion-rules.yml` | Mandatory completion report triggers |
| `rules.yml` | Global rules and conventions |

## Agent Definitions

All agents are defined in `project-lifecycle.yml` under the `agents:` section. This is the single source of truth for:
- Agent purpose and capabilities
- When to use each agent
- Invocation templates
- Skills and outputs

To add or modify an agent, edit `project-lifecycle.yml`.

## Usage

Workflows are referenced in `AGENTS.md` and guide agent orchestration. When invoking an agent, consult the relevant workflow to understand:

1. What steps precede and follow the current action
2. Which artifacts are expected as input/output
3. What triggers or rules apply

### Example: Following a Workflow

```
# User wants to start a new project

1. Check project-lifecycle.yml for the workflow
2. Step 1 says: agent=spec-writer, which auto_continues to validation
3. Invoke spec-writer agent
4. Agent automatically runs validation and clarification steps
5. Proceed to next manual step (user review)
```

## Conventions

- **File naming**: `kebab-case.yml`
- **Step IDs**: `kebab-case`
- **Phase numbers**: Two digits (`01`, `02`, not `1`, `2`)
- **Paths**: Use forward slashes, lowercase with hyphens
