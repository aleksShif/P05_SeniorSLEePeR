import sqlite3

categories = {
    "produce": "Produce", 
    "dairy_and_eggs": "Dairy & Eggs", 
    "meat": "Meat", 
    "pantry": "Pantry", 
    "seafood": "Seafood", 
    "beverages": "Beverages"
}

def create_produce_table():
    DB_FILE="P5.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create it
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    # produce table
    c.execute("CREATE TABLE IF NOT EXISTS produce(id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, product_url TEXT, img_url TEXT, weight TEXT, quantity TEXT, price FLOAT, store TEXT, store_id TEXT, category TEXT)")

    db.commit() #save changes
    db.close()  #close database


def insert_produce(produce, product_url, img_url, weight, quantity, price, store, store_id, category):
    DB_FILE="P5.db"

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

    DB_FILE="P5.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    table = c.execute("SELECT * from produce")
    # print("user table from add_user() call")
    print(table.fetchall())

    db.commit() #save changes
    db.close()  #close database

def check_duplicate(name, store):
    DB_FILE="P5.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    table = c.execute("SELECT * from produce WHERE product_name = ? AND store = ? ", (name, store))

    # print(table.fetchall())
    if table.fetchall() == []:
        db.commit() #save changes
        db.close() 
        # print("duplicate not found")
        return False
    else:
        # print("duplicate found")
        db.commit() #save changes
        db.close() 
        return True
    
def update_duplicate_cat(name, category):
    DB_FILE="P5.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    cat = c.execute("SELECT category from produce WHERE product_name = ?", (name,)).fetchall()
    if cat[0][0] == None:
        return False
    c.execute("UPDATE produce SET category = ? WHERE product_name = ? AND category = ?", (cat + "," + category, name, cat))
   
    db.commit() #save changes
    db.close()  #close database

def check_category(name, store, category):
    DB_FILE="P5.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    table = c.execute("SELECT category from produce WHERE product_name = ? AND store = ?", (name, store)).fetchall()[0][0]

    # print(table)
    # print(table.fetchall())
    # print(table.fetchall()[0][0])
    if table == None:
        # print("no category found")
        db.commit() #save changes
        db.close() 
        return False
    table = table.split(",")
   
    if category in table:
        db.commit() #save changes
        db.close() 
        # print(x[0])
        # print("duplicate found in category")
        return True
    else:
        db.commit() #save changes
        db.close() 
        # print("no duplicate found in category")
        return False

def insert_duplicate(produce, product_url, img_url, weight, quantity, price, store, store_id, category):
    try:
        if check_duplicate(produce, store) and not check_category(produce, store, category):
            update_duplicate_cat(produce, category)
            # print("insert cat")
        elif not check_duplicate(produce, store) :
            # print("insert new")
            insert_produce(produce, product_url, img_url, weight, quantity, price, store, store_id, category)
    except:
        print("oopsies!")
        pass
#     elif check_duplicate(produce, store) and check_category(produce, store, category):
#         print("duplicate found!!")
# create_produce_table()
# insert_produce("apple", None, None, None, None, None, "wholefoods", None, "fruit")
# display_produce()
# insert_duplicate("apple", None, None, None, None, None, "wholefoods", None, "refrigerated")
# display_produce()

def get_ten(category):
    DB_FILE="P5.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    return c.execute("SELECT * from produce WHERE category = ?  ORDER BY RANDOM() LIMIT 10", (category,)).fetchall()

def get_category(category, limit, offset):
    DB_FILE="P5.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    cat = c.execute("SELECT * from produce WHERE category = ? LIMIT ? OFFSET ?;", (category,limit,offset)).fetchall()
    return cat

def get_all(limit, offset):
    DB_FILE="P5.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    cat = c.execute("SELECT * from produce LIMIT ? OFFSET ?;", (limit,offset)).fetchall()
    return cat
