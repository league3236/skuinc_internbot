# -*- coding: utf-8 -*-

import calendarunion
import os
import time
import datetime
import json
import urllib2
from slackclient import SlackClient
from slacker import Slacker
import re


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = u"일정-도와줘"
EXAMPLE_COMMAND1 = u"안녕"
LIST_ALL = u"일정-모두"
LIST_TOMORROW = u"일정-내일"
LIST_TODAY = u"일정-오늘"
INSERT_EVENT = u"일정-추가"
DELETE_EVENT = u"일정-삭제"
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
        answer = "안녕? 나는 일정봇이야. 명령어를 입력해줘! 명령어를 모른다면 '일정-도와줘'를 검색해봐:)"
    elif txt == EXAMPLE_COMMAND:
        answer = "자 한번 사용해보자"
        calendarunion.help_command(channel)
    elif txt.find(LIST_ALL) != -1:
        answer = "검색이 모두 완료되었어:smile:"
        calendarunion.get_AllList(channel)
    elif txt.find(LIST_TOMORROW) != -1:
        answer = "미리 준비하자>__<"
        calendarunion.get_TomorrowList(channel)
    elif txt.find(LIST_TODAY) != -1:
        answer = "오늘 하루도 힘내^__^"
        calendarunion.get_TodayList(channel)
    elif txt.find(INSERT_EVENT) != -1:
        cmd = re.compile(r"((^\S+)+\s*(-D|-d)+\s*(\d{2})+\s*(-T|-t)+\s*((\d+):(\d+))(-|~)((\d+):(\d+))+\s*(-S|-s)+\s*(\D+))")
        if re.match(cmd,txt) is not None:
            answer = "*★*일정 추가 완료*★*:smile:"
            matchobj = cmd.search(txt)
            E_Day=matchobj.group(4)
            s_Time=matchobj.group(6)
            e_Time=matchobj.group(10)
            event_Name = matchobj.group(14)
            s_dateTime = calendarunion.convert(E_Day, s_Time)
            e_dateTime = calendarunion.convert(E_Day, e_Time)
            calendarunion.insert_Event(event_Name, s_dateTime, e_dateTime, channel)
        else:
            answer = "정확하게 입력바랍니다.ex)일정추가 날짜 00:00~00:00 일정제목"
            return None
    elif txt.find(DELETE_EVENT) != -1:
        cmd = re.compile(r"((^\S+)+\s*(-D|-d)+\s*(\d{2})+\s*(-S|-s)+\s*(\D+))")
        if re.match(cmd, txt) is not None:
            answer = "*☆*일정 제거 완료*☆*:smile:"
            matchobj = cmd.search(txt)
            D_Day=matchobj.group(4)
            E_Summary=matchobj.group(6)
            Event_Id=calendarunion.get_EventID(D_Day,E_Summary,channel)
            if Event_Id=='error':
                return None
            calendarunion.delete_Event(Event_Id,channel)
        else:
            answer = "정확하게 입력바랍니다.ex)일정제거 날짜 일정제목"
            return None
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