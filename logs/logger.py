import logging


def setup_logger():
    # Создание объекта логгера
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Создание обработчика для вывода сообщений в файл
    file_handler = logging.FileHandler('logs/app.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Создание форматировщика логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру
    logger.addHandler(file_handler)

    return logger
