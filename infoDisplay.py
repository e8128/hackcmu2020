from infoParse import ClassPeriod 
from infoParse import meetingMinutes
from infoParse import remoteTime
from infoParse import countTime
from optimization import generateAll
from optimization import optimize
import optimization

def infoPrint(schedule):
    for meeting in schedule:
        print(meeting)
    print(countTime(schedule))
    print(remoteTime(schedule))

if __name__ == '__main__':
    potentialSchedules = generateAll(["15210", "15281", "84380", "21355", "11411"])
    schedule = optimize(potentialSchedules)
    # print(schedule)
    # print(countTime(schedule), remoteTime(schedule))
    schedule2 = optimize(potentialSchedules, optimization.minimumFridayHeuristic)
    # print(schedule2)
    # print(countTime(schedule2), remoteTime(schedule2))
    infoPrint(schedule)
    infoPrint(schedule2)
