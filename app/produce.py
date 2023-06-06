import sqlite3


def create_produce_table():
    DB_FILE="produce.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create it
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    # produce table
    c.execute("CREATE TABLE IF NOT EXISTS produce(id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, product_url TEXT, img_url TEXT, weight TEXT, quantity TEXT, price FLOAT, store TEXT, store_id TEXT, category TEXT)")

    db.commit() #save changes
    db.close()  #close database


def insert_produce(produce, product_url, img_url, weight, quantity, price, store, store_id, category):
    DB_FILE="produce.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    c.execute("INSERT INTO produce(product_name, product_url, img_url, weight, quantity, price, store, store_id, category) VALUES (?,?,?,?,?,?,?,?,?)", (produce, product_url, img_url, weight, quantity, price, store, store_id, category))
    
    #prints table
    # table = c.execute("SELECT * from produce")
    # print("user table from add_user() call")
    # print(table.fetchall())

    db.commit() #save changes
    db.close()  #close database

def display_produce():

    DB_FILE="produce.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    table = c.execute("SELECT * from produce")
    # print("user table from add_user() call")
    print(table.fetchall())

    db.commit() #save changes
    db.close()  #close database

