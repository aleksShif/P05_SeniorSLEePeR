import json
import requests
import produce
import sqlite3

def getData():
    url = "https://www.wholefoodsmarket.com/api/products/category/all-products?store=10245&limit=60&offset=939"
    response = requests.get(url).json()
    response = response["results"]
    return response

def populate_db():
    data = getData()
    for x in data:
        produce.insert_produce(x['name'],"https://www.wholefoodsmarket.com/product/" + x['slug'], x['imageThumbnail'], None , None,  x['regularPrice'], "Wholefoods", x['store'], None)

produce.create_produce_table()
populate_db()
produce.display_produce()
# print(getData())


