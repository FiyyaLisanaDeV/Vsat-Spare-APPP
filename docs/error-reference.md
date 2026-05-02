# Katalog Error & HTTP Status Code

Aplikasi menggunakan respons berformat JSON yang konsisten untuk semua endpoint, dan pesan error selalu menggunakan Bahasa Indonesia.

## Format Standar Response Error
```json
{
  "success": false,
  "message": "Pesan error untuk user",
  "errors": null
}
```

## Daftar HTTP Status Code
| Kode | Deskripsi | Kapan Digunakan? |
|---|---|---|
| **200** | OK | Request berhasil. |
| **201** | Created | Data baru berhasil ditambahkan ke database. |
| **400** | Bad Request | Validasi gagal, input salah, atau relasi dicegah (misal: menghapus kategori yang masih dipakai). |
| **401** | Unauthorized | Tidak login, token invalid, atau token expired. |
| **403** | Forbidden | User login, tapi mencoba mengakses halaman/API milik role lain. |
| **404** | Not Found | Data yang diminta tidak ada di database. |
| **409** | Conflict | Data duplikat (misal: email atau SKU sudah ada). |
| **413** | Payload Too Large | Ukuran file upload melebihi batas (misal: file restore > 200MB). |
| **429** | Too Many Requests | Terkena rate limit (misal: gagal login > 5 kali dalam 15 menit). |
| **500** | Internal Server Error | Error dari backend. Stack trace disembunyikan dan hanya dicatat di file log. |
| **503** | Service Unavailable | Sistem sedang dalam maintenance (misal: sedang proses restore database). |

## Katalog Pesan Error Spesifik

### Autentikasi
- *"Email atau password salah."* (401)
- *"Akun Anda dinonaktifkan. Hubungi administrator."* (401)
- *"Sesi Anda telah berakhir. Silakan login kembali."* (401)
- *"Sesi tidak valid. Silakan login kembali."* (401)
- *"Terlalu banyak percobaan login. Coba lagi dalam 15 menit."* (429)
- *"Password baru tidak boleh sama dengan password lama."* (400)
- *"Password minimal 8 karakter, mengandung huruf besar dan angka."* (400)
- *"Anda tidak memiliki akses ke halaman ini."* (403)

### Master Data
- *"SKU sudah terdaftar. Gunakan SKU lain."* (409)
- *"Email sudah digunakan. Gunakan email lain."* (409)
- *"Data tidak ditemukan."* (404)
- *"Kategori masih digunakan oleh [N] barang aktif."* (400)
- *"Barang masih memiliki stok aktif di [N] service point."* (400)
- *"Jenis barang masih digunakan oleh [N] kategori aktif."* (400)

### Backup & Restore
- *"Backup gagal. Periksa koneksi database dan coba lagi."* (500)
- *"Penyimpanan tidak mencukupi untuk membuat backup."* (500)
- *"Format file tidak valid. Hanya file .sql yang diterima."* (400)
- *"Ukuran file melebihi batas 200MB."* (413)
- *"Restore gagal. Database tidak berubah. Backup sebelum restore tersedia."* (500)
- *"Sistem sedang dalam proses restore. Silakan tunggu."* (503)

### Server Error
- *"Terjadi kesalahan sistem. Silakan coba lagi atau hubungi administrator."* (500)
