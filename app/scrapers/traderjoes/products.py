import requests


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

response = requests.post('https://www.traderjoes.com/api/graphql', json=json_data)
print(response.json()['data']['products']['items'])

