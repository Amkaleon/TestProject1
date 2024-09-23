from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.config.database import connect_to_db, insert_data_list
from psycopg2 import Error


def parse_recommendations(browser) -> List[Dict[str, Any]]:
    data_list = []

    # Ожидание, пока элемент с текстом "Может понравиться" станет доступным
    recommendations_container = WebDriverWait(
        browser, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, '//h2[span[text()="Может понравиться"]]')))

    # Скроллим страницу до элемента
    browser.execute_script(
        "arguments[0].scrollIntoView();",
        recommendations_container)

    # Найти родительскую секцию (поиск родительского элемента секции)
    parent_section = recommendations_container.find_element(
        By.XPATH, './ancestor::section')

    # Находим элемент контейнера продуктов, который имеет атрибут data-testid
    # со значением "Products" или "Recommendations"(Может меняться)
    products_container = parent_section.find_element(
        By.XPATH, './/div[@data-testid="Products" or @data-testid="Recommendations"]')
    # Получаем верхнеуровневые div элементы без вложенных div
    product_cards = products_container.find_elements(By.XPATH, './div')

    # Итерация по каждому слайду
    for index, slide in enumerate(product_cards):

        try:
            browser.implicitly_wait(1)
            # Получаем ссылку на изображение
            image_url = slide.find_element(
                By.TAG_NAME, 'img').get_attribute('src')
        except NoSuchElementException:
            image_url = 'Изображение отсутствует'

        try:
            # Получаем ссылку на каталог
            content_url = slide.find_element(
                By.TAG_NAME, 'a').get_attribute('href')
        except NoSuchElementException:
            content_url = 'Ссылка на товар отсутствует'

        try:
            # Забираем описание каталога, которое находится в элементе "span"
            # родительского элемента 'a'
            caption_slide = slide.find_element(
                By.TAG_NAME, 'img').get_attribute('alt')
        except NoSuchElementException:
            caption_slide = 'Описание отсутствует'

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
            "image_url": image_url,
            "content_url": content_url,
            "meta": caption_slide,
            "place": 4,
            "position": index + 1
        })

        connection = connect_to_db()
        try:
            if connection:
                insert_data_list(connection, image_url, content_url, caption_slide, 4, index + 1)
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                connection.close()

    return data_list
