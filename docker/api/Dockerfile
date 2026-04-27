FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_flask ./api_flask
COPY database ./database
COPY spark_processing ./spark_processing

EXPOSE 8000

CMD ["python", "api_flask/app.py"]
