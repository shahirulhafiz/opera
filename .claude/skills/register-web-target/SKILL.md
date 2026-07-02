---
name: register-web-target
description: Initialize the web browse SQLite store and register target URL(s) for crawling. Use when setting up a new app URL/slug, syncing targets from targets.toml, or seeding the crawl frontier before browse-inspect.
---

# register-web-target

Register crawl targets in `docs/browse/webapp.db` through the user-facing CLI.
Use this before running `browse-inspect`.

## Commands

Always run through:

```bash
python scripts/store.py --db docs/browse/webapp.db <command> ...
```

### 1) Initialize store

```bash
python scripts/store.py --db docs/browse/webapp.db init
```

### 2) Register targets

- Single target:

```bash
python scripts/store.py --db docs/browse/webapp.db register --slug <slug> --url <url> [--goal "..."] [--auth "..."]
```

- From config (default root file):

```bash
python scripts/store.py --db docs/browse/webapp.db register-config
```

- One target from config:

```bash
python scripts/store.py --db docs/browse/webapp.db register-config --slug <slug>
```

## Expected result

- Target exists/updated in `targets`.
- Entry URL is seeded into `pages` frontier (`depth=0`, `visited=0`).
- `list-targets` shows the registered slug/url:

```bash
python scripts/store.py --db docs/browse/webapp.db list-targets
```
