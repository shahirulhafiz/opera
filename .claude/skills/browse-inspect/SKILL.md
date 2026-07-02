---
name: browse-inspect
description: Bounded browser crawl that visits every reachable in-scope page, exercises each functionality, captures transient UI feedback (snackbars/toasts/notifications/modals/validation/spinners), and persists elements, behaviors, transitions, and per-action timing/errors into a local SQLite store. Use to inspect and document a web app's actual behavior.
---

# browse-inspect

Discover a web app's **actual** behavior by systematically driving a real browser
through all reachable pages and exercising every functionality, then persisting
what happened into the local SQLite store (`docs/browse/webapp.db`) via
`store.py`. This is a bounded breadth-first crawl, not a single-page snapshot.

## Store helper

All reads/writes go through the CLI (never hand-write SQL):

```bash
python scripts/store.py --db docs/browse/webapp.db <command> ...
```

Key write commands: `init`, `register`, `add-page`, `next-page`, `mark-visited`,
`start-run`, `end-run`, `log-action`, `add-feedback`, and `import --json <file>`
(bulk-load a whole page snapshot at once — preferred).

## Prerequisites

- The target must be registered (either `store.py register --slug <slug> --url <url>`
  or `store.py register-config --config targets.toml [--slug <slug>]`).
  The `register-target` workflow step seeds the frontier.
- Browser tools come from the `cursor-ide-browser` MCP (`browser_navigate`,
  `browser_snapshot`, `browser_take_screenshot`, `browser_click`, `browser_type`,
  `browser_fill`, `browser_select_option`, `browser_press_key`, `browser_scroll`,
  `browser_tabs`, `browser_lock`, `browser_cdp`).

## Bounds (declare before starting; keeps the crawl safe + terminating)

Pick sensible defaults and record them in the run's `bounds_json`:

- `max_pages` (default 25), `max_depth` (default 3), `max_actions` (default 300).
- Same-origin only: skip any URL whose origin differs from the target.
- Visited-set dedupe: normalize URLs (drop fragments, sort query keys) so a page
  is inspected once.
- `max_failed_attempts` per element (default 4) before giving up on it.

## Protocol

### 1. Open a run

- `store.py init` (idempotent) to ensure the DB exists.
- `store.py start-run --slug <slug> --bounds '{"max_pages":25,"max_depth":3,"max_actions":300}'`
  and keep the returned `run_id` for the whole crawl.
- `browser_navigate` to the entry URL, then `browser_lock` for the session.

### 2. Crawl loop (repeat until frontier empty or a bound is hit)

1. `store.py next-page --slug <slug>` → next unvisited URL (stop when `empty: true`).
2. `browser_navigate` to it. **Time every action** (see step 5).
3. `browser_snapshot` (accessibility tree = source of truth) and one
   `browser_take_screenshot` for evidence.
4. Enumerate **every** interactive element: buttons, links, inputs, selects,
   toggles/switches, tabs, menus/dropdowns, forms. For each record role, name,
   tag, a stable selector (via `browser_cdp` Runtime.evaluate / DOM), and bbox.
5. **Exercise each functionality** and record what actually happens:
   - Links / navigation → follow; record a `transition` and enqueue new in-scope
     URLs (`to_page`) into the frontier.
   - Buttons / toggles / tabs / menus → click; diff the snapshot to capture the
     state change; return to the prior state.
   - Forms → fill with safe sample data and submit; **also submit invalid input**
     to surface validation behavior.
6. `store.py import --json <snapshot.json>` to persist the page + its elements,
   behaviors, transitions, per-action log rows, and captured feedback in one call.
7. `store.py mark-visited --page-id <id>` when the page is fully covered.

### 3. Capture transient / ephemeral UI feedback (critical)

Immediately after each action, watch for short-lived feedback and record it to
`ui_feedback` **before it disappears**. For each: capture `feedback_type`, `text`,
`selector`, `appeared_after_ms`, and `dismissed_after_ms` (poll until it clears).

- Snackbars / toasts / notifications / banners.
- Modals / dialogs / confirmation popups (capture title + body + offered actions;
  close them **non-destructively**).
- Inline form validation / helper / error text (tie the message to its field).
- Loading spinners / progress indicators (time until content settles).
- Badge / count / state changes (cart count, unread count, etc.).

Detection: a short `browser_cdp` `Runtime.evaluate` polling loop querying for
`[role=alert]`, `[role=status]`, `[aria-live]`, `.toast`, `.snackbar`,
`.notification`, `.mat-snack-bar`, and dialog roles; plus a screenshot for
evidence (`screenshot_path`).

### 4. Log every action (timing + errors)

Wrap **every** browser action (navigate, click, type, submit, snapshot):

- Record `started_at`, then compute `duration_ms` = wall-clock delta (response time).
- Set `result_status`: `ok` | `error` | `timeout` | `skipped` | `blocked`.
- On failure, capture `error_type` + `error_message`.
- Capture page/console/network problems via `browser_cdp`: enable `Log` and
  `Network`, collect `Runtime.consoleAPICalled` errors into `console_errors_json`,
  and record the response `http_status` from `Network.responseReceived`.
- Persist as `action_log` rows (via `log-action` or inside `import`), and link any
  `ui_feedback` to the originating action.

### 5. Close the run

- `store.py end-run --run <run_id> --status complete` (or `blocked` / `error`).

## Safety rules (non-destructive)

- **Never** trigger obviously destructive/irreversible actions: logout, delete,
  pay, send, submit, unsubscribe, or entering real credentials. Record them as a
  behavior with `notes = not_exercised_destructive` and an `action_log` row with
  `result_status = skipped`.
- Same-origin only; do not follow external links (record the transition `to_url`
  but do not enqueue).
- Anti-rabbit-hole: after `max_failed_attempts` on an element, log it and move on.
  Report blockers (login wall, captcha, infinite scroll) rather than looping.

## Output / verdict

- The DB is the deliverable; optionally `store.py report --slug <slug>` to emit a
  markdown behavior/transition map.
- End with a summary of counts and `store.py stats --slug <slug>` (actions, error
  rate, avg/p95 response time), then a final line:
  `VERDICT: COMPLETE` (crawl finished within bounds) or
  `VERDICT: BLOCKED` (a blocker stopped meaningful progress).

## Pitfalls to avoid

- Cataloging elements without exercising them (misses real behavior).
- Missing transient feedback because you snapshot too late — poll right after the action.
- Unbounded crawling or following external origins.
- Performing destructive actions "just to see what happens".
