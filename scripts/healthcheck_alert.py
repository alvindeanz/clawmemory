#!/usr/bin/env python3
"""
Healthcheck and Alert Script for Memory Sync Jobs via Microsoft Graph API

Checks last run statuses and sends alerts to Teams tech-channel if failures exceed threshold.
"""
import os
import json
import sys
import requests

# config from env
tenant_id = os.getenv('TEAM_TENANT_ID')
client_id = os.getenv('TEAM_CLIENT_ID')
client_secret = os.getenv('TEAM_CLIENT_SECRET')
refresh_token = os.getenv('TEAM_REFRESH_TOKEN')
team_id = os.getenv('TEAM_ID')
channel_id = os.getenv('TEAM_CHANNEL_ID')
threshold = int(os.getenv('FAIL_THRESHOLD', '2'))

missing = [v for v in ['tenant_id','client_id','client_secret','refresh_token','team_id','channel_id'] if not locals().get(v)]
if missing:
    print(f"[ERROR] Missing env vars: {missing}")
    sys.exit(1)

# state files
state_dir = os.path.expanduser('~/clawmemory_state')
jobs = {
    'daily': os.path.join(state_dir, 'daily_sync_state.json'),
    'weekly': os.path.join(state_dir, 'weekly_compound_state.json'),
    'micro': os.path.join(state_dir, 'micro_sync_state.json'),
    'embed': os.path.join(state_dir, 'qmd_index_state.json'),
}

# helper to load failure count

def load_fails(path):
    if not os.path.exists(path): return 0
    with open(path) as f:
        return json.load(f).get('failures', 0)

# get access token
def get_token():
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json().get('access_token')

# send message
def send_alert(token, job, count):
    url = f'https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = { 'body': { 'content': f"⚠️ Memory sync job '{job}' failed {count} times consecutively." } }
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()

# main
def main():
    alerts = [(j, load_fails(p)) for j,p in jobs.items() if load_fails(p) >= threshold]
    if not alerts: return
    token = get_token()
    for j,c in alerts: send_alert(token, j, c)

if __name__ == '__main__': main()
