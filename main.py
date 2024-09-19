import json
import logging

from selenium import webdriver

from logger import setup_logger
from config import useragent
from parsers.header_banner_parser import parse_header_banner
from parsers.home_hot_deals_parser import parse_home_hot_deals
from parsers.main_banners_parser import parse_main_banners
from parsers.recommendations_parser import parse_recommendations
from parsers.under_main_banners_parser import parse_under_main_banners

# Работает на версии python 3.10
# import undetected_chromedriver as uc

# Запускаем логгер для перехвата ошибок
logger = setup_logger()

options = webdriver.ChromeOptions()

# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument(f"--proxy-server={random.choice(proxy_list)}")
options.add_argument(f'--user-agent={useragent}')


def scrap_det_mir():
    """
    Функция для получения данных с главной страницы Детский мир.
    """
    # Список для хранения словарей
    data_list = []
    # Инициализация браузера при помощи библиотеки undetected_chromedriver
    # with uc.Chrome(options=options) as browser:

    try:
        # Инициализация через официальную библиотеку
        with webdriver.Chrome(options=options) as browser:
            browser.get('https://www.detmir.ru/')
            browser.implicitly_wait(2)

            # Парсим баннер в header
            data_list.extend(parse_header_banner(browser))

            # Парсим главные баннеры
            data_list.extend(parse_main_banners(browser))

            # Парсим товары под баннерами
            data_list.extend(parse_under_main_banners(browser))

            # Парсим предложения от брендов
            data_list.extend(parse_home_hot_deals(browser))

            # Парсим секцию "Может понравиться"
            data_list.extend(parse_recommendations(browser))

            print('[+] Парсинг окончен успешно')
            logger.info('[+] Парсинг окончен успешно')
    except Exception as e:
        print('[!] Произошла ошибка во время парсинга')
        logger.error(f'[!] Ошибка при парсинге: {e}', exc_info=True)

    try:
        with open('data.json', 'w', encoding='UTF-8') as json_file:
            # Преобразуем список словарей в строку формата JSON
            json.dump(data_list, json_file, indent=4, ensure_ascii=False)
            logger.info('[+] Данные успешно сохранены в файл data.json')
            print('[+] Данные успешно сохранены в файл data.json')
    except Exception as e:
        logger.error(f'[!] Ошибка при сохранении данных: {e}', exc_info=True)
        print('[!] Произошла ошибка при записи данных в файл data.json')


def main():
    scrap_det_mir()


if __name__ == '__main__':
    main()
