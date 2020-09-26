# Source: https://www.cmu.edu/hub/legend.html

import datetime
import parse

global parsedClassInfo
parsedClassInfo = parse.parseWebsite()

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
           'F': '1900-01-05',
           'S': '1900-01-06',
           'U': '1900-01-07'}

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
    return dowTimes

# Returns how much minutes per week are remote
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

# Takes registration info, returns array of ClassPeriod instances
def getCourseMeetings(courseNumber, lectureNumber, recitationSection):
    if (courseNumber not in parsedClassInfo):
        print("Class information not found")
        return []
    classInfo = parsedClassInfo[courseNumber]
    res = []
    lectureFound = False
    recitationFound = False
    pitts = True
    if (classInfo['Lec/Sec'] == '\xa0' or ("Lec" == classInfo['Lec/Sec'] and lectureNumber == "1") or "Lec " + lectureNumber in classInfo['Lec/Sec'] or recitationSection == classInfo['Lec/Sec']):
        lectureFound = True
        if (recitationSection == classInfo['Lec/Sec']):
            recitationFound = True
        if (classInfo['Location'] != "Pittsburgh, Pennsylvania"):
            pitts = False
        for day in classInfo['Days']:
            res.append(ClassPeriod(courseNumber, parseTime(day, classInfo['Begin']), parseTime(day, classInfo['End']), classInfo['Bldg/Room']))
    others = classInfo['sections']
    for i in range(len(others)):
        o = others[i]
        if (("Lec" == o['Lec/Sec'] and lectureNumber == "1") or "Lec " + lectureNumber in o['Lec/Sec'] or recitationSection == o['Lec/Sec'] or (i == 0 and o['Lec/Sec'] == '\xa0')):
            if (recitationSection == o['Lec/Sec']):
                recitationFound = True
            if (("Lec" == o['Lec/Sec'] and lectureNumber == "1") or "Lec " + lectureNumber in o['Lec/Sec']):
                lectureFound = True
            if (o['Location'] != "Pittsburgh, Pennsylvania"):
                pitts = False
            for day in o['Days']:
                res.append(ClassPeriod(courseNumber, parseTime(day, o['Begin']), parseTime(day, o['End']), o['Bldg/Room']))
            if (i+1 < len(others) and others[i+1]['Lec/Sec'] == '\xa0'):
                for day in others[i+1]['Days']:
                    res.append(ClassPeriod(courseNumber, parseTime(day, others[i+1]['Begin']), parseTime(day, others[i+1]['End']), others[i+1]['Bldg/Room']))
    return (res, lectureFound, recitationFound, pitts)

# Takes course number and returns array of tuples possible (lecture, recitation)
def generatePossibleSections(courseNumber):
    if (courseNumber not in parsedClassInfo):
        print("Class information not found")
        return []
    classInfo = parsedClassInfo[courseNumber]
    profs = dict()
    profs[classInfo['Instructor(s)']] = {"Lec": classInfo['Lec/Sec'], "Sec": []}
    others = classInfo['sections']
    for o in others:
        if ("Lec" in o['Lec/Sec']):
            profs[o['Instructor(s)']] = {"Lec": o['Lec/Sec'], "Sec": []}
        elif (o['Lec/Sec'] != '\xa0'):
            if (o['Instructor(s)'] not in profs):
                profs[o['Instructor(s)']] = {'Lec': o['Lec/Sec'], 'Sec': [o['Lec/Sec']]}
            else:
                profs[o['Instructor(s)']]['Sec'].append(o['Lec/Sec'])
    res = []
    for prof in profs:
        # Remove the Lec from lecture number
        lec = "1" if profs[prof]['Lec'] == "Lec" else (profs[prof]['Lec'] if "Lec" not in profs[prof]['Lec'] else profs[prof]['Lec'][4:])
        if (len(profs[prof]['Sec']) == 0):
            if not lec.isdigit():
                res.append(("1", lec))
            else:
                res.append((lec, 'A'))
        else:
            options = [(lec, sec) for sec in profs[prof]['Sec']]
            i = 0
            while i < len(options):
                (lec, sec) = options[i]
                if not lec.isdigit():
                    options.pop(i)
                    options.append(("1", lec))
                    if (lec != sec):
                        options.append(("1", sec))
                else:
                    i += 1
            res.extend(options)
    return res

# def generatePossibleSectionsDumb(courseNumber):
#     lecture = "123"
#     alpha = "ABCDEFG"
#     ret = []
#     for lectureNumber in lecture:
#         for letter in alpha:
#             if (getCourseMeetings("15112", lectureNumber, letter) is not None):
#                 ret.append((lectureNumber, letter))
#     return ret

# Checks if a course section is located in Pittsburgh
def checkLocation(course, sectionLetter):
    infoDict = parsedClassInfo[course]
    print(infoDict)
    for section in infoDict['sections']:
        if (section['Lec/Sec'] != sectionLetter):
            continue
        if (section['Location'] != 'Pittsburgh, Pennsylvania'):
            return False
    return True

if __name__ == '__main__':
    print(generatePossibleSections("15112"))
    print(generatePossibleSections("15122"))
    print(generatePossibleSections("15424"))
    print(generatePossibleSections("15455"))
    print(getCourseMeetings("18213", "1", "F"))
    print(getCourseMeetings("18213", "2", "Z"))
    print(getCourseMeetings("18740", "1", "SV"))
    print(getCourseMeetings("18100", "2", "F"))
    course1 = Course("15122", "Principles of Imperative Computing", "TR", "08:00AM", "09:20AM", "BH 5001", "Cervesato")
    course2 = Course("15150", "Principles of Functional Programming", "TR", "11:40AM", "01:00PM", "CMU REMOTE", "Brookes")
    print(course1.displayInfo())
    print(allMeetings([course1, course2]))
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

    # print(checkLocation("15295", "A"))
    # print(checkLocation("15295", "W"))
    while True:
        course = input()
        print(generatePossibleSections(course))
        # print(generatePossibleSectionsDumb(course))
        # print(getCourseMeetings(co
    # print(generatePossibleSections("15122"))
    # print(generatePossibleSections("15424"))