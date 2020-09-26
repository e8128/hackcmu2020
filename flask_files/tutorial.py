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
        return redirect(url_for("classes",class_string=classes,option=opt,year=yeer))
    else:
        return render_template("hello.html")

@app.route("/<class_string>/<option>/<year>")
def classes(class_string,option,year):
    print("got user1")
    return str(class_string.split(","))+ " " + option+" "+year

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

if __name__== "__main__":
    app.run(debug="True")