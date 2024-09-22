import os

import psycopg2
from psycopg2 import Error

from logs.logger import setup_logger

logger = setup_logger()

connection = None  # Инициализация

try:

    connection = psycopg2.connect(
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        database=os.getenv("DATABASE_NAME"))

    # # Подключение к существующей базе данных
    # connection = psycopg2.connect(user="postgres",
    #                               password="3225",
    #                               host="localhost",
    #                               port="5432",
    #                               database="postgres")

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # SQL-запрос для создания новой таблицы
    create_table_query = """
        CREATE TABLE IF NOT EXISTS DetMir (
        id SERIAL PRIMARY KEY,
        image_url VARCHAR(255) NOT NULL,
        content_url VARCHAR(255) NOT NULL,
        meta TEXT,
        place INT NOT NULL,
        position INT NOT NULL
    );
    """
    # Выполнение команды: это создает новую таблицу
    cursor.execute(create_table_query)
    connection.commit()
    logger.info("Таблица успешно создана в PostgreSQL", exc_info=True)

except (Exception, Error) as error:
    logger.error(f"Ошибка при работе с PostgreSQL:\n {error}")

finally:
    if connection:
        cursor.close()
        connection.close()


# Функция подключения к базе данных
def connect_to_db():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            database=os.getenv("DATABASE_NAME"))
        return connection

    except (Exception, Error) as error:
        logger.error("Ошибка при подключении к базе данных", error, exc_info=True)
        return None


# Функция для записи значений в таблицу DetMir
def insert_data_list(connection, image_url, content_url, meta, place, position):
    try:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO DetMir (image_url, content_url, meta, place, position)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (image_url, content_url, meta, place, position))
        connection.commit()

    except (Exception, Error) as error:
        logger.error("Ошибка при вставке данных в PostgreSQL", error, exc_info=True)

    finally:
        if cursor:
            cursor.close()
