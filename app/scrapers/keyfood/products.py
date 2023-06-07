import requests
from bs4 import BeautifulSoup



def get_products_from_store(id):
    links_to_scrape = [f"dept/dept-{id}-bakery",  f"dept/dept-{id}-beverages", f"dept/dept-{id}-deli", f"dept/dept-{id}-meatandseafood", f"dept/dept-{id}-pantry", f"dept/dept-{id}-produce", f"dept/dept-{id}-refridgerated", f"dept/dept-{id}-snacks"]
    base_url = "https://keyfoodstores.keyfood.com/store/keyFood/en/c/"


    s = requests.Session()

    # get csrf token
    response = s.get("https://keyfoodstores.keyfood.com/store/keyFood/en/store-locator?query=10282&radius=20&services=").text
    csrf_loc = response.find("CSRFToken = '") + len("CSRFToken = '")
    crsf = response[csrf_loc:csrf_loc+36]

    data = {
        'storeName': id,
        'product': '',
        'shoppingList': '',
        'CSRFToken': crsf,
    } 

    # set csrf token
    s.post("https://keyfoodstores.keyfood.com/store/keyFood/en/store-locator/session-store", data=data)

    # set store
    s.get("https://keyfoodstores.keyfood.com/store/keyFood/en/store-locator/get-session-store")


    for link in links_to_scrape:
        # get products!
        resp = s.get(f"{base_url}{link}?sort=name-asc&page=0")
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')

        results = int(soup.find(class_="js-live-pagination-n-results").attrs["data-pagination-aria-live-results"])
        pages = results // 72

        for i in range(pages + 1):
            resp = s.get(f"{base_url}{link}?sort=name-asc&page={i}")
            html = resp.text
            soup = BeautifulSoup(html, 'html.parser')

            products = soup.find_all(class_="product")

            for product in products:
                name = product.find(class_="product__name").get_text()
                price = product.find(class_="price").get_text()
                image = product.img.get("src")
                print(f"{name} - {price}")

        # produce.insert_produce(name, None, image, None, None, price, "Key Food", id, None)
        # produce, product_url, img_url, weight, quantity, price, store, store_id, category):


get_products_from_store(1472)