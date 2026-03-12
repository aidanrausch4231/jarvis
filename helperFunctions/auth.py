import os
import json
import threading
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/gmail.modify",
]

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"

_creds = None
_services = {}


def _load_or_authorize():
    global _creds
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    _creds = creds
    return creds


def _refresh_token():
    global _creds
    if _creds and _creds.expired and _creds.refresh_token:
        _creds.refresh(Request())
        with open(TOKEN_FILE, "w") as f:
            f.write(_creds.to_json())
    _schedule_refresh()


def _schedule_refresh():
    timer = threading.Timer(3600, _refresh_token)
    timer.daemon = True
    timer.start()


def get_credentials():
    global _creds
    if _creds is None:
        _load_or_authorize()
        _schedule_refresh()
    return _creds


def get_service(api: str, version: str):
    key = f"{api}_{version}"
    if key not in _services:
        creds = get_credentials()
        _services[key] = build(api, version, credentials=creds)
    return _services[key]


def get_calendar_service():
    return get_service("calendar", "v3")


def get_tasks_service():
    return get_service("tasks", "v1")


def get_gmail_service():
    return get_service("gmail", "v1")
