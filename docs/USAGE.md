# ClawMemory Usage Guide

## Overview

ClawMemory helps AI agents maintain persistent memory across sessions using a three-layer architecture inspired by human sleep-based memory consolidation.

---

## Scripts

### qmd_refresh.py

Refreshes the semantic search index by running:
1. `qmd update` - Scans for new/changed files
2. `qmd embed` - Generates vector embeddings

**Usage:**
```bash
./scripts/qmd_refresh.py
```

**Exit codes:**
- `0` - Success
- `1` - Failure (also increments failure counter)

**State file:** `~/.clawmemory/refresh_state.json`
```json
{
  "failures": 0,
  "last_success": "2026-02-11T23:00:00",
  "last_failure": null
}
```

---

### healthcheck_alert.py

Checks failure count and sends alerts when threshold is exceeded.

**Usage:**
```bash
./scripts/healthcheck_alert.py
```

**Alert backends:**

| Backend | Env Var | Example |
|---------|---------|---------|
| Webhook | `ALERT_WEBHOOK_URL` | Slack, Discord, custom |
| Teams | `TEAM_*` vars | Microsoft Teams via Graph API |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAWMEMORY_STATE_DIR` | `~/.clawmemory` | Where to store state files |
| `ALERT_BACKEND` | `webhook` | Alert method: `webhook` or `teams` |
| `ALERT_WEBHOOK_URL` | - | Webhook URL for Slack/Discord/custom |
| `FAIL_THRESHOLD` | `2` | Consecutive failures before alerting |

### Teams-specific variables

| Variable | Description |
|----------|-------------|
| `TEAM_TENANT_ID` | Azure AD tenant ID |
| `TEAM_CLIENT_ID` | App client ID |
| `TEAM_CLIENT_SECRET` | App client secret |
| `TEAM_REFRESH_TOKEN` | OAuth refresh token |
| `TEAM_ID` | Teams team ID |
| `TEAM_CHANNEL_ID` | Channel ID for alerts |

---

## Cron Examples

### Basic nightly refresh
```cron
0 23 * * * cd /workspace && /path/to/scripts/qmd_refresh.py && /path/to/scripts/healthcheck_alert.py
```

### With logging
```cron
0 23 * * * cd /workspace && /path/to/scripts/qmd_refresh.py >> /var/log/clawmemory.log 2>&1 && /path/to/scripts/healthcheck_alert.py
```

---

## Integrating with AI Agents

### OpenClaw / Clawdbot

Add to your `AGENTS.md`:

```markdown
## Memory Retrieval (MANDATORY)

Never read MEMORY.md or memory/*.md in full for lookups. Use qmd:

1. `qmd query "<question>"` — combined search with reranking
2. `qmd get <file>:<line> -l 20` — pull only the snippet you need
3. Only if qmd returns nothing: fall back to reading files
```

### Generic LLM Agents

1. Inject `MEMORY.md` into system prompt at session start
2. For detailed lookups, have the agent call `qmd query "..."` 
3. Use ClawMemory cron to keep the index fresh

---

## Troubleshooting

### "qmd: command not found"
Install qmd first:
```bash
bun install -g https://github.com/tobi/qmd
```
Or ensure `qmd` is in your PATH.

### "qmd update runs but nothing is indexed"
You need to create a collection first:
```bash
cd /path/to/your/workspace
qmd collection add . --name workspace --mask "**/*.md"
```

### "No state file found"
Run `qmd_refresh.py` at least once to create the state file.

### Webhook not working
- Check `ALERT_WEBHOOK_URL` is set correctly
- Test with curl: `curl -X POST -H "Content-Type: application/json" -d '{"text":"test"}' $ALERT_WEBHOOK_URL`

---

## See Also

- [README.md](../README.md) - Quick start guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
