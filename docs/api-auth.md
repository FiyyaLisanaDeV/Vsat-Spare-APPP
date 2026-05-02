# Dokumentasi API Autentikasi

Sistem menggunakan **JWT (JSON Web Token)** dengan mekanisme *Access Token* dan *Refresh Token*.

## 1. Login
- **Endpoint**: `POST /api/auth/login`
- **Rate Limit**: Maksimal 5x gagal per IP dalam 15 menit.
- **Request Body**:
  ```json
  {
    "email": "admin@jakarta.vsat",
    "password": "Password123!"
  }
  ```
- **Response**:
  *Access Token* akan dikembalikan di response body (umur 15 menit), sedangkan *Refresh Token* akan di-set secara otomatis sebagai `httpOnly` cookie (umur 7 hari).

## 2. Refresh Token
- **Endpoint**: `POST /api/auth/refresh`
- **Mekanisme**: Digunakan ketika Access Token sudah *expired*. Frontend wajib memanggil API ini. API akan membaca *Refresh Token* dari cookie `refresh_token`, dan jika valid, akan mengembalikan Access Token baru dan me-rotasi cookie Refresh Token dengan yang baru.
- **Response**:
  ```json
  {
    "success": true,
    "message": "Token diperbarui",
    "data": {
      "access_token": "eyJhbGci...",
      "token_type": "bearer"
    }
  }
  ```

## 3. Logout
- **Endpoint**: `POST /api/auth/logout`
- **Mekanisme**: Wajib menyertakan Access Token di header `Authorization`. Sistem akan menghapus (revoke) Refresh Token di database agar tidak bisa digunakan lagi, dan menghapus cookie di client.

## 4. Get Current User (Me)
- **Endpoint**: `GET /api/auth/me`
- **Mekanisme**: Mengambil detail user yang sedang login menggunakan Access Token yang valid.

## 5. Change Password
- **Endpoint**: `POST /api/auth/change-password`
- **Request Body**:
  ```json
  {
    "current_password": "PasswordLama123!",
    "new_password": "PasswordBaru456!"
  }
  ```
