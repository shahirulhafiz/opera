#!/usr/bin/env python3
"""SessionStart hook: inject a project-aware harness onboarding brief.

Claude Code runs this on a fresh session start, pipes session JSON (including
`cwd`) on stdin, and injects the returned `additionalContext` as a system-reminder
(not visible in the terminal). The text instructs the agent to lead its first
response with a short onboarding brief.

Project-name agnostic by design: this repo is meant to be used as a GitHub
template, so the project name is derived at runtime from the working directory
rather than hardcoded. Claude Code cannot print a banner before the user types;
this is the reliable path to surface onboarding in the agent's first reply.
"""
import json
import os
import sys


def read_payload() -> dict:
    """Best-effort parse of the hook JSON Claude Code pipes on stdin."""
    try:
        raw = sys.stdin.read()
    except (OSError, ValueError):
        return {}
    if not raw or not raw.strip():
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, ValueError):
        return {}


def project_name(payload: dict) -> str:
    cwd = payload.get("cwd") or os.getcwd()
    name = os.path.basename(os.path.normpath(str(cwd)))
    return name or "this project"


def build_context(name: str) -> str:
    return (
        "[HARNESS ONBOARDING - first response only]\n"
        f"You are working in the project '{name}', which is scaffolded on the "
        "Orchestral Harness: a hands-off agent-orchestration template (the harness "
        "is the framework, not the project's name). UNLESS the user's first message "
        "is already a concrete task, begin your first response with a brief "
        "(<=5 lines) orientation, then offer to help:\n"
        "- What this is: a hands-off agent-orchestration harness that routes your "
        "requests to the right agents and workflows — just describe work in plain "
        "language; no @agent or skill tagging.\n"
        "- Routing: trivial edits run directly; features/changes/bugs route through the "
        "orchestrator, which runs the matching workflow from .claude/workflows/registry.yml "
        "(or the built-in ad-hoc route, since the registry ships routeless).\n"
        "- Author a cycle: mention a 'workflow/cycle/pipeline' and the workflow-author "
        "agent scaffolds, validates, and registers it.\n"
        "- Point to README.md and CLAUDE.md for more.\n"
        "Show this only once per session; if the user opens with a concrete task, skip "
        "the greeting and just do the work."
    )


def main() -> int:
    name = project_name(read_payload())
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": build_context(name),
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
