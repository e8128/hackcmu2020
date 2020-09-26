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
    obj = datetime.datetime.strptime("{} {}".format(dowDict[dow], time), "%Y-%m-%d %I:%M%p")
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

def checkOverlap(course1, course2):
    return (course1.end >= course2.start)

# Returns the conflicts in a list of meetings
# Requires: courses sorted
def checkConflicts(meetings):
    conflicts = []
    for i in range(len(meetings)):
        for j in range(i + 1, len(meetings)):
            course1 = meetings[i]
            course2 = meetings[j]
            if (checkOverlap(course1, course2)):
                conflicts.append((course1, course2))

    return conflicts


def meetingMinutes(meeting):
    tdelta = meeting.end - meeting.start
    return int(tdelta.total_seconds()) // 60     

# Returns how many minutes of class on each weekday
def countTime(meetings):
    time = 0
    dowTimes = [0] * 7
    for meeting in meetings:
        minutes = meetingMinutes(meeting)
        dowTimes[meeting.start.weekday()] += minutes
        time += minutes
    return dowTimes[:5]

def remoteTime(meetings):
    remote = 0
    inPerson = 0
    for meeting in meetings:
        minutes = meetingMinutes(meeting)
        if (meeting.room == 'CMU REMOTE'):
            remote += minutes
        else:
            inPerson += minutes
    return (remote, inPerson)
    
course1 = Course("15122", "Principles of Imperative Computing", "TR", "08:00AM", "09:20AM", "BH 5001", "Cervesato")
course2 = Course("15150", "Principles of Functional Programming", "TR", "11:40AM", "01:00PM", "CMU REMOTE", "Brookes")
course3 = Course("48100", "Archi Studio", "MWF", "01:30PM", "4:20PM", "CFA 200", "TBA")

courses = [course1, course2, course3]
meetings = allMeetings(courses)
print("MEETINGS")
for meeting in meetings:
    print(meeting)
print("Meetings: ", meetings)

print("Conflicts: ", checkConflicts(meetings))

print("Minutes per day: ", countTime(meetings))

print("Remote Time: ", remoteTime(meetings))