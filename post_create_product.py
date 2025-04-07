import random

import aiohttp

from CONFIG.config import BEARER_TOKEN, SITE_DB_NAME
from DB_GET.getAllFromAPI import fetch_product_data
from DB_GET.getAllFromDB import get_data_from_db
from GET.APIControllerForPHP import get_product_id, get_product_links
from OpenAI_dir.GPThelper import articles_translation
from POST.APIControllerPHP import create_product
from POST.Ean_checker import ean_to_check
from DB_POST.PostReport import uniqueeansreport, export_db_to_excel


async def create_product_function():
    """ Создание продукта """
    headers = {
        "Authorization": BEARER_TOKEN,
        "Accept": "application/json",
        "database": SITE_DB_NAME,
    }

    articles_id_for_delete = []

    # Получаем данные для продукта из .bd
    # data = get_data_from_db()

    #Получаем данные для продукта из FastAPI
    data = await fetch_product_data()


    # Получаем все EAN для сравнения есть ли уже такие на сайте
    eans_list = [data[index_dict]["ean"] for index_dict in data]
    unique_eans, non_unique_eans = await ean_to_check(eans_list)

    async with aiohttp.ClientSession() as session:
        ids = await get_product_id(session=session, headers=headers, eans_list=non_unique_eans)
        links = await get_product_links(session=session, headers=headers, ids=ids)

    # Записываем какие ean были одинаковые а какие нет
    await uniqueeansreport(non_unique_eans, links)
    export_db_to_excel()
    # if not unique_eans:
    #     print("Не найдено уникальных EAN завершаю программу")
    #     return 0

    # Переводим названия продуктов
    data = await articles_translation(data)

    # Пробегаемся по словарю и создаем для каждого индекса н
    for elem in data:
        # if data[elem]["ean"] not in unique_eans:

        #     continue
        # ean = data[elem]["ean"]
        article_number = f"{data[elem]['product_num']}{random.randint(1, 100)}"
        manufacturer = data[elem]["collection"]
        ean = f"{data[elem]["ean"]}{random.randint(1,1000)}"
        url_key = article_number
        price = data[elem]["price"]
        title = data[elem]["article"]
        search_field = f"{title} {manufacturer} {article_number} {url_key}"
        category_code="sonstige"
        category_id=521
        stock_current = 12
        stock_min = 1

        article_id = await create_product(
            headers=headers,
            search_field=search_field,
            ean=ean,
            price=price,
            title=title,
            url_key=url_key,
            category_code=category_code,
            category_id=category_id,
            stock_min=stock_min,
            stock_current=stock_current,
            manufacturer=manufacturer
        )
        articles_id_for_delete.append(article_id)


    print("Все объекты успешно созданы")
    print(articles_id_for_delete)
    with open("../DELETE/idForDel.txt", "a", encoding="utf-8") as f:
        f.write(str(articles_id_for_delete))
        f.write("\n")