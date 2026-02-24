from icalendar import Calendar
from datetime import datetime
import pytz

class CalendarEngine:
    def __init__(self, ics_path):
        self.ics_path = ics_path

    def _load_calendar(self):
        with open(self.ics_path, 'rb') as f:
            return Calendar.from_ical(f.read())

    def get_upcoming_events(self):
        cal = self._load_calendar()
        now = datetime.now(pytz.UTC)

        events = []

        for component in cal.walk():
            if component.name == "VEVENT":
                start = component.get('dtstart').dt
                summary = str(component.get('summary'))

                if isinstance(start, datetime):
                    if start > now:
                        events.append({
                            "title": summary,
                            "start": start
                        })

        events.sort(key=lambda x: x["start"])
        return events