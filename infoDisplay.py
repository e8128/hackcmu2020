from infoParse import ClassPeriod 
from infoParse import meetingMinutes
from infoParse import remoteTime
from infoParse import countTime
from optimization import generateAll
from optimization import optimize
import optimization

# Example of info return function
def getInfo(schedule):
    return (schedule, countTime(schedule), remoteTime(schedule))

def infoPrint(schedule):
    for meeting in schedule:
        print(meeting)
    print(countTime(schedule))
    print(remoteTime(schedule))

# Populate this dictionary
heuristicDict = {'fridayOff': optimization.minimumFridayHeuristic,
                 'noRemote': optimization.remoteTimeHeuristic}

# Example of how to use optimize
if __name__ == '__main__':
    # from user
    classes = ["15210", "15281", "84380", "21355", "11411"]
    # then generate the potentialSchedules
    potentialSchedules = generateAll(classes)
    # from user
    chosenHeuristic = 'fridayOff'
    schedule = optimize(potentialSchedules, heuristicDict[chosenHeuristic])
    chosenHeuristic = 'noRemote'
    schedule2 = optimize(potentialSchedules, heuristicDict[chosenHeuristic])

    infoPrint(schedule)
    infoPrint(schedule2)
