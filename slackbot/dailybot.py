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
EXAMPLE_COMMAND3 = "today"
BL = True;

# instantiate Slack & Twilio clients

slack = Slacker(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def post_to_channel(message, channel):
    slack.chat.post_message(channel, message, as_user=True)

def parse_slack(msg):
    output_list = msg
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and BOT_ID not in output:
                channel = output['channel']
                command = output['text']    # Get text in JSON
                answer = slack_answer(command, channel)    # Go to desk
                if answer :
                    post_to_channel(answer, channel)
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


def slack_answer(txt, channel):
    if txt == EXAMPLE_COMMAND1:
        answer = "안녕하세요! 일정봇입니다."
    elif txt.find(EXAMPLE_COMMAND2) != -1:
        answer = "내일을 위해 빠샤빠샤!!"
        calendarunion.get_TomorrowList(channel)
    elif txt.find(EXAMPLE_COMMAND3) != -1:
        answer = "오늘 하루도 화잇팅!!"
        calendarunion.get_TodayList(channel)
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