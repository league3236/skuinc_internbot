# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os

from slackclient import SlackClient
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client import file
from httplib2 import Http
from oauth2client.file import Storage
from slacker import Slacker

import datetime
#library???

slack = Slacker(os.environ.get("SLACK_BOT_TOKEN"))

def post_to_channel(message):
    slack.chat.post_message('testtest',message,as_user=True)

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
        answer='Storing credentials to ' + credential_path
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
    answer='All event dateTime and eventName:'
    #nowDate = now.strftime('%Y-%m-%d')
    #print(nowDate)  # 2015-04-19

    if not events:
        answer='No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        answer='DAY:'+start.split('+')[0].split('T')[0],'Time:'+start.split('+')[0].split('T')[1].split(':')[0]+(':')+start.split(':')[1],'Summary:'+event['summary']
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
    answer='Today event dateTime and eventName:'
    post_to_channel(answer)
    if not events:
        answer ='No upcoming events found.'
        post_to_channel(answer)
    for event in events:
        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')
        today = start.split('T')[0]
        if today == nowDate:
            answer ="Time:"+start.split('+')[0].split('T')[1].split(':')[0]+(':')+start.split(':')[1]+"~"+end.split('+')[0].split('T')[1].split(':')[0]+(':')+start.split(':')[1],"summary:"+event['summary']
            post_to_channel(answer)
            #print(event['id'])
    return 0

def get_TomorrowList():
    """Shows basic usage of the Google Calendar API.

            Creates a Google Calendar API service object and outputs a list of the next
            10 events on the user's calendar.
            """
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
    tomorrowDate = str(now + datetime.timedelta(days=1)).split(' ')[0]

    answer='Tomorrow event dateTime and eventName:'
    post_to_channel(answer)
    if not events:
        answer='No upcoming events found.'
        post_to_channel(answer)
    for event in events:
        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')
        tomorrow = start.split('T')[0]

        if tomorrow == tomorrowDate:
            answer = "Time:" + start.split('+')[0].split('T')[1].split(':')[0] + (':') + start.split(':')[1] + "~"+end.split('+')[0].split('T')[1].split(':')[0] + (':') + start.split(':')[1],"summary:" + event['summary']
            post_to_channel(answer)
            # print(event['id'])
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

    e = GCAL.events().insert(calendarId=CA_NAME, sendNotifications=True, body=EVENT).execute()

    answer='''*** %r event added:
           Start: %s
           End:   %s''' % (e['summary'].encode('utf-8'),
                           e['start']['dateTime'].split('T')[0] + " " + e['start']['dateTime'].split('+')[0].split('T')[1].split(':')[0]+(':')+e['start']['dateTime'].split(':')[1],
                           e['end']['dateTime'].split('T')[0] + " " + e['end']['dateTime'].split('+')[0].split('T')[1].split(':')[0]+(':')+e['start']['dateTime'].split(':')[1])

    return 0
#print('DAY:'+start.split('+')[0].split('T')[0],'Time:'+start.split('+')[0].split('T')[1].split(':')[0]+(':')+start.split(':')[1],'Summary:'+event['summary'])

def convert(date,time):
    now = datetime.datetime.now()
    result = now.strftime('%Y-%m-') + date + 'T' + time + ':00'

    return result

def delete_Event(Event_Id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=CA_NAME, timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    answer='Events Delete:'
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
    print('실행되는중')
    #command("event all")
    get_AllList()
    #command("event today")
    get_TodayList()
    #command("Tomorrow")
    get_TomorrowList()

    #insert
    #command("insert 15 13:00-14:00 summary")
    #((^\D+)\s(\d+)\s((\d+):(\d+))(-|~)((\d+):(\d+))\s(\D+))


    #E_Day='14'
    #s_Time='13:00'
    #e_Time='14:00'
    #event_Name = 'test'
    #s_dateTime = convert(E_Day,s_Time)
    #e_dateTime = convert(E_Day,e_Time)
    #insert_Event(event_Name,s_dateTime,e_dateTime)


    #combine start delete

    #command(ex:delete 12 melong) (day"(\d[+2])")(summary"((\D)+\s*(\d+)\s+(\D+)\s*)"3GROUP USE)

    #D_Day='12'
    #E_Summary='melong'
    #Event_Id=get_EventID(D_Day,E_Summary)
    #delete_Event(Event_Id)

if __name__ == '__main__':
    main()
