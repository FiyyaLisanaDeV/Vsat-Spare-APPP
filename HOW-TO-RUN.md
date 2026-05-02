# 🎮 How to Run (Panduan Interaktif Menjalankan Aplikasi)

Pilih metode yang paling nyaman untuk Anda. Anda dapat menggunakan **Docker** (Sangat Direkomendasikan untuk *production* & kemudahan) atau menjalankan secara **Native (Manual)**.

---

<details open>
  <summary><h2>🐳 Metode 1: Menggunakan Docker Compose (Direkomendasikan)</h2></summary>

Metode ini sangat mudah karena Anda tidak perlu meng-*install* Python, Node.js, atau PostgreSQL secara manual. Semuanya sudah dibungkus di dalam *container*.

### 📋 Prasyarat
- Pastikan [Docker Desktop](https://www.docker.com/products/docker-desktop) sudah terinstal dan berjalan di komputer/Windows Anda.

### 🚀 Langkah Eksekusi

1. **Buka Terminal/PowerShell**, arahkan ke direktori root proyek (`Vsat Spare`).
2. Jalankan perintah ajaib ini:
   ```bash
   docker-compose up -d --build
   ```
3. **Tunggu beberapa saat** hingga proses *download* dan *build* selesai.
4. **Cek Aplikasi:**
   - Frontend (Web App): [http://localhost:3000](http://localhost:3000)
   - Backend API Docs (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
5. Untuk mematikan server:
   ```bash
   docker-compose down
   ```
</details>

---

<details>
  <summary><h2>💻 Metode 2: Native / Manual (Untuk Pengembangan Cepat)</h2></summary>

Gunakan metode ini jika Anda sedang men-*develop* atau mengedit kode secara langsung dan ingin proses *hot-reload*.

### 📋 Prasyarat
- **Python 3.10+** (untuk Backend)
- **Node.js 18+ & npm** (untuk Frontend)
- **PostgreSQL Server** berjalan di *localhost*.

### ⚙️ Tahap 1: Konfigurasi Database & Backend
1. Pastikan Anda sudah membuat *database* dengan nama `vsat_spare` di PostgreSQL lokal Anda.
2. Buka terminal baru dan masuk ke folder `backend`:
   ```bash
   cd backend
   ```
3. Aktifkan *virtual environment*:
   ```bash
   .\venv\Scripts\activate
   ```
4. Jalankan migrasi Alembic (Opsional, jika database masih kosong):
   ```bash
   alembic upgrade head
   ```
5. Jalankan server FastAPI:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   *(Backend akan berjalan di [http://localhost:8000](http://localhost:8000))*

### 🎨 Tahap 2: Menjalankan Frontend Next.js
1. Buka tab terminal baru (biarkan terminal *backend* tetap berjalan).
2. Masuk ke folder `frontend`:
   ```bash
   cd frontend
   ```
3. Install dependencies (jika belum):
   ```bash
   npm install
   ```
4. Jalankan *development server*:
   ```bash
   npm run dev
   ```
   *(Frontend akan berjalan di [http://localhost:3000](http://localhost:3000))*

</details>

---

💡 **Butuh Bantuan?** 
Jika terjadi *error* pada saat menjalankan aplikasi, coba hapus folder `node_modules` (di frontend) dan pastikan ekstensi/modul Python di environment sudah lengkap sesuai dengan file `requirements.txt`.
