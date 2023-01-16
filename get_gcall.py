from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """
    Shows basic usage of the Google Calendar API.
    Retrieves the start and name of the next 15 events on the user's primary calendar that is happening today.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 15 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=15, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    events_for_notes = []

    for event in events:
        # print(event)
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start)
        try:
            formated_date_time = datetime.datetime.strptime(
                start, '%Y-%m-%dT%H:%M:%S-05:00')
        except:
            try:
                formated_date_time = datetime.datetime.strptime(
                     start, '%Y-%m-%dT%H:%M:%S-04:00')
            except:
                    formated_date_time = datetime.datetime.today()

        if (formated_date_time.day == datetime.datetime.today().day) and (formated_date_time.month == datetime.datetime.today().month):
            # print(event)
            # print('this event happens today')
            print(start, event['summary'])
            event_name = event['summary']
            try:
                event_description = ''
            except:
                event_description = ""
            try:
                attendees = event['attendees']
            except:
                attendees = ""

            # print(event_name, event_description, attendees)
            google_cal_event_obj = {"event_name": event_name,
                                    "event_description": event_description,
                                    "attendees": attendees
                                    }
            events_for_notes.append(google_cal_event_obj)
    print(events_for_notes)
    return(events_for_notes)


if __name__ == '__main__':
    main()
