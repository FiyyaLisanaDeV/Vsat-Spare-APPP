# 📜 Changelog / Riwayat Pembaruan

Semua perubahan yang signifikan pada proyek ini akan didokumentasikan dalam file ini.

<details open>
  <summary><h2>🎉 [v1.0.0-alpha] - 2026-05-02 (Rilis Inisial)</h2></summary>
  
  **✨ Fitur Baru (Added)**
  - Inisialisasi struktur *Frontend* dengan **Next.js 14**, **Tailwind CSS**, dan **Shadcn UI**.
  - Inisialisasi struktur *Backend* dengan **FastAPI**, **SQLAlchemy**, dan konfigurasi migrasi menggunakan **Alembic**.
  - Setup struktur folder *Admin* dan *Service Point* (*role-based routes*).
  - Integrasi autentikasi menggunakan **JWT**.
  - Penambahan skrip konfigurasi `.env` dan *Docker Compose* untuk orkestrasi lokal.

  **🔧 Perbaikan (Fixed)**
  - Memperbaiki sinkronisasi *driver database* dari `asyncpg` kembali ke mode *sync* `psycopg2` pada `base.py` agar sinkron dengan konfigurasi awal.
  - Memperbaiki peringatan CSS (`unknown at-rules`) di VS Code saat menggunakan sintaks Tailwind (`@tailwind`, `@apply`) pada file `globals.css` melalui pengaturan di `.vscode/settings.json`.

  **🔒 Keamanan (Security)**
  - Implementasi *hashing password* standar menggunakan `bcrypt` untuk semua *user*.
</details>

<details>
  <summary><h2>🛠️ Rencana Selanjutnya (Upcoming)</h2></summary>

  - [ ] Implementasi fungsi ekspor/impor ke PDF dan Excel.
  - [ ] Integrasi diagram visual di *dashboard*.
  - [ ] Pembuatan unit test otomatis dengan Pytest.
</details>
