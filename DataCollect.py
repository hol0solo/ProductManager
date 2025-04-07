import sqlite3
import os


def get_ean():
    products_ean = list()
    path = os.path.abspath("../DB_GET/dbForTest.db")
    print(path)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT EAN FROM products")
    for row in cursor.fetchall():
        products_ean.append(int(row[0]))
    conn.close()
    return products_ean


def get_prices():
    products_price = list()
    path = os.path.abspath("../DB_GET/dbForTest.db")
    print(path)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT PRICE FROM products")
    for row in cursor.fetchall():
        price_str = str(row[0])
        price_float = float(price_str.replace(',', '.'))
        products_price.append(price_float)
    print(len(products_price))
    conn.close()
    return products_price