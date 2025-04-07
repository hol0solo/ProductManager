import sqlite3
import os


def get_data_from_db():
    path = os.path.abspath("../DB_GET/Afterbuy.db")
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    query = """
    SELECT collection, price, article, category, ean, id, product_num
    FROM products 
    WHERE brand_id = 1 AND fabric_id = 3 AND article != "NICHT MEHR PRODUZIERT"
    """

    cursor.execute(query)
    results = cursor.fetchall()
    data = {}

    for index, row in enumerate(results):
        collection, price, article, category, ean, id, product_num = row
        data[index] = {
            "collection": collection,
            "price": price,
            "article": article,
            "category": category,
            "ean": ean,
            "id": id,
            "product_num": product_num
        }

        print(f"Collection: {collection}")
        print(f"Price: {price}")
        print(f"Article: {article}")
        print(f"Category: {category}")
        print(f"EAN: {ean}")
        print(f"ID: {id}")
        print(f"Product_number: {product_num}")
        print("-" * 30)

    conn.close()
    return data