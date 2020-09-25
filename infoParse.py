# Source: https://www.cmu.edu/hub/legend.html

import datetime

abbreviations = {}

file = open("abbreviations.txt", "r").read()
lines = str.splitlines(file)
for i in range(0, len(lines), 2):
    abbreviations[lines[i]] = lines[i + 1]

# Takes a location string and returns its longform
def longForm(location):
    tokens = location.split()
    if tokens[0] in abbreviations:
        tokens[0] = abbreviations[tokens[0]]
    print(tokens)
    return " ".join(tokens)

# Placeholders for days of the week
dowDict = {'M': '1900-01-01',
           'T': '1900-01-02',
           'W': '1900-01-03',
           'R': '1900-01-04',
           'F': '1900-01-05'}

# Returns datetime object
def parseTime(dow, time):
    obj = datetime.datetime.strptime("{} {}".format(dowDict[dow], time), "%Y-%m-%d %H:%M%p")
    return obj

# Represents a course
class Course:
    def __init__(self, courseId, title, days, start, end):
        self.courseId = courseId
        self.title = title
        self.meetingTimes = []
        for day in days:
            meeting = ClassPeriod(courseId, parseTime(day, start), parseTime(day, end))
            self.meetingTimes.append(meeting)
    
    def displayInfo(self):
        print("{} {}".format(self.courseId, self.title))
        print(self.meetingTimes)
        
# Represents a Class Period
class ClassPeriod:
    def __init__(self, classId, start, end):
        self.classId = classId
        self.start = start
        self.end = end

    def __repr__(self):
        return "[{}: {} to {}]".format(self.classId, self.start, self.end)

parseTime("F", "12:50PM")

print(longForm("PH 101"))

course1 = Course("15122", "Principles of Imperative Computing", "TR", "08:00AM", "09:20AM")
course1.displayInfo()