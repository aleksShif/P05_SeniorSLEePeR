import sqlite3
try:
    from db import query_db
except:
    from db import query_db

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
    for img in imgs: 
        return query_db('SELECT img_url FROM produce WHERE id = ?;', (id, ))[0]
    return imgs 

def get_total_price(username):
    ids = get_list_ids_user(username)
    running_tot = 0
    for id in ids: 
       tup = get_list_tuples_itemprice_quantity_totalprice(username,id)
       running_tot += tup[2]
    return running_tot
 
