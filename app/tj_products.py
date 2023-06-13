import requests
import string
import produce


def do_the_thing():
  graphql_query = """query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String = "539", $availability: String = "1", $published: String = "1") {
    products(
      filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}, category_id: {eq: $categoryId}}
      currentPage: $currentPage
      pageSize: $pageSize
    ) {
      items {
        sku
        item_title
        category_hierarchy {
          id
          name
          __typename
        }
        primary_image
        primary_image_meta {
          url
          metadata
          __typename
        }
        sales_size
        sales_uom_description
        price_range {
          minimum_price {
            final_price {
              currency
              value
              __typename
            }
            __typename
          }
          __typename
        }
        retail_price
        fun_tags
        item_characteristics
        __typename
      }
      total_count
      pageInfo: page_info {
        currentPage: current_page
        totalPages: total_pages
        __typename
      }
      aggregations {
        attribute_code
        label
        count
        options {
          label
          value
          count
          __typename
        }
        __typename
      }
      __typename
    }
  }"""

  json_data = {
      'operationName': 'SearchProducts',
      'variables': {
          'storeCode': '539',
          'availability': '1',
          'published': '1',
          'categoryId': 2,
          # TODO: INCREMENT THIS UNTIL 54?
          'currentPage': 1,
          'pageSize': 15,
      },
      'query': graphql_query
  }

  punc = string.punctuation[0:5] + string.punctuation[6:]
  product_base_url = "https://www.traderjoes.com/home/products/pdp/"
  img_base_url = "https://www.traderjoes.com"

  # produce.create_produce_table()
  pages = json_data['variables']['pageSize']
  print(pages)
  for x in range(1,55):
      json_data['variables']['currentPage'] = x
      print("\n\n\n************** current page is " + str(x) + " **************")
      response = requests.post('https://www.traderjoes.com/api/graphql', json=json_data)

      for x in response.json()['data']['products']['items']:
          if len(x['category_hierarchy']) > 2:
            if x['category_hierarchy'][1]['name'] == "Food"  or x['category_hierarchy'][1]['name'] == "Beverages":
              name = x['item_title']
              name_url_comp = name.split(" ")
              name_url = ""
              for i in range(len(name_url_comp)):
                  name_url_comp[i] = name_url_comp[i].strip(punc)
                  name_url = name_url + name_url_comp[i] + "-"
              name_url = name_url[:-1]
              product_url = product_base_url + name_url + "-" + str(x['sku'])
              img_url = img_base_url + x['primary_image_meta']['url']
              # print(img_url)
              weight = str(x['sales_size']) + " " + x['sales_uom_description']
              quantity = 1
              price = str(x['price_range']['minimum_price']['final_price']['value'])
              store = "Trader Joe's"
              #CHANGE THIS
              store_id = 539
              category = None
              # print(x['category_hierarchy'])
              if x['category_hierarchy'][1]['name'] == "Beverages":
                  category = "Beverages"
              elif x['category_hierarchy'][2]['name'] == "For the Pantry" or x['category_hierarchy'][2]['name'] == "Snacks & Sweets" or x['category_hierarchy'][2]['name'] == "Dips, Sauces & Dressings" or  x['category_hierarchy'][2]['name'] == "Bakery":
                  category = "Pantry"
              elif  "dairy" in x['category_hierarchy'][2]['name']  or  x['category_hierarchy'][2]['name'] == "Cheese":
                  category = "Dairy & Eggs"
              elif x['category_hierarchy'][2]['name'] == "Fresh Fruits & Veggies":
                  category = "Produce"
              # print(name)
              produce.insert_duplicate(name, product_url, img_url, weight, quantity, price, store, store_id, category)
            # produce.display_produce()
          # else:
          #     print( " \n\n\n\n\n\n\n\n************************" )
          #     print(x['category_hierarchy'])
  # print("====================================")
  # print(response.json())


  # insert_duplicate(produce, 
  #                  product_url, 
  #                  img_url, 
  #                  weight, 
  #                  quantity, 
  #                  price, 
  #                  store, 
  #                  store_id, 
  #                  category)