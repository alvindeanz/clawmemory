#!/usr/bin/env python3
"""
Incremental QMD Embed Script

Embeds only the new lines appended to memory/YYYY-MM-DD.md files
using qmd. Keeps track of last embedded line per file in state file.
"""
import os
import json
import subprocess
from datetime import date

STATE_DIR = os.path.expanduser("~/clawmemory_state")
STATE_FILE = os.path.join(STATE_DIR, "qmd_index_state.json")
MEMORY_DIR = os.path.join(os.getcwd(), "memory")

# ensure state dir exists
os.makedirs(STATE_DIR, exist_ok=True)

# load or init state
if os.path.exists(STATE_FILE):
    with open(STATE_FILE) as f:
        state = json.load(f)
else:
    state = {}

# today's memory file
today = date.today().isoformat()
file_name = f"{today}.md"
file_path = os.path.join(MEMORY_DIR, file_name)
if not os.path.exists(file_path):
    print(f"[INFO] No memory file for today: {file_path}")
    exit(0)

# read lines
with open(file_path) as f:
    lines = f.readlines()
last_line = state.get(file_name, 0)
new_lines = lines[last_line:]
if not new_lines:
    print("[INFO] No new content to embed.")
    exit(0)

# write new chunk
chunk_path = os.path.join(STATE_DIR, f"{file_name}.chunk.md")
with open(chunk_path, 'w') as f:
    f.writelines(new_lines)

# run qmd embed
try:
    subprocess.run(["qmd", "embed", chunk_path], check=True)
    state[file_name] = len(lines)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"[OK] Embedded lines {last_line}–{len(lines)} for {file_name}")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] qmd embed failed: {e}")
    exit(1)
