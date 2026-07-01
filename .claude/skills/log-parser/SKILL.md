---
name: log-parser
description: efficiently parses large log files to find errors without polluting context.
allowed-tools: Bash
---
# Log Analysis Protocol

Do not use `Read` on large log files directly. Instead, use `Bash` tools to extract relevant signals.

## Procedure
1. **Identify**: Locate the log file (e.g., `error.log`, `system.log`).
2. **Extract**: Use `grep` to find lines containing "Error", "Exception", or "Fail" within the last 500 lines.
   - Example: `grep -C 5 "Error" logs/app.log | tail -n 50`
3. **Isolate**: If a stack trace is found, capture the specific filenames and line numbers mentioned.
4. **Report**: Present the exact error message and the file/line number to the user [9, 10].