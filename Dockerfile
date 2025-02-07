FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot

EXPOSE 9000

CMD ["python", "-m", "bot.main"]