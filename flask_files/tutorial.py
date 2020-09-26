from flask import Flask,redirect,url_for,render_template,request

from datetime import date, time, datetime, timedelta

from infoParse import extractDOW, goodDateFormat
from optimization import optimize

tester = ['15122','18290']
tester = optimize(tester)
print(tester[0])

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



def checkInput(s): #checks if the classes in put is valid
    return '-' in s or s.isalpha()
        

@app.route('/badInput')
def badInput():
    return "BAD"

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
    for elem in classPeriod: 
        classObj = elem
        if classObj.room != 'CMU REMOTE' and classObj.room != 'DNM' and classObj!='TBA':
            timeStart = classObj.start
            timeEnd = classObj.end 
            weekDay = extractDOW(classObj.start)
            weekdaySet[weekDay].append(goodDateFormat(timeStart))
            weekdaySet[weekDay].append(goodDateFormat(timeEnd))
    return weekdaySet
   

#write a fucntiont hat takes a list of schedule return heuristic value 

def timeSubtraction(t1, t2): #takes two strings and finds the mins between
    print(t1,t2)
    difference = None
    newT = t1.split(':')
    hour1 = int(newT[0])
    min1=int(newT[1])
    newT2 = t2.split(':')
    hour2=int(newT2[0])
    min2=int(newT2[1])
    t1 = hour1*60+min1
    t2 = hour2*60+min2
    #t1 = timedelta(hours=hour1, minutes=min1)
    #t2 = timedelta(hours=hour2, minutes=min2)
    if t1 > t2:
        difference = t1 - t2
    else:
        difference = t2 - t1
    return difference
    #return int(difference.total_seconds()) // 60  



def getAvgTimeOnCampus(weekdaySet): #takes a weekdaySet dictionary, finds time spent eachday
    final = []     #return average mins per day 
    for elem in weekdaySet: #index into weekday (monday: [(10:30, 200)])
        print(elem)
        if weekdaySet[elem]!=[]:
            highest = weekdaySet[elem][len(weekdaySet[elem])-1] #ast element should be highest
            lowest = weekdaySet[elem][0]
            timeDiff = timeSubtraction(highest, lowest)
            final.append(timeDiff)
        print(final)
    return sum(final)/len(final)



print(getAvgTimeOnCampus(getWeekInfo(tester[0])))  

if __name__== "__main__":
    #app.run(debug="True")
    pass