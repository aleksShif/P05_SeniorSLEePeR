import requests


def get_stores_near_zip(zip):
    json_data = {
        'request': {
            'appkey': '8559C922-54E3-11E7-8321-40B4F48ECC77',
            'formdata': {
                'geoip': False,
                'dataview': 'store_default',
                'limit': 30,
                'geolocs': {
                    'geoloc': [
                        {
                            'country': 'US',
                            'postalcode': f'{zip}',
                        },
                    ],
                },
                'searchradius': '3000',
                'where': {
                    'or': {
                        'wine': {
                            'eq': '',
                        },
                        'beer': {
                            'eq': '',
                        },
                        'liquor': {
                            'eq': '',
                        },
                        'comingsoon': {
                            'eq': '',
                        },
                    },
                    'name': {
                        'distinctfrom': 'World Class Distribution',
                    },
                },
                'false': '0',
            },
        },
    }

    response = requests.post(
        'https://hosted.where2getit.com/traderjoes/rest/locatorsearch',
        json=json_data,
    )


    return response.json()

if __name__ == "__main__":
    print(get_stores_near_zip(10001))