import requests
import json
try:
    from app.db import query_db
except:
    from app.db import query_db

def get_stores_near_zip(zip):
    response = requests.get(f"https://keyfoodstores.keyfood.com/store/keyFood/en/store-locator?q={zip}&page=0&radius=20&all=false")
    return response.json()

def create_stores_table():
    query_db("CREATE TABLE IF NOT EXISTS stores(id INTEGER PRIMARY KEY AUTOINCREMENT, retailer TEXT, retailer_id INT, lon FLOAT, lat FLOAT, address TEXT)")

def add_keyfood_data(zip): 
    dict = get_stores_near_zip(zip)
    stores_list = dict.get("data")
    create_stores_table()
    for store in stores_list: 
        query_db("INSERT INTO stores(retailer, retailer_id, lon, lat, address) VALUES (?,?,?,?,?)", (store.get("display name"), store.get("name"), store.get("longitude"), store.get("latitude"), store.get("line1")))
    return list

if __name__ == "__main__":
    print(get_stores_near_zip(10001))
    add_keyfood_data(10001)