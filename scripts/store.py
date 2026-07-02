#!/usr/bin/env python3
"""Local SQLite store for the browse-inspect crawl.

Single read/write entry point so the browser agent never hand-writes SQL. Uses
only the Python standard library (sqlite3) - no third-party dependencies.

Runtime data lives at docs/browse/webapp.db by default; the schema is defined in
schema.sql next to this file.

Command groups
--------------
Setup / registration:
    init                              create the DB from schema.sql (idempotent)
    register  --slug --url [...]      upsert a target row
    delete-target --slug              delete a target and related crawl data
    register-config [--config --slug] upsert target(s) from a TOML file

Crawl frontier:
    next-page    --slug               pop the next unvisited page URL (prints URL or nothing)
    mark-visited --page-id            flag a page fully inspected
    add-page     --slug --url [...]   enqueue/insert a page (returns its id)

Capture (writes):
    add-element    ...                insert an element (returns id)
    add-behavior   ...                insert a behavior
    add-transition ...                insert a page transition
    start-run      --slug [...]       open a run (returns run id)
    end-run        --run --status     close a run
    log-action     --run ...          append an action_log row (returns id)
    add-feedback   ...                insert a ui_feedback row
    import         --json FILE        bulk load a page snapshot (elements/behaviors/
                                      transitions/actions/feedback) in one call

Read / query:
    list-targets                      list registered targets
    find      [--role --name --text]  search elements + behaviors/transitions
    query     "<free text>"           free-text search across elements/behaviors/feedback
    logs      --slug [--run --errors-only]
    feedback  --slug [--type]
    stats     --slug [--run]          counts, error rate, avg/p95 duration_ms
    report    --slug                  markdown export of the behavior/transition map

All commands accept --db to override the database path.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None

# Windows-safe UTF-8 output regardless of console code page.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
DEFAULT_DB = "docs/browse/webapp.db"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect(db_path: str) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema)
    conn.commit()


def out(data) -> None:
    """Print a result as JSON so callers can parse it deterministically."""
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def target_id_for_slug(conn: sqlite3.Connection, slug: str) -> int:
    row = conn.execute("SELECT id FROM targets WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        raise SystemExit(f"ERROR: no target registered with slug '{slug}'")
    return int(row["id"])


# --------------------------------------------------------------------------- #
# Setup / registration
# --------------------------------------------------------------------------- #
def cmd_init(conn, args):
    ensure_schema(conn)
    out({"ok": True, "db": args.db, "schema": str(SCHEMA_PATH)})


def cmd_register(conn, args):
    ensure_schema(conn)
    result = _upsert_target(
        conn=conn,
        slug=args.slug,
        url=args.url,
        goal=args.goal,
        auth=args.auth,
    )
    out({"ok": True, **result})


def cmd_delete_target(conn, args):
    ensure_schema(conn)
    row = conn.execute("SELECT id, slug, url FROM targets WHERE slug = ?", (args.slug,)).fetchone()
    if row is None:
        raise SystemExit(f"ERROR: no target registered with slug '{args.slug}'")
    conn.execute("DELETE FROM targets WHERE id = ?", (row["id"],))
    conn.commit()
    out({"ok": True, "deleted": {"id": int(row["id"]), "slug": row["slug"], "url": row["url"]}})


def _upsert_target(
    conn: sqlite3.Connection,
    *,
    slug: str,
    url: str,
    goal: str | None = None,
    auth: str | None = None,
) -> dict[str, Any]:
    ts = now_iso()
    conn.execute(
        """
        INSERT INTO targets (slug, url, goal, auth, registered_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
            url = excluded.url,
            goal = COALESCE(excluded.goal, targets.goal),
            auth = COALESCE(excluded.auth, targets.auth)
        """,
        (slug, url, goal, auth, ts),
    )
    conn.commit()
    tid = target_id_for_slug(conn, slug)
    # Seed the frontier with the entry URL if it is not already present.
    conn.execute(
        """
        INSERT OR IGNORE INTO pages (target_id, url, depth, visited)
        VALUES (?, ?, 0, 0)
        """,
        (tid, url),
    )
    conn.commit()
    return {"target_id": tid, "slug": slug, "url": url}


def _load_targets_from_toml(config_path: str) -> list[dict[str, str | None]]:
    if tomllib is None:
        raise SystemExit("ERROR: TOML parsing requires Python 3.11+ (tomllib module missing)")
    raw = Path(config_path).read_bytes()
    data = tomllib.loads(raw.decode("utf-8"))

    if isinstance(data.get("targets"), list):
        source = data["targets"]
    elif isinstance(data.get("target"), dict):
        source = [data["target"]]
    elif isinstance(data, dict) and "slug" in data and "url" in data:
        source = [data]
    else:
        raise SystemExit(
            "ERROR: config must define either [[targets]] entries, a [target] table, "
            "or top-level slug/url keys"
        )

    targets: list[dict[str, str | None]] = []
    for idx, item in enumerate(source, start=1):
        if not isinstance(item, dict):
            raise SystemExit(f"ERROR: target entry #{idx} is not a table/object")
        slug = item.get("slug")
        url = item.get("url")
        if not slug or not isinstance(slug, str):
            raise SystemExit(f"ERROR: target entry #{idx} is missing string 'slug'")
        if not url or not isinstance(url, str):
            raise SystemExit(f"ERROR: target entry #{idx} is missing string 'url'")
        goal = item.get("goal")
        auth = item.get("auth")
        targets.append(
            {
                "slug": slug,
                "url": url,
                "goal": goal if isinstance(goal, str) else None,
                "auth": auth if isinstance(auth, str) else None,
            }
        )
    return targets


def cmd_register_config(conn, args):
    ensure_schema(conn)
    targets = _load_targets_from_toml(args.config)
    if args.slug:
        targets = [t for t in targets if t["slug"] == args.slug]
        if not targets:
            raise SystemExit(f"ERROR: slug '{args.slug}' not found in config: {args.config}")

    registered: list[dict[str, Any]] = []
    for target in targets:
        registered.append(
            _upsert_target(
                conn=conn,
                slug=str(target["slug"]),
                url=str(target["url"]),
                goal=target["goal"] if isinstance(target["goal"], str) else None,
                auth=target["auth"] if isinstance(target["auth"], str) else None,
            )
        )
    out({"ok": True, "config": args.config, "count": len(registered), "targets": registered})


# --------------------------------------------------------------------------- #
# Frontier
# --------------------------------------------------------------------------- #
def cmd_add_page(conn, args):
    tid = target_id_for_slug(conn, args.slug)
    conn.execute(
        """
        INSERT OR IGNORE INTO pages (target_id, url, title, state, depth, visited)
        VALUES (?, ?, ?, ?, ?, 0)
        """,
        (tid, args.url, args.title, args.state, args.depth),
    )
    conn.commit()
    row = conn.execute(
        "SELECT id, visited FROM pages WHERE target_id = ? AND url = ?", (tid, args.url)
    ).fetchone()
    out({"ok": True, "page_id": row["id"], "url": args.url, "visited": row["visited"]})


def cmd_next_page(conn, args):
    tid = target_id_for_slug(conn, args.slug)
    row = conn.execute(
        """
        SELECT id, url, depth FROM pages
        WHERE target_id = ? AND visited = 0
        ORDER BY depth ASC, id ASC
        LIMIT 1
        """,
        (tid,),
    ).fetchone()
    if row is None:
        out({"ok": True, "page_id": None, "url": None, "empty": True})
        return
    out({"ok": True, "page_id": row["id"], "url": row["url"], "depth": row["depth"]})


def cmd_mark_visited(conn, args):
    conn.execute(
        "UPDATE pages SET visited = 1, captured_at = ? WHERE id = ?",
        (now_iso(), args.page_id),
    )
    conn.commit()
    out({"ok": True, "page_id": args.page_id, "visited": 1})


# --------------------------------------------------------------------------- #
# Capture writes
# --------------------------------------------------------------------------- #
def cmd_add_element(conn, args):
    cur = conn.execute(
        """
        INSERT INTO elements (page_id, ref, role, name, tag, selector, attributes_json, bbox, captured_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            args.page_id, args.ref, args.role, args.name, args.tag,
            args.selector, args.attributes, args.bbox, now_iso(),
        ),
    )
    conn.commit()
    out({"ok": True, "element_id": cur.lastrowid})


def cmd_add_behavior(conn, args):
    cur = conn.execute(
        """
        INSERT INTO behaviors (element_id, action, effect, notes, observed_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (args.element_id, args.action, args.effect, args.notes, now_iso()),
    )
    conn.commit()
    out({"ok": True, "behavior_id": cur.lastrowid})


def cmd_add_transition(conn, args):
    cur = conn.execute(
        """
        INSERT INTO transitions (from_page_id, element_id, action, to_page_id, to_url, observed_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (args.from_page_id, args.element_id, args.action, args.to_page_id, args.to_url, now_iso()),
    )
    conn.commit()
    out({"ok": True, "transition_id": cur.lastrowid})


def cmd_start_run(conn, args):
    tid = target_id_for_slug(conn, args.slug)
    cur = conn.execute(
        "INSERT INTO runs (target_id, started_at, status, bounds_json, notes) VALUES (?, ?, 'running', ?, ?)",
        (tid, now_iso(), args.bounds, args.notes),
    )
    conn.commit()
    out({"ok": True, "run_id": cur.lastrowid, "target_id": tid})


def cmd_end_run(conn, args):
    conn.execute(
        "UPDATE runs SET finished_at = ?, status = ?, notes = COALESCE(?, notes) WHERE id = ?",
        (now_iso(), args.status, args.notes, args.run),
    )
    conn.commit()
    out({"ok": True, "run_id": args.run, "status": args.status})


def _next_seq(conn: sqlite3.Connection, run_id: int) -> int:
    row = conn.execute(
        "SELECT COALESCE(MAX(seq), 0) + 1 AS n FROM action_log WHERE run_id = ?", (run_id,)
    ).fetchone()
    return int(row["n"])


def cmd_log_action(conn, args):
    seq = args.seq if args.seq is not None else _next_seq(conn, args.run)
    cur = conn.execute(
        """
        INSERT INTO action_log
            (run_id, page_id, element_id, seq, action, target_url, started_at,
             duration_ms, result_status, http_status, error_type, error_message,
             console_errors_json, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            args.run, args.page_id, args.element_id, seq, args.action, args.target_url,
            args.started_at or now_iso(), args.duration_ms, args.result_status,
            args.http_status, args.error_type, args.error_message,
            args.console_errors, args.notes,
        ),
    )
    conn.commit()
    out({"ok": True, "action_log_id": cur.lastrowid, "seq": seq})


def cmd_add_feedback(conn, args):
    cur = conn.execute(
        """
        INSERT INTO ui_feedback
            (action_log_id, page_id, feedback_type, role, text, selector,
             appeared_after_ms, dismissed_after_ms, screenshot_path, snapshot_json, observed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            args.action_log_id, args.page_id, args.feedback_type, args.role, args.text,
            args.selector, args.appeared_after_ms, args.dismissed_after_ms,
            args.screenshot_path, args.snapshot, now_iso(),
        ),
    )
    conn.commit()
    out({"ok": True, "feedback_id": cur.lastrowid})


# --------------------------------------------------------------------------- #
# Bulk import
# --------------------------------------------------------------------------- #
def cmd_import(conn, args):
    """Load a page snapshot in one call.

    Expected JSON shape (all sections optional except page):
    {
      "slug": "my-app",
      "run_id": 1,
      "page": {"url": "...", "title": "...", "state": "...", "depth": 1},
      "elements": [
        {"ref": "e1", "role": "button", "name": "Submit", "tag": "button",
         "selector": "#submit", "attributes": {...}, "bbox": [x,y,w,h],
         "behaviors": [{"action": "click", "effect": "state_change", "notes": "..."}],
         "actions": [
            {"action": "click", "duration_ms": 120, "result_status": "ok",
             "http_status": 200, "error_type": null, "error_message": null,
             "console_errors": [...], "notes": "...",
             "feedback": [
                {"feedback_type": "snackbar", "text": "Saved", "role": "status",
                 "selector": ".snackbar", "appeared_after_ms": 80,
                 "dismissed_after_ms": 4000, "screenshot_path": "..."}
             ]}
         ]}
      ],
      "transitions": [
        {"element_ref": "e1", "action": "click", "to_url": "...", "to_page": {"url": "...", "depth": 2}}
      ]
    }
    """
    # utf-8-sig tolerates an optional BOM (common when files are written on Windows).
    data = json.loads(Path(args.json).read_text(encoding="utf-8-sig"))
    slug = data["slug"]
    tid = target_id_for_slug(conn, slug)
    run_id = data.get("run_id")

    page = data["page"]
    conn.execute(
        """
        INSERT INTO pages (target_id, url, title, state, depth, visited, captured_at)
        VALUES (?, ?, ?, ?, ?, 1, ?)
        ON CONFLICT(target_id, url) DO UPDATE SET
            title = COALESCE(excluded.title, pages.title),
            state = COALESCE(excluded.state, pages.state),
            visited = 1,
            captured_at = excluded.captured_at
        """,
        (tid, page["url"], page.get("title"), page.get("state"),
         page.get("depth", 0), now_iso()),
    )
    prow = conn.execute(
        "SELECT id FROM pages WHERE target_id = ? AND url = ?", (tid, page["url"])
    ).fetchone()
    page_id = int(prow["id"])

    ref_to_element_id: dict[str, int] = {}
    counts = {"elements": 0, "behaviors": 0, "actions": 0, "feedback": 0,
              "transitions": 0, "pages_enqueued": 0}

    for el in data.get("elements", []) or []:
        cur = conn.execute(
            """
            INSERT INTO elements (page_id, ref, role, name, tag, selector, attributes_json, bbox, captured_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                page_id, el.get("ref"), el.get("role"), el.get("name"), el.get("tag"),
                el.get("selector"),
                json.dumps(el.get("attributes"), ensure_ascii=False) if el.get("attributes") is not None else None,
                json.dumps(el.get("bbox")) if el.get("bbox") is not None else None,
                now_iso(),
            ),
        )
        element_id = cur.lastrowid
        counts["elements"] += 1
        if el.get("ref"):
            ref_to_element_id[el["ref"]] = element_id

        for beh in el.get("behaviors", []) or []:
            conn.execute(
                "INSERT INTO behaviors (element_id, action, effect, notes, observed_at) VALUES (?, ?, ?, ?, ?)",
                (element_id, beh.get("action", "unknown"), beh.get("effect"), beh.get("notes"), now_iso()),
            )
            counts["behaviors"] += 1

        for act in el.get("actions", []) or []:
            if run_id is None:
                raise SystemExit("ERROR: import with 'actions' requires top-level 'run_id'")
            seq = _next_seq(conn, run_id)
            ce = act.get("console_errors")
            acur = conn.execute(
                """
                INSERT INTO action_log
                    (run_id, page_id, element_id, seq, action, target_url, started_at,
                     duration_ms, result_status, http_status, error_type, error_message,
                     console_errors_json, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id, page_id, element_id, seq, act.get("action", "unknown"),
                    act.get("target_url"), act.get("started_at") or now_iso(),
                    act.get("duration_ms"), act.get("result_status"), act.get("http_status"),
                    act.get("error_type"), act.get("error_message"),
                    json.dumps(ce, ensure_ascii=False) if ce is not None else None,
                    act.get("notes"),
                ),
            )
            action_log_id = acur.lastrowid
            counts["actions"] += 1

            for fb in act.get("feedback", []) or []:
                conn.execute(
                    """
                    INSERT INTO ui_feedback
                        (action_log_id, page_id, feedback_type, role, text, selector,
                         appeared_after_ms, dismissed_after_ms, screenshot_path, snapshot_json, observed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        action_log_id, page_id, fb.get("feedback_type", "unknown"), fb.get("role"),
                        fb.get("text"), fb.get("selector"), fb.get("appeared_after_ms"),
                        fb.get("dismissed_after_ms"), fb.get("screenshot_path"),
                        json.dumps(fb.get("snapshot"), ensure_ascii=False) if fb.get("snapshot") is not None else None,
                        now_iso(),
                    ),
                )
                counts["feedback"] += 1

    for tr in data.get("transitions", []) or []:
        to_page_id = None
        to = tr.get("to_page")
        if to and to.get("url"):
            conn.execute(
                """
                INSERT OR IGNORE INTO pages (target_id, url, depth, visited)
                VALUES (?, ?, ?, 0)
                """,
                (tid, to["url"], to.get("depth", page.get("depth", 0) + 1)),
            )
            trow = conn.execute(
                "SELECT id FROM pages WHERE target_id = ? AND url = ?", (tid, to["url"])
            ).fetchone()
            to_page_id = int(trow["id"])
            counts["pages_enqueued"] += 1
        element_id = ref_to_element_id.get(tr.get("element_ref"))
        conn.execute(
            """
            INSERT INTO transitions (from_page_id, element_id, action, to_page_id, to_url, observed_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (page_id, element_id, tr.get("action", "navigate"), to_page_id, tr.get("to_url"), now_iso()),
        )
        counts["transitions"] += 1

    conn.commit()
    out({"ok": True, "page_id": page_id, "counts": counts})


# --------------------------------------------------------------------------- #
# Reads / queries
# --------------------------------------------------------------------------- #
def cmd_list_targets(conn, args):
    rows = conn.execute(
        "SELECT id, slug, url, goal, auth, registered_at FROM targets ORDER BY id"
    ).fetchall()
    out([dict(r) for r in rows])


def cmd_find(conn, args):
    clauses, params = [], []
    if args.role:
        clauses.append("e.role LIKE ?")
        params.append(f"%{args.role}%")
    if args.name:
        clauses.append("e.name LIKE ?")
        params.append(f"%{args.name}%")
    if args.text:
        clauses.append("(e.name LIKE ? OR e.selector LIKE ? OR e.role LIKE ?)")
        params.extend([f"%{args.text}%"] * 3)
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = f"""
        SELECT e.id AS element_id, e.role, e.name, e.tag, e.selector,
               p.url AS page_url, p.title AS page_title
        FROM elements e
        JOIN pages p ON p.id = e.page_id
        {where}
        ORDER BY e.id
        LIMIT ?
    """
    params.append(args.limit)
    rows = conn.execute(sql, params).fetchall()
    results = []
    for r in rows:
        d = dict(r)
        d["behaviors"] = [
            dict(b) for b in conn.execute(
                "SELECT action, effect, notes FROM behaviors WHERE element_id = ?",
                (r["element_id"],),
            ).fetchall()
        ]
        d["transitions"] = [
            dict(t) for t in conn.execute(
                "SELECT action, to_url FROM transitions WHERE element_id = ?",
                (r["element_id"],),
            ).fetchall()
        ]
        results.append(d)
    out(results)


def cmd_query(conn, args):
    like = f"%{args.text}%"
    elements = conn.execute(
        """
        SELECT e.id AS element_id, e.role, e.name, e.selector, p.url AS page_url
        FROM elements e JOIN pages p ON p.id = e.page_id
        WHERE e.name LIKE ? OR e.role LIKE ? OR e.selector LIKE ?
        LIMIT ?
        """,
        (like, like, like, args.limit),
    ).fetchall()
    behaviors = conn.execute(
        """
        SELECT b.action, b.effect, b.notes, e.name AS element_name, p.url AS page_url
        FROM behaviors b
        JOIN elements e ON e.id = b.element_id
        JOIN pages p ON p.id = e.page_id
        WHERE b.action LIKE ? OR b.effect LIKE ? OR b.notes LIKE ?
        LIMIT ?
        """,
        (like, like, like, args.limit),
    ).fetchall()
    feedback = conn.execute(
        """
        SELECT f.feedback_type, f.text, f.selector, p.url AS page_url
        FROM ui_feedback f LEFT JOIN pages p ON p.id = f.page_id
        WHERE f.text LIKE ? OR f.feedback_type LIKE ?
        LIMIT ?
        """,
        (like, like, args.limit),
    ).fetchall()
    out({
        "elements": [dict(r) for r in elements],
        "behaviors": [dict(r) for r in behaviors],
        "feedback": [dict(r) for r in feedback],
    })


def _run_ids_for_slug(conn, slug, run):
    tid = target_id_for_slug(conn, slug)
    if run is not None:
        return [run]
    rows = conn.execute("SELECT id FROM runs WHERE target_id = ? ORDER BY id", (tid,)).fetchall()
    return [int(r["id"]) for r in rows]


def cmd_logs(conn, args):
    run_ids = _run_ids_for_slug(conn, args.slug, args.run)
    if not run_ids:
        out([])
        return
    placeholders = ",".join("?" * len(run_ids))
    sql = f"""
        SELECT id, run_id, seq, action, target_url, duration_ms, result_status,
               http_status, error_type, error_message
        FROM action_log
        WHERE run_id IN ({placeholders})
    """
    if args.errors_only:
        sql += " AND (result_status NOT IN ('ok','skipped') OR error_type IS NOT NULL)"
    sql += " ORDER BY run_id, seq LIMIT ?"
    rows = conn.execute(sql, [*run_ids, args.limit]).fetchall()
    out([dict(r) for r in rows])


def cmd_feedback(conn, args):
    tid = target_id_for_slug(conn, args.slug)
    params = [tid]
    type_clause = ""
    if args.type:
        type_clause = " AND f.feedback_type = ?"
        params.append(args.type)
    sql = f"""
        SELECT f.feedback_type, f.text, f.role, f.selector,
               f.appeared_after_ms, f.dismissed_after_ms, p.url AS page_url
        FROM ui_feedback f
        LEFT JOIN pages p ON p.id = f.page_id
        WHERE p.target_id = ?{type_clause}
        ORDER BY f.id
        LIMIT ?
    """
    params.append(args.limit)
    rows = conn.execute(sql, params).fetchall()
    out([dict(r) for r in rows])


def _percentile(values: list[int], pct: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    k = max(0, min(len(ordered) - 1, int(round((pct / 100.0) * (len(ordered) - 1)))))
    return ordered[k]


def cmd_stats(conn, args):
    run_ids = _run_ids_for_slug(conn, args.slug, args.run)
    if not run_ids:
        out({"ok": True, "runs": 0, "actions": 0})
        return
    placeholders = ",".join("?" * len(run_ids))
    rows = conn.execute(
        f"""
        SELECT duration_ms, result_status, error_type
        FROM action_log WHERE run_id IN ({placeholders})
        """,
        run_ids,
    ).fetchall()
    total = len(rows)
    errors = sum(
        1 for r in rows
        if (r["result_status"] not in ("ok", "skipped")) or r["error_type"] is not None
    )
    durations = [int(r["duration_ms"]) for r in rows if r["duration_ms"] is not None]
    avg = round(sum(durations) / len(durations), 1) if durations else None
    out({
        "ok": True,
        "runs": len(run_ids),
        "actions": total,
        "errors": errors,
        "error_rate": round(errors / total, 3) if total else 0,
        "avg_duration_ms": avg,
        "p95_duration_ms": _percentile(durations, 95),
        "max_duration_ms": max(durations) if durations else None,
    })


def cmd_report(conn, args):
    tid = target_id_for_slug(conn, args.slug)
    target = conn.execute("SELECT * FROM targets WHERE id = ?", (tid,)).fetchone()
    pages = conn.execute(
        "SELECT * FROM pages WHERE target_id = ? ORDER BY depth, id", (tid,)
    ).fetchall()
    lines = [
        f"# Web app behavior report: {target['slug']}",
        "",
        f"- Entry URL: {target['url']}",
        f"- Goal: {target['goal'] or '(none)'}",
        f"- Pages discovered: {len(pages)}",
        "",
    ]
    for p in pages:
        lines.append(f"## Page: {p['title'] or '(untitled)'} - {p['url']}")
        els = conn.execute(
            "SELECT * FROM elements WHERE page_id = ? ORDER BY id", (p["id"],)
        ).fetchall()
        if not els:
            lines.append("_No elements captured._\n")
            continue
        lines.append("")
        lines.append("| Role | Name | Selector | Behaviors |")
        lines.append("|------|------|----------|-----------|")
        for e in els:
            behs = conn.execute(
                "SELECT action, effect, notes FROM behaviors WHERE element_id = ?", (e["id"],)
            ).fetchall()
            beh_txt = "; ".join(
                f"{b['action']}->{b['effect'] or '?'}" + (f" ({b['notes']})" if b["notes"] else "")
                for b in behs
            ) or "-"
            lines.append(
                f"| {e['role'] or ''} | {e['name'] or ''} | `{e['selector'] or ''}` | {beh_txt} |"
            )
        lines.append("")
        fbs = conn.execute(
            """
            SELECT feedback_type, text FROM ui_feedback
            WHERE page_id = ? ORDER BY id
            """,
            (p["id"],),
        ).fetchall()
        if fbs:
            lines.append("**UI feedback observed:**")
            for f in fbs:
                lines.append(f"- {f['feedback_type']}: {f['text'] or ''}")
            lines.append("")
    print("\n".join(lines))


# --------------------------------------------------------------------------- #
# Argument parsing
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Local SQLite store for browse-inspect crawls.")
    p.add_argument("--db", default=DEFAULT_DB, help=f"SQLite path (default: {DEFAULT_DB})")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("init", help="create the DB from schema.sql")
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("register", help="upsert a target")
    sp.add_argument("--slug", required=True)
    sp.add_argument("--url", required=True)
    sp.add_argument("--goal")
    sp.add_argument("--auth")
    sp.set_defaults(func=cmd_register)

    sp = sub.add_parser("delete-target", help="delete a target by slug")
    sp.add_argument("--slug", required=True)
    sp.set_defaults(func=cmd_delete_target)

    sp = sub.add_parser("register-config", help="upsert target(s) from a TOML config")
    sp.add_argument(
        "--config",
        default="targets.toml",
        help="path to TOML config (default: targets.toml)",
    )
    sp.add_argument("--slug", help="optional single slug filter")
    sp.set_defaults(func=cmd_register_config)

    sp = sub.add_parser("add-page", help="enqueue/insert a page")
    sp.add_argument("--slug", required=True)
    sp.add_argument("--url", required=True)
    sp.add_argument("--title")
    sp.add_argument("--state")
    sp.add_argument("--depth", type=int, default=0)
    sp.set_defaults(func=cmd_add_page)

    sp = sub.add_parser("next-page", help="pop the next unvisited page")
    sp.add_argument("--slug", required=True)
    sp.set_defaults(func=cmd_next_page)

    sp = sub.add_parser("mark-visited", help="mark a page visited")
    sp.add_argument("--page-id", type=int, required=True, dest="page_id")
    sp.set_defaults(func=cmd_mark_visited)

    sp = sub.add_parser("add-element", help="insert an element")
    sp.add_argument("--page-id", type=int, required=True, dest="page_id")
    sp.add_argument("--ref")
    sp.add_argument("--role")
    sp.add_argument("--name")
    sp.add_argument("--tag")
    sp.add_argument("--selector")
    sp.add_argument("--attributes", help="JSON string")
    sp.add_argument("--bbox", help="JSON [x,y,w,h]")
    sp.set_defaults(func=cmd_add_element)

    sp = sub.add_parser("add-behavior", help="insert a behavior")
    sp.add_argument("--element-id", type=int, required=True, dest="element_id")
    sp.add_argument("--action", required=True)
    sp.add_argument("--effect")
    sp.add_argument("--notes")
    sp.set_defaults(func=cmd_add_behavior)

    sp = sub.add_parser("add-transition", help="insert a transition")
    sp.add_argument("--from-page-id", type=int, required=True, dest="from_page_id")
    sp.add_argument("--element-id", type=int, dest="element_id")
    sp.add_argument("--action", required=True)
    sp.add_argument("--to-page-id", type=int, dest="to_page_id")
    sp.add_argument("--to-url", dest="to_url")
    sp.set_defaults(func=cmd_add_transition)

    sp = sub.add_parser("start-run", help="open a crawl run")
    sp.add_argument("--slug", required=True)
    sp.add_argument("--bounds", help="JSON bounds blob")
    sp.add_argument("--notes")
    sp.set_defaults(func=cmd_start_run)

    sp = sub.add_parser("end-run", help="close a crawl run")
    sp.add_argument("--run", type=int, required=True)
    sp.add_argument("--status", required=True, choices=["complete", "blocked", "error"])
    sp.add_argument("--notes")
    sp.set_defaults(func=cmd_end_run)

    sp = sub.add_parser("log-action", help="append an action_log row")
    sp.add_argument("--run", type=int, required=True)
    sp.add_argument("--page-id", type=int, dest="page_id")
    sp.add_argument("--element-id", type=int, dest="element_id")
    sp.add_argument("--seq", type=int)
    sp.add_argument("--action", required=True)
    sp.add_argument("--target-url", dest="target_url")
    sp.add_argument("--started-at", dest="started_at")
    sp.add_argument("--duration-ms", type=int, dest="duration_ms")
    sp.add_argument("--result-status", dest="result_status")
    sp.add_argument("--http-status", type=int, dest="http_status")
    sp.add_argument("--error-type", dest="error_type")
    sp.add_argument("--error-message", dest="error_message")
    sp.add_argument("--console-errors", dest="console_errors", help="JSON array")
    sp.add_argument("--notes")
    sp.set_defaults(func=cmd_log_action)

    sp = sub.add_parser("add-feedback", help="insert a ui_feedback row")
    sp.add_argument("--action-log-id", type=int, dest="action_log_id")
    sp.add_argument("--page-id", type=int, dest="page_id")
    sp.add_argument("--feedback-type", required=True, dest="feedback_type")
    sp.add_argument("--role")
    sp.add_argument("--text")
    sp.add_argument("--selector")
    sp.add_argument("--appeared-after-ms", type=int, dest="appeared_after_ms")
    sp.add_argument("--dismissed-after-ms", type=int, dest="dismissed_after_ms")
    sp.add_argument("--screenshot-path", dest="screenshot_path")
    sp.add_argument("--snapshot", help="JSON string")
    sp.set_defaults(func=cmd_add_feedback)

    sp = sub.add_parser("import", help="bulk load a page snapshot from JSON")
    sp.add_argument("--json", required=True, help="path to JSON file")
    sp.set_defaults(func=cmd_import)

    sp = sub.add_parser("list-targets", help="list registered targets")
    sp.set_defaults(func=cmd_list_targets)

    sp = sub.add_parser("find", help="search elements")
    sp.add_argument("--role")
    sp.add_argument("--name")
    sp.add_argument("--text")
    sp.add_argument("--limit", type=int, default=50)
    sp.set_defaults(func=cmd_find)

    sp = sub.add_parser("query", help="free-text search")
    sp.add_argument("text")
    sp.add_argument("--limit", type=int, default=50)
    sp.set_defaults(func=cmd_query)

    sp = sub.add_parser("logs", help="list action_log rows")
    sp.add_argument("--slug", required=True)
    sp.add_argument("--run", type=int)
    sp.add_argument("--errors-only", action="store_true", dest="errors_only")
    sp.add_argument("--limit", type=int, default=200)
    sp.set_defaults(func=cmd_logs)

    sp = sub.add_parser("feedback", help="list ui_feedback rows")
    sp.add_argument("--slug", required=True)
    sp.add_argument("--type", dest="type")
    sp.add_argument("--limit", type=int, default=200)
    sp.set_defaults(func=cmd_feedback)

    sp = sub.add_parser("stats", help="run statistics")
    sp.add_argument("--slug", required=True)
    sp.add_argument("--run", type=int)
    sp.set_defaults(func=cmd_stats)

    sp = sub.add_parser("report", help="markdown export")
    sp.add_argument("--slug", required=True)
    sp.set_defaults(func=cmd_report)

    return p


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    conn = connect(args.db)
    try:
        args.func(conn, args)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
