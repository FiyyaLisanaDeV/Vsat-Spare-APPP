FROM python:3.11-slim

# Install postgresql-client untuk pg_dump dan psql
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        curl \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements dulu (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode
COPY . .

# Buat direktori logs dan backups jika belum ada
RUN mkdir -p /logs /backups

EXPOSE 8000

# Jalankan migration + seed lalu start server
CMD ["sh", "-c", "alembic upgrade head && python -m app.db.seed && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
