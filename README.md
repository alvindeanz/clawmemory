# ClawMemory

✨ **DreamClaw your AI’s memory**—pack it every night so your agent never forgets a thing! ✨

ClawMemory is a lightweight, open-source memory synchronization toolkit designed for AI agents. It implements a three-layer, incremental memory architecture with semantic search, enabling agents to maintain persistent context without overloading their prompt windows.

Key features:

- **Three-layer memory**: Daily context sync, weekly knowledge compounding, and hourly micro-sync safety net.
- **Incremental indexing**: Only new content is embedded into the semantic index to save compute.
- **Semantic search**: Built on `qmd` (BM25 + vector search + reranking) to efficiently retrieve relevant memory snippets.
- **Healthchecks & alerts**: Monitor sync jobs and alert on repeated failures to Microsoft Teams.
- **Easy to deploy**: Cron-based jobs, simple Python scripts, and clear configuration.

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/clawmemory.git
cd clawmemory
```

### 2. Install dependencies

Use your preferred Python environment:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Set the following variables (example for bash):

```bash
export TEAM_TENANT_ID=<your-tenant-id>
export TEAM_CLIENT_ID=<your-client-id>
export TEAM_CLIENT_SECRET=<your-client-secret>
export TEAM_REFRESH_TOKEN=<your-refresh-token>
export TEAM_ID=<your-team-id>
export TEAM_CHANNEL_ID=<your-channel-id>
export FAIL_THRESHOLD=2  # optional, default=2
```

### 4. Make scripts executable

```bash
chmod +x scripts/qmd_incremental_embed.py scripts/healthcheck_alert.py
```

### 5. Set up cron jobs

Edit your crontab (`crontab -e`) and add:

```cron
# Daily incremental embed (23:00 Asia/Taipei)
0 23 * * * cd /path/to/clawmemory && ./scripts/qmd_incremental_embed.py >> logs/daily_embed.log 2>&1 && ./scripts/healthcheck_alert.py

# Weekly memory compound (Sunday 22:00 Asia/Taipei)
0 22 * * 0 cd /path/to/clawmemory && crabot-agent-run "WEEKLY MEMORY COMPOUND ..." >> logs/weekly_compound.log 2>&1 && ./scripts/healthcheck_alert.py

# Hourly micro-sync (10,13,16,19,22 Asia/Taipei)
0 10,13,16,19,22 * * * cd /path/to/clawmemory && crabot-agent-run "MICRO-SYNC ..." >> logs/micro_sync.log 2>&1 && ./scripts/healthcheck_alert.py
```

### 6. Enjoy persistent AI memory!

---

For detailed documentation, see [USAGE.md](docs/USAGE.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
