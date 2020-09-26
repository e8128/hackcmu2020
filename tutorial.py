from flask import Flask,redirect,url_for,render_template,request
from infoDisplay import getBestSchedule,getInfo
from optimization import getUnits

app = Flask(__name__)

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
    remoteTime = info[2][0] #info[2] is tuple of (remote, oncampusTime)
    campusTime = info[2][1]
    units = getUnits(classes)
    distance = info[3] 
    return render_template("hello.html",name=option,timeWalked=distance,
                            remote=remoteTime,timeAtSchool=campusTime
                            ,units=units)

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

'''
def getUnits(classes): #takes list of classes and returns total units taken
    unitCount = 0 
    for c in classes:
        c=str(c)
        c=c.strip()
            if c in tester:
                unitCount += tester[c]
        return unitCount
'''

    


def splitString(s): # takes string data we recieve from website 
    newStr = s.split(' ')
    classes = newStr[0]
    opt = newStr[1]
    year = newStr[2] 
    classes=eval(classes)
    return [classes,opt, year] 





if __name__== "__main__":
    app.run(debug="True")