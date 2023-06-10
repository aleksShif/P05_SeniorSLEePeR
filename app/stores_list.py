# create table
# add store, user
# get list all stores per user 
import sqlite3
try:
    from db import query_db
except:
    from db import query_db

def create_stores_list_table():
    # query_db("DROP TABLE IF EXISTS stores_list;")
    query_db("CREATE TABLE IF NOT EXISTS stores_list(username TEXT, store_id INTEGER)")

def get_stores_from_user(username):
    res = query_db('SELECT stores_list.store_id, stores.retailer, stores.retailer_id, stores.lon, stores.lat, stores.address FROM stores_list JOIN stores ON stores.id=stores_list.store_id WHERE stores_list.username = ?;', (username, ), all=True)
    stores = []
    for store in res:
        d = {
            "id": store[0],
            "retailer": store[1],
            "retailer_id": store[2],
            "lon": store[3],
            "lat": store[4],
            "address": store[5],
            "saved": True,
        }
        stores.append(d)

    return stores

def add_store(username, id):
    if query_db("SELECT * FROM stores_list WHERE username == ? AND store_id == ?", (username, id)) is None:
        query_db("INSERT INTO stores_list VALUES (?, ?);", (username, id))

    return

def remove_store(username, id):
    query_db("DELETE FROM stores_list WHERE username == ? AND store_id == ?;", (username, id))



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

