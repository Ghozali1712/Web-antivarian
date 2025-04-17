import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import os
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Date, MetaData, ForeignKey, text
import psycopg2
import os

# Set page config
st.set_page_config(
    page_title="Aplikasi Laporan Penjualan - by Bang Imam",
    page_icon="📊",
    layout="wide"
)

# Database connection
DATABASE_URL = os.environ.get("DATABASE_URL")
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
    Column('store_id', Integer, ForeignKey('stores.id')),
    Column('name', String),
    Column('target', Integer),
    Column('shift1', Integer),
    Column('shift2', Integer),
    Column('total', Integer),
    Column('achievement', Float)
)

# Ensure tables exist
metadata.create_all(engine)

# Function to initialize session state variables
def initialize_session_state():
    if 'products' not in st.session_state:
        st.session_state.products = []
    if 'store_name' not in st.session_state:
        st.session_state.store_name = ""
    if 'period' not in st.session_state:
        st.session_state.period = datetime.date.today()
    if 'store_id' not in st.session_state:
        st.session_state.store_id = None
    if 'edit_index' not in st.session_state:
        st.session_state.edit_index = -1

# Function to save data to database
def save_data():
    with engine.connect() as conn:
        # Check if store already exists
        if st.session_state.store_id is None:
            # Insert new store
            result = conn.execute(
                stores.insert().values(
                    store_name=st.session_state.store_name,
                    period=st.session_state.period
                )
            )
            conn.commit()
            
            # Get the store ID
            result = conn.execute(
                sqlalchemy.select(stores.c.id)
                .where(stores.c.store_name == st.session_state.store_name)
                .where(stores.c.period == st.session_state.period)
                .order_by(stores.c.id.desc())
                .limit(1)
            )
            store_id = result.fetchone()[0]
            st.session_state.store_id = store_id
        else:
            # Update existing store
            conn.execute(
                stores.update()
                .where(stores.c.id == st.session_state.store_id)
                .values(
                    store_name=st.session_state.store_name,
                    period=st.session_state.period
                )
            )
            conn.commit()
            store_id = st.session_state.store_id
            
        # Delete existing products for this store
        conn.execute(products.delete().where(products.c.store_id == store_id))
        conn.commit()
        
        # Insert all products
        for product in st.session_state.products:
            conn.execute(
                products.insert().values(
                    store_id=store_id,
                    name=product['name'],
                    target=product['target'],
                    shift1=product['shift1'],
                    shift2=product['shift2'],
                    total=product['total'],
                    achievement=product['achievement']
                )
            )
        conn.commit()
    
    st.success("Data berhasil disimpan ke database!")

# Function to load data from database
def load_data():
    with engine.connect() as conn:
        # Find the latest store data
        result = conn.execute(
            sqlalchemy.select(stores)
            .order_by(stores.c.id.desc())
            .limit(1)
        )
        store_data = result.fetchone()
        
        if store_data:
            st.session_state.store_id = store_data[0]  # id
            st.session_state.store_name = store_data[1]  # store_name
            st.session_state.period = store_data[2]  # period
            
            # Get products for this store
            result = conn.execute(
                sqlalchemy.select(products)
                .where(products.c.store_id == st.session_state.store_id)
            )
            
            products_list = []
            for row in result:
                products_list.append({
                    'name': row[2],  # name
                    'target': row[3],  # target
                    'shift1': row[4],  # shift1
                    'shift2': row[5],  # shift2
                    'total': row[6],   # total
                    'achievement': row[7]  # achievement
                })
            
            st.session_state.products = products_list

# Function to add a new product
def add_product(name, target):
    if name and target > 0:
        # Create a new product
        new_product = {
            'name': name,
            'target': target,
            'shift1': 0,
            'shift2': 0,
            'total': 0,
            'achievement': 0
        }
        
        # Add to the products list
        if st.session_state.edit_index >= 0:
            # Replace the product being edited
            st.session_state.products[st.session_state.edit_index] = new_product
            st.session_state.edit_index = -1  # Reset edit index
        else:
            # Add a new product
            st.session_state.products.append(new_product)
        
        # Clear form
        st.session_state.new_product_name = ""
        st.session_state.new_product_target = 0
        
        # Save data
        save_data()
        
        # Force app to rerun to show updated data
        st.rerun()
    else:
        st.error("Mohon isi nama produk dan target penjualan dengan benar.")

# Function to update sales data
def update_sales(index, shift1, shift2):
    if index >= 0 and index < len(st.session_state.products):
        product = st.session_state.products[index]
        product['shift1'] = shift1
        product['shift2'] = shift2
        product['total'] = shift1 + shift2
        
        # Calculate achievement percentage
        if product['target'] > 0:
            product['achievement'] = (product['total'] / product['target']) * 100
        else:
            product['achievement'] = 0
            
        # Save data
        save_data()
        
        # Force app to rerun to show updated data
        st.rerun()

# Function to delete a product
def delete_product(index):
    if index >= 0 and index < len(st.session_state.products):
        st.session_state.products.pop(index)
        save_data()
        st.rerun()

# Function to edit a product
def edit_product(index):
    if index >= 0 and index < len(st.session_state.products):
        product = st.session_state.products[index]
        st.session_state.new_product_name = product['name']
        st.session_state.new_product_target = product['target']
        st.session_state.edit_index = index

# Function to reset all data
def reset_data():
    st.session_state.products = []
    st.session_state.store_name = ""
    st.session_state.period = datetime.date.today()
    st.session_state.edit_index = -1
    st.session_state.store_id = None
    save_data()
    st.rerun()

# Function to generate a report
def generate_report():
    # Create dataframe for report
    df = pd.DataFrame(st.session_state.products)
    
    if not st.session_state.products:
        st.warning("Tidak ada data produk untuk ditampilkan dalam laporan.")
        return
    
    # Generate text format report
    report_title = f"Laporan sales *PALING MURAH*"
    
    # Format the period
    if isinstance(st.session_state.period, datetime.date):
        period_str = st.session_state.period.strftime("%d - %d %B %Y")
        # Get the end date (assume 7 days period)
        end_date = st.session_state.period + datetime.timedelta(days=6)
        period_str = f"{st.session_state.period.strftime('%d')} - {end_date.strftime('%d %B %Y')}"
    else:
        period_str = str(st.session_state.period)
        
    report_header = f"Periode : {period_str}\n*{st.session_state.store_name}*\n"
    
    # Generate text report
    report_text = f"{report_title}\n{report_header}\n"
    
    # Add each product
    for product in st.session_state.products:
        product_text = f"""
*{product['name']}*
Target: {product['target']}
Sales Shift 1 : {product['shift1']}
Sales shift 2 : {product['shift2']}
Total : {product['total']}
Ach: {product['achievement']:.0f}%
"""
        report_text += product_text + "\n"
    
    # Display the report in a text area
    st.text_area("Laporan untuk Copy Paste", report_text, height=500)
    
    # Also display visual report
    st.header(f"Laporan Penjualan - {st.session_state.store_name}")
    st.subheader(f"Periode: {period_str}")
    
    # Calculate summary statistics
    total_target = df['target'].sum()
    total_sales = df['total'].sum()
    overall_achievement = (total_sales / total_target * 100) if total_target > 0 else 0
    
    # Display summary statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Target", f"{total_target:,.0f}")
    with col2:
        st.metric("Total Penjualan", f"{total_sales:,.0f}")
    with col3:
        st.metric("Achievement Overall", f"{overall_achievement:.2f}%")
    
    # Format the dataframe for display
    display_df = df.copy()
    display_df = display_df.rename(columns={
        'name': 'Nama Produk',
        'target': 'Target',
        'shift1': 'Shift 1',
        'shift2': 'Shift 2',
        'total': 'Total',
        'achievement': 'Achievement (%)'
    })
    
    # Format numeric columns
    numeric_cols = ['Target', 'Shift 1', 'Shift 2', 'Total']
    for col in numeric_cols:
        display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}")
    
    display_df['Achievement (%)'] = display_df['Achievement (%)'].apply(lambda x: f"{x:.2f}%")
    
    # Display the dataframe
    st.dataframe(display_df, use_container_width=True)
    
    # Create a bar chart for achievement comparison
    st.subheader("Achievement per Produk")
    chart_df = df[['name', 'achievement']].copy()
    chart_df.columns = ['Produk', 'Achievement (%)']
    
    # Sort by achievement for better visualization
    chart_df = chart_df.sort_values('Achievement (%)', ascending=False)
    
    # Create the chart
    chart = st.bar_chart(
        chart_df.set_index('Produk'),
        use_container_width=True
    )
    
# Initialize session state
initialize_session_state()

# Try to load data if it exists
try:
    load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")

# Main app UI
st.title("📊 Aplikasi Laporan Penjualan")
st.markdown("##### Dibuat oleh: Bang Imam")

# Store and period settings
with st.expander("⚙️ Pengaturan Toko dan Periode", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        store_name = st.text_input("Nama Toko", st.session_state.store_name)
        st.session_state.store_name = store_name
    
    with col2:
        period = st.date_input("Periode Laporan", st.session_state.period)
        st.session_state.period = period
    
    if st.button("Simpan Pengaturan"):
        save_data()
        st.success("Pengaturan berhasil disimpan!")

# Product management section
st.header("Manajemen Produk")

# Form for adding/editing products
with st.form(key="product_form"):
    st.subheader("Tambah/Edit Produk")
    
    # Initialize form input variables if needed
    if 'new_product_name' not in st.session_state:
        st.session_state.new_product_name = ""
    if 'new_product_target' not in st.session_state:
        st.session_state.new_product_target = 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("Nama Produk", st.session_state.new_product_name)
    
    with col2:
        product_target = st.number_input("Target Penjualan", min_value=0, value=int(st.session_state.new_product_target))
    
    submitted = st.form_submit_button("Simpan Produk")
    
    if submitted:
        st.session_state.new_product_name = product_name
        st.session_state.new_product_target = product_target
        add_product(product_name, product_target)

# Display and manage existing products
if st.session_state.products:
    st.subheader("Daftar Produk")
    
    # Create a dataframe for display
    df = pd.DataFrame(st.session_state.products)
    
    # Display each product with input fields for sales
    for i, product in enumerate(st.session_state.products):
        with st.container():
            # First row for product name and target
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{product['name']}**")
            
            with col2:
                st.write(f"Target: {product['target']:,.0f}")
            
            # Second row for inputs and stats
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                shift1 = st.number_input(
                    "Shift 1", 
                    min_value=0, 
                    value=int(product['shift1']),
                    key=f"shift1_{i}"
                )
            
            with col2:
                shift2 = st.number_input(
                    "Shift 2", 
                    min_value=0, 
                    value=int(product['shift2']),
                    key=f"shift2_{i}"
                )
            
            with col3:
                st.write(f"Total: {product['total']:,.0f}")
            
            with col4:
                st.write(f"Ach: {product['achievement']:.2f}%")
            
            # Third row for buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                if st.button("💾 Simpan", key=f"update_{i}"):
                    update_sales(i, shift1, shift2)
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_{i}"):
                    edit_product(i)
            
            with col3:
                if st.button("🗑️ Hapus", key=f"delete_{i}"):
                    delete_product(i)
        
        st.markdown("---")

# Report generation
st.header("Laporan")

if st.button("Generate Laporan"):
    generate_report()

# Reset data button (with confirmation)
st.header("Reset Data")
if st.button("Reset Semua Data"):
    confirmation = st.checkbox("Saya yakin ingin menghapus semua data")
    if confirmation:
        reset_data()
        st.success("Semua data telah direset!")
