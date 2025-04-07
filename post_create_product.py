import random

from DB_GET.getAllFromDB import get_data_from_db
from OpenAI_dir.GPThelper import articles_translation
from POST.APIControllerPHP import create_product
from POST.Ean_checker import ean_to_check
from DB_POST.PostReport import uniqueEansReport


async def create_product_function():
    """ Создание продукта """
    articles_id_for_delete = []

    # Получаем данные для продукта
    data = get_data_from_db()

    # Получаем все EAN для сравнения есть ли уже такие на сайте
    # eans_list = [data[index_dict]["ean"] for index_dict in data]
    # unique_eans = await ean_to_check(eans_list)
    # if not unique_eans:
    #     await uniqueEansReport(unique_eans, eans_list)
    #     print("Не найдено уникальных EAN завершаю программу")
    #     return 0

    # Переводим названия продуктов
    data = await articles_translation(data)

    # Пробегаемся по словарю и создаем для каждого индекса н
    for elem in data:
        # if data[elem]["ean"] not in unique_eans:
        #     continue
        # ean = data[elem]["ean"]
        print(data[elem])
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