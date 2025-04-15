# Panduan Penggunaan Database SQLite

Aplikasi ini sudah dilengkapi dengan database SQLite yang siap digunakan. SQLite adalah database ringan yang tersimpan dalam satu file dan tidak memerlukan server database terpisah seperti PostgreSQL.

## Keunggulan SQLite

1. **Tidak perlu instalasi server database** - SQLite berjalan langsung dengan aplikasi
2. **Portabel** - Database tersimpan dalam satu file yang mudah dicadangkan atau dipindahkan
3. **Mudah digunakan** - Tidak perlu konfigurasi tambahan
4. **Performa baik** - Untuk aplikasi dengan jumlah data kecil atau menengah

## Cara Menggunakan Aplikasi dengan SQLite

1. Pastikan Python sudah terinstal di komputer Anda (Python 3.7+)

2. Buka Command Prompt dan install paket yang diperlukan:
   ```
   pip install streamlit pandas numpy sqlalchemy
   ```

3. Jalankan aplikasi:
   ```
   streamlit run app_sqlite.py
   ```

4. File database `sales_database.db` akan otomatis dibuat (jika belum ada) dan digunakan untuk menyimpan data.

## Berbagi Data Antar Perangkat

Untuk berbagi data antar perangkat, Anda dapat:

1. **Menyalin file database** - Cukup salin file `sales_database.db` ke perangkat lain yang juga menjalankan aplikasi
2. **Menggunakan penyimpanan bersama** - Menempatkan file database di folder jaringan yang dapat diakses oleh beberapa perangkat
3. **Menggunakan cloud storage** - Menyimpan file database di layanan cloud yang dapat disinkronkan ke beberapa perangkat

## Struktur Database

Database SQLite ini menggunakan struktur yang sama dengan versi PostgreSQL:

1. Tabel `stores` - Menyimpan informasi toko dan periode
2. Tabel `products` - Menyimpan informasi produk dan data penjualan

## Backup Database

Untuk membuat cadangan database:

1. Cukup salin file `sales_database.db` ke lokasi aman
2. Untuk memulihkan, ganti file `sales_database.db` dengan file cadangan

## Catatan

- SQLite ideal untuk penggunaan lokal atau tim kecil
- Tidak disarankan untuk penggunaan dengan banyak pengguna secara bersamaan
- Jika aplikasi akan digunakan secara intensif oleh banyak orang, pertimbangkan untuk menggunakan versi PostgreSQL