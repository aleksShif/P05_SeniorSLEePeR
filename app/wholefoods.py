import json
import requests

def getData():
    url = "https://www.wholefoodsmarket.com/api/products/category/all-products?store=10245&limit=60&offset=0"
    response = requests.get(url).text
    response = response[16296:]
    response = response[:-187]
    reponse = "" + response + "]"
    data = json.loads(response)
    return type(data[0])

print(getData())
