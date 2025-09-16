# Используем официальный Python образ
FROM python:3.11

# Устанавливаем зависимости
WORKDIR /parser
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем исходники парсера
COPY . .

# Экспонируем порт FastAPI
EXPOSE 8000

# Команда для запуска Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
