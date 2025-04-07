import psycopg2
from psycopg2.extras import execute_values
from CONFIG.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_database():
    conn = None
    cursor = None
    try:
        # Выводим параметры для отладки
        print("Параметры подключения:")
        print(f"dbname: {DB_NAME}")
        print(f"user: {DB_USER}")
        print(f"password: {DB_PASSWORD}")
        print(f"host: {DB_HOST}")
        print(f"port: {DB_PORT}")

        # Подключаемся к базе данных
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Создаем таблицу PriceCompare66, если она не существует
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS PriceCompare66 (
            id SERIAL PRIMARY KEY,
            EAN TEXT,
            PriceFromPHPAPI REAL,
            PriceFromBD REAL
        )
        """)

        conn.commit()
        print("Таблица PriceCompare66 успешно создана или уже существует.")

    except psycopg2.Error as e:
        print(f"Ошибка PostgreSQL: {e}")
        raise
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Функция для добавления данных в таблицу
def insert_prices(zip_obj):
    conn = None
    cursor = None
    try:
        create_database()
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        data_to_insert = list(zip_obj)
        if not data_to_insert:
            print("Нет данных для вставки.")
            return

        execute_values(cursor, """
        INSERT INTO PriceCompare66 (EAN, PriceFromPHPAPI, PriceFromBD) 
        VALUES %s
        """, data_to_insert)

        conn.commit()
        print(f"Все данные успешно добавлены в таблицу! Добавлено строк: {len(data_to_insert)}")

    except psycopg2.Error as e:
        print(f"Ошибка PostgreSQL при вставке данных: {e}")
        raise
    except Exception as e:
        print(f"Неизвестная ошибка при вставке данных: {e}")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Пример использования
if __name__ == "__main__":
    # Пример zip_obj: список кортежей (EAN, PriceFromPHPAPI, PriceFromBD)
    example_data = [
        ("4067282", 4299.00, 4000.00),
        ("4067283", 6849.00, 6500.00)
    ]
    insert_prices(example_data)