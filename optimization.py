from infoParse import ClassPeriod
from infoParse import parseTime
from infoParse import getCourseMeetings

potentialSchedules = []

# Omkar's generate meeting time function
def generateMeetingTimes(course, info):
    lecture, section = info
    return getCourseMeetings(course, lecture, section)
    # if (section == ('1', 'A')):
    #     start = parseTime("M", "5:30PM")
    # else:
    #     start = parseTime("T", "5:30PM")
    # return [ClassPeriod("15122", start, start, "CMU REMOTE")]

def generatePossibleSections(course):
    return [('1', 'A'), ('1', 'B')]

# Generates all potential course schedules
def fullSearch(allPossibilities, current, meetingList):
    if (current >= len(allPossibilities)):
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
        allPossibilities.append([generateMeetingTimes(course, section) for section in possibleSections])
    print("allPossibilities: ", allPossibilities)
    fullSearch(allPossibilities, 0, [])

if __name__ == '__main__':
    optimize(["15122", "15213"])

    print(len(potentialSchedules))
    for potentialSchedule in potentialSchedules:
        print(potentialSchedule)

    print(getCourseMeetings("15122", "1", "C"))
    print(getCourseMeetings("15455", "1", "A"))