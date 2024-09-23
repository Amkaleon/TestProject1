from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from app.config.database import connect_to_db, insert_data_list
from psycopg2 import Error


def parse_header_banner(browser) -> List[Dict[str, Any]]:
    data_list = []

    # Находим header с баннером в самом верху страницы
    header_container = browser.find_element(
        By.XPATH, '//header[@role="banner"]/div[@data-testid="advContainer"]')

    try:
        # Получаем изображение с background-image в CSS-селекторе вложенного
        # div
        image_url = header_container.find_element(
            By.XPATH, './/div/div/div').get_attribute('style')
        # Чтобы сильно не усложнять - разбил background-image по кавычкам.
        # Можно еще через регулярные выражения.
        parts_image_url = image_url.split('"')
    except NoSuchElementException:
        parts_image_url = 'Изображение отсутствует'

    try:
        # Забираем ссылку на каталог в атрибуте 'href' элемента 'a'
        content_url = header_container.find_element(
            By.TAG_NAME, 'a').get_attribute('href')
    except NoSuchElementException:
        content_url = 'Ссылка на товар отсутствует'

    """
    Добавляем данные в словарь, где:
    image_url - ссылка на изображение товара,
    content_url - ссылка на каталог или товар,
    meta - описание баннера если присутствует,
    place - нумерация блока с баннерами,
    position - позиция баннера в слайдера. Или позиция товара в блоке.
    """
    # Добавляем данные в список
    data_list.append({
        "image_url": parts_image_url[1],
        "content_url": content_url,
        "meta": 'Описание отсутствует',
        "place": 5,
        "position": 1
    })

    connection = connect_to_db()
    try:
        if connection:
            insert_data_list(connection, parts_image_url[1], content_url, 'Описание отсутствует', 5, 1)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            connection.close()

    return data_list
