# -*- coding: utf-8 -*-

from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES1 = 'https://www.googleapis.com/auth/calendar'
EMAIL = 'league3236@skuniv.ac.kr','subeen2150@skuniv.ac.kr','shs4161@skuniv.ac.kr','jebigbang18@skuniv.ac.kr','mynadahun@skuniv.ac.kr','sports1014@skuniv.ac.kr','twinpapa2003@skuniv.ac.kr'
store = file.Storage('storage.json')####
creds = store.get()


if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES1)
    creds = tools.run_flow(flow, store)
GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

GMT_OFF = '+09:00'      # PDT/MST/GMT-7
EVENT = {
    'summary': 'testtest',
    'start':  {'dateTime': '2017-07-15T14:00:00%s' % GMT_OFF},
    'end':    {'dateTime': '2017-07-15T14:30:00%s' % GMT_OFF},
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

#print('''*** %r event added:
#    Start: %s
#    End:   %s''' % (e['summary'].encode('utf-8'),
#        e['start']['dateTime'], e['end']['dateTime']))
print('''*** %r event added:
    Start: %s
    End:   %s''' % (e['summary'].encode('utf-8'),
        e['start']['dateTime'].split('T')[0]+" "+e['start']['dateTime'].split('T')[1].split('+')[0],
                    e['end']['dateTime'].split('T')[0]+" "+e['end']['dateTime'].split('T')[1].split('+')[0]))
