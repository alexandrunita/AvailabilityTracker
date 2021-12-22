from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date, timedelta
import sqlite3
import database

from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Initializing list of approved OOF Types
OOF_TYPES = [
    "Vacation",
    "Bank Holiday",
    "Attending Training",
    "Delivering Training"
]

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
    currentDate = date.today()
    currentDateString = currentDate.strftime("%A %d. %B %Y")

    # collect all users from DB
    users = database.username_lookup(None)

    # declare list of usernames : userNames
    userNames = []
    # iterate through the list of tuples containing full user info
    # append each username to userNames list
    for user in users:
        userNames.append(user[1])

    # TODO - distinct marker for each OOF day for each person

    # collect list of all month names and required colspan for each
    # reset set a cursor starting with current month first day to ensure no issues with date arithmatic
    months = []
    i = 0
    firstDayOfCurrentMonth = currentDate.replace(day = 1)
    # create list of days that will hold formatted strings of all day values for the next 12 months
    dayStrings = []
    dateCursor = currentDate
    # iterate through 12 months - limit to be exposed to end users on availability page
    for i in range(12):
        currentMonth = {}
        # collect name of current month
        currentMonth["name"] = firstDayOfCurrentMonth.strftime("%B")
        # check if current month is December, increment to next year
        if firstDayOfCurrentMonth.month % 12 == 0:
            firstDayofNextMonth = firstDayOfCurrentMonth.replace(month=1, year=firstDayOfCurrentMonth.year+1)        
        else:
            firstDayofNextMonth = firstDayOfCurrentMonth.replace(month=firstDayOfCurrentMonth.month+1)
        # check if we are on the currentDate, if yes find out number of days until end of this month
        # else find out total number of days in month
        if currentDate.month == firstDayOfCurrentMonth.month and currentDate.year == firstDayOfCurrentMonth.year:
            currentMonth["daysLeft"] = (firstDayofNextMonth - currentDate).days
        else:
            currentMonth["daysLeft"] = (firstDayofNextMonth - firstDayOfCurrentMonth).days
        # iterate through all days left to append to daysStrings
        j = 0
        for j in range(currentMonth["daysLeft"]):
            dayStrings.append(dateCursor.strftime("%d"))
            # increment dateCursor with one more day
            dateCursor = dateCursor + timedelta(days=1)
        currentMonth["year"] = firstDayOfCurrentMonth.year
        # move to next moth in iteration
        firstDayOfCurrentMonth = firstDayofNextMonth
        # append current month details to months list
        months.append(currentMonth)
    # return availability template
    return render_template("availability.html", currentDateString = currentDateString, userNames = userNames, months = months, dayStrings = dayStrings)


@app.route("/bookOOF", methods=["GET","POST"])
@login_required
def bookOOF():
    """Book OOF day"""

    # check if POST used
    if request.method == "POST":
        # store OOF details in variables
        startDate = request.form.get("startDate")
        endDate = request.form.get("endDate")
        halfDay = request.form.get("halfDay")
        oofType = request.form.get("oofType")  
        # validate user inputs
        if oofType not in OOF_TYPES:
            return apology("Bad Request - Unsupported OOF Type", 400)
        # check if this is a half day request
        # by default it will not be a half day
        isHalfDay = False
        if startDate == endDate and halfDay == "True":
            isHalfDay = True
        # check if no startDate or endDate provided
        if not startDate or not endDate:
            return apology("Bad Request - must provide StartDate AND EndDate for OOF request", 400)
        # check if startDate > endDate
        if date.fromisoformat(startDate) > date.fromisoformat(endDate):
            return apology("Bad Request - OOF End Date cannot precede Start Date", 400)
        # check if startDate before Today
        if date.fromisoformat(startDate) < date.today():
            return apology("Bad Request - OOF Start Date cannot precede Today", 400)
        # if oofDay failed to be inserted in DB, return apology and explain cause is conflict with prior OOF day
        if not database.insert_OOF(startDate, endDate, isHalfDay, oofType, session["user_id"]):
            return apology("OOF NOT BOOKED - request conflicts with previous OOF booking for this user", 400)
        # return booking confirmation page
        return render_template("bookOOF.html", booked = True, startDate = startDate, endDate = endDate, isHalfDay = isHalfDay, oofType = oofType)
    # if GET is used => return form
    # display all booked OOF days for current user at bottom of page
    oofDays = database.lookup_bookedOOF(session["user_id"], date.today().isoformat())
    # if user has no pre-existent booked OOF days, add nothing to standard template
    return render_template("bookOOF.html", oofTypes = OOF_TYPES, oofDays = oofDays)
    


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