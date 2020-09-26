from flask import Flask,redirect,url_for,render_template,request

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
        # TODO: update data after returning from optimize
        labels = [
            'JAN', 'FEB', 'MAR', 'APR',
            'MAY', 'JUN', 'JUL', 'AUG',
            'SEP', 'OCT', 'NOV', 'DEC'
        ]
        values = [
            967.67, 1190.89, 1079.75, 1349.19,
            2328.91, 2504.28, 2873.83, 4764.87,
            4349.29, 6458.30, 9907, 16297
        ]
        return render_template("hello.html", title='Bitcoin Monthly Price in USD', max=17000, labels=labels, values=values)

# TODO: pass this into optimize
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





if __name__== "__main__":
    app.run(debug="True")