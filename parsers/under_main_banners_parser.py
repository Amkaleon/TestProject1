from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def parse_under_main_banners(browser) -> List[Dict[str, Any]]:
    data_list = []

    # Находим контейнер под основными баннерами
    under_main_banners_container = browser.find_element(By.XPATH, '//section[@data-testid="tileUnderMainCarouselBlock"]')

    # Прокрутить страницу до элемента
    browser.execute_script("arguments[0].scrollIntoView();", under_main_banners_container)
    browser.implicitly_wait(2)

    # Находим все карточки товаров внутри контейнера
    item_cards = under_main_banners_container.find_elements(By.XPATH, './/li[@data-testid="advContainer"]')

    for index, item_card in enumerate(item_cards):
        try:
            browser.implicitly_wait(1)

            # Получаем ссылку на изображение
            image_url = item_card.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except NoSuchElementException:
            image_url = 'Изображение отсутствует'

        try:
            # Получаем ссылку на каталог
            content_url = item_card.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except NoSuchElementException:
            content_url = 'Ссылка на товар отсутствует'

        try:
            # Получаем описание товара
            caption_slide = item_card.find_element(By.TAG_NAME, 'img').get_attribute('alt')
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
            "place": 2,
            "position": index + 1
        })

    return data_list
