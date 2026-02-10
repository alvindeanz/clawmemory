#!/usr/bin/env python3
"""
Full QMD Index Refresh Script

Runs a full semantic index update and embed for all memory files using qmd.
This ensures new content is searchable without incremental chunk limitations.
"""
import subprocess
import sys

def main():
    try:
        subprocess.run(["qmd", "update"], check=True)
        subprocess.run(["qmd", "embed"], check=True)
        print("[OK] Full QMD index update and embed completed.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] QMD update/embed failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
