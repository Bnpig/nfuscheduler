#!/usr/bin/python3


import time
import threading
import os
import sys
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import webbrowser




def gtime(event):
    if list(event["start"].keys()).count("date") >= 1:
        return time.mktime(datetime.datetime.strptime(event["start"]["date"], "%Y-%m-%d").timetuple())
    return time.mktime(datetime.datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S+08:00").timetuple())


def contains(dicts, obj):
    return list(dicts.keys()).count(obj) >= 1


def gtype(obj):
    c = "date"
    if list(obj["start"].keys()).count(c) == 0:
        c = "dateTime"
    return obj


def put(dicts, obj):
    st = gtime(obj)
    if contains(dicts, st):
        dicts.get(st).append(obj)
    else:
        dicts.update({st: [obj]})
    return dicts


os.environ['TZ'] = 'Asia/Taipei'
time.tzset()

DAYSTART_UNIX = time.mktime(datetime.datetime.strptime(datetime.datetime.fromtimestamp(
    time.time()).strftime("%Y-%m-%d"), "%Y-%m-%d").timetuple())
DAYEND_UNIX = DAYSTART_UNIX + 86400.0 - 1
WEEKEND_UNIX = DAYSTART_UNIX + (86500.0)*14-1
TODAY = datetime.datetime.fromtimestamp(DAYSTART_UNIX).strftime("%Y-%m-%d")
print(TODAY)
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    service = build('calendar', 'v3', credentials=creds)

    page_token = None
    week = {}
    daily = {}
    while True:
        events = service.events().list(calendarId='nfu.edu.tw_v8hham7ijjiqrm9slb67u8refg@group.calendar.google.com',
                                       pageToken=page_token).execute()
        for event in events['items']:
            stunix = 0
            edunix = 0
            if list(event["start"].keys()).count("date") >= 1:
                stunix = time.mktime(datetime.datetime.strptime(
                    event["start"]["date"], "%Y-%m-%d").timetuple())

            elif list(event["start"].keys()).count("dateTime") >= 1:
                stunix = time.mktime(datetime.datetime.strptime(
                    event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S+08:00").timetuple())

            if list(event["end"].keys()).count("date") >= 1:
                edunix = time.mktime(datetime.datetime.strptime(
                    event["end"]["date"], "%Y-%m-%d").timetuple())-1

            elif list(event["end"].keys()).count("dateTime") >= 1:
                edunix = time.mktime(datetime.datetime.strptime(
                    event["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S+08:00").timetuple())

            if (edunix < DAYSTART_UNIX and stunix < DAYSTART_UNIX) or (stunix > DAYEND_UNIX and edunix > DAYSTART_UNIX):

                if (edunix < DAYSTART_UNIX and stunix < DAYSTART_UNIX) or (stunix > WEEKEND_UNIX and edunix > DAYSTART_UNIX):
                    continue
                else:
                    # print(stunix,edunix,DAYSTART_UNIX,DAYEND_UNIX,WEEKEND_UNIX)
                    # print(event)
                    week = put(week, event)
            else:
                daily = put(daily, event)

        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return daily, week
    k = list(daily.keys())
    k.sort()
    for key in k:
        for event in daily.get(key):
            print(datetime.datetime.fromtimestamp(
                key).strftime("%Y-%m-%d"), event["summary"])

    k = list(week.keys())
    k.sort()
    for key in k:
        for event in week.get(key):
            print(datetime.datetime.fromtimestamp(
                key).strftime("%Y-%m-%d"), event["summary"])


if __name__ == '__main__':
    main()
