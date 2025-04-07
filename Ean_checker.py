import aiohttp

from CONFIG.config import BEARER_TOKEN, SITE_DB_NAME, SITE_API_URL


async def ean_to_check(ean_list):
    headers = {
        "Authorization": BEARER_TOKEN,
        "Accept": "application/json",
        "database": SITE_DB_NAME,
    }
    data = {
        "key": "ean",
        "value": ean_list,
    }
    url = f"{SITE_API_URL}/products/get-id"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, json=data) as response:
            if response.status == 200:
                json_data = await response.json()
                if json_data["product_id"]:
                    eans_in_api = list(json_data["product_id"].keys())
                    result = list(set(ean_list) - set(eans_in_api))
                    print("Уникальные EAN:", result)
                    return result
            else:
                print("Уникальные EAN:", ean_list)
                return ean_list