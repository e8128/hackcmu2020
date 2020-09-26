from flask import Flask,redirect,url_for,render_template,request
from infoDisplay import getBestSchedule,getInfo
from optimization import getUnits

#Stackoverflow solution: https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

app = Flask(__name__)


optionNames = { 'o-cardio': 'Cardio', 'fridayOff': 'No Fridays!', 
            'latestTime': 'Latest Time', 'earliestTime': 'Early Bird',
            'noRemote':'No Remote', 'o-downtime':'Most Break Between Class',
            'o-getMeOut': 'Least Break Between Classes','o-iHateWalking': 'No-Cardio'
}

@app.route("/",methods=["POST","GET"])
def home():
    print("routed home")
    if request.method=="POST":
        classes=request.form["classes"]
        opt = request.form.get("options")
        yeer = request.form.get("year")
        print(opt)
        return redirect(url_for("classes",class_string=classes,option=opt,year=yeer))
    else:
        return render_template("hello.html",name=None,timeWalked=None,remote=None,timeAtSchool=None,units=None)

@app.route("/<class_string>/<option>")
def classes(class_string,option):
    print("Input:", class_string, option)
    classes = class_string.split(", ")
    schedule = getBestSchedule(classes, option)
    info = getInfo(schedule)
    print(info) #TODO: display schedule
    weekdayTime = info[1] #list from length 7 each index is time in mins spent
    makeGraphWeekday(weekdayTime)
    remoteTime = info[2][0] #info[2] is tuple of (remote, oncampusTime)
    campusTime = info[2][1]
    units = getUnits(classes)
    distance = info[3] 
    numSched = info[4]
    name = optionNames[option]
    if distance == 0:
        distance = '< 1'

    return render_template("hello.html",name=name,timeWalked=distance,
                            remote=remoteTime,timeAtSchool=campusTime
                            ,units=units, numSched=numSched, graphed=True)

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


def makeGraphWeekday(classes): #takes list of classes times and returns bar graph
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    mins = classes
    ax.bar(days, mins)
    plt.xlabel('Weekday')
    plt.ylabel('Time Spent in Mins')
    plt.title('Time Spent on Classes by Weekday')
    plt.savefig('./static/assets/weekdayPlot.png')

makeGraphWeekday([1,2,3,5,6,6,2])



    


def splitString(s): # takes string data we recieve from website 
    newStr = s.split(' ')
    classes = newStr[0]
    opt = newStr[1]
    year = newStr[2] 
    classes=eval(classes)
    return [classes,opt, year] 





if __name__== "__main__":
    app.run(debug="True")