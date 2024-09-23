import logging
import os

def setup_logger():
    # Создание объекта логгера
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Получение абсолютного пути к папке logs
    logs_dir = os.path.join(os.path.dirname(__file__), '../logs')
    os.makedirs(logs_dir, exist_ok=True)  # Создаем папку, если ее нет

    file_handler = logging.FileHandler(os.path.join(logs_dir, 'app.log'), encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Создание форматировщика логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру
    logger.addHandler(file_handler)

    return logger
