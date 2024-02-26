import requests
import config

if config.use_mock():
    url_base = "http://127.0.0.1:5000"
else:
    url_base = "https://api.element.market"
url_api = "/openapi/v1/collection"
url_stats = "/stats?collection_slug="
headers = {"accept": "application/json"}


def get_collection_data(collection_name):
    url = f'{url_base}{url_api}{url_stats}{collection_name}'
    response = requests.get(url, headers=headers)
    return response
