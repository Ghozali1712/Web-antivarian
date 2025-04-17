import streamlit as st
import os

# Fungsi untuk membaca data dari Prodsus.txt
PRODSUS_PATH = os.path.join(os.path.dirname(__file__), 'Prodsus.txt')
def read_prodsus():
    if not os.path.exists(PRODSUS_PATH):
        return "File Prodsus.txt tidak ditemukan."
    with open(PRODSUS_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def parse_prodsus(text):
    # Parsing sederhana, bisa dikembangkan sesuai kebutuhan
    lines = text.split('\n')
    data = []
    current = {}
    for line in lines:
        if line.startswith('*') and line.endswith('*'):
            if current:
                data.append(current)
            current = {'Produk': line.strip('*').strip()}
        elif ':' in line:
            key, val = line.split(':', 1)
            current[key.strip()] = val.strip()
    if current:
        data.append(current)
    return data

def show_prodsus_report():
    st.title('📋 Laporan Prodsus')
    raw = read_prodsus()
    st.text_area('Isi File Prodsus.txt', raw, height=300)
    data = parse_prodsus(raw)
    if data:
        st.subheader('Tabel Laporan Prodsus')
        st.dataframe(data, use_container_width=True)
    else:
        st.warning('Data tidak ditemukan atau format salah.')

if __name__ == "__main__":
    show_prodsus_report()