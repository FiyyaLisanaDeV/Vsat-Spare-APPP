# Panduan Setup & Instalasi

## Prasyarat
- **Docker** terinstal (versi >= 24.0.0 direkomendasikan)
- **Docker Compose** terinstal (versi >= 2.0.0 direkomendasikan)
- Port yang belum digunakan: `3000` (Frontend), `8000` (Backend), `5432` (PostgreSQL), `5050` (pgAdmin - opsional)

## Langkah Instalasi

1. **Clone Repository**
   ```bash
   git clone <url-repo>
   cd vsat-spare
   ```

2. **Persiapan Environment Variable**
   Salin template `.env.example` menjadi `.env`.
   ```bash
   cp .env.example .env
   ```
   **PENTING**: Ubah nilai `SECRET_KEY` dan `REFRESH_SECRET_KEY` di dalam `.env` sebelum menjalankan aplikasi untuk production!

3. **Menjalankan Sistem**
   Gunakan docker compose untuk menjalankan seluruh layanan.
   ```bash
   docker compose up -d
   ```

4. **Verifikasi Container**
   Pastikan semua container dalam status `healthy`.
   ```bash
   docker compose ps
   ```

5. **Akses Aplikasi**
   Setelah semua container berjalan:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - pgAdmin (jika diaktifkan): [http://localhost:5050](http://localhost:5050)

## Mengatasi Port Conflict (Bentrok)
Jika Anda mendapatkan error port sedang digunakan (misalnya port `3000` atau `5432`), buka file `.env` dan ubah variabel port, misalnya:
```env
FRONTEND_PORT=3001
BACKEND_PORT=8001
DB_PORT=5433
```
Lalu jalankan ulang: `docker compose up -d`

## Melihat Log
Sistem backend menyimpan log di folder `logs/`. Untuk melihat log secara real-time dari container:
```bash
docker logs vsat_backend -f
```

## Menjalankan Seed Manual (Opsional)
Sistem sudah menjalankan seed otomatis saat pertama kali startup. Namun jika Anda perlu mereset atau menambahkan ulang seed data:
```bash
docker exec vsat_backend python -m app.db.seed
```
Script seed bersifat idempoten (aman dijalankan berulang kali tanpa membuat duplikat).
