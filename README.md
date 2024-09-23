# Детский мир

Этот проект собирает данные о товарах с сайта "Детский мир" и сохраняет их в файл **.json** и таблицу **DetMir**.

## Структура проекта

- `app/` – содержит основной скрипт и связанные файлы.
  - `main.py` – основной скрипт для запуска скрапера.
  - `config/` – содержит конфигурационные файлы.
    - `config.py` – список прокси и юзерагент.
    - `database.py` – функции для работы с базой данных.
    - `webdriver.py` – инициализация веб-драйвера.
  - `parsers/` – содержит парсеры для извлечения данных.
    - `header_banner_parser.py` – парсер баннера в шапке.
    - `home_hot_deals_parser.py` – парсер предложений от брендов.
    - `main_banners_parser.py` – парсер главных баннеров.
    - `recommendations_parser.py` – парсер блока "Может понравиться".
    - `under_main_banners_parser.py` – парсер товаров под баннерами.
- `logs/` – содержит лог-файлы приложения.
  - `app.log` – файл с логами приложения.
  - `logger.py` – настройка логирования.
- `webdriver/` – содержит chromedriver.exe.
- `DetMir.json` – файл с информацией о товарах.
- `Dockerfile` – конфигурация для Docker-образа.
- `docker-compose.yml` – конфигурация для управления сервисом PostgreSQL.
- `requirements.txt` – список необходимых Python-библиотек.
- `README.md` – документация проекта.


## Предварительные требования

Перед запуском проекта убедитесь, что у вас установлены следующие программы:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Настройка проекта

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/Amkaleon/TestProject1.git
   cd TestProject1
   pip install -r requirements.txt
   ```

2. **Соберите и запустите сервисы:**

   Для сборки и запуска базы данных PostgreSQL выполните команду:

   ```bash
   docker-compose up --build
   ```

   Эта команда:
   - Запустит сервис PostgreSQL.

3. **Подключение к PostgreSQL:**

   Вы можете получить доступ к базе данных через следующую команду Docker:

   ```bash
   docker exec -it testproject1-db-1 psql -U postgres -d postgres
   ```

   Также можно подключиться с помощью инструментов, таких как **pgAdmin**, используя следующие параметры:
   - Хост: `localhost`
   - Порт: `5432`
   - База данных: `postgres`
   - Пользователь: `postgres`
   - Пароль: `3225`

## Запуск скрейпера

Скрипт скрейпера находится в файле `main.py` и выполняет следующие действия:

- Сбор данных о товарах с сайта "Детский мир".
- Сохранение данных в таблице `DetMir` в базе данных PostgreSQL.
- Сохранение данных в файле `DetMir.json`.

Для запуска скрейпера:

2. После запуска `docker-compose up --build` станет доступна запись данных в базу PostgreSQL. 
   Перейдите в директорию `app/`.
   Откройте и запустите файл `main.py`.


## Структура базы данных

Таблица `DetMir` в PostgreSQL имеет следующую структуру:

| Колонка       | Тип        | Описание                              |
|---------------|------------|---------------------------------------|
| `id`          | SERIAL     | Первичный ключ                        |
| `image_url`   | VARCHAR(255)| URL изображения товара                |
| `content_url` | VARCHAR(255)| URL страницы товара                   |
| `meta`        | TEXT       | Дополнительные метаданные             |
| `place`       | INT        | Порядок отображения                   |
| `position`    | INT        | Позиция товара в списке               |
