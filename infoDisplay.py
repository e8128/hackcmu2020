from infoParse import ClassPeriod 
from infoParse import meetingMinutes
from infoParse import remoteTime
from infoParse import countTime
from optimization import generateAll
from optimization import optimize
from optimization import getDistanceWalked
import optimization

junk1 = 0
junk2 = 0

# Example of info return function
def getInfo(schedule):
    return (schedule, countTime(schedule), remoteTime(schedule),
             getDistanceWalked(schedule) )

# TODO: Return earliest/latest class times (see optimization.py heuristics)
def infoPrint(schedule):
    for meeting in schedule:
        print(meeting)
    print(countTime(schedule))
    print(remoteTime(schedule))

# Populate this dictionary
heuristicDict = {'fridayOff': optimization.minimumFridayHeuristic,
                 'noRemote': optimization.remoteTimeHeuristic,
                 'latestTime': optimization.latestTimeHeuristic,
                 'earliestTime': optimization.earliestTimeHeuristic,
                 'o-cardio': optimization.largeCardio,
                 'o-downtime': optimization.maxTimeOnCampus,
                 'o-getMeOut': optimization.leastTimeOnCampus,
                 'o-iHateWalking': optimization.getDistanceWalked,
                 'shortestTime': optimization.shortestTimeHeuristic
                 }

def getBestSchedule (classes, option):
    (potentialSchedules, junk1, junk2) = generateAll(classes)
    schedule = optimize(potentialSchedules, heuristicDict[option])
    return schedule

# Example of how to use optimize
if __name__ == '__main__':
    # from user
    classes = ["15210", "15281", "84380", "21355", "11411"]
    # then generate the potentialSchedules
    global junk1
    global junk2
    (potentialSchedules, junk1, junk2) = generateAll(classes)
    # from user
    chosenHeuristic = 'fridayOff'
    schedule = optimize(potentialSchedules, heuristicDict[chosenHeuristic])
    chosenHeuristic = 'noRemote'
    schedule2 = optimize(potentialSchedules, heuristicDict[chosenHeuristic])
    chosenHeuristic = 'latestTime'
    schedule3 = optimize(potentialSchedules, heuristicDict[chosenHeuristic])
    chosenHeuristic = 'earliestTime'
    schedule4 = optimize(potentialSchedules, heuristicDict[chosenHeuristic])
    
    chosenHeuristic = 'shortestTime'
    schedule5 = optimize(potentialSchedules, heuristicDict[chosenHeuristic])

    infoPrint(schedule)
    infoPrint(schedule2)
    infoPrint(schedule3)
    infoPrint(schedule4)
    infoPrint(schedule5)
