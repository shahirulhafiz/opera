# Agentic Factory Runtime Policy

This repository uses `.claude/` agent, skill, and workflow files.

## Locations

| Path | Content |
|------|---------|
| `.claude/workflows/` | Workflow definitions and execution gates |
| `.claude/agents/` | Agent system prompts and routing |
| `.claude/skills/` | Skill playbooks and task protocols |

## Default Operating Mode

Use the **Lean profile** by default:
- Prefer direct execution for small, targeted changes.
- Invoke heavyweight agents only when user intent or task complexity requires them.
- Load context files on demand, not all at once.

Escalate to **Full profile** only for:
- Full specification creation and validation
- Full phase implementation and verification
- Explicit user request for full pipeline behavior

## Invocation Guardrails

- Do not trigger `phase-manager` or `completion-report` for routine fixes unless requested.
- Run `docs-context-awareness` only for docs creation, structural updates, or uncertain conventions.
- Use debugger verification by risk level:
  - High risk / cross-module / migration: required
  - Small contained fix: optional
- Prefer stage-based spec loading for implementation and verification tasks.

## Tool Relevance Filter

Before invoking a heavyweight specialist tool/agent, enforce:
- Relevance check: does this tool directly improve the requested outcome?
- Scope check: for narrow tasks, avoid unrelated specialists.
- Justification check: include a one-line reason category:
  - `error-diagnosis`
  - `phase-completion`
  - `spec-production`
  - `security-review`

If a tool does not pass relevance + scope checks, skip invocation.

## Exploration Efficiency Policy

- Default to `quick_discovery` for exploratory requests.
- Budget for quick exploration:
  - Max parallel explore agents: 1
  - Max tool uses per pass: 10
  - Max files read in initial pass: 6
- If quick pass is insufficient, stop and ask before deepening unless the user explicitly requested a deep dive.
- Deep exploration is allowed only for unresolved ambiguity or high-risk investigation, with max 2 parallel explore agents.

## Query-Shape Routing

- Needle query (specific symbol/file/path): use direct `ReadFile`/`rg`/`Glob`; avoid explore subagents.
- Scoped architecture query (single subsystem): one explore agent, quick pass first.
- Cross-system query: two-phase flow (quick pass, then gated deep pass if needed).

## Stop-And-Ask Escalation

If exploration exceeds budget thresholds (agent count, tool uses, repeated reads):
- Pause exploration.
- Return concise findings so far.
- Ask user whether to continue with deeper investigation.

## Token Optimization Metrics

Track these after rollout:
- Average tokens for non-phase tasks (target: reduce by 40%+)
- Number of heavy-skill invocations on small fixes (target: <= 1)
- Number of completion reports generated outside phase completion (target: near zero unless requested)

Weekly tuning knobs:
- `phase completion threshold`
- `high-risk task` criteria
- Lean vs Full profile overrides
