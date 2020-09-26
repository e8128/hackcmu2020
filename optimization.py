from infoParse import ClassPeriod
from infoParse import parseTime
from infoParse import getCourseMeetings
from infoParse import checkConflicts
from infoParse import generatePossibleSections
from infoParse import remoteTime
from infoParse import countTime

from infoParse import extractDOW

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
    return (cleanedSchedules, len(potentialSchedules), len(cleanedSchedules))

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

def shortestTimeHeuristic(meetings):
    weekdaySet = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 
                 'Thursday':[], 'Friday':[], 'Saturday':[],
                 'Sunday':[]}
    totalTime = 0
    for meeting in meetings: 
        # classObj.start
        weekDay = extractDOW(meeting.start)
        weekdaySet[weekDay].append(meeting.start)
        weekdaySet[weekDay].append(meeting.end)
    for day in weekdaySet:
        if len(weekdaySet[day]) <= 0:
            continue
        highest = weekdaySet[day][-1]
        lowest = weekdaySet[day][0]
        totalTime += timeSubtraction(lowest, highest)
    return totalTime

def getWeekInfo(classPeriod): #takes 1-d obj and maps all times to weekday set
    weekdaySet = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 
                'Thursday':[], 'Friday':[], 'Saturday':[],
                'Sunday':[]}
    for elem in classPeriod: 
        classObj = elem
        # classObj.start 
        if classObj.room != 'CMU REMOTE' and classObj.room != 'DNM' and classObj!='TBA':
            timeStart = classObj.start
            timeEnd = classObj.end 
            weekDay = extractDOW(classObj.start)
            print(weekDay in weekdaySet)
            weekdaySet[weekDay].append(timeStart)
            weekdaySet[weekDay].append(timeEnd)
    return weekdaySet

# def timeSubtraction(t1, t2): #takes two strings and finds the mins between
#     print(t1,t2)
#     difference = None
#     newT = t1.split(':')
#     hour1 = int(newT[0])
#     min1=int(newT[1])
#     newT2 = t2.split(':')
#     hour2=int(newT2[0])
#     min2=int(newT2[1])
#     t1 = hour1*60+min1
#     t2 = hour2*60+min2
#     #t1 = timedelta(hours=hour1, minutes=min1)
#     #t2 = timedelta(hours=hour2, minutes=min2)
#     if t1 > t2:
#         difference = t1 - t2
#     else:
#         difference = t2 - t1
#     return difference
    #return int(difference.total_seconds()) // 60  

def timeSubtraction(t1, t2):
    timedelta = t2 - t1
    return abs((int(timedelta.total_seconds()) // 60))

def getAvgTimeOnCampus(weekdaySet): #takes a weekdaySet dictionary, finds time spent eachday
    final = []     #return average mins per day 
    for elem in weekdaySet: #index into weekday (monday: [(10:30, 200)])
        timeDiff = 0
        if weekdaySet[elem]!=[]:
            # print('weekdaything', weekdaySet[elem])
            highest = weekdaySet[elem][len(weekdaySet[elem])-1] #ast element should be highest
            lowest = weekdaySet[elem][0]
            timeDiff = timeSubtraction(highest, lowest)
            final.append(timeDiff)
    # print('final here',final)
    return sum(final)/len(final) 

distance = {'Doherty Hall': {'location': 'Doherty Hall', 'Doherty Hall': '0', 'Tepper Quad': '5', 'Margaret Morrison': '7', 'Wean hall': '1', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '12', 'Scaife Hall': '4', 'ANSYS': '3', 'Hammerschlag Hall': '4', 'Hamburg Hall': '5', 'Porter hall': '5', 'Posner Hall': '6', 'Gates and Hillman Centers': '5'}, 'DH': {'location': 'Doherty Hall', 'Doherty Hall': '0', 'Tepper Quad': '5', 'Margaret Morrison': '7', 'Wean hall': '1', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '12', 'Scaife Hall': '4', 'ANSYS': '3', 'Hammerschlag Hall': '4', 'Hamburg Hall': '5', 'Porter hall': '5', 'Posner Hall': '6', 'Gates and Hillman Centers': '5'}, 'Tepper Quad': {'location': 'Tepper Quad', 'Doherty Hall': '5', 'Tepper Quad': '0', 'Margaret Morrison': '8', 'Wean hall': '4', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '9', 'Scaife Hall': '7', 'ANSYS': '6', 'Hammerschlag Hall': '7', 'Hamburg Hall': '2', 'Porter hall': '8', 'Posner Hall': '8', 'Gates and Hillman Centers': '2'}, 'Margaret Morrison': {'location': 'Margaret Morrison Carnegie Hall', 'Doherty Hall': '7', 'Tepper Quad': '8', 'Margaret Morrison': '0', 'Wean hall': '8', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '16', 'Scaife Hall': '7', 'ANSYS': '7', 'Hammerschlag Hall': '6', 'Hamburg Hall': '7', 'Porter hall': '6', 'Posner Hall': '1', 'Gates and Hillman Centers': '7'}, 'Wean Hall': {'location': 'Wean Hall', 'Doherty Hall': '1', 'Tepper Quad': '4', 'Margaret Morrison': '8', 'Wean hall': '0', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '11', 'Scaife Hall': '3', 'ANSYS': '2', 'Hammerschlag Hall': '3', 'Hamburg Hall': '3', 'Porter hall': '4', 'Posner Hall': '8', 'Gates and Hillman Centers': '3'}, 'CMU REMOTE': {'location': 'CMU REMOTE', 'Doherty Hall': '0', 'Tepper Quad': '0', 'Margaret Morrison': '0', 'Wean hall': '0', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '0', 'Scaife Hall': '0', 'ANSYS': '0', 'Hammerschlag Hall': '0', 'Hamburg Hall': '0', 'Porter hall': '0', 'Posner Hall': '0', 'Gates and Hillman Centers': '0'}, 'Mellon Institute': {'location': 'Mellon Institute MELLON', 'Doherty Hall': '12', 'Tepper Quad': '9', 'Margaret Morrison': '16', 'Wean hall': '11', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '0', 'Scaife Hall': '13', 'ANSYS': '13', 'Hammerschlag Hall': '14', 'Hamburg Hall': '9', 'Porter hall': '14', 'Posner Hall': '16', 'Gates and Hillman Centers': '9'}, 'Scaife hall': {'location': 'Scaife Hall', 'Doherty Hall': '4', 'Tepper Quad': '7', 'Margaret Morrison': '7', 'Wean hall': '3', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '13', 'Scaife Hall': '0', 'ANSYS': '1', 'Hammerschlag Hall': '1', 'Hamburg Hall': '6', 'Porter hall': '1', 'Posner Hall': '7', 'Gates and Hillman Centers': '6'}, 'Ansys Hall': {'location': 'Ansys Hall', 'Doherty Hall': '3', 'Tepper Quad': '6', 'Margaret Morrison': '7', 'Wean hall': '2', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '13', 'Scaife Hall': '1', 'ANSYS': '0', 'Hammerschlag Hall': '1', 'Hamburg Hall': '5', 'Porter hall': '2', 'Posner Hall': '7', 'Gates and Hillman Centers': '5'}, 'Hammerschlag': {'location': 'Hammerschlag Hall', 'Doherty Hall': '4', 'Tepper Quad': '7', 'Margaret Morrison': '6', 'Wean hall': '3', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '14', 'Scaife Hall': '1', 'ANSYS': '1', 'Hammerschlag Hall': '0', 'Hamburg Hall': '6', 'Porter hall': '2', 'Posner Hall': '6', 'Gates and Hillman Centers': '6'}, 'Hamburg Hall': {'location': 'Hamburg Hall', 'Doherty Hall': '5', 'Tepper Quad': '2', 'Margaret Morrison': '7', 'Wean hall': '3', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '9', 'Scaife Hall': '6', 'ANSYS': '5', 'Hammerschlag Hall': '6', 'Hamburg Hall': '0', 'Porter hall': '7', 'Posner Hall': '8', 'Gates and Hillman Centers': '0'}, 'Porter Hall': {'location': 'Porter hall', 'Doherty Hall': '5', 'Tepper Quad': '8', 'Margaret Morrison': '6', 'Wean hall': '4', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '14', 'Scaife Hall': '1', 'ANSYS': '2', 'Hammerschlag Hall': '2', 'Hamburg Hall': '7', 'Porter hall': '0', 'Posner Hall': '6', 'Gates and Hillman Centers': '7'}, 'Posner Hall': {'location': 'Posner Hall', 'Doherty Hall': '6', 'Tepper Quad': '8', 'Margaret Morrison': '1', 'Wean hall': '8', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '16', 'Scaife Hall': '7', 'ANSYS': '7', 'Hammerschlag Hall': '6', 'Hamburg Hall': '8', 'Porter hall': '6', 'Posner Hall': '0', 'Gates and Hillman Centers': '8'}, 'Gates and Hillman Center': {'location': 'Gates and Hillman Centers', 'Doherty Hall': '5', 'Tepper Quad': '2', 'Margaret Morrison': '7', 'Wean hall': '3', 'CMU REMOTE': '0', 'Mellon Institute MELLON': '9', 'Scaife Hall': '6', 'ANSYS': '5', 'Hammerschlag Hall': '6', 'Hamburg Hall': '0', 'Porter hall': '7', 'Posner Hall': '8', 'Gates and Hillman Centers': '0'}}

def getRoom(s): #gets room from string
    i = 0 
    final = ''
    while i <len(s) and not s[i].isdigit() :
        final+=s[i]
        i+=1
    final = final.strip()
    return final


def getDistanceWalked(classPeriods): #takes a list of classes periods
                                     #walked each day 
    weekdaySet = {'Monday':0, 'Tuesday':0,'Wednesday':0, 
                'Thursday':0, 'Friday':0, 'Saturday':0,
                'Sunday':0}
    if len(classPeriods)==1:
        return weekDaySet
    for i in range(1,len(classPeriods)):
        lastRoom = classPeriods[i-1].room
        lastday = extractDOW(classPeriods[i-1].start)
        room = classPeriods[i].room
        currday = extractDOW(classPeriods[i].start)

        if lastday == currday:
            # print(currday)
            lastRoom = getRoom(lastRoom)
            room = getRoom(room)
            if lastRoom in distance and room in distance[lastRoom]:
                distanceWalked = distance[lastRoom][room] #key twice into dictionary
                # print(distanceWalked)
                weekdaySet[currday] = weekdaySet[currday] + int(distanceWalked)
            else:
                weekdaySet[currday]+=5
    return sum(weekdaySet.values()) #returns the sum of all distance walked

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


def largeCardio(sched):
    return -1 * getDistanceWalked(sched)

def leastTimeOnCampus(sched):
    return getAvgTimeOnCampus(getWeekInfo(sched))

def maxTimeOnCampus(sched):
    return -1 * leastTimeOnCampus(sched)

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
