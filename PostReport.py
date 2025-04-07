import asyncio
import asyncpg
from typing import List
from CONFIG.config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT


DB_CONFIG = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "host": DB_HOST,
    "port": DB_PORT
}


async def uniqueEansReport(eans_unique_list: List[str], eans_list: List[str]) -> None:
    """
    Асинхронно записывает EAN в таблицу unique_eans_report.

    Args:
        eans_unique_list: Список уникальных EAN
        eans_list: Полный список всех EAN
    """
    # Устанавливаем соединение с базой данных
    conn = await asyncpg.connect(**DB_CONFIG)

    try:
        # Создаем таблицу, если она еще не существует
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS unique_eans_report (
                id SERIAL PRIMARY KEY,
                ean VARCHAR(255) NOT NULL,
                unique_check BOOLEAN NOT NULL
            )
        ''')

        # Подготавливаем данные для вставки
        values = []
        unique_set = set(eans_unique_list)  # Для быстрой проверки уникальности

        for ean in eans_list:
            is_unique = ean in unique_set
            values.append((ean, is_unique))

        # Асинхронно вставляем все записи одним запросом
        await conn.executemany('''
            INSERT INTO unique_eans_report (ean, unique_check)
            VALUES ($1, $2)
        ''', values)

        print(f"Успешно записано {len(values)} записей в базу данных")
    except Exception as e:
        print(f"Ошибка при записи в базу данных: {e}")
    finally:
        await conn.close()


# Пример использования
async def main():
    eans_unique_list = ["1234567890123", "9876543210987"]
    eans_list = ["1234567890123", "9876543210987", "1111111111111", "1234567890123"]

    await uniqueEansReport(eans_unique_list, eans_list)


if __name__ == "__main__":
    asyncio.run(main())