# create table
# add store, user
# get list all stores per user 
try:
    from db import query_db
except:
    from db import query_db

def create_stores_list_table():
    query_db("DROP TABLE IF EXISTS stores_list;")
    query_db("CREATE TABLE IF NOT EXISTS stores_list(username TEXT, store_id INTEGER)")

def get_store_list_ids_user(username):
    conn = sqlite3.connect("P5.db")
    cur = conn.cursor()
    unformatted = cur.execute('SELECT store_id FROM stores_list WHERE username = ?;', (username, )).fetchall()
    conn.close()
    formatted = []
    for i in unformatted:
        formatted.append(i[0])
    return (formatted)

def add_store(username, id):
    query_db("INSERT INTO stores_list VALUES (?, ?);", (username, id))


# def get_stores_list_ids(user):
#     id_list = get_store_list_ids_user(user)
#     conn = sqlite3.connect("P5.db") 
#     curr = conn.cursor() 
#     formatted = []
#     for i in id_list:  
#         unformatted = cur.execute('SELECT retailer FROM stores WHERE id = ?;', (i, )).fetch() 
#         formatted.append(unformatted[0])
#     conn.close() 
#     return (formatted)

