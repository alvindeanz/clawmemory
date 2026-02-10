# ClawMemory Usage Guide

This document provides detailed usage instructions and configuration examples for ClawMemory.

## Directory Layout

```
clawmemory/
├── memory/                # AI agent memory logs (daily markdown files)
├── scripts/
│   ├── qmd_incremental_embed.py
│   └── healthcheck_alert.py
├── docs/
│   └── USAGE.md
├── pyproject.toml
├── requirements.txt
├── README.md
├── LICENSE
└── .github/
```

## Memory Directory

- Place your daily `.md` logs under `memory/YYYY-MM-DD.md`.
- These files are appended by your agent or cron jobs.

## Scripts

### qmd_incremental_embed.py

Incrementally embed new lines from `memory/YYYY-MM-DD.md` into the QMD index.

```bash
./scripts/qmd_incremental_embed.py
```

### healthcheck_alert.py

Monitor failure counts across sync jobs and send alerts to Microsoft Teams.

```bash
./scripts/healthcheck_alert.py
```

## Configuration

### Environment Variables

```bash
export TEAM_TENANT_ID=
export TEAM_CLIENT_ID=
export TEAM_CLIENT_SECRET=
export TEAM_REFRESH_TOKEN=
export TEAM_ID=
export TEAM_CHANNEL_ID=
export FAIL_THRESHOLD=2
```

### Cron Jobs

Add to your `crontab -e`:

```cron
# Daily embed (23:00 Asia/Taipei)
0 23 * * * cd /path/to/clawmemory && ./scripts/qmd_incremental_embed.py >> logs/daily_embed.log 2>&1 && ./scripts/healthcheck_alert.py
```

Adjust schedules for weekly and hourly micro-sync.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md).
