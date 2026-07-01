---
name: tdd-repro
description: Forces a TDD workflow for bug fixing. Use when the user asks to fix a bug or an error.
allowed-tools: Bash, Read, Write, Edit
---
# Test-Driven Debugging Protocol

You are a strict TDD practitioner. You MUST follow this procedure sequentially. Do not skip steps.

## Phase 1: Prove the Failure (RED)
1. **Analyze**: Read the existing tests and the error logs provided by the user.
2. **Reproduce**: Create a NEW test file (e.g., `repro_issue_[id]`) that specifically targets the reported bug. Use the project's existing test conventions for file naming and structure.
3. **Verify**: Run the test. **It MUST fail.** If it passes, the bug is not reproduced; stop and ask the user for clarification.

## Phase 2: Implement the Fix (GREEN)
1. **Plan**: Propose the minimal code change required to make the test pass.
2. **Edit**: Modify the source code.
3. **Verify**: Run the reproduction test again. It must pass.

## Phase 3: Cleanup
1. **Refactor**: Clean up the code if necessary, ensuring tests still pass.
2. **Report**: Output the specific root cause and how the test proved it.

> **CRITICAL RULE:** Do not edit source code until you have a failing test case that confirms the issue [1-3].