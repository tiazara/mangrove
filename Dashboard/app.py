import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Page config
st.set_page_config(
    page_title="MANGROVIA-PANTURA | Decision Support System",
    page_icon="🦀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0284c7 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white !important;
        font-weight: 800;
        margin: 0;
        font-size: 26px;
    }
    .main-header p {
        color: #93c5fd !important;
        margin-top: 6px;
        margin-bottom: 0;
        font-size: 14px;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-card h3 {
        margin: 0;
        color: #1e293b;
        font-size: 22px;
    }
    .metric-card p {
        margin: 0;
        color: #64748b;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    csv_path = r'd:\Kuliah\Lomba\ASEC Arsen Unair 2026\Analisis_Data\mangrovia_pantura_dataset.csv'
    if not os.path.exists(csv_path):
        # Fallback relative
        csv_path = 'mangrovia_pantura_dataset.csv'
    df = pd.read_csv(csv_path)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Header banner
st.markdown("""
<div class="main-header">
    <div style="font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #38bdf8; text-transform: uppercase;">
        Sistem Pendukung Keputusan Konservasi & Restorasi Mangrove Pantura Jawa
    </div>
    <h1>🦀 MANGROVIA-PANTURA</h1>
    <p>Platform Analitik Geospasial Berbasis Priority Index (Threat × Dependence × Vulnerability) Menghadapi Amblesan Tanah dan Rob di Pesisir Pantai Utara Jawa</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔍 Filter Wilayah & Indeks")

region_filter = st.sidebar.multiselect(
    "Pilih Segmen Koridor Pantura:",
    options=['Pantura Barat', 'Pantura Tengah', 'Pantura Timur'],
    default=['Pantura Barat', 'Pantura Tengah', 'Pantura Timur']
)

priority_slider = st.sidebar.slider(
    "Ambang Batas Skor Prioritas (P):",
    min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.05
)

tipologi_options = list(df['Tipologi'].unique())
tipologi_filter = st.sidebar.multiselect(
    "Saring Tipologi Sosio-Ekologis:",
    options=tipologi_options,
    default=tipologi_options
)

# Filter dataframe
filtered_df = df[
    (df['region'].isin(region_filter)) &
    (df['Priority'] >= priority_slider[0]) &
    (df['Priority'] <= priority_slider[1]) &
    (df['Tipologi'].isin(tipologi_filter))
]

# Key Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p>Total Grid Terpantau</p>
        <h3>{len(filtered_df):,} km²</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    mean_p = filtered_df['Priority'].mean() if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <p>Rata-rata Prioritas</p>
        <h3 style="color: #dc2626;">{mean_p:.3f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    mean_subs = filtered_df['subsidence'].mean() if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <p>Rata-rata Amblesan</p>
        <h3 style="color: #ea580c;">{mean_subs:.1f} cm/th</h3>
    </div>
    """, unsafe_allow_html=True)

with col4:
    tot_pop = filtered_df['pop'].sum() if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <p>Estimasi Jiwa Terancam</p>
        <h3 style="color: #2563eb;">{tot_pop/1e6:.2f} Juta</h3>
    </div>
    """, unsafe_allow_html=True)

with col5:
    kritis_cnt = len(filtered_df[filtered_df['Priority'] >= 0.5])
    st.markdown(f"""
    <div class="metric-card">
        <p>Grid Prioritas Kritis (P≥0.5)</p>
        <h3 style="color: #b91c1c;">{kritis_cnt:,} Titik</h3>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Tabs for visual exploration
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Peta Interaktif Priority Index",
    "📊 Profil T, D, V & Hotspot Spasial",
    "🧩 Klaster Tipologi Sosio-Ekologis",
    "📋 Panduan Aksi & Kebijakan Spesifik"
])

with tab1:
    st.subheader("Distribusi Spasial Indeks Prioritas MANGROVIA-PANTURA")
    st.write("Warna semakin merah menandakan tingkat urgensi intervensi darurat yang semakin tinggi (kombinasi ancaman abrasi/amblesan parah, ketergantungan nelayan tinggi, dan kemiskinan warga).")
    
    # Scatter plot on coordinates
    fig_map = px.scatter(
        filtered_df, x='lon', y='lat', color='Priority',
        color_continuous_scale='YlOrRd',
        range_color=[0, 1],
        hover_data=['region', 'Tipologi', 'subsidence', 'Priority', 'pop'],
        labels={'lon': 'Bujur Timur (Longitude)', 'lat': 'Lintang Selatan (Latitude)', 'Priority': 'Skor Prioritas'},
        title="Sebaran Grid Spasial 1 km x 1 km di Sepanjang Pantai Utara Jawa"
    )
    fig_map.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.subheader("Analisis 3 Komponen Pembangun Indeks")
    c1, c2 = st.columns(2)
    with c1:
        fig_box = px.box(
            filtered_df, x='region', y='Priority', color='region',
            color_discrete_sequence=['#3b82f6', '#ef4444', '#10b981'],
            title="Perbandingan Distribusi Skor Prioritas Antarsegmen Pantura",
            labels={'region': 'Segmen Pantura', 'Priority': 'Indeks Prioritas'}
        )
        fig_box.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
        
    with c2:
        hot_counts = filtered_df.groupby(['region', 'Hotspot_Cat']).size().reset_index(name='Jumlah Grid')
        fig_hot = px.bar(
            hot_counts, x='region', y='Jumlah Grid', color='Hotspot_Cat',
            title="Konsentrasi Spasial Klaster Hotspot (Getis-Ord Gi*)",
            color_discrete_map={
                'Konsentrasi Sangat Tinggi': '#dc2626',
                'Konsentrasi Tinggi': '#f97316',
                'Netral': '#94a3b8',
                'Konsentrasi Rendah (Coldspot)': '#2563eb'
            }
        )
        fig_hot.update_layout(height=380)
        st.plotly_chart(fig_hot, use_container_width=True)

with tab3:
    st.subheader("Tipologi Sosio-Ekologis Hasil Klastering K-Means")
    st.write("Segmentasi berbasis profil gabungan Ancaman Biofisik (T), Ketergantungan (D), dan Kerentanan Ekonomi (V).")
    
    fig_radar = px.scatter_3d(
        filtered_df.sample(min(len(filtered_df), 1500), random_state=42),
        x='pct_T', y='pct_D', z='pct_V', color='Tipologi',
        labels={'pct_T': 'Threat (T)', 'pct_D': 'Dependence (D)', 'pct_V': 'Vulnerability (V)'},
        title="Distribusi Ruang Fitur 3D Tipologi Sosio-Ekologis Pantura"
    )
    fig_radar.update_layout(height=520, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_radar, use_container_width=True)

with tab4:
    st.subheader("Rekomendasi Kebijakan & Aksi Intervensi Berdasarkan Tipologi Wilayah")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        ### 🚨 Tipe 1: Darurat Sabuk Hijau & Relokasi Adaptif
        *(Dominan di Pantura Tengah: Sayung Demak & Pesisir Pekalongan)*
        * **Karakteristik**: Amblesan tanah ekstrem ($>10\text{ cm/th}$), rob permanen, tambak tenggelam, warga miskin & nelayan skala kecil.
        * **Aksi Intervensi**:
          1. **Pembangunan Struktur Hibrida (APBO)**: Memasang Alat Pemecah Gelombang Bambu semi-permeabel untuk meredam ombak dan menangkap endapan sedimen lumpur pantai.
          2. **Penanaman Spesies Perakaran Tunjang Kuat**: Bibit *Rhizophora mucronata* dan *Avicennia marina* pada substrat lumpur yang telah stabil.
          3. **Jaring Pengaman Sosial Adaptif**: Bantuan kompensasi mata pencaharian alternatif dan skema relokasi bertahap bagi keluarga yang rumahnya tenggelam permanen.
        """)
        
        st.markdown("""
        ### 🏭 Tipe 2: Kawasan Industri & Tambak Intensif
        *(Dominan di Pantura Barat: Karawang, Subang, Bekasi Industri)*
        * **Karakteristik**: Ancaman konversi tinggi, aset ekonomi warga relatif lebih tinggi dari industri/kota, tutupan mangrove terfragmentasi.
        * **Aksi Intervensi**:
          1. **Kewajiban Sabuk Hijau (Green Belt)**: Penegakan aturan wajib sabuk mangrove 30% pada tambak intensif dan kawasan industri pantai.
          2. **Moratorium Sumur Air Tanah Dalam**: Menghentikan ekstraksi air tanah industri untuk mengerem laju penurunan tanah (*land subsidence*).
        """)

    with col_b:
        st.markdown("""
        ### 🐟 Tipe 3: Konservasi Silvofishery Berkelanjutan
        *(Dominan di Pantura Timur: Ujung Pangkah Gresik, Rembang, Jepara)*
        * **Karakteristik**: Ancaman abrasi relatif lebih rendah, ketergantungan nelayan tradisional sangat tinggi, potensi budidaya kepiting bakau.
        * **Aksi Intervensi**:
          1. **Pengembangan Silvofishery (Wana Mina)**: Integrasi tambak udang/bandeng ramah lingkungan di sela-sela tegakan pohon mangrove.
          2. **Ekowisata Mangrove & Pasar Karbon**: Sertifikasi kredit karbon biru (*blue carbon*) dan ekowisata berbasis pemberdayaan kelompok sadar wisata (Pokdarwis).
        """)
        
        st.markdown("""
        ### 🛡️ Tipe 4: Zona Penyangga Stabil & Pemantauan Rutin
        * **Karakteristik**: Kondisi biofisik relatif stabil, kepadatan penduduk pesisir rendah.
        * **Aksi Intervensi**:
          1. **Pemantauan Citra Satelit Berkala**: Patroli digital berbasis Sentinel-1/Sentinel-2 untuk mencegah pembabatan mangrove liar baru.
          2. **Penguatan Regulasi Tata Ruang Pesisir (RZWP-3-K)**.
        """)

st.markdown("---")
st.caption("MANGROVIA-PANTURA © 2026 | Airlangga Statistics Essay Competition (ASEC) ARSEN UNAIR 2026")
