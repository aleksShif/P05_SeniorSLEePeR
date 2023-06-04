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

@app.route("/onboarding")
def onboarding():
    return render_template("onboarding-stores.html")

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", logged_in=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Sorry, we got lost in the aisles."), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error_code=500, error_message="Uh oh, something went wrong."), 404


if __name__ == "__main__":
    app.debug = True
    app.run()