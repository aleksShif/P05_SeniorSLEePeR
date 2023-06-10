import auth
import produce
import stores_list
import stores

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



