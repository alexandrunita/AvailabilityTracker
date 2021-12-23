import sqlite3
from datetime import date, timedelta

def username_lookup(userName):
    """ Lookup user from availability.db by unique username """

    # connect to db
    conn = sqlite3.connect("availability.db")
    # create cursor
    c = conn.cursor()

    # check if lookup initiated for specific user or for all users
    if userName:
        # query for username in db
        c.execute("SELECT * FROM users WHERE username = ?", (userName,))
    else:
        c.execute("SELECT * FROM users")
    
    # store user/users list into variable
    users = c.fetchall()
    # commit connect and close
    conn.commit()
    conn.close()
    # return user
    return users


def insert_user(userName, passwordHash):
    """ Insert new user into availability.db """
    # connect to db
    conn = sqlite3.connect("availability.db")
    # create cursor
    c = conn.cursor()
    # insert user
    c.execute("INSERT INTO users (username, pw_hash) VALUES(?, ?)", (userName, passwordHash))
    # commit and close connection
    conn.commit()
    conn.close()

def lookup_bookedOOF(user_id, today):
    """ Lookup availability.db to get all booked OOF days for user_id """
    # TODO - connect to database, look up current booked OOF => return booked OOF days to caller
    # connect to db
    conn = sqlite3.connect("availability.db")
    # create cursor
    c = conn.cursor()
    # lookup all booked oof with end date after today for current user
    c.execute("SELECT * FROM oof_days WHERE user_id = ? AND end_date >= ? ORDER BY start_date", (user_id, today))
    oofDays = c.fetchall()
    # commit & close
    conn.commit()
    conn.close()
    # return oofDays - list of tuples
    return oofDays


def insert_OOF(startDate, endDate, isHalfDay, oofType, user_id):
    """ Insert OOF period in availability.db """
    # connect to db
    conn = sqlite3.connect("availability.db")
    # create cursor
    c = conn.cursor()
    # collect oof_type_id
    c.execute("SELECT id FROM oof_types WHERE name = ?", (oofType,))
    oof_type_id = c.fetchone()[0]
    # collect current OOF days for user_id in oofDays variable
    c.execute("SELECT start_date, end_date FROM oof_days WHERE user_id = ? AND end_date >= ?", (user_id, startDate))
    oofDays = c.fetchall()
    # check if there are any overlapping OOF Days during this time frame for the requesting user
    currentStartDate = date.fromisoformat(startDate)
    currentEndDate = date.fromisoformat(endDate)
    for oofDay in oofDays:
        oldStartDate = date.fromisoformat(oofDay[0])
        oldEndDate = date.fromisoformat(oofDay[1])
        # if conflict is found, exit function and return False for main function to understand insert failed
        if (oldStartDate <= currentStartDate <= oldEndDate) or (oldStartDate <= currentEndDate <= oldEndDate):
            return False
    # insert oof day into DB
    c.execute("INSERT INTO oof_days (user_id, oof_type_id, start_date, end_date, full_day) VALUES(?, ?, ?, ?, ?)", (user_id, oof_type_id, startDate, endDate, int(isHalfDay)))
    # commint and close
    conn.commit()
    conn.close()
    # return True for calling function to know insert was successful
    return True


def remove_OOF(user_id, startDate, endDate):
    """ Removes or shortens booked OOFs """
    # connect to db
    conn = sqlite3.connect("availability.db")
    # create cursor
    c = conn.cursor()
    # initialize today
    today = date.today()
    # check if startDate is before today => we will shorten OOF interval by adjusting endDate to yesterday
    # if startDate > today => we will remove the OOF interval from oof_days altogether
    if startDate < today:
        c.execute("UPDATE oof_days SET end_date = ? WHERE start_date = ? AND end_date = ? AND user_id = ?", ((today - timedelta(days=1)).isoformat(), startDate.isoformat(), endDate.isoformat(), user_id))
    else:
        c.execute("DELETE FROM oof_days WHERE start_date = ? AND end_date = ? and user_id = ?", (startDate.isoformat(), endDate.isoformat(), user_id))
    # commit and close
    conn.commit()
    conn.close()
    # return True to signal removal/shortening successful
    return True