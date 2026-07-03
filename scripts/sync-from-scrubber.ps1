<#
.SYNOPSIS
    Update the current branch with the latest from a remote branch (default: scrubber/main).

.DESCRIPTION
    Fetches the given remote and merges <Remote>/<Branch> into the current branch.
    Because the local history and scrubber history can be unrelated (separate roots),
    the merge uses --allow-unrelated-histories. Aborts cleanly if the working tree is
    dirty or if the merge hits conflicts.

.PARAMETER Remote
    Name of the git remote to sync from. Defaults to 'scrubber'.

.PARAMETER Branch
    Branch on the remote to merge. Defaults to 'main'.

.PARAMETER Push
    If set, pushes the current branch to 'origin' after a successful merge.

.EXAMPLE
    ./scripts/sync-from-scrubber.ps1

.EXAMPLE
    ./scripts/sync-from-scrubber.ps1 -Remote scrubber -Branch main -Push
#>
[CmdletBinding()]
param(
    [string]$Remote = 'scrubber',
    [string]$Branch = 'main',
    [switch]$Push
)

$ErrorActionPreference = 'Stop'

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

# Ensure we're inside a git repo.
& git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) {
    throw 'Not inside a git repository.'
}

# Refuse to run with a dirty working tree.
$dirty = & git status --porcelain
if ($dirty) {
    throw 'Working tree is not clean. Commit or stash your changes first.'
}

$currentBranch = (& git rev-parse --abbrev-ref HEAD).Trim()
$ref = "$Remote/$Branch"

Write-Host "Fetching '$Remote'..." -ForegroundColor Cyan
Invoke-Git fetch $Remote

# Report divergence before merging.
$revList = & git rev-list --left-right --count "HEAD...$ref"
if ($LASTEXITCODE -ne 0) {
    throw "git rev-list --left-right --count 'HEAD...$ref' failed with exit code $LASTEXITCODE"
}
$counts = $revList.Trim() -split '\s+'
Write-Host "Current branch '$currentBranch' is $($counts[0]) ahead, $($counts[1]) behind '$ref'." -ForegroundColor Yellow

Write-Host "Merging '$ref' into '$currentBranch'..." -ForegroundColor Cyan
& git merge $ref --allow-unrelated-histories --no-edit
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Merge produced conflicts. Resolve them, then run:' -ForegroundColor Red
    Write-Host '  git add <files>; git commit' -ForegroundColor Red
    Write-Host 'Or abort with: git merge --abort' -ForegroundColor Red
    throw 'Merge conflict.'
}

Write-Host 'Merge complete. Working tree status:' -ForegroundColor Green
Invoke-Git status --short --branch

if ($Push) {
    Write-Host "Pushing '$currentBranch' to origin..." -ForegroundColor Cyan
    Invoke-Git push origin $currentBranch
    Write-Host 'Push complete.' -ForegroundColor Green
}