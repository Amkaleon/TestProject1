# Используем официальный образ Python 3.11
FROM python:3.11-slim

#Устанавливаем рабочую директорию в контейнере
WORKDIR /Test_Project1

# Копируем содержимое репозитория в рабочую директорию
COPY . /Test_Project1

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Указываем точку входа для выполнения
CMD ['python', 'main.py']