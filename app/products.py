import requests
from bs4 import BeautifulSoup
import produce


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
        print(f"getting {link}")
        # get products!
        resp = s.get(f"{base_url}{link}?sort=name-asc&page=0")
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')

        results = int(soup.find(class_="js-live-pagination-n-results").attrs["data-pagination-aria-live-results"])
        pages = results // 72

        for i in range(pages + 1):
            print(f'on page {i} of {pages}')
            resp = s.get(f"{base_url}{link}?sort=name-asc&page={i}")
            html = resp.text
            soup = BeautifulSoup(html, 'html.parser')

            products = soup.find_all(class_="product")

            for product in products:
                name = product.find(class_="product__name").get_text()
                price = product.find(class_="price").get_text().split()
                image = product.img.get("src")
                url = product.find(class_="product-card-anchor no-link").get("href")
                # print(f"{name} - {price}")
                # print(price[0])
                if link == f"dept/dept-{id}-bakery" or link == f"dept/dept-{id}-pantry" or link == f"dept/dept-{id}-snacks":
                    produce.insert_duplicate(name, f"https://www.keyfood.com/{url}", image, None, price[1], price[0], "Key Food", id, "Pantry")
                if link == f"dept/dept-{id}-beverages":
                    produce.insert_duplicate(name, f"https://www.keyfood.com/{url}", image, None, price[1], price[0], "Key Food", id, "Beverages")
                if link == f"dept/dept-{id}-meatandseafood":
                    if "fillet" in name.lower() or "tuna" in name.lower() or "salmon" in name.lower() or "season - " in name.lower() or "anchovies" in name.lower() or "sardine" in name.lower() or "octopus" in name.lower() or "lobster" in name.lower() or "crab" in name.lower():
                        produce.insert_duplicate(name, f"https://www.keyfood.com/{url}", image, None, price[1], price[0], "Key Food", id, "Seafood")
                    elif "meat" in name.lower() or "turkey" in name.lower() or "pork" in name.lower() or "chicken" in name.lower() or "beef" in name.lower() or "sausage" in name.lower() or "salami" in name.lower() or "ham" in name.lower() or "bacon" in name.lower() or "lamb" in name.lower() or "veal" in name.lower() or "steak" in name.lower() or "rib" in name.lower() or "brisket" in name.lower() or "bone" in name.lower() or "wing" in name.lower():
                        produce.insert_duplicate(name, f"https://www.keyfood.com/{url}", image, None, price[1], price[0], "Key Food", id, "Meat")
                    else:
                        produce.insert_duplicate(name, f"https://www.keyfood.com/{url}", image, None, price[1], price[0], "Key Food", id, None)
                if link == f"dept/dept-{id}-produce":
                    produce.insert_duplicate(name, f"https://www.keyfood.com/{url}", image, None, price[1], price[0], "Key Food", id, "Produce")
                if link == f"dept/dept-{id}-refridgerated":
                    if "milk" in name.lower() or "yogurt" in name.lower() or "cheese" in name.lower() or "cream" in name.lower() or "butter" in name.lower() or "sour cream" in name.lower() or "egg" in name.lower() or "eggs" in name.lower() or "margarine" in name.lower() or "dannon" in name.lower() or "blue bonnet" in name.lower():
                        produce.insert_duplicate(name, f"https://www.keyfood.com/{url}", image, None, price[1], price[0], "Key Food", id, "Dairy & Eggs")
                    elif "meat" in name.lower() or "turkey" in name.lower() or "pork" in name.lower() or "chicken" in name.lower() or "beef" in name.lower() or "sausage" in name.lower() or "salami" in name.lower() or "ham" in name.lower() or "bacon" in name.lower() or "lamb" in name.lower() or "veal" in name.lower() or "steak" in name.lower() or "rib" in name.lower() or "brisket" in name.lower() or "bone" in name.lower() or "wing" in name.lower():
                        produce.insert_duplicate(name, f"https://www.keyfood.com/{url}", image, None, price[1], price[0], "Key Food", id, "Meat")
                    else:
                        produce.insert_duplicate(name, f"https://www.keyfood.com/{url}", image, None, price[1], price[0], "Key Food", id, None)
 
                
# insert_produce(produce, product_url, img_url, weight, quantity, price, store, store_id, category)
        # produce.insert_produce(name, None, image, None, None, price, "Key Food", id, None)
        # produce, product_url, img_url, weight, quantity, price, store, store_id, category):


# get_products_from_store(1472)