from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import sqlite3

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
    return apology("TODO", 200)

@app.route("/login", methods=["GET","POST"])
def login():
    """ Login page """

    # Forget any user_id
    session.clear()

    # check if POST used    
    if request.method == "POST":
        return apology("TODO", 400)
    
    # for GET return login page
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
        conn = sqlite3.connect("availability.db")
        c = conn.cursor()
        c.execute("SELECT username FROM users")
        currentUsers = c.fetchall()[0]
        conn.commit()
        conn.close()
        print(currentUsers)
        if userName in currentUsers:
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
        conn = sqlite3.connect("availability.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, pw_hash) VALUES(?, ?)", (userName, passwordHash))
        conn.commit()
        conn.close()
        # return successful registration screen
        return render_template("register.html", registered=True)
    
    # for GET return register page
    return render_template("register.html")


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