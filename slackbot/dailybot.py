# -*- coding: utf-8 -*-

import calendarunion
import os
import time
import datetime
import json
import urllib2
from slackclient import SlackClient
from slacker import Slacker


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
EXAMPLE_COMMAND1 = "hi"
EXAMPLE_COMMAND2 = "tomorrow"
BL = True;

# instantiate Slack & Twilio clients

slack = Slacker(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def post_to_channel(message):
    slack.chat.post_message('testtest', message, as_user=True)

def parse_slack(msg):
    output_list = msg
    # print(output_list)
    # print(len(output_list))

    if output_list and len(output_list) > 0:
        for output in output_list:
            #print(output)

            if output and 'text' in output and 'BOT_ID' not in output:
                command = output['text']
                answer = slack_answer(command)

             	if answer :
			slack_client.api_call(
                     		"chat.postMessage",
                     		channel=output['channel'],
                      		text=answer,
				username='일정봇',
				as_user=True
                	)

    return None

def calendar_report():
	now = datetime.datetime.now()
	hour = now.hour
	min = now.minute
	sec = now.second;
	global BL
	if hour == 17 and min == 55 and BL:
		payload = {"text": "내일 일정확인해볼래?"}
		url = "https://hooks.slack.com/services/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"
		req = urllib2.Request(url)
		req.add_header('Content-Type', 'application/json')
		urllib2.urlopen(req, json.dumps(payload))
		BL = False
	if hour == 18 and min == 01:
		BL = True
	return None


def slack_answer(txt):
    if txt == EXAMPLE_COMMAND1:
        answer = "안녕하세요! 일정봇입니다."
    elif txt == EXAMPLE_COMMAND2:
        calendarunion.get_TomorrowList() 
	#payload = {"text": "내일일정 알림!!!"}
	#url = "https://hooks.slack.com/services/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"
	#req = urllib2.Request(url)
	#req.add_header('Content-Type', 'application/json')
	#urllib2.urlopen(req, json.dumps(payload))
	#return None
    else:
        return None

    return answer

if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("Connected!")
        while True:
	    calendar_report()
            parse_slack(slack_client.rtm_read())
            time.sleep(1)
    else:
        print("Connection failed.")
