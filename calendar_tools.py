import datetime
import logging
from langchain_core.tools import tool
from google_api import createService


def google_Calendar_client():
    API_NAME = "calendar"
    API_VERSION = "v3"
    SCOPES = [
        "https://www.googleapis.com/auth/calendar.events.freebusy",
        "https://www.googleapis.com/auth/calendar.events",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.settings.readonly",
    ]
    service = createService("credentials.json", API_NAME, API_VERSION, SCOPES)
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
    try:
        calendar_service = google_Calendar_client()
        now = (
            datetime.datetime.now(datetime.timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )
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
    except Exception as e:
        logging.error(f"Error fetching events: {e}")
        return []


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

    try:
        calendar_service = google_Calendar_client()
        datetime_str = f"{date} {time}"
        target_datetime = datetime.strptime(datetime_str, "%B %d, %Y %I:%M %p")

        # Prepare start and end times in ISO 8601 format
        start_time = target_datetime.isoformat() + "Z"
        end_time = (target_datetime + timedelta(hours=1)).isoformat() + "Z"

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
            return (
                f"You are busy during this time. Here are your events:\n"
                + "\n".join(event_details)
            )
        else:
            return "You are free during this time."
    except Exception as e:
        logging.error(f"Error checking availability: {e}")
        return f"Sorry, I couldn't check your availability due to an error: {e}"


@tool
def get_current_date():
    """Provides the current date in a user-friendly format.

    Returns:
        str: The current date in a format like "June 27, 2025."
    """
    from datetime import datetime

    return datetime.now().strftime("%B %d, %Y")


@tool
def delete_event_by_datetime(start_datetime: str, end_datetime: str):
    """Delete an event from the user's primary Google Calendar based on its time and date.

    Args:
        start_datetime (str): The start time of the event in ISO 8601 format (e.g., '2025-06-30T14:00:00Z').
        end_datetime (str): The end time of the event in ISO 8601 format (e.g., '2025-06-30T15:00:00Z').

    Returns:
        str: A confirmation message or an error message.
    """
    try:
        calendar_service = google_Calendar_client()

        events_result = (
            calendar_service.events()
            .list(
                calendarId="primary",
                timeMin=start_datetime,
                timeMax=end_datetime,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return "No events found for the specified time and date."

        for event in events:
            event_id = event["id"]
            calendar_service.events().delete(
                calendarId="primary", eventId=event_id
            ).execute()

        return f"Deleted {len(events)} event(s) successfully."
    except Exception as e:
        logging.error(f"Error deleting event(s): {e}")
        return f"Sorry, I couldn't delete the event(s) due to an error: {e}"


@tool
def create_event(summary: str, start: str, end: str):
    """Create a new event in the user's primary Google Calendar.
    Args:
        summary (str): Title or description of the event.
        start (str): Event start time in ISO 8601 datetime format (e.g., '2025-06-30T14:00:00Z').
        end (str): Event end time in ISO 8601 datetime format can be Optional.

    Returns:
        str: A link to the created event in Google Calendar, or a confirmation message.
    """
    try:
        calendar_service = google_Calendar_client()
        settings = calendar_service.settings().get(setting="timezone").execute()
        timezone = settings.get("value", "UTC")
        logging.info(f"Using timezone: {timezone}")

        if start.endswith('Z'):
            start = start[:-1]
        if end.endswith('Z'):
            end = end[:-1]

        ev = {
            "summary": summary,
            "start": {"dateTime": start, "timeZone": timezone},
            "end": {"dateTime": end, "timeZone": timezone},
        }
        logging.info(f"Creating event: {ev}")
        created = (
            calendar_service.events().insert(calendarId="primary", body=ev).execute()
        )
        return created.get("htmlLink", "✅ Event created")

    except Exception as e:
        logging.error(f"Error creating event: {e}")
        return f"Sorry, I couldn't create the event due to an error: {e}"
