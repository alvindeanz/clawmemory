#!/usr/bin/env python3
"""
QMD Full Refresh Script

Runs a full semantic index update and embed for all memory files using qmd.
Tracks success/failure state for healthcheck monitoring.
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

def main():
    state = load_state()
    now = datetime.now().isoformat()
    
    try:
        subprocess.run(["qmd", "update"], check=True)
        subprocess.run(["qmd", "embed"], check=True)
        
        # Success - reset failure count
        state['failures'] = 0
        state['last_success'] = now
        save_state(state)
        print(f"[OK] QMD refresh completed at {now}")
        return 0
        
    except subprocess.CalledProcessError as e:
        # Failure - increment counter
        state['failures'] += 1
        state['last_failure'] = now
        save_state(state)
        print(f"[ERROR] QMD refresh failed: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
