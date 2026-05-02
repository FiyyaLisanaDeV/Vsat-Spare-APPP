# Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    SERVICE_POINTS {
        int id PK
        string name
        enum type "service_representative, subcon, pic_lokasi"
        string city
        string province
        string pic_name
        string pic_phone
        string pic_email "nullable"
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        enum role "admin_jakarta, user_sp"
        int service_point_id FK "nullable"
        boolean is_active
        boolean force_password_change
        timestamp last_login
        timestamp created_at
        timestamp updated_at
    }

    REFRESH_TOKENS {
        int id PK
        int user_id FK
        string token_hash UK
        timestamp expires_at
        boolean revoked
        timestamp created_at
    }

    ITEM_TYPES {
        int id PK
        string name
        boolean is_active
        timestamp created_at
    }

    ITEM_CATEGORIES {
        int id PK
        int type_id FK
        string name
        boolean is_active
        timestamp created_at
    }

    SPARE_ITEMS {
        int id PK
        string sku UK
        string name
        int type_id FK
        int category_id FK
        string unit
        boolean requires_serial
        int min_stock
        text catatan "nullable"
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    STOCK {
        int id PK
        int service_point_id FK "Unique Pair"
        int spare_item_id FK "Unique Pair"
        int qty
        int updated_by FK "User ID"
        timestamp updated_at
    }

    %% Relationships
    SERVICE_POINTS ||--o{ USERS : "has"
    USERS ||--o{ REFRESH_TOKENS : "owns"
    ITEM_TYPES ||--o{ ITEM_CATEGORIES : "contains"
    ITEM_TYPES ||--o{ SPARE_ITEMS : "categorizes"
    ITEM_CATEGORIES ||--o{ SPARE_ITEMS : "sub-categorizes"
    SERVICE_POINTS ||--o{ STOCK : "stores"
    SPARE_ITEMS ||--o{ STOCK : "tracked_in"
    USERS ||--o{ STOCK : "updates"
```

## Penjelasan Relasi
1. **User & Service Point**: User dengan role `user_sp` wajib terhubung ke salah satu `service_points`. Admin Jakarta tidak wajib terhubung.
2. **Refresh Token**: Berelasi 1-to-many dari `users`. Disimpan di database untuk mekanisme revoke token (keamanan tambahan).
3. **Item Type, Category, Spare Item**: Hierarki master data barang. Spare Item terikat pada jenis dan kategori tertentu.
4. **Stock**: Merupakan tabel relasional (many-to-many) antara `service_points` dan `spare_items`. Memiliki Unique Constraint pada kombinasi `(service_point_id, spare_item_id)` untuk mencegah duplikasi baris stok untuk barang yang sama di lokasi yang sama.
