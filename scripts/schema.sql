-- SQLite schema for the browse-inspect crawl store.
-- Driven by store.py (Python stdlib sqlite3). Runtime data lives at
-- docs/browse/webapp.db; this file defines the tables and is idempotent
-- (all statements use IF NOT EXISTS) so `store.py init` can run repeatedly.

PRAGMA foreign_keys = ON;

-- One registered web application / entry point.
CREATE TABLE IF NOT EXISTS targets (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    slug          TEXT NOT NULL UNIQUE,
    url           TEXT NOT NULL,
    goal          TEXT,
    auth          TEXT,
    registered_at TEXT NOT NULL
);

-- One crawl run against a target. Brackets every action in action_log.
CREATE TABLE IF NOT EXISTS runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    target_id   INTEGER NOT NULL REFERENCES targets(id) ON DELETE CASCADE,
    started_at  TEXT NOT NULL,
    finished_at TEXT,
    status      TEXT NOT NULL DEFAULT 'running',   -- running | complete | blocked | error
    bounds_json TEXT,                              -- JSON: max_pages/max_depth/max_actions/...
    notes       TEXT
);

-- A page (or distinct app state) discovered during a crawl. The `visited`
-- flag drives the BFS frontier so each page is inspected once per target.
CREATE TABLE IF NOT EXISTS pages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    target_id   INTEGER NOT NULL REFERENCES targets(id) ON DELETE CASCADE,
    url         TEXT NOT NULL,
    title       TEXT,
    state       TEXT,                              -- optional label for SPA states
    depth       INTEGER NOT NULL DEFAULT 0,
    visited     INTEGER NOT NULL DEFAULT 0,        -- 0 = queued (frontier), 1 = inspected
    captured_at TEXT,
    UNIQUE (target_id, url)
);

-- An interactive element found on a page.
CREATE TABLE IF NOT EXISTS elements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id         INTEGER NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
    ref             TEXT,                          -- snapshot ref handle
    role            TEXT,
    name            TEXT,                          -- accessible name / label
    tag             TEXT,
    selector        TEXT,                          -- stable CSS/XPath selector
    attributes_json TEXT,                          -- JSON blob of notable attributes
    bbox            TEXT,                          -- JSON [x,y,w,h]
    captured_at     TEXT
);

-- A behavior observed when an element is exercised (or intentionally skipped).
CREATE TABLE IF NOT EXISTS behaviors (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    element_id  INTEGER NOT NULL REFERENCES elements(id) ON DELETE CASCADE,
    action      TEXT NOT NULL,                     -- click | type | submit | hover | ...
    effect      TEXT,                              -- navigation | state_change | validation | none
    notes       TEXT,                              -- e.g. not_exercised_destructive
    observed_at TEXT
);

-- Behavior graph: performing `action` on `element` led from one page to another.
CREATE TABLE IF NOT EXISTS transitions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    from_page_id INTEGER NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
    element_id   INTEGER REFERENCES elements(id) ON DELETE SET NULL,
    action       TEXT NOT NULL,
    to_page_id   INTEGER REFERENCES pages(id) ON DELETE SET NULL,
    to_url       TEXT,
    observed_at  TEXT
);

-- Observability: one row per action attempted, with response time and errors.
CREATE TABLE IF NOT EXISTS action_log (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id              INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    page_id             INTEGER REFERENCES pages(id) ON DELETE SET NULL,
    element_id          INTEGER REFERENCES elements(id) ON DELETE SET NULL,
    seq                 INTEGER,                   -- monotonic order within the run
    action              TEXT NOT NULL,             -- navigate | click | type | submit | snapshot | ...
    target_url          TEXT,
    started_at          TEXT,
    duration_ms         INTEGER,                   -- response time
    result_status       TEXT,                      -- ok | error | timeout | skipped | blocked
    http_status         INTEGER,
    error_type          TEXT,
    error_message       TEXT,
    console_errors_json TEXT,                      -- JSON array of console/page errors
    notes               TEXT
);

-- Transient / ephemeral UI feedback triggered by an action.
CREATE TABLE IF NOT EXISTS ui_feedback (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    action_log_id     INTEGER REFERENCES action_log(id) ON DELETE CASCADE,
    page_id           INTEGER REFERENCES pages(id) ON DELETE SET NULL,
    feedback_type     TEXT NOT NULL,               -- snackbar|toast|notification|modal|alert|validation|spinner|banner|badge
    role              TEXT,
    text              TEXT,
    selector          TEXT,
    appeared_after_ms INTEGER,
    dismissed_after_ms INTEGER,
    screenshot_path   TEXT,
    snapshot_json     TEXT,
    observed_at       TEXT
);

CREATE INDEX IF NOT EXISTS idx_pages_frontier   ON pages (target_id, visited);
CREATE INDEX IF NOT EXISTS idx_elements_page    ON elements (page_id);
CREATE INDEX IF NOT EXISTS idx_behaviors_elem   ON behaviors (element_id);
CREATE INDEX IF NOT EXISTS idx_actionlog_run    ON action_log (run_id);
CREATE INDEX IF NOT EXISTS idx_feedback_action  ON ui_feedback (action_log_id);
CREATE INDEX IF NOT EXISTS idx_feedback_type    ON ui_feedback (feedback_type);
