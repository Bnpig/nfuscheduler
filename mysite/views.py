from django.http import HttpResponse
from django import template
from django.shortcuts import render
from mysite.NFUcalendar import main
from mysite.NFUclass import loadClass, CLASS_ELEMENT
import datetime
import time
import copy
d, w = main()
CLS = loadClass()
week_daily = []
classtime = ["08:10~09:00", "09:10~10:00", "10:10~11:00", "11:10~12:00",
             "13:20~14:10", "14:20~15:10", "15:20~16:10", "16:20~17:10"]
for class_time in range(8):
    z = []
    ce = CLASS_ELEMENT()
    ce.NAMEONLY(classtime[class_time])
    z.append(ce)
    for week in range(5):
        z.append(CLS["CSIE B"].week[week][class_time])
    week_daily.append(z)


def index(request):
    global d, w, CLS, week_daily
    daily = []
    k = list(d.keys())
    k.sort()
    for key in k:
        for event in d.get(key):
            daily.append(event)

    weekly = []
    k = list(w.keys())
    k.sort()
    for key in k:
        for event in w.get(key):
            weekly.append(event)
    classes = CLS['CSIE B']

    today = datetime.datetime.fromtimestamp(time.time()).today().weekday()
    daily_classes = classes.week[today]
    todayis = ""
    if today == 0:
        todayis = "星期一"
    elif today == 1:
        todayis = "星期二"
    elif today == 2:
        todayis = "星期三"
    elif today == 3:
        todayis = "星期四"
    elif today == 4:
        todayis = "星期五"
    elif today == 5:
        todayis = "星期六"
    elif today == 6:
        todayis = "星期日"
    TODAY_date = datetime.datetime.fromtimestamp(
        time.time()).strftime("%Y-%m-%d")
    wd = copy.copy(week_daily)
    NOWDATE = datetime.datetime.fromtimestamp(
        time.time())
    LASTUPDATE = NOWDATE.strftime("%Y-%m-%d %H:%M:%S")
    seconds = (datetime.datetime.strptime(NOWDATE.strftime("%H:%M:%S"), "%H:%M:%S") -
               datetime.datetime(1970, 1, 1, 0, 0, 0)).seconds

    if seconds > 61800:
        pass
    else:
        CLST = 0
        if seconds > 58200:
            CLST = 7
        if seconds > 54600:
            CLST = 6
        if seconds > 51000:
            CLST = 5
        if seconds > 43200:
            CLST = 4
        if seconds > 39600:
            CLST = 3
        if seconds > 36000:
            CLST = 2
        if seconds > 32400:
            CLST = 1
        else:
            CLST = 0
        daily_classes[CLST].isnowClass()
        for r in range(6):
            wd[CLST][r].isnowClass()
    print(seconds)
    return render(request, 'index.html', locals())
