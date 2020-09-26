from infoParse import ClassPeriod
from infoParse import parseTime
from infoParse import getCourseMeetings
from infoParse import checkConflicts
from infoParse import generatePossibleSections
from infoParse import remoteTime
from infoParse import countTime
from infoParse import parsedClassInfo

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
            if len(sectionMeetings) == 0:
                raise Exception("Invalid class {} in schedule".format(course))
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


def getUnits(courses): #takes list of classes and returns total units taken
    unitCount = 0 
    for c in courses:
        c=str(c)
        c=c.strip()
        if c in parsedClassInfo:
            unitCount += float(parsedClassInfo[c]['Units']) #parsedClassInfo is global 
                                                    #dictionary containing a 
                                                    #two layer dictionary 
        else:
            unitCount+=10 #if not in parsed class info it will default to 10 added 
    return unitCount


def remoteTimeHeuristic(schedule):
    remTime, inPersonTime = remoteTime(schedule)
    return remTime

def minimumFridayHeuristic(schedule):
    cTime = countTime(schedule)
    return cTime[4] # Friday

def earliestTimeHeuristic(schedule):
    earliestTime = 2400
    for meeting in schedule:
        startTime = meeting.start.hour * 60 + meeting.start.minute
        earliestTime = min(startTime, earliestTime)
    return -earliestTime

def latestTimeHeuristic(schedule):
    latestTime = 0
    for meeting in schedule:
        endTime = meeting.end.hour * 60 + meeting.end.minute
        latestTime = max(endTime, latestTime)
    return latestTime

# Takes a list of schedules and returns the best schedule based on heuristic
# Returns None when no schedule exists: Front End should check this
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
    #print(optimize(["18290", "18220", "18202", "15122", "18200"]))
    pass