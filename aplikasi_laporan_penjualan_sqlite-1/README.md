# Aplikasi Laporan Penjualan

Aplikasi berbasis Streamlit untuk mengelola laporan penjualan dengan perhitungan otomatis total penjualan dan persentase achievement.

## Cara Menjalankan Aplikasi

### Persiapan

1. **Instal Python**: Pastikan Python 3.7 atau yang lebih baru sudah terinstal di komputer Anda.

2. **Instal Paket yang Dibutuhkan**:
   Buka Command Prompt atau Terminal dan jalankan:
   ```
   pip install streamlit pandas numpy sqlalchemy psycopg2-binary python-dotenv
   ```

3. **Setup Database**:
   - Aplikasi ini menggunakan PostgreSQL untuk menyimpan data
   - Buat file bernama `.env` di folder yang sama dengan app.py
   - Isi dengan detail koneksi database sebagai berikut:
   ```
   DATABASE_URL=postgres://username:password@hostname:port/database_name
   ```
   
   Catatan: Jika Anda tidak ingin mengatur database sendiri, Anda dapat mengubah app.py untuk menggunakan penyimpanan file lokal.

### Menjalankan Aplikasi

1. Buka Command Prompt atau Terminal
2. Navigasi ke folder yang berisi app.py:
   ```
   cd path/ke/folder/aplikasi
   ```
3. Jalankan aplikasi:
   ```
   streamlit run app.py
   ```
4. Untuk membuat aplikasi bisa diakses dari perangkat lain dalam jaringan yang sama:
   ```
   streamlit run app.py --server.address=0.0.0.0 --server.port=5000
   ```

## Fitur Aplikasi

- Manajemen nama toko dan periode laporan
- Tambah, edit, dan hapus produk
- Input penjualan per shift (2 shift)
- Perhitungan otomatis total penjualan dan persentase achievement
- Laporan berbentuk teks untuk copy-paste
- Visualisasi data dengan grafik

## Struktur Folder

```
.
├── app.py                  # File utama aplikasi
├── .streamlit/             # Folder konfigurasi Streamlit
│   └── config.toml         # File konfigurasi Streamlit
└── .env                    # File untuk variabel lingkungan database (perlu dibuat)
```

## Versi Offline Tanpa Database

Jika Anda ingin menggunakan aplikasi tanpa database PostgreSQL, Anda bisa mengubah file app.py untuk menggunakan penyimpanan file JSON lokal dengan mengganti fungsi save_data() dan load_data() seperti yang dijelaskan dalam komentar di file app.py.