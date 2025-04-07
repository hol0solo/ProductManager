import asyncio
import json

from CONFIG.config import SITE_API_URL
from DB_GET.DataCollect import get_ean, get_prices


async def get_product_id(session, headers, eans_list=None):
    print("ФУНКЦИЯ ДЛЯ ПОЛУЧЕНИЯ ID")
    url = f"{SITE_API_URL}/products/get-id"
    if not eans_list:
        eans_list = await asyncio.to_thread(get_ean)
    data = {
        "key": "article_number",
        "value": eans_list
    }

    async with session.get(url, headers=headers, json=data) as response:
        response_json = await response.json()
        ids = list(response_json["product_id"].values())
        return ids


async def get_product_price(session, headers, eans_list=None):
    url = f"{SITE_API_URL}/product-price/get-price"
    ids = await get_product_id(session, headers, eans_list)
    data = {
        "value": ids
    }
    async with session.get(url, headers=headers, json=data) as response:
        response_json = await response.json()
        print(json.dumps(response_json, indent=4))
        return list(response_json["data"].values())


async def price_compare(session, headers, eans_list=None, prices_for_compare=None):
    if not eans_list:
        eans_list = await asyncio.to_thread(get_ean)
    print("Сравниваем цены")
    print(eans_list)
    prices_new = await get_product_price(session, headers, eans_list)
    print("Получили ЦЕНЫ")
    if not prices_for_compare:
        prices_for_compare = await asyncio.to_thread(get_prices)
    list_obj = list(zip(eans_list, prices_new, prices_for_compare))
    return list_obj


async def get_product_links(session, headers, ids):
    url = f"{SITE_API_URL}/product-content/get-url"
    data = {
        "language": "de",
        "ids": ids,
    }
    async with session.get(url, headers=headers, json=data) as response:
        response_json = await response.json()
        links = list(response_json["data"].values())
        links_full = [f"https://www.jvfurniture.co.uk/{link}" for link in links]
        return links_full