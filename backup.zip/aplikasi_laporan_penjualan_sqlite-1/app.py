import streamlit as st
import app_sqlite
import app_prodsus

# Menu navigasi di sidebar
st.sidebar.title('Menu Aplikasi')
app_choice = st.sidebar.radio(
    'Pilih Aplikasi:',
    ('Laporan Penjualan', 'Laporan Prodsus')
)

if app_choice == 'Laporan Penjualan':
    app_sqlite.main()
elif app_choice == 'Laporan Prodsus':
    app_prodsus.show_prodsus_report()
