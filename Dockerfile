FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ /app/app/
COPY migrations/ /app/migrations/
COPY alembic.ini /app/alembic.ini

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
