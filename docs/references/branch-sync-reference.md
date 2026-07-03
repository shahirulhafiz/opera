# Branch Sync Reference — updating `main` from `scrubber/main`

How to update the local `main` branch with the latest changes from the
`scrubber` remote. Automated by [`scripts/sync-from-scrubber.ps1`](../../scripts/sync-from-scrubber.ps1).

## Background

This repo has two remotes:

| Remote | URL | Role |
|--------|-----|------|
| `origin` | `github.com/shahirulhafiz/opera.git` | Primary/publish remote |
| `scrubber` | `github.com/shahirulhafiz/scrubber.git` | Upstream source of harness updates |

The local `main` and `scrubber/main` histories have **no common ancestor**
(separate root commits). A normal `git merge` or `git pull` therefore refuses to
combine them, so the sync must pass `--allow-unrelated-histories`.

## Quick start

```powershell
# From the repo root. Merges scrubber/main into the current branch.
./scripts/sync-from-scrubber.ps1

# Merge and then push the result to origin
./scripts/sync-from-scrubber.ps1 -Push

# Override the remote or branch
./scripts/sync-from-scrubber.ps1 -Remote scrubber -Branch main
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-Remote` | `scrubber` | Git remote to sync from |
| `-Branch` | `main` | Branch on the remote to merge |
| `-Push` | *(off)* | Push the current branch to `origin` after a clean merge |

## What the script does

1. Verifies it is inside a git repo and the working tree is **clean** (aborts otherwise).
2. `git fetch <remote>`.
3. Prints how many commits the current branch is ahead / behind `<remote>/<branch>`.
4. `git merge <remote>/<branch> --allow-unrelated-histories --no-edit`.
5. On conflict: stops and prints the resolve / abort instructions.
6. On success: prints `git status`, and pushes to `origin` if `-Push` was given.

## Manual equivalent

If you prefer to run it by hand:

```powershell
git fetch scrubber
git rev-list --left-right --count HEAD...scrubber/main   # ahead/behind check
git merge scrubber/main --allow-unrelated-histories --no-edit
git status
git push origin main                                     # optional
```

## Handling conflicts

If the merge reports conflicts:

```powershell
git status                 # see conflicted files
# ...edit files to resolve...
git add <resolved-files>
git commit                 # completes the merge

# or, to bail out entirely:
git merge --abort
```

## Notes & safety

- The script **will not run** with uncommitted changes — commit or stash first.
- It never force-pushes and never touches git config.
- After merging, the branch is ahead of `origin/main` until you push
  (with `-Push` or `git push origin main`).
- First-time sync pulled in only `.claude/skills/analyze-requirements/SKILL.md`;
  the rest of `scrubber/main`'s content was already present.

## See also

- Script: [`scripts/sync-from-scrubber.ps1`](../../scripts/sync-from-scrubber.ps1)
- Git docs: [`git merge --allow-unrelated-histories`](https://git-scm.com/docs/git-merge#Documentation/git-merge.txt---allow-unrelated-histories)
