import requests
import json
import sqlite3

try:
    from db import query_db
except:
    from db import query_db
from playwright.sync_api import sync_playwright

def get_stores_near_zip_wfm(zip):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("https://www.wholefoodsmarket.com/stores")
        
        with page.expect_response("https://www.wholefoodsmarket.com/stores/search") as response:
            search_bar = page.query_selector("#store-finder-search-bar")
            search_bar.fill(f"{zip}")
            search_bar.press('Enter')

        response = response.value
        return response.json()

def get_stores_near_zip_kf(zip):
    response = requests.get(f"https://keyfoodstores.keyfood.com/store/keyFood/en/store-locator?q={zip}&page=0&radius=20&all=false")
    return response.json()

def create_stores_table():
    query_db("DROP TABLE IF EXISTS stores;")
    query_db("CREATE TABLE IF NOT EXISTS stores(id INTEGER PRIMARY KEY AUTOINCREMENT, retailer TEXT, retailer_id INT, lon FLOAT, lat FLOAT, address TEXT)")

def add_keyfood_data(zip): 
    dict = get_stores_near_zip_kf(zip)
    stores_list = dict.get("data")
    for store in stores_list: 
        
        query_db("INSERT INTO stores(retailer, retailer_id, lon, lat, address) VALUES (?,?,?,?,?)", (store.get("displayName"), store.get("name"), store.get("longitude"), store.get("latitude"), store.get("line1")))

def add_wfm_data(zip):
    list = get_stores_near_zip_wfm(zip)
    #print(dict)
    for dict in list:
        #print(dict)
        query_db("INSERT INTO stores(retailer, retailer_id, lon, lat, address) VALUES (?,?,?,?,?)", ("Whole Foods Market", dict.get("storeId"), dict.get("location").get("geometry").get("coordinates")[1], dict.get("location").get("geometry").get("coordinates")[0], dict.get("location").get("address").get("line1")))
        

def add_all_stores(zip): 
    create_stores_table()
    add_keyfood_data(zip)
    add_wfm_data(zip)

def get_list_store_ids():
    conn = sqlite3.connect("P5.db")
    cur = conn.cursor()
    unformatted = cur.execute("SELECT id FROM stores").fetchall()
    conn.close()
    formatted = []
    for i in unformatted:
        formatted.append(i[0])
    return formatted

def get_list_dict_id_address_lat_long():
    ids = get_list_store_ids()
    print(ids)
    list = []
    for id in ids: 
        retailer = query_db("SELECT retailer FROM stores WHERE id = ?",(id,))
        lat = query_db("SELECT lat FROM stores WHERE id = ?",(id,))
        lon = query_db("SELECT lon FROM stores WHERE id = ?",(id,))
        address = query_db("SELECT address FROM stores WHERE id = ?",(id,))
        dict = {
            "id": id, 
            "retailer": retailer,
            "lat": lat,
            "lon": lon
        }
        list.append(dict)
    return list


if __name__ == "__main__":
    #print(get_stores_near_zip_kf(10001))
    #print(get_stores_near_zip_wfm(10001))
    add_all_stores(10001)
    print(get_list_dict_id_address_lat_long())
