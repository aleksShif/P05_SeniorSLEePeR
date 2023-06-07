try:
    from db import query_db
except:
    from db import query_db

import sys 

# TESTED
def create_users_cart_table(): 
    #db.query_db("DROP TABLE IF EXISTS users;")
    query_db("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, onboarding INT)")
    query_db("CREATE TABLE IF NOT EXISTS cart(username TEXT, id INTEGER, quantity INTEGER)")

def add_new_user(username, password, onboarding = 0): 
    query_db("INSERT INTO users VALUES (?, ?, ?);", (username, password, onboarding))

def check_username_availability(username):
    user = query_db("SELECT * FROM users WHERE username = ?", (username,))
    return user is None

def check_creds(username, password):
    passw = query_db("SELECT password FROM users WHERE username = ?", (username,))
    return (len(passw) != 0 and password == passw[0][0])

def update_user_password(username, new_password):
    # query_db("UPDATE users SET password = ? WHERE username = ?", (username, new_password))
    query_db("DELETE FROM users WHERE username = ?", (username,))
    add_new_user(username, new_password)

def delete_user(username):
    query_db("DELETE FROM users WHERE username = ?", (username))

def get_user_password(username):
    password = query_db("SELECT password FROM users WHERE username = ?", (username,))
    return password

def get_onboarding_val(username):
    return query_db("SELECT onboarding FROM users WHERE username = ?", (username,))[0]

def update_onboarding_val(username, new_onboarding):
    passw = get_user_password(username)
    add_new_user(username, passw, onboarding = new_onboarding)

# LINES BELOW ONLY GET RUN IF "EXPLICITY RAN" with `python3 app/db/auth.py`
# if __name__ == "__main__":
#     create_users_cart_table()
#     print(check_username_availability("epap"))
#     add_new_user("epap", "hi")
#     print(check_creds("epap", "hi"))
#     print(check_creds("epap", "hi2"))
#     print(check_username_availability("epap"))

create_users_cart_table()