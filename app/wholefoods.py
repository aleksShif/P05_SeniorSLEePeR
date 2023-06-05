import json
import requests
import produce
import sqlite3

def getData():
    url = "https://www.wholefoodsmarket.com/api/products/category/all-products?store=10245&limit=60&offset=0"
    response = requests.get(url).text
    response = response[16296:]
    response = response[:-187]
    data = json.loads(response)
    return data

def populate_db():
    data = getData()
    for x in data:
        produce.insert_produce(x['name'], x['imageThumbnail'], None , x['regularPrice'], "Wholefoods", x['store'])

produce.create_produce_table()
populate_db()
produce.display_produce()



