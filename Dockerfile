# Базовый образ: Docker-образ Python версии 3.8
FROM python:3.8

# Установка /app в качестве рабочей директории контейнера
WORKDIR /app

# Копирование файлов с хоста в директорию /app внутри контейнера
COPY . .

# Установка зависимостей, указанных в requirements.txt
RUN pip install -r requirements.txt

# Запуск приложения
CMD ["python", "app.py"]
