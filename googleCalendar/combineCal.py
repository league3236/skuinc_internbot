
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client import file
from httplib2 import Http
from oauth2client.file import Storage


import datetime
#library???


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'#, 'https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/plus.login'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
CA_NAME='skuniv.ac.kr_86in1lo83oq31vht666aotr7kk@group.calendar.google.com'#our calendar
EMAIL = 'league3236@skuniv.ac.kr','subeen2150@skuniv.ac.kr','shs4161@skuniv.ac.kr','jebigbang18@skuniv.ac.kr','mynadahun@skuniv.ac.kr','sports1014@skuniv.ac.kr','twinpapa2003@skuniv.ac.kr'



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_AllList():
    """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now1 = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=CA_NAME, timeMin=now1, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    #now1 = datetime.datetime.now()
    print('All event dateTime and eventName:')
    #nowDate = now.strftime('%Y-%m-%d')
    #print(nowDate)  # 2015-04-19

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start.split('+')[0], event['summary'])
    return 0

def get_TodayList():
    """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now1 = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=CA_NAME, timeMin=now1, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    now=datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    print('Today event dateTime and eventName:')

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime')
        today = start.split('T')[0]
        if today == nowDate:
           print(start.split('+')[0], event['summary'])
           print(event['id'])
    return 0

def insert_Event(EventName,StartTime,EndTime):
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

    GMT_OFF = '+09:00'  # PDT/MST/GMT-7
    EVENT = {
        'summary': EventName,
        'start': {'dateTime': StartTime+'%s' % GMT_OFF},#2017-07-12T14:00:00
        'end': {'dateTime': EndTime+'%s' % GMT_OFF},#2017-07-12T14:30:00
        'attendees': [
            {'email': EMAIL[0]},
            {'email': EMAIL[1]},
            {'email': EMAIL[2]},
            {'email': EMAIL[3]},
            {'email': EMAIL[4]},
            {'email': EMAIL[5]},
            {'email': EMAIL[6]},
        ],
    }

    e = GCAL.events().insert(calendarId='skuniv.ac.kr_86in1lo83oq31vht666aotr7kk@group.calendar.google.com',
                             sendNotifications=True, body=EVENT).execute()

    print('''*** %r event added:
        Start: %s
        End:   %s''' % (e['summary'].encode('utf-8'),
                        e['start']['dateTime'].split('T')[0] + " " + e['start']['dateTime'].split('T')[1].split('+')[0],
                        e['end']['dateTime'].split('T')[0] + " " + e['end']['dateTime'].split('T')[1].split('+')[0]))

    return 0

def delete_Event(Event_Id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    print('Events Delete:')
    service.events().delete(calendarId=CA_NAME, eventId=Event_Id).execute()

    return 0

def get_EventID(D_Day,E_Summary):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now1 = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=CA_NAME, timeMin=now1, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    now = datetime.datetime.now()
    WhatDate = now.strftime('%Y-%m-'+D_Day)

    for event in events:
        start = event['start'].get('dateTime')
        today = start.split('T')[0]
        if ((today == WhatDate) and (event['summary']==E_Summary)):
            event_id = event['id']
    return event_id

def main():
    get_AllList()
    get_TodayList()
    #insert_Event('melong','2017-07-12T14:30:00','2017-07-12T15:30:00')

    #combine start
    #D_Day='12'
    #E_Summary='melong'
    #Event_Id=get_EventID(D_Day,E_Summary)
    #delete_Event(Event_Id)

if __name__ == '__main__':
    main()
