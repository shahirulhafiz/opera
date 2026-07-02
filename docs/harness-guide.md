# Harness Guide — concepts & terminology (for humans)

A plain-language guide to how this harness works and what everything is called,
so you and the AI use the **same words**. This is the friendly version; the terse
canonical reference is [`.claude/GLOSSARY.md`](../.claude/GLOSSARY.md) (the source
of truth — if the two ever disagree, the glossary wins).

## The one-minute version

You describe work in plain language. A router agent (the **orchestrator**) picks
a **workflow** and runs its **steps** in order, handing each step to a specialist
**agent**. Some steps are **gated** — they only continue if the agent returns an
approved verdict. You never tag agents or skills by hand.

## Core concepts

| Term | In plain language | Also known as |
|------|-------------------|---------------|
| **harness** | The whole system that routes your request and runs the work. | the framework |
| **orchestrator** | The "traffic controller" agent. It doesn't do the work — it picks the plan and runs it. | — |
| **workflow** | A reusable, ordered recipe of steps saved as one YAML file. **This is the word we use.** | *cycle*, *pipeline* (synonyms — fine to say, but "workflow" is canonical) |
| **step** | One unit of work inside a workflow. | — |
| **agent** | A specialist worker (e.g. `implementer`, `code-reviewer`, `debugger`). | — |
| **skill** | A playbook an agent follows for a particular task. | — |
| **route** | An entry in the registry that says "requests about X use workflow Y." | — |
| **registry** | The list of all routes (`registry.yml`) — how the orchestrator decides. | — |
| **gated step** | A step that only proceeds if the agent returns an approved result. | gate |
| **verdict** | The machine-checkable result a gated step returns (e.g. `APPROVE` / `REVISE`). | — |

> **Why "workflow" and not "cycle"/"pipeline"?** They mean the same thing, but
> mixing words made requests ambiguous. We standardized on **workflow** as the
> canonical noun. You can still *say* "cycle" or "pipeline" — the AI understands
> them as synonyms — but docs, files, and config all use "workflow".

## What happens when you make a request

1. **Routing.** The orchestrator reads the **registry** and picks the best-matching
   **workflow**. If nothing matches, it uses the built-in **ad-hoc route**
   (`implementer → code-reviewer + test-expert → debugger`).
2. **Sizing (execution tier).** It sizes the effort:
   - **Trivial** (~≤15 lines / one file) → done directly, no orchestration.
   - **Fast lane** → the essentials only (`execute → review + test`).
   - **Full** → every step runs.
3. **Running steps.** Each step is handed to its **agent**. Independent steps can
   run in parallel.
4. **Gates.** At a **gated step**, the orchestrator checks the agent's **verdict**
   and either continues or loops back to fix things (up to a retry limit).
5. **Escalation.** At a **manual** step — or any real decision, destructive action,
   or ambiguity — it stops and asks **you**.

## Step types

Every step is one of two kinds:

| Type | What it does |
|------|--------------|
| **`agent`** (default) | Hands the work to a specialist agent. |
| **`manual`** | Pauses and asks **you** — for a decision, an approval, or a risky action. |

## Profiles vs execution tiers

You'll see two related words; here's the difference:

- **Profile** = the mode the assistant runs in overall: **Lean** (default, do the
  smallest thing that works) or **Full** (heavier, spec-driven work).
- **Execution tier** = how big a single run is: **Trivial**, **Fast lane**, or **Full**.

They line up like this:

| Profile | Uses tier(s) |
|---------|--------------|
| **Lean** | Trivial, Fast lane |
| **Full** | Full |

## Creating your own workflow

You have two options — both without touching the orchestrator:

- **Just ask:** say *"add a workflow that does X → Y → Z"* and the
  `workflow-author` agent scaffolds, validates, and registers it.
- **By hand:** copy `.claude/workflows/_template.yml`, fill in `match` + `steps`,
  run the validator, then add a route to `registry.yml`.

Full schema and rules live in
[`.claude/workflows/README.md`](../.claude/workflows/README.md).

## Where the words are defined

- **Canonical quick-reference:** [`.claude/GLOSSARY.md`](../.claude/GLOSSARY.md)
- **This friendly guide:** you're reading it.
- **Runtime policy for the AI:** [`../CLAUDE.md`](../CLAUDE.md)
