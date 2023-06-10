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
            page.wait_for_load_state('networkidle')
            search_bar = page.query_selector("#store-finder-search-bar")
            search_bar.fill(f"{zip}")
            search_bar.press('Enter')

        response = response.value
        return response.json()

def get_stores_near_zip_kf(zip):
    response = requests.get(f"https://keyfoodstores.keyfood.com/store/keyFood/en/store-locator?q={zip}&page=0&radius=20&all=false")
    return response.json()

def get_stores_near_zip_tj(zip):
    json_data = {
        'request': {
            'appkey': '8559C922-54E3-11E7-8321-40B4F48ECC77',
            'formdata': {
                'geoip': False,
                'dataview': 'store_default',
                'limit': 30,
                'geolocs': {
                    'geoloc': [
                        {
                            'country': 'US',
                            'postalcode': f'{zip}',
                        },
                    ],
                },
                'searchradius': '3000',
                'where': {
                    'or': {
                        'wine': {
                            'eq': '',
                        },
                        'beer': {
                            'eq': '',
                        },
                        'liquor': {
                            'eq': '',
                        },
                        'comingsoon': {
                            'eq': '',
                        },
                    },
                    'name': {
                        'distinctfrom': 'World Class Distribution',
                    },
                },
                'false': '0',
            },
        },
    }

    response = requests.post(
        'https://hosted.where2getit.com/traderjoes/rest/locatorsearch',
        json=json_data,
    )


    return response.json()

def create_stores_table():
    # UNIQUE -> https://stackoverflow.com/questions/19337029/insert-if-not-exists-statement-in-sqlite
    query_db("CREATE TABLE IF NOT EXISTS stores(id INTEGER PRIMARY KEY, retailer TEXT, retailer_id INT, lon FLOAT, lat FLOAT, address TEXT UNIQUE, line2 TEXT, img_url TEXT)")

def add_keyfood_data(zip): 
    dict = get_stores_near_zip_kf(zip)
    stores_list = dict.get("data")
    print(f"{len(stores_list)} Key Foods found near {zip}")
    for store in stores_list: 
        query_db("INSERT OR IGNORE INTO stores(retailer, retailer_id, lon, lat, address, line2, img_url) VALUES (?,?,?,?,?, ?, NULL)", (store.get("displayName"), store.get("name"), store.get("longitude"), store.get("latitude"), store.get("line1"), store.get("town") + ", " + store.get("state") + " " + store.get("postalCode")))

def add_wfm_data(zip):
    list = get_stores_near_zip_wfm(zip)
    print(f"{len(list)} Whole Foods found near {zip}")
    #print(dict)
    for dict in list:
        #print(dict)
        query_db("INSERT OR IGNORE INTO stores(retailer, retailer_id, lon, lat, address, line2, img_url) VALUES (?,?,?,?,?, ?, NULL)", ("Whole Foods Market", dict.get("storeId"), dict.get("location").get("geometry").get("coordinates")[0], dict.get("location").get("geometry").get("coordinates")[1], dict.get("location").get("address").get("line1"), dict.get("location").get("address").get("city") + ", " + dict.get("location").get("address").get("state") + " " + dict.get("location").get("address").get("postalCode")))
        
def add_tj_data(zip): 
    dict = get_stores_near_zip_tj(zip)
    stores_list = dict.get("response").get("collection")
    print(f"{len(stores_list)} Trader Joe's found near {zip}")
    for store in stores_list:
        query_db("INSERT OR IGNORE INTO stores(retailer, retailer_id, lon, lat, address, line2, img_url) VALUES (?,?,?,?,?, ?, NULL)", ("Trader Joe's", store.get("clientkey"), store.get("longitude"), store.get("latitude"), store.get("address1"), store.get("city") + ", " + store.get("state") + " " + store.get("postalcode")))

def add_all_stores(zip): 
    create_stores_table()
    add_keyfood_data(zip)
    add_wfm_data(zip)
    add_tj_data(zip)

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
    # print(ids)
    list = []
    for id in ids: 
        retailer, lat, lon, address = query_db("SELECT retailer, lat, lon, address FROM stores WHERE id = ?",(id,))
        # lat = query_db("SELECT lat FROM stores WHERE id = ?",(id,))[0]
        # lon = query_db("SELECT lon FROM stores WHERE id = ?",(id,))[0]
        # address = query_db("SELECT address FROM stores WHERE id = ?",(id,))[0]
        dict = {
            "id": id, 
            "retailer": retailer,
            "lat": lat,
            "lon": lon,
            "address": address
        }
        list.append(dict)
    return list


if __name__ == "__main__":
    #print(get_stores_near_zip_kf(10001))
    #print(get_stores_near_zip_wfm(10001))
    # add_all_stores(10282)
    add_all_stores(10001)
    print(get_list_dict_id_address_lat_long())
