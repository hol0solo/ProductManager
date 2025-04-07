import aiohttp
from typing import List
from CONFIG.config import BEARER_TOKEN, SITE_DB_NAME, SITE_API_URL


async def ean_to_check(ean_list: List[str]):
    """ Проверяет EAN на уникальность через API и возвращает уникальные и неуникальные значения."""
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
                    eans_in_api = set(json_data["product_id"].keys())

                    # Уникальные EAN (те, что есть в ean_list, но нет в eans_in_api)
                    unique_eans = list(set(ean_list) - eans_in_api)

                    # Неуникальные EAN (те, что есть и в ean_list, и в eans_in_api)
                    non_unique_eans = list(set(ean_list) & eans_in_api)

                    print("Уникальные EAN:", unique_eans)
                    print("Неуникальные EAN:", non_unique_eans)
                    return unique_eans, non_unique_eans
            else:
                # Если запрос не успешен, считаем все EAN уникальными, неуникальных нет
                print("Уникальные EAN:", ean_list)
                print("Неуникальные EAN: []")
                return ean_list, []


# Пример использования
async def main():
    ean_list = ["1234567890123", "9876543210987", "1111111111111"]
    unique, non_unique = await ean_to_check(ean_list)
    print("Результат:")
    print("Уникальные:", unique)
    print("Неуникальные:", non_unique)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())