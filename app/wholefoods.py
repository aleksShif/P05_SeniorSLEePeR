import json
import requests
import produce
import sqlite3

categories = ["Beverages", "wine-beer-spirits"]
def getData():
    for food in categories:
        x = 0
        while x < 939: 
            url = f"https://www.wholefoodsmarket.com/api/products/category/{food}?store=10245&limit=60&offset={x}"
            response = requests.get(url).json()
            response = response["results"]
            if food == "Produce"  or food == "Meat" or food == "Seafood" or food == "Beverages":
                populate_db(response, food)
            elif food == "dairy-eggs":
                populate_db(response, "Dairy & Eggs")
            elif food == "pantry-essentials" or food == "breads-rolls-bakery" or food == "supplements" or food == "snacks-chips-salsas-dips":
                populate_db(response, "Pantry")
            elif food == "wine-beer-spirits":
                populate_db(response, "Beverages")
            x += 60
        


def populate_db(data, category):
    for x in data:
        if 'imageThumbnail' in x:
            produce.insert_produce(x['name'],"https://www.wholefoodsmarket.com/product/" + x['slug'], x['imageThumbnail'], None , None,  x['regularPrice'], "Wholefoods", x['store'], category)
        else:
            produce.insert_produce(x['name'],"https://www.wholefoodsmarket.com/product/" + x['slug'], None, None , None,  x['regularPrice'], "Wholefoods", x['store'], category)

produce.create_produce_table()
getData()
produce.display_produce()
# print(getData())


