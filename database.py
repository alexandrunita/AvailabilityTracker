import sqlite3
from datetime import date

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


def insert_OOF(startDate, endDate, isHalfDay, oofType, user_id):
    """ Insert OOF period in avaiability.db """
    # connect to db
    conn = sqlite3.connect("availability.db")
    # create cursor
    c = conn.cursor()
    # collect oof_type_id
    c.execute("SELECT id FROM oof_types WHERE name = ?", (oofType,))
    oof_type_id = c.fetchone()[0]
    # collect current OOF days for user_id in oofDays variable
    c.execute("SELECT start_date, end_date FROM oof_days WHERE user_id = ?", (user_id,))
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