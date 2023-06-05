from flask import Flask, render_template, request, session, redirect, url_for, flash
from auth import *
from cart import *
from db import * 
from produce import *
from input_check import *

app = Flask(__name__)
app.secret_key = b'pAHy827suhda*216jdaa'

@app.route("/")
def root():
    if 'username' in session:
        return redirect(url_for("catalog"))
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
        
        flash('Invalid credentials')
        return render_template('login.html')

    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session:  
        return redirect(url_for('catalog'))

    if request.method == 'POST':  
        new_user = request.form['new_username'].strip()
        new_pass = request.form['new_password']
        new_pass_confirm = request.form['new_password_confirm']

        if not new_pass == new_pass_confirm:
            flash('Passwords do not match')
            return redirect(url_for("register"))

        if check_username_requirements(new_user) and check_password_requirements(new_pass) and check_username_availability(new_user):
            add_new_user(new_user, new_pass)
            session['username'] = new_user
            return redirect(url_for('catalog'))

        if not check_username_requirements(new_user):
            flash("Username has to be 4 characters or longer")

        if not check_password_requirements(new_pass):
            flash("Password has to be 4 characters or longer")

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
    if 'username' not in session:
        return redirect(url_for("root"))
    return render_template("catalog.html", logged_in=True)


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for("login"))

    username = session.get("username")

    if request.method == 'POST':  
        new_pass = request.form['password']
        new_pass_confirm = request.form['confirm-password']

        if not new_pass == new_pass_confirm:
            flash('Passwords do not match')
            return redirect(url_for("profile"))

        if check_password_requirements(new_pass):
            update_user_password(username, new_pass)
            return redirect(url_for('catalog'))

        if not check_password_requirements(new_pass):
            flash("Password has to be 4 characters or longer")

        return redirect(url_for("profile"))

    return render_template("profile.html", logged_in=True, username=username)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Sorry, we got lost in the aisles."), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error_code=500, error_message="Uh oh, something went wrong."), 500


if __name__ == "__main__":
    app.debug = True
    app.run()