#!/usr/bin/env python3
"""
QMD Full Refresh Script

Runs a full semantic index update and embed for all memory files using qmd.
Tracks success/failure state for healthcheck monitoring.

Zero external dependencies - uses only Python standard library.
"""
import os
import json
import subprocess
import sys
from datetime import datetime

STATE_DIR = os.path.expanduser(os.getenv('CLAWMEMORY_STATE_DIR', '~/.clawmemory'))
STATE_FILE = os.path.join(STATE_DIR, 'refresh_state.json')


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {'failures': 0, 'last_success': None, 'last_failure': None}


def save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def check_collection_exists():
    """Check if at least one qmd collection exists."""
    try:
        result = subprocess.run(
            ["qmd", "collection", "list"],
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr
        
        # Check for "No collections" message or empty output
        if "No collections" in output or "no collections" in output.lower():
            return False
        if result.returncode != 0:
            return False
        # If we got some output without error, assume collection exists
        return bool(result.stdout.strip())
    except FileNotFoundError:
        print("[ERROR] qmd command not found. Install with: bun install -g @anthropics/qmd", file=sys.stderr)
        sys.exit(1)


def main():
    state = load_state()
    now = datetime.now().isoformat()
    
    # Pre-flight check: ensure collection exists
    if not check_collection_exists():
        print("[ERROR] No qmd collection found!", file=sys.stderr)
        print("", file=sys.stderr)
        print("Create one first:", file=sys.stderr)
        print("  cd /path/to/your/workspace", file=sys.stderr)
        print("  qmd collection add . --name workspace --mask \"**/*.md\"", file=sys.stderr)
        
        state['failures'] += 1
        state['last_failure'] = now
        state['last_error'] = 'No collection found'
        save_state(state)
        return 1
    
    try:
        # Run qmd update
        result_update = subprocess.run(["qmd", "update"], capture_output=True, text=True)
        if result_update.returncode != 0:
            raise subprocess.CalledProcessError(result_update.returncode, "qmd update", result_update.stderr)
        
        # Run qmd embed
        result_embed = subprocess.run(["qmd", "embed"], capture_output=True, text=True)
        if result_embed.returncode != 0:
            raise subprocess.CalledProcessError(result_embed.returncode, "qmd embed", result_embed.stderr)
        
        # Success - reset failure count
        state['failures'] = 0
        state['last_success'] = now
        state['last_error'] = None
        save_state(state)
        print(f"[OK] QMD refresh completed at {now}")
        return 0
        
    except subprocess.CalledProcessError as e:
        state['failures'] += 1
        state['last_failure'] = now
        state['last_error'] = str(e)
        save_state(state)
        print(f"[ERROR] QMD refresh failed: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
