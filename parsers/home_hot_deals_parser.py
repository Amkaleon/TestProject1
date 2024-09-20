from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_home_hot_deals(browser) -> List[Dict[str, Any]]:
    data_list = []

    # Ожидание, пока элемент с текстом "Предложения от брендов" станет доступным
    home_hot_deals_block_container = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, '//section[@data-testid="homeHotDealsBlock"]'))
    )

    # Скроллим страницу до элемента
    browser.execute_script("arguments[0].scrollIntoView();", home_hot_deals_block_container)

    # Собираем все слайды в этом блоке
    banners_carousel = home_hot_deals_block_container.find_element(By.XPATH, './/div[@data-testid="Banners"]')

    slide_elements = banners_carousel.find_elements(By.XPATH, './/li[@data-testid="advContainer"]')

    # Итерация по каждому слайду
    for index, slide in enumerate(slide_elements):

        try:
            browser.implicitly_wait(1)

            # Получаем ссылку на изображение
            image_url = slide.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except NoSuchElementException:
            image_url = 'Изображение отсутствует'

        try:
            # Получаем ссылку на каталог
            content_url = slide.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except NoSuchElementException:
            content_url = 'Ссылка на товар отсутствует'

        try:
            # Получаем описание товара
            caption_slide = slide.find_element(By.TAG_NAME, 'img').get_attribute('alt')
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
            "place": 3,
            "position": index + 1
        })

        try:
            """
            Так как изображения для баннера подгружаются динамически.
            Нажимаем кнопку переключить слайд вперёд после того как собрали данные с предыдущего.
            """
            # Переключаем слайды
            WebDriverWait(home_hot_deals_block_container, 1).until(
                EC.presence_of_element_located(
                    (By.XPATH, './/button[@data-testid="BannersNext"]'))).click()
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            break

    return data_list
