import datetime
import logging
from langchain_core.tools import tool

from google_api import createService


def google_Calendar_client(client_secret):
    API_NAME = "calendar"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    service = createService(client_secret, API_NAME, API_VERSION, SCOPES)
    return service


@tool
def list_events(num: int = 5):
    """Fetch upcoming events from the user's primary Google Calendar.

    Retrieves the next `num` events starting from the current time, sorted by start time.

    Args:
        num (int): Maximum number of future events to return. Default is 5.
    Returns:
        List[dict]: A list of dictionaries, each containing:
            - 'summary' (str): The event’s title (empty string if none).
            - 'start' (str): The event’s start datetime in ISO 8601 format.
    """

    calendar_service = google_Calendar_client("credentials.json")
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events = (
        calendar_service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=num,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
        .get("items", [])
    )
    logging.info(events)
    return [
        {"summary": e.get("summary", ""), "start": e["start"].get("dateTime")}
        for e in events
    ]


@tool
def check_availability(date: str, time: str):
    """Checks if the user has free time at the given date and time.

    Args:
        date (str): The date for checking availability (e.g., "June 30, 2025").
        time (str): The time for checking availability (e.g., "2:00 PM").

    Returns:
        str: A message indicating whether the user is free or busy at the given time.
    """
    from datetime import datetime, timedelta

    
    datetime_str = f"{date} {time}"
    target_datetime = datetime.strptime(datetime_str, "%B %d, %Y %I:%M %p")

    # Prepare start and end times in ISO 8601 format
    start_time = target_datetime.isoformat() + "Z"
    end_time = (target_datetime + timedelta(hours=1)).isoformat() + "Z"


    calendar_service = google_Calendar_client("credentials.json")

    # Query events within the specified time range
    events_result = (
        calendar_service.events()
        .list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])


    if events:
        event_details = [
            f"- {event.get('summary', 'No Title')} from {event['start'].get('dateTime', 'Unknown')} to {event['end'].get('dateTime', 'Unknown')}"
            for event in events
        ]
        return f"You are busy during this time. Here are your events:\n" + "\n".join(
            event_details
        )
    else:
        return "You are free during this time."


@tool
def get_current_date():
    """Provides the current date in a user-friendly format.

    Returns:
        str: The current date in a format like "June 27, 2025."
    """
    from datetime import datetime

    return datetime.now().strftime("%B %d, %Y")


@tool
def create_event(summary: str, start: str, end: str):
    """Create a new event in the user's primary Google Calendar.
    Args:
        summary (str): Title or description of the event.
        start (str): Event start time in ISO 8601 datetime format (e.g., '2025-06-30T14:00:00Z').
        end (str): Event end time in ISO 8601 datetime format can be Optional.

    Returns:
        str: A link to the created event in Google Calendar, or a confirmation message."""

    calendar_service = google_Calendar_client("credentials.json")
    settings = calendar_service.settings().get(setting='timezone').execute()
    timezone = settings.get('value', 'UTC')
    ev = {
        "summary": summary,
        "start": {"dateTime": start, "timeZone": timezone},
        "end": {"dateTime": end, "timeZone": timezone},
    }
    created = calendar_service.events().insert(calendarId="primary", body=ev).execute()
    return created.get("htmlLink", "✅ Event created")
