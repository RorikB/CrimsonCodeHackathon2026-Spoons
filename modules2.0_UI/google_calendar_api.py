"""
Google Calendar API Integration
================================

Uses OAuth 2.0 to access your Google Calendar with real-time sync.
"""

import os
from datetime import datetime, timedelta
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes define what your app can access
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarAPI:
    def __init__(self):
        self.service = None
        self.credentials_file = 'credentials.json'
        self.token_file = 'token.json'
        
    def authenticate(self):
        """Authenticate with Google Calendar API using OAuth"""
        creds = None
        
        # Check if we already have a valid token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh expired token
                print("Refreshing expired token...")
                creds.refresh(Request())
            else:
                # First time - open browser for authorization
                if not os.path.exists(self.credentials_file):
                    print("❌ Error: credentials.json not found!")
                    print("Please follow GOOGLE_CALENDAR_API_SETUP.txt to create it.")
                    return False
                
                print("Opening browser for authorization...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for next time
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
            print("✓ Authorization successful!")
        
        # Build the service
        self.service = build('calendar', 'v3', credentials=creds)
        return True
    
    def get_upcoming_events(self, max_results=10):
        """Get upcoming events from primary calendar"""
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            now = datetime.now(pytz.UTC).isoformat().replace('+00:00', 'Z')
            
            print(f"Fetching next {max_results} events...")
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Format events
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                
                formatted_events.append({
                    'title': event.get('summary', 'Untitled Event'),
                    'start': start,
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'all_day': 'date' in event['start']  # True if only date, not dateTime
                })
            
            return formatted_events
            
        except Exception as e:
            print(f"❌ Error fetching events: {e}")
            return []
    
    def get_todays_events(self):
        """Get all events happening today"""
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            # Get start and end of today in UTC
            now = datetime.now(pytz.UTC)
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=today_start.isoformat(),
                timeMax=today_end.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                
                formatted_events.append({
                    'title': event.get('summary', 'Untitled Event'),
                    'start': start,
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'all_day': 'date' in event['start']
                })
            
            return formatted_events
            
        except Exception as e:
            print(f"❌ Error fetching today's events: {e}")
            return []
    
    def whats_my_day_like(self):
        """Get a summary of today's schedule"""
        events = self.get_todays_events()
        
        return {
            'total': len(events),
            'events': events,
            'has_busy_day': len(events) >= 3
        }


# Example usage
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  GOOGLE CALENDAR API - SMART MIRROR INTEGRATION")
    print("="*60 + "\n")
    
    cal = GoogleCalendarAPI()
    
    # Authenticate (opens browser on first run)
    if not cal.authenticate():
        print("\n❌ Authentication failed. Check GOOGLE_CALENDAR_API_SETUP.txt")
        exit(1)
    
    print("\n✓ Connected to Google Calendar!\n")
    
    # Get today's summary
    print("="*60)
    print("  ☀️  WHAT'S MY DAY LIKE?")
    print("="*60 + "\n")
    
    day = cal.whats_my_day_like()
    
    print(f"📅 Today: {datetime.now().strftime('%A, %B %d, %Y')}")
    print(f"Total events: {day['total']}\n")
    
    if day['has_busy_day']:
        print("⚠️  Looks like a busy day!\n")
    
    if day['events']:
        print("TODAY'S SCHEDULE:")
        print("-" * 60)
        for event in day['events']:
            all_day_label = " (All Day)" if event['all_day'] else ""
            print(f"\n📅 {event['title']}{all_day_label}")
            print(f"   ⏰ {event['start']}")
            if event['location']:
                print(f"   📍 {event['location']}")
    else:
        print("✨ No events today! Free day!")
    
    print("\n" + "="*60)
    print("  UPCOMING EVENTS (Next 10)")
    print("="*60 + "\n")
    
    upcoming = cal.get_upcoming_events(max_results=10)
    
    if upcoming:
        for event in upcoming:
            print(f"• {event['title']}")
            print(f"  {event['start']}\n")
    else:
        print("No upcoming events found.")
    
    print("\n" + "="*60)
