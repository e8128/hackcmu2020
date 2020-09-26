from infoParse import ClassPeriod
from infoParse import parseTime
from infoParse import getCourseMeetings
from infoParse import checkConflicts
from infoParse import generatePossibleSections

potentialSchedules = []

# calls Omkar's generate meeting time function
def generateMeetingTimes(course, info):
    lecture, section = info
    return getCourseMeetings(course, lecture, section)

# tries all potential sections
# def generatePossibleSections(course):
#     return [('1', 'A'), ('1', 'B')]

# Generates all potential course schedules
def fullSearch(allPossibilities, current, meetingList):
    # potentially do an early check for conflicts here to improve performance
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

# Takes a list of courses
# Generate all possible course schedules
def generateAll(courses):
    allPossibilities = []
    for course in courses:
        possibleSections = generatePossibleSections(course)
        sectionMeetings = []
        for section in possibleSections:
            (meetings, garbo1, garbo2, garbo3) = generateMeetingTimes(course, section)
            sectionMeetings.append(meetings)
        allPossibilities.append(sectionMeetings)
    fullSearch(allPossibilities, 0, [])

# Note: generateAll must be called first
def postProcess():
    # print(potentialSchedules)
    cleanedSchedules = []
    for schedule in potentialSchedules:
        schedule.sort(key=lambda meeting: meeting.start)
        # Must be a conflict-free schedule
        if (len(checkConflicts(schedule)) == 0):
            cleanedSchedules.append(schedule)
    return cleanedSchedules

# Can really only be called once
def optimize(courses):
    generateAll(courses)
    potentialSchedules = postProcess()
    print("Number of Valid Schedules Generated:", len(potentialSchedules))
    # print(potentialSchedules)
    for potentialSchedule in potentialSchedules:
        print(potentialSchedule)
    

if __name__ == '__main__':
    # optimize(["15122", "15213"])
    # optimize(["16384", "18290", "18213", "18200"])
    # optimize(["15210", "15281", "84380", "21355", "11411"])
    optimize(["73401"])
    # 18202
    potentialSchedules = postProcess()

    # print(getCourseMeetings("15122", "1", "C"))
    # print(getCourseMeetings("15455", "1", "A"))
    # print(getCourseMeetings("15445", "1", "H"))
    # print(getCourseMeetings("15424", "1", "A"))
    # print(getCourseMeetings("15424", "1", "B"))
    # print(getCourseMeetings("15440", "1", "C"))
    # print(getCourseMeetings("15122", "2", "K"))

