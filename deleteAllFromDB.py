import aiohttp
import asyncio
import json
import ast
from CONFIG.config import BEARER_TOKEN, SITE_DB_NAME, SITE_API_URL

headers = {
    "Authorization": BEARER_TOKEN,
    "Accept": "application/json",
    "database": SITE_DB_NAME,
}


base_url = SITE_API_URL


def read_ids_from_file(file_path):
    ids = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Парсим строку как список Python
                print(line.strip())
                print(type(line))
                line = line.strip()
                if line:
                    print("ПРЕОБРАЗОВАНИЕ")
                    id_list = ast.literal_eval(line)  # Преобразуем строку "[457314, 457315, ...]" в список
                    print("ПРЕОБРАЗОВАЛИ")
                    ids.extend(id_list)
        return ids
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return []


async def delete_request(session, url, headers):
    try:
        async with session.delete(url, headers=headers) as response:
            if response.status in (200, 204):
                print(f"Успешно удалено: {url}")
            else:
                print(f"Ошибка при удалении {url}: статус {response.status}, ответ: {await response.text()}")
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе к {url}: {e}")


async def delete_by_id(session, id, headers):
    urls = [
        f"{base_url}/product/{id}",              # Product
        f"{base_url}/product-variation/{id}",    # Product Categories
        f"{base_url}/product-property/1/{id}",   # Product Property
        f"{base_url}/product-supplier-info/{id}" # ProductSupplierInfo
    ]

    await asyncio.gather(*[delete_request(session, url, headers) for url in urls])