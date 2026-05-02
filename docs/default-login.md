# Default Login Kredensial

Sistem memiliki satu akun Administrator Utama yang dibuat secara otomatis saat sistem pertama kali dijalankan (melalui proses seeding).

## Akun Administrator

- **Email**: `admin@jakarta.vsat`
- **Password**: `Admin123!`
- **Role**: `admin_jakarta`

## Peringatan Penting
> ⚠️ **WAJIB GANTI PASSWORD**
> 
> Akun default ini dikonfigurasi dengan flag `force_password_change = true`. 
> Saat pertama kali Anda login menggunakan kredensial ini, sistem akan langsung memblokir semua akses halaman dan **memaksa Anda untuk mengganti password**.

## Aturan Password Baru
Sistem keamanan mengharuskan password baru Anda memenuhi kriteria berikut:
- Minimal **8 karakter**.
- Minimal mengandung **1 huruf besar** (A-Z).
- Minimal mengandung **1 angka** (0-9).
- Tidak boleh sama dengan password yang sedang digunakan saat ini.

Setelah Anda mengganti password, Anda akan langsung diarahkan ke Dashboard Admin dan dapat menggunakan sistem seperti biasa.
