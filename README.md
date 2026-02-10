# ClawMemory

✨ **DreamClaw your AI's memory**—pack it every night so your agent never forgets a thing! ✨

ClawMemory is a lightweight, open-source memory synchronization toolkit for AI agents. Inspired by how humans consolidate memories during sleep, it implements a **three-layer architecture** that keeps your agent's context fresh without overloading prompt windows.

---

## 🧠 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    Three-Layer Memory                        │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Daily Context Sync (Every Night)                  │
│  └─ Capture the day's conversations → memory/YYYY-MM-DD.md  │
│                                                             │
│  Layer 2: Weekly Knowledge Compound (Every Sunday)          │
│  └─ Distill weekly insights → Update MEMORY.md              │
│                                                             │
│  Layer 3: Hourly Micro-Sync (Safety Net)                    │
│  └─ Lightweight checks during work hours                    │
├─────────────────────────────────────────────────────────────┤
│  Bottom Layer: Semantic Search (qmd)                        │
│  └─ BM25 + Vector Search + Reranking                        │
│  └─ Query past memories instantly                           │
└─────────────────────────────────────────────────────────────┘
```

**Key insight**: Don't stuff everything into the context window. Keep a curated "cheat sheet" (MEMORY.md) always loaded, and search the archive when needed.

---

## ✨ Features

- **Zero Python dependencies**: Uses only standard library—no `pip install` needed
- **Nightly full refresh**: Runs `qmd update && qmd embed` to keep semantic index fresh
- **Pre-flight checks**: Validates collection exists before refresh, fails loudly if not
- **Flexible alerts**: Webhook (Slack/Discord) or Microsoft Teams
- **Failure tracking**: Auto-alerts after N consecutive failures
- **Works with any agent**: Platform-agnostic, just needs markdown files

---

## 📦 Prerequisites

### Install qmd

ClawMemory uses [qmd](https://github.com/anthropics/qmd) for semantic search. Install it first:

```bash
bun install -g @anthropics/qmd
```

### Create a collection (required before first refresh)

```bash
cd /path/to/your/workspace
qmd collection add . --name workspace --mask "**/*.md"
```

> ⚠️ **Important**: You must create a collection before running `qmd update && qmd embed`. Without it, refresh will succeed but nothing will be indexed.

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/alvindeanz/clawmemory.git
cd clawmemory
```

### 2. Configure environment variables

> 💡 **No `pip install` needed!** Scripts use only Python standard library.

```bash
# State directory (optional, default: ~/.clawmemory)
export CLAWMEMORY_STATE_DIR=~/.clawmemory

# Alert backend: "webhook" or "teams"
export ALERT_BACKEND=webhook

# For Slack/Discord/Generic webhook:
export ALERT_WEBHOOK_URL=https://hooks.slack.com/services/xxx

# Failure threshold (optional, default: 2)
export FAIL_THRESHOLD=2
```

<details>
<summary>📋 Microsoft Teams Configuration</summary>

```bash
export ALERT_BACKEND=teams
export TEAM_TENANT_ID=your-tenant-id
export TEAM_CLIENT_ID=your-client-id
export TEAM_CLIENT_SECRET=your-client-secret
export TEAM_REFRESH_TOKEN=your-refresh-token
export TEAM_ID=your-team-id
export TEAM_CHANNEL_ID=your-channel-id
```
</details>

### 3. Make scripts executable

```bash
chmod +x scripts/qmd_refresh.py scripts/healthcheck_alert.py
```

### 4. Set up cron job

```bash
crontab -e
```

Add:

```cron
# Nightly QMD refresh (23:00 local time)
0 23 * * * cd /path/to/workspace && /path/to/clawmemory/scripts/qmd_refresh.py && /path/to/clawmemory/scripts/healthcheck_alert.py
```

### 5. Enjoy persistent AI memory! 🎉

---

## 📁 Recommended Workspace Structure

```
your-workspace/
├── MEMORY.md              # Curated long-term memory (injected every session)
├── AGENTS.md              # Agent behavior rules
├── memory/
│   ├── 2026-02-07.md      # Daily logs
│   ├── 2026-02-08.md
│   ├── 2026-02-09.md
│   └── projects.md        # Long-term reference files
└── .clawmemory/           # State files (auto-created)
    └── refresh_state.json
```

---

## 🔧 Scripts

| Script | Purpose |
|--------|---------|
| `qmd_refresh.py` | Runs full `qmd update && qmd embed`, tracks success/failure |
| `healthcheck_alert.py` | Checks failure count, sends alert if threshold exceeded |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE)
