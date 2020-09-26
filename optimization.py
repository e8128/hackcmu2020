from infoParse import ClassPeriod
from infoParse import parseTime
from infoParse import getCourseMeetings
from infoParse import checkConflicts
from infoParse import generatePossibleSections
from infoParse import remoteTime
from infoParse import countTime

potentialSchedules = []

# Calls Omkar's generate meeting time function
def generateMeetingTimes(course, info):
    lecture, section = info
    return getCourseMeetings(course, lecture, section)

# Generates all potential course schedules
def fullSearch(allPossibilities, current, meetingList):
    # Potentially do an early check for conflicts here to improve performance
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
            # TODO: Check the boolean flags properly
            (meetings, garbo1, garbo2, garbo3) = generateMeetingTimes(course, section)
            if (garbo3):
                sectionMeetings.append(meetings)
        allPossibilities.append(sectionMeetings)
    fullSearch(allPossibilities, 0, [])
    # Post-process to remove illegal schedules
    cleanedSchedules = []
    for schedule in potentialSchedules:
        schedule.sort(key=lambda meeting: meeting.start)
        # Must be a conflict-free schedule
        if (len(checkConflicts(schedule)) == 0):
            cleanedSchedules.append(schedule)
    return cleanedSchedules

# Following are Schedule Heuristics: smaller is better

def remoteTimeHeuristic(schedule):
    remTime, inPersonTime = remoteTime(schedule)
    return remTime

def minimumFridayHeuristic(schedule):
    cTime = countTime(schedule)
    return cTime[4] # Friday

# Takes a list of schedules and returns the best schedule based on heuristic
def optimize(potentialSchedules, heuristicFunction=remoteTimeHeuristic):
    # print("Number of Valid Schedules Generated:", len(potentialSchedules))
    currentSchedule = None
    currentVal = None
    for schedule in potentialSchedules:
        heuristic = heuristicFunction(schedule)
        if (currentSchedule is None or heuristic < currentVal):
            currentSchedule = schedule
            currentVal = heuristic
    return currentSchedule

if __name__ == '__main__':
    # optimize(["15122", "15213"])
    # optimize(["16384", "18290", "18213", "18200"])
    # optimize(["15210", "15281", "84380", "21355", "11411"])
    print(optimize(["18290", "18220", "18202", "15122", "18200"]))
