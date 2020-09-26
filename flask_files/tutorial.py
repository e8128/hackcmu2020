from flask import Flask,redirect,url_for,render_template,request

from datetime import date, time, datetime, timedelta

import infoParse
from optimization import optimize
tester = ['15122','18220','18290','18202']
tester = optimize(tester)

app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def home():
    print("routed home")
    if request.method=="POST":
        classes=request.form["classes"]
        opt = request.form.get("options")
        yeer = request.form.get("year")
        print(opt)
        if checkInput(classes):
            return redirect(url_for('badInput'))
        else:
            return redirect(url_for("classes",class_string=classes,option=opt,year=yeer))
    else:
        return render_template("hello.html")

@app.route("/<class_string>/<option>/<year>")
def classes(class_string,option,year):
    print("got user1")
    unitCount = getUnits(class_string.split(','))
    return str(unitCount)+ " " + option+" "+year

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        user=request.form["nm"]
        print(url_for("user",usr=user))
        return redirect(url_for("user",usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    print("got user")
    return usr


<<<<<<< Updated upstream

def checkInput(s): #checks if the classes in put is valid
    return '-' in s or s.isalpha()
        

@app.route('/badInput')
def badInput():
    return "BAD"

tester = {'18213': 12, '15251':30}

def getUnits(classes): #takes list of classes and returns total units taken
    unitCount = 0 
    for c in classes:
        c=str(c)
        c=c.strip()
        if c in tester:
            unitCount += tester[c]
    return unitCount


    


def splitString(s): # takes string data we recieve from website 
    newStr = s.split(' ')
    classes = newStr[0]
    opt = newStr[1]
    year = newStr[2] 
    classes=eval(classes)
    return [classes,opt, year] 

=======
'''
    self.classId = classId
    self.start = start
    self.end = end
    self.room = room
'''
test = ['Monday 09:20 to 10:10 @ CMU REMOTE', 'Monday 10:40 to 11:30 @ Mellon Institute MELLON', 'Tuesday 08:00 to 09:20 @ CMU REMOTE', 'Tuesday 13:30 to 14:50 @ CMU REMOTE', 'Thursday 08:00 to 09:20 @ CMU REMOTE', 'Thursday 13:30 to 14:50 @ CMU REMOTE', 'Friday 09:20 to 10:10 @ Doherty Hall 2210']

# [[Monday 09:20 to 10:10 @ CMU REMOTE, Monday 10:40 to 11:30 @ Mellon Institute 
# MELLON, Tuesday 08:00 to 09:20 @ CMU REMOTE, Tuesday 13:30 to 14:50 @ CMU REMOTE, 
# Thursday 08:00 to 09:20 @ CMU REMOTE, Thursday 13:30 to 14:50 @ CMU REMOTE, 
# Friday 09:20 to 10:10 @ Doherty Hall 2210], [Monday 09:20 to 10:10 @ CMU REMOTE, 
# Monday 10:40 to 11:30 @ Tepper Quad 1102, Tuesday 08:00 to 09:20 @ CMU REMOTE, 
# Tuesday 13:30 to 14:50 @ CMU REMOTE, Thursday 08:00 to 09:20 @ CMU REMOTE, 
# Thursday 13:30 to 14:50 @ CMU REMOTE, Friday 09:20 to 10:10 @ Doherty Hall 2210], 
# [Monday 10:40 to 11:30 @ CMU REMOTE, Monday 10:40 to 11:30 @ Mellon Institute MELLON,
#  Tuesday 08:00 to 09:20 @ CMU REMOTE, Tuesday 13:30 to 14:50 @ CMU REMOTE, 
#  Thursday 08:00 to 09:20 @ CMU REMOTE, Thursday 13:30 to 14:50 @ CMU REMOTE, 
#  Friday 10:40 to 11:30 @ Baker Hall A51], [Monday 10:40 to 11:30 @ CMU REMOTE, 
#  Monday 10:40 to 11:30 @ Tepper Quad 1102, Tuesday 08:00 to 09:20 @ CMU REMOTE, 
#  Tuesday 13:30 to 14:50 @ CMU REMOTE, Thursday 08:00 to 09:20 @ CMU REMOTE, 
#  Thursday 13:30 to 14:50 @ CMU REMOTE, Friday 10:40 to 11:30 @ Baker Hall A51]]

def getWeekInfo(classPeriod): #takes 1-d obj and maps all times to weekday set
    weekdaySet = {'Monday':[], 'Tuesday':[],' Wednesday':[], 
                'Thursday':[], 'Friday':[], 'Saturday':[],
                'Sunday':[]}
    for elem in lst: 
        if classPeriod.room != 'CMU REMOTE' and classPeriod.room != 'DNM' and classPeriod!='TBA':
            timeStart = classPeriod.start
            timeEnd = classPeriod.end 
            weekDay = extractDOW(dateObj)
            weekdaySet[weekDay].append(goodDateFormat(dateObj))
            weekdaySet[weekDay].append(goodDateFormat(dateObj))
    return weekdaySet
        

def getAvgTimeOnCampus(weekdaySet): #takes a weekdaySet dictionary, finds time spent eachday
    final = []     #return average mins per day 
    for elem in weekdaySet: #index into weekday (monday: [(10:30, 200)])
        maxTime = max(weekdaySet[elem])
        minTime = min(weekdaySet[elem])
        timeDiff = timeSubtraction(maxTime, minTime)
        final.append(timeDiff)
    return sum(final)/length(final)

#write a fucntiont hat takes a list of schedule return heuristic value 
print(tester[0])

def timeSubtraction(t1, t2): #takes two strings and finds the mins between
    difference = None
    if t1 > t2:
        difference = t1 - t2 
    else:
        difference = t2 - t1 
    return int(difference.total_seconds()) // 60  
>>>>>>> Stashed changes




if __name__== "__main__":
    app.run(debug="True")