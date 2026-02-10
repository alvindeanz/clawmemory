#!/usr/bin/env python3
"""
Healthcheck and Alert Script for ClawMemory

Supports multiple alert backends:
  - Generic Webhook (Slack, Discord, custom)
  - Microsoft Teams (via Graph API)

Environment Variables:
  CLAWMEMORY_STATE_DIR    - State directory (default: ~/.clawmemory)
  ALERT_BACKEND           - "webhook" or "teams" (default: webhook)
  ALERT_WEBHOOK_URL       - Generic webhook URL (for Slack/Discord/custom)
  FAIL_THRESHOLD          - Consecutive failures before alerting (default: 2)
  
  # Teams-specific (only if ALERT_BACKEND=teams):
  TEAM_TENANT_ID, TEAM_CLIENT_ID, TEAM_CLIENT_SECRET, 
  TEAM_REFRESH_TOKEN, TEAM_ID, TEAM_CHANNEL_ID
"""
import os
import json
import sys
import requests
from datetime import datetime

# Configuration
STATE_DIR = os.path.expanduser(os.getenv('CLAWMEMORY_STATE_DIR', '~/.clawmemory'))
STATE_FILE = os.path.join(STATE_DIR, 'refresh_state.json')
ALERT_BACKEND = os.getenv('ALERT_BACKEND', 'webhook').lower()
WEBHOOK_URL = os.getenv('ALERT_WEBHOOK_URL', '')
THRESHOLD = int(os.getenv('FAIL_THRESHOLD', '2'))

# Teams config
TEAMS_CONFIG = {
    'tenant_id': os.getenv('TEAM_TENANT_ID'),
    'client_id': os.getenv('TEAM_CLIENT_ID'),
    'client_secret': os.getenv('TEAM_CLIENT_SECRET'),
    'refresh_token': os.getenv('TEAM_REFRESH_TOKEN'),
    'team_id': os.getenv('TEAM_ID'),
    'channel_id': os.getenv('TEAM_CHANNEL_ID'),
}


def load_state():
    """Load the refresh state from disk."""
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE) as f:
        return json.load(f)


def send_webhook_alert(message: str):
    """Send alert via generic webhook (Slack/Discord/custom)."""
    if not WEBHOOK_URL:
        print("[WARN] ALERT_WEBHOOK_URL not set, skipping alert")
        return False
    
    # Try Slack/Discord format first
    payload = {"text": message, "content": message}
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        r.raise_for_status()
        print(f"[OK] Webhook alert sent")
        return True
    except Exception as e:
        print(f"[ERROR] Webhook failed: {e}", file=sys.stderr)
        return False


def send_teams_alert(message: str):
    """Send alert via Microsoft Teams Graph API."""
    cfg = TEAMS_CONFIG
    missing = [k for k, v in cfg.items() if not v]
    if missing:
        print(f"[ERROR] Missing Teams config: {missing}", file=sys.stderr)
        return False
    
    try:
        # Get access token
        token_url = f"https://login.microsoftonline.com/{cfg['tenant_id']}/oauth2/v2.0/token"
        token_data = {
            'grant_type': 'refresh_token',
            'refresh_token': cfg['refresh_token'],
            'client_id': cfg['client_id'],
            'client_secret': cfg['client_secret'],
            'scope': 'https://graph.microsoft.com/.default'
        }
        token_resp = requests.post(token_url, data=token_data, timeout=10)
        token_resp.raise_for_status()
        access_token = token_resp.json()['access_token']
        
        # Send message
        msg_url = f"https://graph.microsoft.com/v1.0/teams/{cfg['team_id']}/channels/{cfg['channel_id']}/messages"
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        payload = {'body': {'content': message}}
        msg_resp = requests.post(msg_url, headers=headers, json=payload, timeout=10)
        msg_resp.raise_for_status()
        
        print(f"[OK] Teams alert sent")
        return True
    except Exception as e:
        print(f"[ERROR] Teams alert failed: {e}", file=sys.stderr)
        return False


def send_alert(message: str):
    """Send alert via configured backend."""
    if ALERT_BACKEND == 'teams':
        return send_teams_alert(message)
    else:
        return send_webhook_alert(message)


def main():
    state = load_state()
    
    if state is None:
        print("[INFO] No state file found, skipping healthcheck")
        return 0
    
    failures = state.get('failures', 0)
    last_failure = state.get('last_failure', 'unknown')
    
    if failures >= THRESHOLD:
        message = (
            f"⚠️ **ClawMemory Alert**\n"
            f"QMD refresh failed {failures} times consecutively.\n"
            f"Last failure: {last_failure}\n"
            f"Please check logs and run manually."
        )
        send_alert(message)
        return 1
    
    print(f"[OK] Healthcheck passed (failures: {failures}/{THRESHOLD})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
