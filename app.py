from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
import sqlite3
import database

from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# root route function
@app.route("/")
@login_required
def index():
    """ Show current Team availability """

    # Collect current date
    currentDate = date.today().strftime("%A %d. %B %Y")

    # collect all users from DB
    users = database.username_lookup(None)

    # TODO
    # remove password hash from users before sending data to FrontEnd

    # declare list of usernames : userNames
    userNames = []
    # iterate through the list of tuples containing full user info
    # append each username to userNames list
    for user in users:
        userNames.append(user[1])

    print(userNames)

    # return availability template
    return render_template("availability.html", currentDate=currentDate, userNames = userNames)
    

@app.route("/login", methods=["GET","POST"])
def login():
    """ Login page """

    # Forget any user_id
    session.clear()

    # check if POST used    
    if request.method == "POST":
        # store userName in variable
        userName = request.form.get("username")
        # return apology for blank username
        if not userName:
            return apology("must provide username", 403)
        # store password in variable
        password = request.form.get("password")
        # return apology for blank password
        if not password:
            return apology("must provide password", 403)
        # query database for username, collect first entry from list of size 1
        existingUser = database.username_lookup(userName)[0]
        # check if user was found and if provided password matches DB hash
        if not existingUser or not check_password_hash(existingUser[2], password):
            return apology("invalid username and/or password", 403)
        # remember logged in userid
        session["user_id"] = existingUser[0]
        # redirect to home page
        return redirect("/")

    # for GET method return login page
    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    """ Registration Page """

    # Forget any user_id
    session.clear()

    # check if method is POST
    if request.method == "POST":
        # ensure UserName was provided
        userName = request.form.get("username")
        if not userName:
            return apology("must provide username")
        # query existing users and make sure username is not already taken
        existingUser = database.username_lookup(userName)
        if existingUser:
            return apology("username already taken, try another one")
        # check if password or confirmation blank
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation:
            return apology("password and confirmation must be filled in")
        # ensure password and confirmation match
        if password != confirmation:
            return apology("password and confirmation must match")
        # generate password hash
        passwordHash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        # insert new user into db
        database.insert_user(userName, passwordHash)
        # return successful registration screen
        return render_template("register.html", registered=True)
    
    # for GET return register page
    return render_template("register.html")


@app.route("/logout")
def logout():
    """ Log user out """
    # forget user_id
    session.clear()
    # redirect usert to homepage/login
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# Run App in Debug Mode
# This will Reload the app automatically once app code changes
if __name__ == '__main__':
    app.run(debug = True)