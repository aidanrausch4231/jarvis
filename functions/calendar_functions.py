from datetime import datetime, timezone
from auth import get_calendar_service


def get_upcoming_events(max_results=10):
    service = get_calendar_service()
    now = datetime.now(timezone.utc).isoformat()
    result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return result.get("items", [])


def get_events_in_range(start: str, end: str):
    """start and end as ISO 8601 strings e.g. '2024-01-01T00:00:00Z'"""
    service = get_calendar_service()
    result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime,"
        )
        .execute()
    )
    return result.get("items", [])


def get_event(event_id: str):
    service = get_calendar_service()
    return service.events().get(calendarId="primary", eventId=event_id).execute()


def create_event(summary: str, start: str, end: str, description: str = "", location: str = ""):
    """start and end as ISO 8601 strings"""
    service = get_calendar_service()
    body = {
        "summary": summary,
        "description": description,
        "location": location,
        "start": {"dateTime": start, "timeZone": "UTC"},
        "end": {"dateTime": end, "timeZone": "UTC"},
    }
    return service.events().insert(calendarId="primary", body=body).execute()


def update_event(event_id: str, updates: dict):
    """Pass only the fields you want to change in updates dict"""
    service = get_calendar_service()
    event = get_event(event_id)
    event.update(updates)
    return service.events().update(calendarId="primary", eventId=event_id, body=event).execute()


def delete_event(event_id: str):
    service = get_calendar_service()
    service.events().delete(calendarId="primary", eventId=event_id).execute()


def list_calendars():
    service = get_calendar_service()
    result = service.calendarList().list().execute()
    return result.get("items", [])
