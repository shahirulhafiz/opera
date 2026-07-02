---
name: browse-query
description: Answer natural-language questions about a previously inspected web app by querying the local SQLite store (docs/browse/webapp.db). Finds where an element is, what behavior/feedback an action produces, and observability facts like slowest or failing actions. Use when the user asks where something is or how the app behaves.
---

# browse-query

Answer questions about a web app that was already inspected by the `browse-inspect`
crawl, using the local SQLite store as the source of truth. This is the "when the
user asks, you know where to find it" path — do **not** re-drive the browser to
answer a question that the store can already answer.

## Store helper

Read through the CLI (all commands print JSON):

```bash
python scripts/store.py --db docs/browse/webapp.db <command> ...
```

If `docs/browse/webapp.db` does not exist or the target is not present, tell the
user the app has not been inspected yet and suggest running the `web-automation`
workflow (or the `browse-inspect` step) for that target.

## Question → command mapping

- **"Where is the <X> button/link/field?"** →
  `find --name "<X>"` (or `--role button --name "<X>"`). Return the element's
  `selector`, `page_url`, role, and any recorded `behaviors`/`transitions`.
- **"What does <X> do?" / "Where does <X> lead?"** →
  `find --name "<X>"`; report its `behaviors` (effect) and `transitions` (`to_url`).
- **"What message/snackbar/toast/validation shows when I do <X>?"** →
  `feedback --slug <slug>` (optionally `--type snackbar|toast|modal|validation|...`),
  or `query "<keyword>"` to search feedback text.
- **Free-text ("anything about checkout")** →
  `query "<text>"` — searches element names/roles/selectors, behaviors, and
  feedback text together.
- **"Which actions errored?"** → `logs --slug <slug> --errors-only`.
- **"What was the slowest page/action?" / "response times?"** →
  `stats --slug <slug>` (avg/p95/max `duration_ms`) and `logs --slug <slug>` to
  drill into individual `duration_ms` values.
- **"What is the error rate for this run?"** → `stats --slug <slug> [--run <id>]`.
- **"What targets have been inspected?"** → `list-targets`.

## Answering

1. Pick the narrowest command for the question and run it.
2. Summarize the JSON in plain language, always citing the concrete
   `selector` + `page_url` (so the user/agent can act on it) and the observed
   `behavior`/`feedback`/timing where relevant.
3. If nothing matches, say so plainly and suggest re-inspecting that target rather
   than guessing.

Keep answers grounded strictly in stored data — never invent selectors or
behaviors that are not in the DB.
