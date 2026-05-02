# 🚀 VSAT Spare Management System

Selamat datang di repositori **VSAT Spare Management System**! 
Aplikasi ini adalah solusi *full-stack* modern untuk manajemen stok perangkat *spare* VSAT, dikembangkan menggunakan teknologi terkini untuk memastikan performa yang cepat, aman, dan *scalable*.

---

## 🛠️ Tech Stack Utama

Aplikasi ini dibagi menjadi dua bagian utama:

<details>
  <summary><b>1. Frontend (Antarmuka Pengguna)</b> <i>[Klik untuk detail]</i></summary>

  - **Framework:** Next.js 14 (App Router)
  - **Bahasa:** TypeScript
  - **Styling:** Tailwind CSS + Shadcn UI
  - **State/Data Fetching:** React Hooks
</details>

<details>
  <summary><b>2. Backend (API & Logika Bisnis)</b> <i>[Klik untuk detail]</i></summary>

  - **Framework:** FastAPI
  - **Bahasa:** Python 3.10+
  - **Database:** PostgreSQL
  - **ORM & Migrasi:** SQLAlchemy + Alembic
  - **Autentikasi:** JWT (JSON Web Tokens) dengan Role-Based Access Control (Admin & Service Point)
</details>

---

## 🌟 Fitur Unggulan (Interactive Checklist)

Berikut adalah beberapa fitur yang telah dan sedang dikembangkan. Centang secara lokal saat meninjau:

- [x] **Secure Authentication** (Sistem Login dengan JWT & Enkripsi *Password* menggunakan bcrypt)
- [x] **Role-Based Routing** (Pembagian hak akses antara `Admin` dan `Service Point`)
- [x] **Master Data Management** (CRUD Jenis Barang, Merk Barang, Lokasi, dll.)
- [x] **Automated Database Backups** (Sistem *backup* otomatis menggunakan APScheduler)
- [ ] **Real-time Notifications** (Segera hadir!)
- [ ] **Advanced Reporting & Analytics** (Segera hadir!)

---

## 📚 Navigasi Dokumentasi Lengkap

Pilih panduan interaktif di bawah ini untuk memulai:

👉 **[Cara Menjalankan Aplikasi (How To Run)](HOW-TO-RUN.md)**
👉 **[Riwayat Pembaruan (Changelog)](CHANGELOG.md)**

---

*Dibuat dengan ❤️ untuk sistem pengelolaan inventaris yang lebih baik.*
