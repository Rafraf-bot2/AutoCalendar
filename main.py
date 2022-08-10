from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

# If modifying scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def createEvent(period):
    Infos = (
            ['Session Etudes', 'Faut etudier mon gars'] 
            if period[2] == '11' 
            else ['Session Travail', 'Faut bosser mon gars']
        )
    
    event = {
            'summary': Infos[0],
            'description': Infos[1],
            'start': {
                'dateTime': period[0]+'T00:00:00',
                'timeZone' : 'Europe/Paris'
            },
            'end': {
                'dateTime': period[1]+'T23:59:00',
                'timeZone' : 'Europe/Paris'
            },
            'reminders' : {
                'useDefault': False
            },
            'colorId' : period[2]
        }
    return event

def main():
    apiKey = os.environ.get("API_KEY")
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
            creds = flow.run_local_server(port=8000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds, developerKey=apiKey)
        
        calendarFile = open('calendar.txt', 'r')
        lines = calendarFile.readlines()
        
        for line in lines:
            period = line.split()
            event = createEvent(period)
            print(event)
            event = service.events().insert(calendarId='primary', body=event).execute()

        
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()