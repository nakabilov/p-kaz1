# Используем базовый образ Python
FROM python:3.8

# Устанавливаем переменную окружения PYTHONUNBUFFERED, чтобы вывод был напрямую в логи и не кэшировался
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt /code/

# Устанавливаем зависимости из файла requirements.txt
RUN pip install  -r requirements.txt

# Копируем все файлы из текущего каталога в контейнер в рабочую директорию
COPY . /code/

# Запускаем команду для миграции базы данных
RUN python manage.py migrate

# Определяем порт, который будет слушать контейнер
EXPOSE 8000

# Запускаем сервер Django при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

