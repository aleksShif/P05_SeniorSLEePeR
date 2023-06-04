from playwright.sync_api import sync_playwright

def get_stores_near_zip(zip):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("https://www.wholefoodsmarket.com/stores")
        
        with page.expect_response("https://www.wholefoodsmarket.com/stores/search") as response:
            search_bar = page.query_selector("#store-finder-search-bar")
            search_bar.fill(f"{zip}")
            search_bar.press('Enter')

        response = response.value
        return response.json()


if __name__ == "__main__":
    print(get_stores_near_zip(10001))