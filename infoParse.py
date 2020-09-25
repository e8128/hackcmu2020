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
    def __init__(self, courseId, title, days, start, end, room, instructor):
        self.courseId = courseId
        self.title = title
        self.meetingTimes = []
        for day in days:
            meeting = ClassPeriod(courseId, parseTime(day, start), parseTime(day, end), room)
            self.meetingTimes.append(meeting)
        self.room = room
        self.instructor = instructor
    
    def displayInfo(self):
        ret = "{} {}\n".format(self.courseId, self.title)
        ret += "Meetings: {}".format(self.meetingTimes)
        return ret
        
def extractDOW(dateObj):
    return dateObj.strftime("%A")

def goodDateFormat(dateObj):
    return dateObj.strftime("%H:%M")

# Represents a Class Period
class ClassPeriod:
    def __init__(self, classId, start, end, room):
        self.classId = classId
        self.start = start
        self.end = end
        self.room = room

    def __repr__(self):
        return "{} {} to {} @ {}".format(extractDOW(self.start), goodDateFormat(self.start), goodDateFormat(self.end),
            longForm(self.room))

# Takes a list of classes and returns all meetings
# Also sorts by time
def allMeetings(courses):
    meetings = []
    for course in courses:
        for meeting in course.meetingTimes:
            meetings.append(meeting)
    meetings.sort(key=lambda meeting: meeting.start)
    return meetings

parseTime("F", "12:50PM")

print(longForm("PH 101"))

course1 = Course("15122", "Principles of Imperative Computing", "TR", "08:00AM", "09:20AM", "BH 5001", "Cervesato")
course2 = Course("15150", "Principles of Functional Programming", "TR", "11:40AM", "01:00PM", "CMU REMOTE", "Brookes")
print(course1.displayInfo())
print(allMeetings([course1, course2]))
