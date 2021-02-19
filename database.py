import sqlite3

def username_lookup(userName):
    """ Lookup user from availability.db by unique username """
    # connect to db
    conn = sqlite3.connect("availability.db")
    # create cursor
    c = conn.cursor()
    # query for username in db
    c.execute("SELECT * FROM users WHERE username = ?", (userName,))
    # store user into variable
    user = c.fetchone()
    # commit connect and close
    conn.commit()
    conn.close()
    # return user
    return user


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