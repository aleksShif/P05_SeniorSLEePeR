import auth
import produce
import stores_list
import stores
import wholefoods
import products

zips = {
    "brooklyn": "11226",
    "the bronx": "10460",
    "manhattan": "10001",
    "staten island": "10314",
    "queens": "11367",
}

print("creating database tables...", end=" ", flush=True)
auth.create_users_cart_table()
stores_list.create_stores_list_table()
produce.create_produce_table()
print("done")


for borough, zip in zips.items():
    print(f"adding stores in {borough}")
    stores.add_all_stores(zip)
    print("done")

_stores = stores.get_list_dict_id_address_lat_long()

for store in _stores:
    print(f"getting data from: {store}")
    if store["retailer"] == "Whole Foods Market":
        wholefoods.get_store_products(store["retailer_id"])
    elif store["retailer"] == "Trader Joe's":
        pass
    else:
        products.get_products_from_store(store["retailer_id"])

        
        

