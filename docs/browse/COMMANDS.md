# Web Browse Store Commands

Run all commands from repo root:

```powershell
cd c:\Workstation\Flux\opera
```

## Base pattern

```powershell
python scripts/store.py --db docs/browse/webapp.db <command> [options]
```

If `python` is not available, use `py` instead.

## Setup

Initialize DB schema (safe to run repeatedly):

```powershell
python scripts/store.py --db docs/browse/webapp.db init
```

Show CLI help:

```powershell
python scripts/store.py --help
```

## Register targets

Register all targets from root `targets.toml`:

```powershell
python scripts/store.py --db docs/browse/webapp.db register-config
```

Register one target by slug from `targets.toml`:

```powershell
python scripts/store.py --db docs/browse/webapp.db register-config --slug my-app
```

Register one target manually:

```powershell
python scripts/store.py --db docs/browse/webapp.db register --slug my-app --url https://example.com
```

Optional fields:

```powershell
python scripts/store.py --db docs/browse/webapp.db register --slug my-app --url https://example.com --goal "Smoke test" --auth "none"
```

List registered targets:

```powershell
python scripts/store.py --db docs/browse/webapp.db list-targets
```

Delete one target by slug (also removes related pages/runs/elements/logs via DB cascade):

```powershell
python scripts/store.py --db docs/browse/webapp.db delete-target --slug my-app
```

## Crawl frontier

Add a page:

```powershell
python scripts/store.py --db docs/browse/webapp.db add-page --slug my-app --url https://example.com/about --depth 1
```

Get next unvisited page:

```powershell
python scripts/store.py --db docs/browse/webapp.db next-page --slug my-app
```

Mark page visited:

```powershell
python scripts/store.py --db docs/browse/webapp.db mark-visited --page-id 1
```

## Runs and action logs

Start run:

```powershell
python scripts/store.py --db docs/browse/webapp.db start-run --slug my-app --bounds "{\"max_pages\":25,\"max_depth\":3,\"max_actions\":300}"
```

Log action:

```powershell
python scripts/store.py --db docs/browse/webapp.db log-action --run 1 --action click --result-status ok --duration-ms 120
```

End run:

```powershell
python scripts/store.py --db docs/browse/webapp.db end-run --run 1 --status complete
```

## Query results

Find elements:

```powershell
python scripts/store.py --db docs/browse/webapp.db find --name "Login"
```

Free-text query:

```powershell
python scripts/store.py --db docs/browse/webapp.db query "checkout error"
```

Errors only:

```powershell
python scripts/store.py --db docs/browse/webapp.db logs --slug my-app --errors-only
```

Feedback messages:

```powershell
python scripts/store.py --db docs/browse/webapp.db feedback --slug my-app
```

Stats:

```powershell
python scripts/store.py --db docs/browse/webapp.db stats --slug my-app
```

Markdown report:

```powershell
python scripts/store.py --db docs/browse/webapp.db report --slug my-app
```
