import sqlite3


def create_produce_table():
    DB_FILE="P5.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create it
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    # produce table
    c.execute("CREATE TABLE IF NOT EXISTS produce(id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, img_url TEXT, weight FLOAT, price FLOAT, store_name TEXT, store_loc TEXT)")

    db.commit() #save changes
    db.close()  #close database


def insert_produce(produce, img_url, weight, price, store, store_loc):
    DB_FILE="P5.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    c.execute("INSERT INTO produce(product_name, img_url, weight, price, store_name, store_loc) VALUES (?,?,?,?,?,?)", (produce, img_url, weight, price, store, store_loc))
    
    #prints table
    table = c.execute("SELECT * from produce")
    print("user table from add_user() call")
    print(table.fetchall())

    db.commit() #save changes
    db.close()  #close database

def display_produce():

    DB_FILE="P5.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    table = c.execute("SELECT * from produce")
    print("user table from add_user() call")
    print(table.fetchall())

    db.commit() #save changes
    db.close()  #close database

