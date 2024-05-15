import sqlite3

conn = sqlite3.connect("userDB.db")
c = conn.cursor()


# create the table and add data
def init():
    c.execute(""" CREATE TABLE IF NOT EXISTS users(
    username string, password int)
    """)
    user = c.fetchone()
    if user == None:
        c.execute("INSERT INTO users VALUES ('adi12','3011de5fcb6c8a55f1442a777620af0f')")
        c.execute("INSERT INTO users VALUES ('Moshe', '66dbbbd2d3edde6f07af03521ae90b72')")
        c.execute("INSERT INTO users VALUES ('alex', '049754413fdf62ba3b68e6650a184a42')")
        c.execute("INSERT INTO users VALUES ('thomas', 'dfc8c58e3c127565f4c1b331af4b9f56')")
        c.execute("INSERT INTO users VALUES ('david', '5d33d900ad8819dee3df730fc8a412b5')")
        conn.commit()


# fins the user by usename & password
def search_user(username, password):
    # Execute the query with parameters to prevent SQL injection
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

    # Fetch one row to check if the user exists
    user = c.fetchone()

    # Check if user exists
    if user is None:
        return False
    return True

# adds a newly uploaded file to files table
def add_new_user(username, password):
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()


# edit user details
def edit_user(username, old_password, new_password):
    c.execute(f"SELECT * FROM users WHERE username =  '{username}' AND password = '{old_password}'")
    result = c.fetchone()
    if result[0]:
        remove_user(username)
        c.execute("INSERT INTO users VALUES (?, ?)", (username, new_password))
    return result[0] if result else None


# removes the user - admin only
def remove_user(username):
    c.execute(f"DELETE FROM users WHERE username =  '{username}' ")
    conn.commit()


def close_connection():
    conn.close()


init()