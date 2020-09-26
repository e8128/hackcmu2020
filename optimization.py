from infoParse import ClassPeriod
from infoParse import parseTime

potentialSchedules = []

# Omkar's generate meeting time function
def generateMeetingTimes(section):
    if (section == ('1', 'A')):
        start = parseTime("M", "5:30PM")
    else:
        start = parseTime("T", "5:30PM")
    return [ClassPeriod("15122", start, start, "CMU REMOTE")]

def generatePossibleSections(course):
    return [('1', 'A'), ('1', 'B')]

# Generates all potential course schedules
def fullSearch(allPossibilities, current, meetingList):
    if (current >= len(allPossibilities)):
        print(meetingList)
        potentialSchedules.append(meetingList)
        return
    potentialSections = allPossibilities[current]
    if (len(potentialSections) == 0):
        raise Exception("No sections available")
    for sectionTimes in potentialSections:
        newMeetingList = meetingList.copy()
        for meeting in sectionTimes:
            newMeetingList.append(meeting)
            fullSearch(allPossibilities, current + 1, newMeetingList)
    return True

# Takes a list of courses to optimize
# Returns the optimal one
def optimize(courses):
    allPossibilities = []
    for course in courses:
        possibleSections = generatePossibleSections(course)
        print(possibleSections)
        allPossibilities.append([generateMeetingTimes(section) for section in possibleSections])
    print(allPossibilities)
    fullSearch(allPossibilities, 0, [])

optimize(["15122", "15150", "15213"])

print(len(potentialSchedules))
print(potentialSchedules)
