from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar ']
TIMEZONE = "Asia/Calcutta"

def createEvent(start,end,recurenceEnd,summary,Description=None,location=None,freq="WEEKLY"):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        event = {
  'summary': summary,
  'location': location,
  'start': {
    'dateTime': start,
    'timeZone': TIMEZONE
  },
  'end': {
    'dateTime': end,
    'timeZone': TIMEZONE
  },
   'recurrence': [
    f'RRULE:FREQ={freq};UNTIL={recurenceEnd}',
   ]
  
}      
        event_result = service.events().insert(calendarId='primary',
       body={
  "summary": "Automating calendar",
  "description": "This is a tutorial example of automating google calendar with python",
  "start": {
    "dateTime": start,
    "timeZone": "Asia/Kolkata"
  },
  "end": {
    "dateTime": end,
    "timeZone": "Asia/Kolkata"
  },
}
   ).execute()
        
        """event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        calendar_list_entry = service.calendarList().get(calendarId='calendarId').execute()
        print( calendar_list_entry['summary'])"""
    except ValueError as error:
        print('An error occurred: %s' % error)
        


