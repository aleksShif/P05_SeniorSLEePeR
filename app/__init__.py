from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def root():
    return render_template("landing.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.debug = True
    app.run()