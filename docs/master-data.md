# Dokumentasi Master Data

Modul Master Data hanya dapat diakses oleh user dengan role `admin_jakarta`. Semua entitas menggunakan pola CRUD (Create, Read, Update, Delete) yang serupa dengan penerapan *Soft Disable* (bukan hard delete).

## 1. Aturan Umum & Soft Disable
- Data tidak pernah dihapus secara permanen dari database.
- Sebagai gantinya, digunakan atribut `is_active` (boolean). Jika di-set `false`, maka data dianggap nonaktif.
- Data yang nonaktif tetap dapat dilihat di UI jika pengguna mencentang filter "Tampilkan Nonaktif".

## 2. Validasi Relasi (Penting)
Untuk menjaga integritas data, tidak semua data dapat dinonaktifkan secara sepihak:
- **Item Type (Jenis Barang)**: Tidak bisa dinonaktifkan jika masih digunakan oleh kategori barang aktif.
- **Item Category (Kategori Barang)**: Tidak bisa dinonaktifkan jika masih digunakan oleh spare item aktif.
- **Spare Item**: Tidak bisa dinonaktifkan jika barang tersebut masih memiliki stok (`qty > 0`) di service point manapun.
- **User**: Pengguna tidak dapat menonaktifkan akunnya sendiri.

## 3. Validasi Duplikasi (Uniqueness)
- **SKU Spare Item**: SKU bersifat unik. Jika mencoba menambah/edit SKU yang sudah ada di database, akan ditolak.
- **Email Pengguna**: Email bersifat unik untuk keperluan login.
- **Stock Constraint**: Pada tabel `stock`, kombinasi `(service_point_id, spare_item_id)` adalah unik.

## 4. Endpoints

| Entitas | Base URL | Fitur Utama |
|---|---|---|
| Service Point | `/api/service-points` | Kelola lokasi gudang dan perwakilan |
| Pengguna | `/api/users` | Kelola akun, reset password, toggle active |
| Jenis Barang | `/api/items/types` | Kelola item types (RF Equipment, Modem, dll) |
| Kategori Barang | `/api/items/categories` | Kelola kategori di dalam tipe (Outdoor Unit, Konektor, dll) |
| Spare Item | `/api/items/spare` | Kelola SKU, Nama, Satuan, dan Min Stock |

Setiap endpoint mendukung operasi:
- `GET` (List dengan pagination dan pencarian)
- `POST` (Create)
- `PUT /{id}` (Edit/Update)
- `PATCH /{id}/toggle-active` (Soft disable / enable)
