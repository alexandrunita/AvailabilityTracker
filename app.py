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
    # check if POST used    
    if request.method == "POST":
        return apology("TODO", 400)
    
    # for GET return login page
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    """ Registration Page """
    # check if method is POST
    if request.method == "POST":
        return apology("TODO", 400)
    
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