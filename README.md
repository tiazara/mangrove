# SABUK HIJAU: Sistem Pendukung Keputusan Berbasis Fusi Data Multi-Sumber dan Pemodelan Probabilistik untuk Prioritas Mitigasi Coastal Squeeze Mangrove Pantura

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pydeck WebGL](https://img.shields.io/badge/Pydeck-GPU_WebGL-47A248?style=flat&logo=webgl&logoColor=white)](https://deckgl.readthedocs.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Modern_Theme-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-Spatial_Data-139C5A?style=flat&logo=geopandas&logoColor=white)](https://geopandas.org/)

**Airlangga Statistics Essay Competition (ASEC) 2026 — Arsen Universitas Airlangga**  
*Tim Peneliti / Pengembang: SABUK HIJAU Pantura Team*

---

## 🌊 Ringkasan Eksekutif & Latar Belakang Ilmiah

Hutan mangrove di sepanjang Pantai Utara (Pantura) Jawa mengalami ancaman eksistensial ganda yang dikenal sebagai **coastal squeeze** (*penjepitan pesisir*):
1. **Sumbu Laut (Tekanan Vertikal)**: Amblesan tanah (*land subsidence*) ekstrem berbasis InSAR Sentinel-1 (2017–2023) yang mencapai hingga 4,8 cm/tahun (GNSS lokal hingga 11,6 cm/tahun) dipadu kenaikan muka laut (*sea level rise* / SLR ~0,55 cm/tahun) jauh melampaui laju akresi sedimen alami (~0,50 cm/tahun). Defisit vertikal ini mengancam menenggelamkan tegakan mangrove secara permanen sebelum tahun 2050 (median tahun 2068).
2. **Sumbu Darat (Restriksi Lateral)**: Infrastruktur keras buatan manusia (jalan tol tanggul laut Semarang-Demak, jalan arteri Pantura, pemukiman padat, serta pematang tambak beton permanen) berjarak dekat ($\le 500\text{ m}$) di belakang tegakan, mengunci ruang akomodasi alami mangrove untuk bermigrasi mundur ke arah darat.

Repositori ini menyajikan rangkaian riset terintegrasi: mulai dari pengolahan data geospasial skala besar (Google Earth Engine, Sentinel-1/2, InSAR, WorldPop, OSM), pemodelan ekonometrika spasial (*state-space Kalman filter*, WLS klaster, Huber robust, SIMEX), hingga **Sistem Pendukung Keputusan (*Decision Support System* / DSS) Spasial Berbasis Web** yang interaktif.

---

## 🗺️ Wilayah Kajian & Unit Analisis Spasial

Penelitian mencakup **5 koridor pesisir strategis Pantura** yang mewakili variasi kombinasi tekanan biofisik dan antropogenik:

| Koridor Wilayah | Jumlah Transek | Karakteristik Biofisik & Justifikasi Pemilihan |
| :--- | :---: | :--- |
| **Pekalongan** | 290 | **Episentrum Kritis**: Amblesan tanah sangat tinggi (GNSS hingga 11,6 cm/th, InSAR hingga 4,8 cm/th) dan risiko tenggelam tercepat. |
| **Semarang – Demak** | 315 | **Tekanan Ganda**: Amblesan tinggi dengan keberadaan tanggul laut raksasa, tol terintegrasi, dan banjir rob Sayung. |
| **Cirebon** | 405 | **Ruang Terjepit**: Sabuk mangrove tipis di antara pematang tambak intensif dan persawahan; potensi tinggi perluasan ke darat. |
| **Surabaya – Madura** | 1.165 | **Sabuk Resilien**: Sabuk mangrove delta terluas dengan resiliensi alami tinggi dan tekanan defisit relatif rendah. |
| **Jepara (Kontrol)** | 190 | **Baseline Kontrol**: Pesisir batuan vulkanik Muria yang stabil dengan amblesan rendah (+0,05 cm/th). |
| **Total Pantura** | **2.365** | **Garis pantai evaluasi sepanjang ~591 km.** |

* **Unit Analisis**: Transek tegak lurus pantai sepanjang 3.500 m (500 m ke arah laut lepas dan 3.000 m ke arah pedalaman darat), dipasang setiap interval 250 m, dengan titik observasi mikro setiap 10 m di sepanjang transek.
* **Domain Analisis**:
  * **920 transek bermangrove aktif**: Dianalisis untuk dinamika pergerakan tepi (*edge retreat*), pemodelan nowcasting/forecasting, dan klasifikasi 4 kuadran mitigasi.
  * **1.445 transek non-mangrove**: Dianalisis berdasarkan kondisi substrat dan tutupan lahan untuk menentukan potensi restorasi hidrologis, penangkap sedimen, atau perlindungan buatan.
* **Agregasi 259 Ruas Kawasan Prioritas**: Peleburan spasial transek bertetangga dengan rekomendasi seragam minimal 500 m (total 591,2 km) untuk memudahkan perencanaan anggaran APBD/Bappeda.

---

## 🔬 Metodologi & Alur Fusi Data Multi-Sumber

```
+---------------------------------------------------------------------------------------------------+
|                                  FUSI DATA MULTI-SUMBER PANTURA                                   |
|   Sentinel-1 SAR (VH/VV) + Sentinel-2 (NDVI) + InSAR Subsidence (Ohenhen) + EOT20 Tides + OSM     |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                ASIMILASI STATE-SPACE KALMAN FILTER                                |
|           Rekonstruksi deret waktu posisi tepi laut bulanan Jan 2021 – Agu 2026 (68 bulan)        |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                  PEMODELAN EKONOMETRIKA SPASIAL                                   |
|   1. Estimasi Tren Tepi Mangrove (v_edge) via Regresi OLS & Kalman Gain                           |
|   2. Model Kausalitas Penggerak Mundur: WLS Klaster, Huber Robust, dan SIMEX (Koreksi Galat)      |
|   3. Bukti Empiris: v_edge dipicu defisit vertikal (p < 0.001) dan dihambat barrier lateral       |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                             MATRIKS KEPUTUSAN 4 KUADRAN & 11 AKSI                                 |
|   * RED (Rekayasa Hibrida: Permeable Dam)        * YELLOW (Pengayaan Sabuk Hijau)                 |
|   * ORANGE (Pembukaan Ruang Mundur Mangrove: Jebol Tambak) * GREEN (Konservasi Ketat Alami)        |
|   * + 7 Kategori Aksi Non-Mangrove (Restorasi Lumpur, Hidrologis Tambak, Silvofishery, dll.)      |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                 SISTEM PENDUKUNG KEPUTUSAN (DSS)                                  |
|   Dashboard Interaktif Streamlit: Tab Peta WebGL + Tab Dinamika Kausalitas + Tab Simulator What-If|
+---------------------------------------------------------------------------------------------------+
```

---

## 📊 Matriks 4 Kuadran & 11 Rekomendasi Aksi Lapangan

### 1. Tipologi 4 Kuadran Mangrove (920 Transek Domain Mangrove)
* 🔴 **`RED · Rekayasa Hibrida`** (15 transek | 1,6%): Tekanan laut tinggi $\times$ restriksi lateral tinggi. Membutuhkan intervensi struktur permeable dam bambu untuk memulihkan elevasi substrat.
* 🟠 **`ORANGE · Pembukaan Ruang Mundur Mangrove`** (242 transek | 26,3%): Tekanan laut tinggi $\times$ restriksi lateral rendah. Pembukaan pematang tambak untuk memberikan ruang migrasi mundur ke darat.
* 🟡 **`YELLOW · Pengayaan Sabuk Hijau`** (153 transek | 16,6%): Tekanan laut rendah $\times$ restriksi lateral tinggi. Pengayaan jenis akar tunjang/kokoh pelindung aset permukiman.
* 🟢 **`GREEN · Konservasi Ketat`** (510 transek | 55,4%): Tekanan laut rendah $\times$ restriksi lateral rendah. Zona lindung mandiri berdaya lentur alami tinggi.

### 2. Komposisi 11 Rekomendasi Kanonik (2.365 Transek Pesisir Pantura)
1. `GREEN · Konservasi Ketat` (510 transek)
2. `Perlindungan Pantai Terbangun` (486 transek)
3. `Restorasi Alami Lumpur` (460 transek)
4. `ORANGE · Pembukaan Ruang Mundur Mangrove` (242 transek)
5. `Restorasi Hidrologis + Sedimen` (187 transek)
6. `YELLOW · Pengayaan Sabuk Hijau` (153 transek)
7. `Lahan Darat (Non-Prioritas)` (132 transek)
8. `Penangkap Sedimen + Lumpur` (125 transek)
9. `Silvofishery Tambak Aktif` (45 transek)
10. `RED · Rekayasa Hibrida` (15 transek)
11. `Restorasi Hidrologis Tambak` (10 transek)

---

## 📁 Struktur Repositori

```text
mangrove/
├── code/                                # Modul Analisis Ilmiah & Pemodelan
│   ├── analisis/
│   │   ├── 01_Eksplorasi_Data.ipynb     # Audit data, kekosongan Sentinel-1/2, harmonisasi
│   │   ├── 02_Analisis_Coastal_Squeeze.ipynb # Kalman filter, regresi WLS, Huber, SIMEX
│   │   ├── muat_data.py                 # Pipeline loader data geospasial & deret waktu
│   │   └── hasil/
│   │       ├── analisis/                # Matriks estimasi, parameter model, Y_bulanan.parquet
│   │       └── dashboard/               # GeoJSON transek, kawasan prioritas, layer_tambahan/
│   └── dataset/                         # Tabel kovariat transek, laju InSAR, barrier, WorldPop
│
├── Dashboard/                           # Aplikasi Web Decision Support System (DSS)
│   ├── app.py                           # Entrypoint Streamlit (Header band & Pill Navigation)
│   ├── theme.py                         # Desain token, palet Coraly-Dark, Google Font Inter
│   ├── components.py                    # Komponen UI modular (Header, KPI Cards, Title Modules)
│   ├── constants.py                     # Nomenklatur kanonik, batas koordinat, angka headline
│   ├── data.py                          # Data loader dengan st.cache_data & GeoPandas
│   ├── maps.py                          # Generator peta Pydeck WebGL GPU-accelerated 50 ms
│   ├── charts.py                        # Generator visualisasi analitis Plotly
│   ├── tab_peta.py                      # Tab 1: Peta Spasial & Tipologi Intervensi
│   ├── tab_dinamika.py                  # Tab 2: Dinamika Tepi Laut & Kausalitas Penggerak
│   ├── tab_kebijakan.py                 # Tab 3: Rencana Aksi Presisi & Simulator What-If
│   ├── assets/
│   │   └── style.css                    # CSS kustom terintegrasi
│   ├── requirements.txt                 # Dependensi pustaka Dashboard
│   └── README.md                        # Dokumentasi teknis Dashboard
│
├── esai_sabuk_hijau.md                  # Naskah lengkap esai ilmiah ASEC 2026
├── requirements.txt                     # Dependensi tingkat root untuk Streamlit Cloud
├── .gitignore                           # Filter file raster/biner besar
└── README.md                            # Dokumentasi utama repositori
```

---

## 💻 Panduan Menjalankan Secara Lokal

### 1. Prasyarat
* Python 3.10 atau versi yang lebih baru.
* Git.

### 2. Instalasi Lingkungan Virtual
```bash
# Kloning repositori
git clone https://github.com/username/mangrove.git
cd mangrove

# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Instal dependensi
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard DSS
```bash
# Dari root repositori
streamlit run Dashboard/app.py

# Atau masuk ke dalam folder Dashboard
cd Dashboard
streamlit run app.py
```
Aplikasi akan otomatis terbuka pada browser di `http://localhost:8501`.

---

## ☁️ Panduan Deploy ke Streamlit Community Cloud

Aplikasi ini sudah **100% siap dideploy** ke [Streamlit Community Cloud](https://share.streamlit.io/) secara gratis:

1. **Pastikan Seluruh Berkas Telah Ter-push ke GitHub**:
   ```bash
   git add .
   git commit -m "feat: perbarui arsitektur dashboard sabuk hijau dan bersihkan berkas lama"
   git push origin main
   ```
2. **Buka Streamlit Cloud**:
   * Kunjungi [share.streamlit.io](https://share.streamlit.io/) dan login menggunakan akun GitHub Anda.
3. **Buat Aplikasi Baru (*Create App*)**:
   * Klik tombol **"Create app"** (atau **"New app"**).
   * Pilih opsi **"I already have an app"**.
4. **Isi Konfigurasi Deployment**:
   * **Repository**: Pilih repositori Anda (contoh: `username/mangrove`).
   * **Branch**: `main`.
   * **Main file path**: Ketik `Dashboard/app.py`.
   * **App URL (opsional)**: Tentukan custom subdomain (contoh: `sabuk-hijau-pantura.streamlit.app`).
5. **Klik "Deploy!"**:
   * Streamlit Cloud akan membaca `requirements.txt`, menginstal dependensi (`geopandas`, `pydeck`, `pyogrio`, dll.), dan menyajikan dashboard dalam waktu 1–2 menit.

---

## 📚 Sitasi & Sumber Data Terbuka

1. **Global Mangrove Watch (GMW v4.0)**: Bunting et al. (2022). *Global Mangrove Extent 1996–2020*.
2. **Laju Amblesan Tanah InSAR**: Ohenhen et al. (2024), dikalibrasi stasiun GNSS Badan Informasi Geospasial (BIG; Susilo et al., 2023).
3. **Kenaikan Muka Air Laut (SLR)**: Kismawardhani et al. (2018) & Altimetri Satelit AVISO.
4. **Laju Akresi Sedimen Pb-210**: Murdiyarso et al. (2018) & Lovelock et al. (2015).
5. **Infrastruktur & Garis Pantai**: OpenStreetMap (OSM) via Overpass API.
6. **Tutupan Lahan Dinamis**: Google Dynamic World & ESA WorldCover 10m.
7. **Model Pasang Surut Global**: Empirical Ocean Tide model (EOT20; Hart-Davis et al., 2021).
8. **Kepadatan Penduduk Pesisir**: WorldPop High Resolution 100m (Proyeksi 2026).

---

*Dikembangkan untuk Airlangga Statistics Essay Competition (ASEC) 2026 — Arsen Universitas Airlangga.*
