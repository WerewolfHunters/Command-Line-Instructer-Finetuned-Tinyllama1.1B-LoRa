# 🧪 Dynamic Evaluation

This file captures real-time responses from the `agent.py` CLI agent, scoring the plan quality and dry-run capability for each prompt.

| Prompt                                                                 | Steps Generated | Dry Run Success | Score (0-2) |
|------------------------------------------------------------------------|------------------|------------------|-------------|
| Create a new Git branch and switch to it.                              | 2                | ✅ Yes            | 2           |
| Compress the folder reports into reports.tar.gz.                       | 2                | ✅ Yes            | 2           |
| List all Python files in the current directory recursively.            | 1                | ✅ Yes            | 2           |
| Set up a virtual environment and install requests.                     | 3                | ✅ Yes            | 2           |
| Fetch only the first ten lines of a file named output.log.            | 1                | ✅ Yes            | 2           |

✅ **All plans were well-structured, clear, and executable.** Logs were saved to `logs/trace.jsonl` for traceability.
