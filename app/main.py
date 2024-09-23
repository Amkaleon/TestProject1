import json

from app.config.webdriver import create_driver
from logs.logger import setup_logger
from app.parsers.header_banner_parser import parse_header_banner
from app.parsers.home_hot_deals_parser import parse_home_hot_deals
from app.parsers.main_banners_parser import parse_main_banners
from app.parsers.recommendations_parser import parse_recommendations
from app.parsers.under_main_banners_parser import parse_under_main_banners

# Работает на версии python 3.10
# import undetected_chromedriver as uc

# Запускаем логгер для перехвата ошибок
logger = setup_logger()


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
        with create_driver() as browser:
            browser.get('https://www.detmir.ru/')
            browser.implicitly_wait(2)

            try:
                # Парсим баннер в header
                data_list.extend(parse_header_banner(browser))
            except Exception as e:
                logger.error(f'[!] На странице отстутствует баннер в шапке страницы'
                             f'{e}', exc_info=True)

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

            try:
                with open('../DetMir.json', 'w', encoding='UTF-8') as json_file:
                    # Преобразуем список словарей в строку формата JSON
                    json.dump(data_list, json_file, indent=4, ensure_ascii=False)

                    logger.info('[+] Данные успешно сохранены в файл DetMir.json')
                    print('[+] Данные успешно сохранены в файл DetMir.json')
                    print('[+] Данные успешно сохранены в таблицу DetMir')
            except Exception as e:
                logger.error(f'[!] Ошибка при сохранении данных: {e}', exc_info=True)
                print('[!] Произошла ошибка при записи данных в файл DetMir.json')
                print('[!] Произошла ошибка при записи данных в таблицу DetMir')
    except Exception as e:
        print(f'[!] Произошла ошибка во время парсинга: {e}')
        logger.error(f'[!] Ошибка при парсинге: {e}', exc_info=True)


def main():
    scrap_det_mir()


if __name__ == '__main__':
    main()


