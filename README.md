# Orchestral Harness

A hands-off agent-orchestration template for Claude Code / Cursor. Describe what
you want in plain language; a generic **orchestrator** agent routes the request
to the right workflow and runs it end-to-end, spawning specialist subagents in a
gated sequence. No `@agent` or skill tagging. New workflows are added
declaratively — one YAML file plus one registry entry — with no change to the
orchestrator.

> This is a starter template. It ships with the engine and a small set of worker
> agents, but **no concrete workflow** — every request uses the built-in ad-hoc
> route until you author one.

## How to use it

Just describe the work. Routing is automatic:

- **Trivial edit** (~≤15 lines / one file) → handled directly, no orchestration.
- **Feature / change / bug / multi-file** → the `orchestrator` selects the
  matching workflow from [.claude/workflows/registry.yml](.claude/workflows/registry.yml).
  Since the registry ships routeless, it runs the built-in **ad-hoc route**:
  `implementer → code-reviewer + test-expert → debugger`.
- **Mention a "workflow / cycle / pipeline / route"** → the `workflow-author`
  agent scaffolds it from the template, validates it, and registers it.

## What's in the box

- **Agents** (`.claude/agents/`): `orchestrator`, `workflow-author`,
  `implementer`, `code-reviewer`, `test-expert`, `debugger`.
- **Skills** (`.claude/skills/`): `author-workflow`, `validate-config`,
  `execute-plan`, `tdd-repro`, `monitor-logic`, `log-parser`.
- **Workflows** (`.claude/workflows/`): `registry.yml` (routing source of truth,
  routeless by default), `_template.yml` (copy-to-create a cycle), and
  [README.md](.claude/workflows/README.md) (schema + robustness rules).

## Author a cycle

1. Copy `.claude/workflows/_template.yml` to `.claude/workflows/{id}.yml` and fill
   in `match` + `steps` (each `agent`/`skill` must exist; gated steps need a
   `verdict_contract`).
2. Validate it (see below); proceed only on exit 0.
3. Add an `enabled` route to `registry.yml`.

Or just ask — the `workflow-author` agent does all three. Full schema and
robustness rules: [.claude/workflows/README.md](.claude/workflows/README.md).

## Validate

The one deterministic check in the harness:

```bash
python .claude/skills/validate-config/scripts/validate_config.py            # full scan
python .claude/skills/validate-config/scripts/validate_config.py <file>     # one workflow
```

Exits non-zero on errors only (warnings are informational). Requires Python 3
with PyYAML.

## Prerequisite

Nested subagents require **Claude Code >= v2.1.172**. If your CLI is older, run
`claude --agent orchestrator` as the main session (a main thread can spawn
subagents on older versions).

## Layout

```
.
├── README.md                 # this file
├── CLAUDE.md                 # agent runtime policy + session-start brief
├── .claude/
│   ├── agents/               # orchestrator, workflow-author, + workers
│   ├── skills/               # engine + worker skills (each a SKILL.md)
│   └── workflows/            # registry.yml, _template.yml, README.md
└── docs/                     # project docs scaffold (structure guide + folders)
```

See [CLAUDE.md](CLAUDE.md) for how the AI routes requests, and
[.claude/workflows/README.md](.claude/workflows/README.md) for the workflow schema.
