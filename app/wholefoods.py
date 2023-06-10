import json
import requests
import produce
import sqlite3

categories = ["produce", "dairy-eggs", "meat", "pantry-essentials", "breads-rolls-bakery", "supplements", "seafood", "beverages", "wine-beer-spirits"]
def get_store_products(store_id):
    for food in categories:
        print(f"getting {food}")
        x = 0

        # getting pages
        url = f"https://www.wholefoodsmarket.com/api/products/category/{food}?store={store_id}&limit=60&offset={x}"
        response = requests.get(url).json()

        # NOTE: not sure if this is correct but wtv!
        pages = (response["meta"]["total"]["value"] + 1) // 60

        while x <= pages: 
            print(f"on page {x} of {pages}")
            url = f"https://www.wholefoodsmarket.com/api/products/category/{food}?store={store_id}&limit=60&offset={x}"
            response = requests.get(url).json()
            response = response["results"]
            if food == "produce"  or food == "meat" or food == "seafood" or food == "beverages":
                populate_db(response, food.capitalize())
            elif food == "dairy-eggs":
                populate_db(response, "Dairy & Eggs")
            elif food == "pantry-essentials" or food == "breads-rolls-bakery" or food == "supplements" or food == "snacks-chips-salsas-dips":
                populate_db(response, "Pantry")
            elif food == "wine-beer-spirits":
                populate_db(response, "Beverages")
            x += 1
        


def populate_db(data, category):
    for x in data:
        if 'imageThumbnail' in x:
            produce.insert_produce(x['name'],"https://www.wholefoodsmarket.com/product/" + x['slug'], x['imageThumbnail'], None , None,  x['regularPrice'], "Wholefoods", x['store'], category)
        else:
            produce.insert_produce(x['name'],"https://www.wholefoodsmarket.com/product/" + x['slug'], None, None , None,  x['regularPrice'], "Wholefoods", x['store'], category)

if __name__ == "__main__":
    produce.create_produce_table()
    get_store_products(10245)
    produce.display_produce()
# print(getData())


