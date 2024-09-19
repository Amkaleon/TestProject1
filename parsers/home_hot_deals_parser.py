from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_home_hot_deals(browser) -> List[Dict[str, Any]]:
    data_list = []

    # Находим контейнер "Предложения от брендов"
    home_hot_deals_block_container = browser.find_element(By.XPATH, '//section[@data-testid="homeHotDealsBlock"]')

    # Скроллим страницу до элемента
    browser.execute_script("arguments[0].scrollIntoView();", home_hot_deals_block_container)

    # Собираем все слайды в этом блоке
    slide_elements = home_hot_deals_block_container.find_elements(By.CLASS_NAME, 'swiper-slide')

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
            # Попробуем найти вторую кнопку
            WebDriverWait(home_hot_deals_block_container, 1).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="mainPageContainer"]/section[4]/div/div/button[2]'))).click()
        except TimeoutException:
            # Если первую не нашли, нажимаем на первую
            WebDriverWait(home_hot_deals_block_container, 1).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="mainPageContainer"]/section[4]/div/div/button'))).click()

    return data_list
