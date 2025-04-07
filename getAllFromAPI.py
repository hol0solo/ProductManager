import json
import aiohttp


async def fetch_product_data():
    url = "http://192.168.0.167:8000/v1/product/by-fabric/3"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            print(json.dumps(response_json, indent=4))

            data = {}
            for index, elem in enumerate(response_json):
                data[index] = {
                    "ean": elem["ean"],
                    "price": elem["price"],
                    "collection": elem["collection"],
                    "article": elem["article"],
                    "product_num": elem["product_num"],
                }

    for elem in data:
        print(data[elem])

    return data