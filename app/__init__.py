from flask import Flask, render_template, request, session, redirect, url_for
from auth import *
from cart import *
from db import * 
from produce import *
from input_check import *

app = Flask(__name__)
app.secret_key = b'pAHy827suhda*216jdaa'

@app.route("/")
def root():
    return render_template("landing.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session: 
        return redirect(url_for('catalog'))
    if request.method == 'POST': 
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if check_creds(username, password):
            session['username'] = request.form['username']
            return redirect(url_for('catalog'))
        return render_template('login.html', error="Wrong username and password")
    return render_template("login.html", error='')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session:  
        return redirect(url_for('catalog'))

    if request.method == 'POST':  
        new_user = request.form['new_username'].strip()
        new_pass = request.form['new_password']
        new_pass_confirm = request.form['new_password_confirm']

        if not new_pass == new_pass_confirm:
            return redirect(url_for("register"))

        if check_username_requirements(new_user) and check_password_requirements(new_pass) and check_username_availability(new_user):
            add_new_user(new_user, new_pass)
            session['username'] = new_user
            return redirect(url_for('catalog'))

        return redirect(url_for("register"))
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/onboarding")
def onboarding():
    return render_template("onboarding-stores.html")

@app.route("/catalog")
def catalog():
    logged_in = False
    session_username = ""

    if 'username' in session:
        logged_in = True
        session_username = session['username']
    return render_template("catalog.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Sorry, we got lost in the aisles."), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error_code=500, error_message="Uh oh, something went wrong."), 404


if __name__ == "__main__":
    app.debug = True
    app.run()