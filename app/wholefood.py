import json
import requests

def get_data():
    data = requests.get("https://www.wholefoodsmarket.com/api/products/category/[leafCategory]?leafCategory=all-products&store=10245&limit=60&offset=0").text
    # data = json.loads(data)
    print(data)
    # data = data[16216:]

    # print(data)
    # return data

# print(get_data())
get_data()