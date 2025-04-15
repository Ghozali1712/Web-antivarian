import os
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Date, MetaData
from dotenv import load_dotenv

def setup_database():
    # Load .env file
    load_dotenv()
    
    # Get database URL from environment
    DATABASE_URL = os.environ.get("DATABASE_URL")
    
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL tidak ditemukan!")
        print("Pastikan file .env sudah dibuat dengan benar berdasarkan .env.example")
        return False
    
    try:
        # Create engine and connect to database
        engine = create_engine(DATABASE_URL)
        metadata = MetaData()
        
        # Define tables
        stores = Table(
            'stores', metadata,
            Column('id', Integer, primary_key=True),
            Column('store_name', String),
            Column('period', Date)
        )
        
        products = Table(
            'products', metadata,
            Column('id', Integer, primary_key=True),
            Column('store_id', Integer, sqlalchemy.ForeignKey('stores.id')),
            Column('name', String),
            Column('target', Integer),
            Column('shift1', Integer),
            Column('shift2', Integer),
            Column('total', Integer),
            Column('achievement', Float)
        )
        
        # Create tables if they don't exist
        metadata.create_all(engine)
        # Perbaikan: Tambahkan kolom start_date dan end_date jika belum ada di tabel stores
        from sqlalchemy import text
        with engine.connect() as conn:
            table_info = conn.execute(text("PRAGMA table_info(stores)")).fetchall()
            columns = [col[1] for col in table_info]
            if 'start_date' not in columns:
                conn.execute(text("ALTER TABLE stores ADD COLUMN start_date TEXT"))
            if 'end_date' not in columns:
                conn.execute(text("ALTER TABLE stores ADD COLUMN end_date TEXT"))
        
        print("Database berhasil diatur!")
        print("Tabel 'stores' dan 'products' telah dibuat.")
        return True
        
    except Exception as e:
        print(f"ERROR: Terjadi kesalahan saat mengatur database: {str(e)}")
        return False

if __name__ == "__main__":
    # Run setup when the script is executed directly
    success = setup_database()
    
    if success:
        print("\nDatabase siap digunakan!")
        print("Anda sekarang dapat menjalankan aplikasi dengan perintah:")
        print("streamlit run app.py")
    else:
        print("\nPenyiapan database gagal.")
        print("Pastikan informasi koneksi database sudah benar di file .env")