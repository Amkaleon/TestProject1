import time
from pprint import pprint
from typing import List, Dict, Any

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_main_banners(browser) -> List[Dict[str, Any]]:
    data_list = []
    # Находим секцию с главным баннером. Ожидаем, пока элемент станет видимым.
    main_banners_container = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//section[@data-testid="homeMainBlock"]'))
    )

    # Пытаемся переключать слайды, нажимая кнопку "вперёд". Количество нажатий равно числу слайдов.
    while True:
        try:
            # Ожидаем появления кнопки переключения слайдов и кликаем по ней.
            button = WebDriverWait(main_banners_container, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="mainPageContainer"]/section[2]/div/div/div/button[2]'))
            )
            button.click()
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            # Если кнопка не найдена или истекло время ожидания, значит мы дошли до последнего слайда, выходим из цикла.
            break

    # Ожидаем 15 секунд, чтобы все слайды подгрузились корректно.
    # time.sleep(15)

    # Ожидаем появления карусели с баннерами.
    banners_carousel_container = WebDriverWait(main_banners_container, 20).until(
        EC.presence_of_element_located((By.XPATH, './/div[@data-testid="BannersCarousel"]'))
    )

    # Находим все слайды баннеров в карусели.
    slide_elements = banners_carousel_container.find_elements(By.XPATH, './/div[@data-testid="advContainer"]')



    # Итерация по каждому слайду
    for index, slide in enumerate(slide_elements):
        try:
            browser.implicitly_wait(3)

            # Получаем ссылку на изображение
            img_element = WebDriverWait(slide, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'img')))
            image_url = img_element.get_attribute('src')

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
        data_list.append({
            "image_url": image_url,
            "content_url": content_url,
            "meta": caption_slide,
            "place": 1,
            "position": index + 1
        })

    # Возвращаем список всех собранных данных.
    return data_list
