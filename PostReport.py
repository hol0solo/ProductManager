import pandas as pd
import asyncpg
from typing import List

import psycopg2

from CONFIG.config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

DB_CONFIG = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "host": DB_HOST,
    "port": DB_PORT
}


async def uniqueeansreport(non_unique_eans: List[str], links: List[str]) -> None:
    """
    Асинхронно записывает неуникальные EAN и соответствующие ссылки в таблицу unique_eans_report.

    Args:
        non_unique_eans: Список неуникальных EAN
        links: Список ссылок, соответствующих неуникальным EAN
    """
    # Проверяем, что списки имеют одинаковую длину
    if len(non_unique_eans) != len(links):
        raise ValueError("Длина списка non_unique_eans и links должна совпадать")

    # Устанавливаем соединение с базой данных
    conn = await asyncpg.connect(**DB_CONFIG)

    try:
        # Создаем таблицу, если она еще не существует
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS unique_eans_report1 (
                id SERIAL PRIMARY KEY,
                ean VARCHAR(255) NOT NULL,
                link TEXT NOT NULL
            )
        ''')

        # Подготавливаем данные для вставки
        values = list(zip(non_unique_eans, links))

        # Асинхронно вставляем все записи одним запросом
        await conn.executemany('''
            INSERT INTO unique_eans_report1 (ean, link)
            VALUES ($1, $2)
        ''', values)

        print(f"Успешно записано {len(values)} записей в базу данных")

    except asyncpg.exceptions.PostgresError as e:
        print(f"Ошибка базы данных: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    finally:
        # Закрываем соединение
        await conn.close()


def export_db_to_excel():
    # Подключаемся к базе данных PostgreSQL
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    # Выполняем запрос
    query = "SELECT id, ean, link FROM unique_eans_report1"
    df = pd.read_sql_query(query, conn)

    # Сохраняем в Excel
    df.to_excel("products_from_db.xlsx", index=False)

    # Закрываем соединение
    conn.close()
    print("Данные из базы успешно записаны в products_from_db.xlsx")