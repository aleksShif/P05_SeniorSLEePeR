try:
    from db import query_db
except:
    from db import query_db

import sys 

# TESTED
def create_users_cart_table(): 
    #db.query_db("DROP TABLE IF EXISTS users;")
    query_db("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, zip INT, onboarding INT)")
    query_db("CREATE TABLE IF NOT EXISTS cart(username TEXT, id INTEGER, quantity INTEGER)")

def add_new_user(username, password, onboarding = 0): 
    query_db("INSERT INTO users VALUES (?, ?, NULL, ?);", (username, password, onboarding))

def check_username_availability(username):
    user = query_db("SELECT * FROM users WHERE username = ?", (username,))
    return user is None

def check_creds(username, password):
    user = query_db("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return user is not None

def update_user_password(username, new_password):
    query_db("UPDATE users SET password = ? WHERE username = ?", (new_password, username))

def delete_user(username):
    query_db("DELETE FROM users WHERE username = ?", (username))

def get_user_password(username):
    return query_db("SELECT password FROM users WHERE username = ?", (username,))

def get_onboarding_val(username):
    return query_db("SELECT onboarding FROM users WHERE username = ?", (username,))[0]

def update_onboarding_val(username, new_onboarding):
    query_db("UPDATE users SET onboarding = ? WHERE username = ?", (new_onboarding, username))


def get_user_zip(username):
    return query_db("SELECT zip FROM users WHERE username = ?", (username,))[0]

def update_user_zip(username, new_zip):
    query_db("UPDATE users SET zip = ? WHERE username = ?", (new_zip, username))

# LINES BELOW ONLY GET RUN IF "EXPLICITY RAN" with `python3 app/db/auth.py`
# if __name__ == "__main__":
#     create_users_cart_table()
#     print(check_username_availability("epap"))
#     add_new_user("epap", "hi")
#     print(check_creds("epap", "hi"))
#     print(check_creds("epap", "hi2"))
#     print(check_username_availability("epap"))

create_users_cart_table()