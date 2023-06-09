import sqlite3
try:
    from db import query_db
except:
    from db import query_db

def add_new_item(username, item_id, quantity):
    query_db("INSERT INTO cart(username, id) VALUES (?, ?, ?);", (username, item_id, quantity))
# NOT TESTED

# CART ITSELF
def get_list_ids_user(username):
    conn = sqlite3.connect("P5.db")
    cur = conn.cursor()
    unformatted = cur.execute('SELECT id FROM cart WHERE username = ?;', (username, )).fetchall()
    conn.close()
    formatted = []
    for i in unformatted:
        formatted.append(i[0])
    return (formatted)

def get_list_product_names(username):
    ids = get_list_ids_user(username)
    names = []
    for id in ids: 
        names.append(query_db('SELECT product_name FROM produce WHERE id = ?;', (id, ))[0])
    return names 

def get_list_tuples_itemprice_quantity_totalprice(username):
    ids = get_list_ids_user(username)
    prices = []
    for id in ids: 
        price = query_db('SELECT price FROM produce WHERE id = ?;', (id, ))[0]
        quantity = query_db('SELECT quantity FROM care WHERE id = ? AND username = ?;', (id, ))[0]
        prices.append(price, quantity, price * quantity)
    return prices

def get_list_product_imgs(username):
    ids = get_list_ids_user(username)
    imgs = []
    for id in ids: 
        imgs.append(query_db('SELECT img_url FROM produce WHERE id = ?;', (id, ))[0])
    return imgs 

# forgot, add later
# def updateQuantity()

# CART SUMMARY

def get_list_store_names(username):
    ids = get_list_ids_user(username)
    stores = []
    for id in ids: 
        store_id = query_db('SELECT store_id FROM produce WHERE id = ?;', (id, ))[0]
        store_name = query_db('SELECT retailer FROM stores WHERE id = ?;', (store_id, ))[0]
        stores.append(store_name)
    return stores

def get_list_store_ids(username):
    ids = get_list_ids_user(username)
    stores = []
    for id in ids: 
        stores.append(query_db('SELECT store_id FROM produce WHERE id = ?;', (id, ))[0])
    return stores

def get_total_price(username):
    ids = get_list_ids_user(username)
    running_tot = 0
    for id in ids: 
       tup = get_list_tuples_itemprice_quantity_totalprice(username,id)
       running_tot += tup[2]
    return running_tot

# return {store name: number of items, ...}
'''
def get_store_numitems(username): 
    
    ids = get_list_ids_user(username)
    names = []
    num_items = []
    dict = {}

    for id in ids: 
        names.append(query_db('SELECT store_name FROM produce WHERE id = ?;', (id, ))[0])

    for store in names: 
        num_items.append(names.count(store))
    
    for key in names:
        if key not in names.keys():
            for value in num_items:
                dict[key] = value
    
    return dict
    '''
    
def get_num_unique_stores(username): 
    store_ids = get_list_store_ids(username)
    num_unique = len(set(store_ids))
    return num_unique

'''
def get_num_items_names_store
'''