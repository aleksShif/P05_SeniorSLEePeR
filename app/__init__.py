from flask import Flask, render_template, request, session, redirect, url_for, flash, abort, jsonify
from auth import *
from cart import *
from db import * 
from produce import *
from stores_list import * 
from input_check import *
from functools import wraps
import stores
import requests
import math
import json
import stores_list

app = Flask(__name__)
app.secret_key = b'pAHy827suhda*216jdaa'

with open("app/keys/mapbox.txt") as f:
    mapbox_token = f.read().strip()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = session.get("username")
        if username is None:
            return redirect("/")
        
        if get_onboarding_val(username) != -1:
            return redirect("/onboarding")

        return f(*args, **kwargs)
    return decorated_function


categories = {
    "produce": "Produce", 
    "dairy_and_eggs": "Dairy & Eggs", 
    "meat": "Meat", 
    "pantry": "Pantry", 
    "seafood": "Seafood", 
    "beverages": "Beverages"
}

@app.route("/")
def root():
    if 'username' in session:
        return redirect(url_for("catalog"))
    return render_template("landing.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session: 
        return redirect(url_for('catalog'))
    if request.method == 'POST': 
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if check_creds(username, password):
            session['username'] = request.form['username']
            return redirect(url_for('catalog'))
        
        flash('Invalid credentials')
        return render_template('login.html')

    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session:  
        return redirect(url_for('catalog'))

    if request.method == 'POST':  
        new_user = request.form['new_username'].strip()
        new_pass = request.form['new_password']
        new_pass_confirm = request.form['new_password_confirm']

        if new_pass != new_pass_confirm:
            flash('Passwords do not match')
            return redirect(url_for("register"))

        if check_username_requirements(new_user) and check_password_requirements(new_pass) and check_username_availability(new_user):
            add_new_user(new_user, new_pass)
            session['username'] = new_user
            return redirect(url_for('catalog'))

        if not check_username_requirements(new_user):
            flash("Username has to be 4 characters or longer")

        if not check_password_requirements(new_pass):
            flash("Password has to be 4 characters or longer")

        if not check_username_availability(new_user):
            flash("Username already taken")

        return redirect(url_for("register"))

    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/user/stores")
@login_required
def user_stores():
    # TODO: CHANGE URL WHEN DEPLOYED
    username = session.get("username")
    zip = get_user_zip(username)
    
    stores = requests.get(f"http://127.0.0.1:5000/{url_for('store_search')}?zip={zip}").json()

    saved_stores = stores_list.get_stores_from_user(username)
    saved_store_ids = [store["id"] for store in saved_stores]

    stores = [store for store in stores if store["id"] not in saved_store_ids]
    stores = saved_stores + stores

    resp = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/{zip}.json?types=postcode&limit=1&access_token={mapbox_token}").json()
    zip_coords = resp["features"][0]["center"]
 
    return render_template("stores.html", stores=stores, zip=zip, zip_lon=zip_coords[0], zip_lat=zip_coords[1], logged_in=True)


@app.route("/api/all_items/<limit>/<offset>")
def get_all_category(limit, offset):
    cat = {}
    for cat in categories: 
        cat[cat] = get_all(categories[cat], limit, offset)

@app.route("/api/user/stores", methods=["GET", "POST"])
def api_user_stores():
    if "username" not in session:
        return redirect("/")

    username = session.get("username")
    if request.method == "POST":
        new_store_ids = list(request.form.keys())
    
        saved_stores = stores_list.get_stores_from_user(username)
        saved_store_ids = [store["id"] for store in saved_stores]

        for store_id in saved_store_ids:
            if store_id not in new_store_ids:
                stores_list.remove_store(username, store_id)

        for id in new_store_ids:
            stores_list.add_store(username, id)

        update_onboarding_val(username, -1)

        return redirect("/")
    
    return jsonify(stores_list.get_store_list_ids_user(username))

    
@app.route("/api/user/stores.geojson")
@login_required
def api_user_stores_geojson():
    username = session.get("username")
    stores = stores_list.get_store_list_ids_user(username)

    features = []

    for store in stores:
        feature = {
            'type': 'Feature',
            'properties': {
                'retailer': store["retailer"],
                'address': store["address"],
                'id': store["id"]
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [store["lon"], store["lat"]]
            }
        }
        features.append(feature)
        

    geojson = {
        'type': "FeatureCollection",
        'features': features
    }

    return jsonify(geojson)



@app.route("/onboarding", methods=["GET", "POST"])
def onboarding():
    if session.get("username") is None:
        return redirect("/")    

    username = session.get("username")

    if request.method == "POST":
        if request.form.get("zip", None):
            update_user_zip(username, request.form.get('zip'))
            update_onboarding_val(username, 1)

    if get_onboarding_val(username) == 0:
        # TODO: CHECK IF IT IS VALID ZIP
        return render_template("onboarding-zip.html")
    
    if get_onboarding_val(username) == 1:
        zip = get_user_zip(username)
        # TODO: CHANGE URL WHEN DEPLOYED
        stores = requests.get(f"http://127.0.0.1:5000/{url_for('store_search')}?zip={zip}").json()

        resp = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/{zip}.json?types=postcode&limit=1&access_token={mapbox_token}").json()
        zip_coords = resp["features"][0]["center"]

        return render_template("onboarding-stores.html", stores=stores, zip=zip, zip_lon=zip_coords[0], zip_lat=zip_coords[1])
    
    return redirect("catalog")

@app.route("/catalog")
@login_required
def catalog():
    suggestions = {}
    for x in categories.values():
        suggestions[x] = get_ten(x)

    print(suggestions)

    return render_template("catalog.html", logged_in=True, suggestions=suggestions, categories=categories)


@app.route("/user/account", methods=['GET', 'POST'])
@login_required
def profile():
    username = session.get("username")

    if request.method == 'POST':  
        new_pass = request.form['password']
        new_pass_confirm = request.form['confirm-password']

        if not new_pass == new_pass_confirm:
            flash('Passwords do not match')
            return redirect(url_for("profile"))

        if check_password_requirements(new_pass):
            update_user_password(username, new_pass)
            return redirect(url_for('catalog'))

        if not check_password_requirements(new_pass):
            flash("Password has to be 4 characters or longer")

        return redirect(url_for("profile"))

    return render_template("account.html", logged_in=True, username=username)



@app.route('/catalog/<category>')
@login_required
def catalog_with_category(category):
    if category not in categories.keys():
        abort(404)

    page = request.args.get('page', "1")

    return render_template("category.html", category_slug=category, category=categories[category], logged_in=True)


@app.route('/cart')
@login_required
def cart():
    return render_template("cart.html", username=session.get("username"), logged_in=True)

@app.route("/catalog/search")
@app.route("/catalog/<category>/search")
@login_required
def search(category="all"):
    return render_template("search.html", logged_in=True)


@app.route("/api/stores/search")
def store_search():
    zip = request.args.get('zip')

    resp = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/{zip}.json?types=postcode&limit=1&access_token={mapbox_token}").json()
    coords = resp["features"][0]["center"]

    store_list = stores.get_list_dict_id_address_lat_long()

    for store in store_list:
        store.update({"dist":math.dist(coords, [store["lon"], store["lat"]])})

    store_list.sort(key=lambda store: store["dist"])

    return store_list[:100]


def store_search_geojson():
    zip = request.args.get('zip')

    # TODO: CHANGE URL WHEN DEPLOYED
    stores = requests.get(f"http://127.0.0.1:5000/{url_for('store_search')}?zip={zip}").json()

    features = []

    for store in stores:
        feature = {
            'type': 'Feature',
            'properties': {
                'retailer': store["retailer"],
                'address': store["address"],
                'id': store["id"]
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [store["lon"], store["lat"]]
            }
        }
        features.append(feature)
        

    geojson = {
        'type': "FeatureCollection",
        'features': features
    }

    return jsonify(geojson)

@app.route()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Sorry, we got lost in the aisles.", logged_in="username" in session), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error_code=500, error_message="Uh oh, something went wrong.", logged_in="username" in session), 500


if __name__ == "__main__":
    app.debug = True
    app.run()