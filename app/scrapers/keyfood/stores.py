import requests

def get_stores_near_zip(zip):
    response = requests.get(f"https://keyfoodstores.keyfood.com/store/keyFood/en/store-locator?q={zip}&page=0&radius=20&all=false")
    return response.json()


if __name__ == "__main__":
    print(get_stores_near_zip(10001))