import sqlite3

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