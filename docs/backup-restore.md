# Panduan Backup & Restore Database

Sistem ini memiliki modul terintegrasi untuk melakukan pencadangan (backup) dan pemulihan (restore) database secara langsung melalui UI Admin.

## Lokasi File & Retensi
- File backup disimpan di direktori `/backups/` di dalam container backend. 
- Folder ini di-mount (bind mount) ke folder `./backups/` di *host machine* (sehingga file tetap aman meskipun container dihapus).
- Format nama file: `backup_YYYYMMDD_HHMM.sql`.

## 1. Auto Backup Harian
- **Library**: `APScheduler` (Berjalan otomatis di background proses FastAPI).
- **Jadwal**: Setiap hari pukul 01:00 WIB (`Asia/Jakarta`).
- **Retensi**: Menyimpan 14 file terbaru. File ke-15 dan lebih lama akan otomatis dihapus untuk menghemat ruang disk.

## 2. Backup Manual
- Dapat di-*trigger* kapan saja melalui dashboard Admin di halaman **Backup & Restore**.
- File hasil backup akan langsung masuk ke daftar riwayat dan dapat di-*download*.

## 3. Proses Restore
Restore sangat berbahaya karena akan menimpa seluruh data yang ada. Proses ini dijaga dengan sangat ketat.

### Aturan & Mekanisme:
1. **Validasi**: Ukuran maksimal file upload adalah 200MB. Hanya file ber-ekstensi `.sql` yang diizinkan.
2. **Pre-Restore Backup**: Sebelum restore dijalankan, sistem *wajib* membuat auto backup terlebih dahulu dengan prefix `pre_restore_YYYYMMDD_HHMM.sql`. Jika restore gagal, pengguna tidak kehilangan data terakhirnya.
3. **Koneksi Database**: Sistem akan mematikan paksa (terminate) semua koneksi database aktif lainnya (kecuali koneksi restore itu sendiri) menggunakan query `pg_terminate_backend`.
4. **Restricting Access**: Selama proses restore berjalan, middleware FastAPI akan memblokir semua request API masuk dan mengembalikan HTTP Status 503 (Service Unavailable) hingga proses selesai.
5. **Session Revocation**: Jika restore sukses, sistem akan menghapus semua token JWT dari database, memaksa seluruh pengguna (termasuk admin) untuk logout dan login kembali dengan kredensial dari database yang baru saja di-restore.

### Troubleshooting Backup:
- Pastikan folder `./backups` memiliki izin tulis (write permission) di *host*.
- Pastikan Docker container backend memiliki `postgresql-client` terinstal (ini sudah dikonfigurasi di `Dockerfile`).
