from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gemini import get_schedule
import os.path
import pickle
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    #access google calendar api
    service = access_api()

    #Create calendar if it doesn't exist
    calendar_id = create_calendar(service)

    message = "one hour work from home, one hour apply to internship, one hour study for java, tutoring 5-6:30"

    # clear the calendar in case the program is being run twice for the same day
    if "tomorrow" in message:
        clear_schedule(service, (datetime.today() + timedelta(1)).strftime('%Y-%m-%d'), calendar_id)
    else:
        clear_schedule(service, datetime.today().strftime('%Y-%m-%d'), calendar_id)

    # get schedule from gemini
    schedule = get_schedule(message)

    # add events to calendar
    for event in schedule:
        add_event(service, calendar_id, event)

def access_api():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service
    
def create_calendar(service):
    #List all calendars
    calendar_list = service.calendarList().list().execute().get('items', [])
    
    #Check for the calendar
    for calendar in calendar_list:
        if calendar['summary'] =="Automated Schedule":
            return calendar['id']
    
    #Create a new calendar if not found
    new_calendar = {
        'summary': 'Automated Schedule',
        'timeZone': 'Australia/Perth'
    }
    created_calendar = service.calendars().insert(body=new_calendar).execute()
    print(f"Created calendar: {created_calendar['id']}")
    
    return created_calendar['id']

def clear_schedule(service, date, calendar_id):
    # get list of events
    events = service.events().list(calendarId=calendar_id,timeMin=date+"T00:00:00Z",timeMax=date+"T23:59:59Z").execute()
    
    # delete each event
    for event in events['items']:
        service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
        print(f"Deleted event: {event['id']}")

def add_event(service, calendar_id, event):
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"Created event: {created_event['id']}")

if __name__ == '__main__':
    main()
