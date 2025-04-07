import json

import requests

from CONFIG.config import SITE_API_URL
from DB_GET.DataCollect import get_EAN, get_prices


def get_product_id(headers, eans_list=None):
    print("ФУНКЦИЯ ДЛЯ ПОЛУЧЕНИЯ ID")
    url = f"{SITE_API_URL}/products/get-id"
    if not eans_list:
        eans_list = get_EAN()
    data = {
        "key": "article_number",
        "value": eans_list
    }

    response = requests.get(url, headers=headers, json=data)
    ids = list(response.json()["product_id"].values())
    return ids


def get_product_price(headers, eans_list=None):
    url = f"{SITE_API_URL}/product-price/get-price"
    ids = get_product_id(headers, eans_list)
    data = {
        "value": ids
    }
    response = requests.get(url, headers=headers, json=data)
    print(json.dumps(response.json(), indent=4))
    return list(response.json()["data"].values())


def price_compare(headers, eans_list=None, prices_for_compare=None):
    if not eans_list:
        eans_list = get_EAN()
    print("Сравниваем цены")
    print(eans_list)
    prices_new = get_product_price(headers, eans_list)
    print("Получили ЦЕНЫ")
    if not prices_for_compare:
        prices_for_compare = get_prices()
    list_obj = list(zip(eans_list, prices_new, prices_for_compare))
    return list_obj