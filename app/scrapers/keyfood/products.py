import requests
from bs4 import BeautifulSoup


def get_products_from_store(id):
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

    # get products!
    html = s.get("https://keyfoodstores.keyfood.com/store/keyfoodstores/en/Departments/c/Departments?sort=name-asc&page=0").text
    soup = BeautifulSoup(html, 'html.parser')

    results = int(soup.find(class_="js-live-pagination-n-results").attrs["data-pagination-aria-live-results"])
    pages = results // 72

    for i in range(pages + 1):
        html = s.get(f"https://keyfoodstores.keyfood.com/store/keyfoodstores/en/Departments/c/Departments?sort=name-asc&page={i}").text
        soup = BeautifulSoup(html, 'html.parser')

        products = soup.find_all(class_="product")

        for product in products:
            name = product.find(class_="product__name").get_text()
            price = product.find(class_="price").get_text()
            image = product.img.get("src")


get_products_from_store(1640)