import json
import copy


def ff(s):
    if s.count("一") >= 1:
        return 0
    elif s.count("二") >= 1:
        return 1
    elif s.count("三") >= 1:
        return 2
    elif s.count("四") >= 1:
        return 3
    elif s.count("五") >= 1:
        return 4
    elif s.count("六") >= 1:
        return 5
    elif s.count("日") >= 1:
        return 6


class CLASS_ELEMENT:
    # 單一課堂
    teacher = None
    location = None
    zh_location = None
    class_time = None
    EVA_standard = None
    class_name = None
    isNowClass = False
    book = None

    def __init__(self):
        self.class_name = ""
        self.teacher = ""
        self.location = ""
        self.zh_location = ""
        self.class_time = ""
        self.EVA_standard = ""
        self.book = ""
        self.isNowClass = False

    def setClass(self, CLASSformat, class_name):
        self.class_name = class_name
        self.teacher = CLASSformat["授課教師"]
        self.location = CLASSformat["LOCATION"]
        self.zh_location = CLASSformat["上課地點"]
        self.class_time = {}
        for week in CLASSformat["上課時間"]:
            self.class_time.update({ff(week): CLASSformat["上課時間"][week]})
        self.EVA_standard = CLASSformat["評量標準"]
        self.book = CLASSformat["教科書"]

    def NAMEONLY(self, name):
        self.class_name = name

    def isnowClass(self):
        self.isNowClass = True

    def getWeeks(self):
        return self.class_time


class CLASSES:
    # 集合課堂 的 周*
    week = []

    def __init__(self):
        for i in range(7):
            self.week.append([CLASS_ELEMENT(), CLASS_ELEMENT(), CLASS_ELEMENT(), CLASS_ELEMENT(
            ), CLASS_ELEMENT(), CLASS_ELEMENT(), CLASS_ELEMENT(), CLASS_ELEMENT()])

    def addClass(self, CLSformat, CLASSname):
        ce = CLASS_ELEMENT()
        ce.setClass(CLSformat, CLASSname)
        for wek in list(ce.getWeeks().keys()):
            # wek int
            # ce.getWeeks.get(wek) list
            for class_time in ce.getWeeks().get(wek):
                self.week[wek][class_time-1] = copy.copy(ce)

    def getDay(self, day):
        d = 0
        if (type(day) == int):
            d = day-1
        else:
            if day.count("一") >= 1:
                d = 0
            elif day.count("二") >= 1:
                d = 1
            elif day.count("三") >= 1:
                d = 2
            elif day.count("四") >= 1:
                d = 3
            elif day.count("五") >= 1:
                d = 4
            elif day.count("六") >= 1:
                d = 5
            elif day.count("日") >= 1:
                d = 6
        return self.week[day]


def loadClass():
    with open("CLASS.json", "r", encoding="utf-8") as f:
        js = json.load(f)
    CLS = {}
    for CLASS in list(js.keys()):
        classes = CLASSES()
        for CLASS_ in list(js.get(CLASS).keys()):
            # CLASS_ -> class name
            classes.addClass(js.get(CLASS).get(CLASS_), CLASS_)
        CLS.update({CLASS: classes})

    return CLS


if __name__ == '__main__':
    load()
