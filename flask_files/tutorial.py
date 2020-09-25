from flask import Flask,redirect,url_for,render_template,request

app = Flask(__name__)

@app.route("/")
def home():
    print("routed home")
    return "Hello! this is the main page<h1>HELLO<h1>"


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