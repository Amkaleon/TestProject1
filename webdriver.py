import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config import useragent


def create_driver():
    options = webdriver.ChromeOptions()

    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument(f"--proxy-server={random.choice(proxy_list)}")
    options.add_argument(f'--user-agent={useragent}')
    options.add_argument("--disable-popup-blocking")  # Отключает блокировку всплывающих окон
    options.add_argument("--disable-notifications")  # Отключает уведомления

    # Получаем путь к папке с вебдрайвером
    driver_path = os.path.join(os.path.dirname(__file__), 'webdriver', 'chromedriver.exe')

    # Инициализация сервиса для драйвера
    service = Service(driver_path)

    # Инициализация драйвера
    driver = webdriver.Chrome(service=service, options=options)

    return driver

