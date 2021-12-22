from flask import redirect, render_template, request, session
from functools import wraps
from datetime import date, timedelta

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def calculate_userDateStrings(startDate, endDate, userOOFDays):
    """Generates individual user Day String lists with symbols to be used in Availability Page tabel"""
    # creating dictionary of userDayStrings which will have keys : username + values : symbols for each vacation day
    usersDayStrings = {}
    # declare individual user string list within this dictionary
    for user in userOOFDays.keys():
        usersDayStrings[user] = []

    # TODO loop through each user
    # foreach user loop through all days between startDate and End
    # if vacation day or WE, add expected symbol || else => add available symbol O

    # populate userDayStrings with available + Weekend
    for user in userOOFDays.keys():
        # initialize cursorDate
        cursorDate = startDate
        while cursorDate <= endDate:
            # if no vacation data, will only have weekends
            # check if cursorDate is a weekend date according to standard EU/US calendar
            if cursorDate.isocalendar().weekday > 5:
                usersDayStrings[user].append("WE")
            else:
                usersDayStrings[user].append("O")        
            cursorDate = cursorDate + timedelta(days=1)
    
    # loop through each user's OOF Dates and edit usersDayStrings with necessary vacation symbols
    for user in userOOFDays.keys():
        for userOOFDay in userOOFDays[user]:
            # if date of current OOF entry is before startDate, skip to next instance of the loop
            cursorDate = date.fromisoformat(userOOFDay[0])
            if cursorDate < startDate:
                continue
            else:
                # determine time delta from startDate of query and current OOF entry date
                # this will be the index into which we need to edit usersDayStrings and add necessary vacation symbol
                delta = (cursorDate - startDate).days
                # skip Weekends
                if cursorDate.isocalendar().weekday > 5:
                    continue
                # check for Vacation
                if userOOFDay[1] == 1:
                    # check for halfDay
                    if userOOFDay[2] == 1:
                        usersDayStrings[user][delta] = "hV"
                    else:
                        usersDayStrings[user][delta] = "V"
                # check for Bank Holiday
                if userOOFDay[1] == 2:
                    usersDayStrings[user][delta] = "BH"
                # check for Attending Training
                if userOOFDay[1] == 3:
                    # check for halfday
                    if userOOFDay[2] == 1:
                        usersDayStrings[user][delta] = "hAT"
                    else:
                        usersDayStrings[user][delta] = "AT"
                # check for Delivering Training
                if userOOFDay[1] == 4:
                    # check for halfday
                    if userOOFDay[2] == 1:
                        usersDayStrings[user][delta] = "hDT"
                    else:
                        usersDayStrings[user][delta] = "DT"
    # return dictionary
    return usersDayStrings