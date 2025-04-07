import aiohttp
import asyncio
import json

from CONFIG.config import SITE_API_URL, BEARER_TOKEN, SITE_DB_NAME


async def post_request(session, url, headers, data):
    ''' Делаем асинхронный ПОСТ запрос для API на PHP '''
    try:
        async with session.post(url, headers=headers, json=data) as response:
            json_response = await response.json()
            print(json.dumps(json_response, indent=4))
            return json_response
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе к {url}: {e}")
        raise


async def post_product_id(session, headers, ean, manufacturer, url_key):
    ''' ПОСТ запрос для создания Artikel_id '''
    data = {
        "is_search_indexed": 0,
        "subsequent_article": 0,
        "tax_id": 3,
        "package_unit": 1,
        "suggested_price": 0,
        "is_live_shopping_active": 1,
        "is_inactive": 0,
        "updated_by": "API",
        "article_number": url_key,
        "base_unit": 0,
        "manufacturer": manufacturer,
        "ean": ean,
        "url_key": url_key,
        "live_shopping_discount": 0,
        "has_fixed_bundle_price": 0,
        "is_bundle_configurable": 0
    }
    url = f"{SITE_API_URL}/product"
    response = await post_request(session, url, headers, data)
    return response["data"]["article_id"]


async def post_product_price(session, id, price, headers):
    ''' ПОСТ запрос для создания ЦЕНЫ '''
    data = {
        "article_id": id,
        "price": price,
        "price_basis": "brutto",
        "filter": "default",
        "currency": "GBP"
    }
    url = f"{SITE_API_URL}/product-price"
    await post_request(session, url, headers, data)


async def post_product_content(session, id, headers, title, url_key, search_field):
    ''' ПОСТ запрос для создания КОНТЕНТА '''
    data = {
        "article_id": id,
        "language": "de",
        "title": f"{title}",
        "url_key": f"{url_key}",
        "search_field": search_field
    }
    url = f"{SITE_API_URL}/product-content"
    await post_request(session, url, headers, data)


async def post_product_category(session, id, headers, category_code, category_id):
    ''' Пост запрос для создания КАТЕГОРИИ '''
    print(category_code)
    print(type(category_code))
    print(category_id)
    print(type(category_id))
    data = {
        "article_id": id,
        "category_code": category_code,
        "category_id": category_id,
        "sort_order": 2,
    }
    url = f"{SITE_API_URL}/product-category"
    await post_request(session, url, headers, data)


async def post_product_stock(session, id, headers, stock_current, stock_min):
    data = {
        "article_id": id,
        "stock": stock_current,
        "min_stock": stock_min,
        "ignore_stock":1,
        "storage_location":"default"
    }
    url = f"{SITE_API_URL}/product-stock"
    await post_request(session, url, headers, data)


async def post_product_supplier_info(session, id, headers):
    data = {
        "article_id": id,
        "supplier_id": 0,
        "supplier_info_id": 99822,
        "purchase_price": "0.0000000000",
        "sold_quantity": 0,
        "delivery_time": 0
    }
    url = f"{SITE_API_URL}/product-supplier-info"
    await post_request(session, url, headers, data)


async def post_product_property(session, id, headers):
    data = {
        "property_id": 1,
        "article_id": id
    }
    url = f"{SITE_API_URL}/product-property"
    await post_request(session, url, headers, data)


async def create_product(ean, price, title, url_key, category_code, category_id, stock_current, stock_min,
                         manufacturer, search_field):
    ''' Конечная функция создания продукта '''
    headers = {
        "Authorization": BEARER_TOKEN,
        "Accept": "application/json",
        "database": SITE_DB_NAME,
    }

    async with aiohttp.ClientSession() as session:
        article_id = await post_product_id(session=session, headers=headers, ean=ean,
                                           manufacturer=manufacturer, url_key=url_key)
        print("АРТИКЛЬ ID", article_id)

        await asyncio.gather(
            post_product_price(session=session, id=article_id, price=price, headers=headers),
            post_product_content(session=session, id=article_id, headers=headers, title=title, url_key=url_key,
                                 search_field=search_field),

            post_product_category(session=session, id=article_id, headers=headers, category_code=category_code,
                                  category_id=category_id),
            post_product_stock(session=session, id=article_id, headers=headers, stock_current=stock_current,
                               stock_min=stock_min),

            post_product_supplier_info(session=session, id=article_id, headers=headers),
            post_product_property(session=session, id=article_id, headers=headers)
        )
    return article_id

