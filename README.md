# CSPI Pantura Jawa Grand Synthesis (2021–2024)
### *Coastal Squeeze Priority Index* Pantura Jawa: Integrasi Geospasial Multidimensi & Statistika Spasial
**Airlangga Statistics Essay Competition (ASEC) 2026 — Arsen Universitas Airlangga**  
**Tim Peneliti**: Mutia & Reno (Universitas Gadjah Mada)  
**Kepatuhan Temporal**: 100% Menggunakan Data Observasi 5 Tahun Terakhir ($\ge 2021$)

---

## 🌊 Ringkasan Proyek
Penelitian ini mengembangkan indeks komposit terintegrasi bernama **Coastal Squeeze Priority Index (CSPI)** untuk memetakan, mengkuantifikasi, dan menyusun prioritas mitigasi fenomena *coastal squeeze* di sepanjang Pantai Utara (Pantura) Jawa. Mangrove Pantura terjepit di antara ancaman laut (*seaward hazard* berupa amblesan tanah vertikal & abrasi) dan batas keras darat (*landward barrier* berupa pemukiman padat & tambak intensif).

Penelitian berfokus pada 5 simpul strategis pesisir Pantura:
1. **Cirebon (Jawa Barat)**: Dominasi tambak intensif dan keterbatasan ruang mangrove.
2. **Pekalongan (Jawa Tengah)**: **Episentrum Kritis Tertinggi** (Amblesan tanah ekstrem -9,78 cm/tahun & degradasi kanopi $\Delta\text{NDVI} = -0,119$).
3. **Semarang - Demak (Jawa Tengah)**: Penjepitan tambak budidaya raksasa (70% wilayah pesisir) dan rob Sayung.
4. **Surabaya (Jawa Timur)**: Sabuk muara delta terluas (1.772 Ha) dengan ketahanan kanopi alami.
5. **Jepara (Jawa Tengah)**: Garis pantai batuan Muria stabil (+0,05 cm/tahun) sebagai **Zona Kontrol Alami (*Baseline Control*)**.

---

## 📁 Struktur Repositori

```text
├── Codes/
│   ├── GEE_Script_CSPI_Harmonized_2021_2024.js   # Skrip Google Earth Engine komposit 16-band 10m
│   ├── notebooks/                                # 4 Notebook Modular Ter-Render Penuh
│   │   ├── 01_Ekstraksi_Dataset_Fisik_dan_Hazard.ipynb
│   │   ├── 02_Ekstraksi_Dataset_Ekologis_Mangrove.ipynb
│   │   ├── 03_Ekstraksi_Dataset_Antropogenik_Penduduk.ipynb
│   │   └── 04_Sintesis_Grand_CSPI_dan_Analisis_Statistik.ipynb
│   └── Outputs/
│       ├── Visualisasi/                          # 10 Gambar Publikasi Ilmiah 300 DPI
│       └── Statistik/                            # 7 Tabel Uji Statistik & Metrik (CSV)
│
├── Dataset/
│   ├── 01_Fisik_Hazard/                          # Data GNSS CORS Clean & GeoJSON Garis Pantai
│   ├── 02_Ekologis_Mangrove/                     # Metadata & Vektor Mangrove
│   ├── 04_Tabel_Ekstraksi_CSV_Excel/             # 5 Master Tabel Ekstraksi CSV
│   ├── Penduduk/                                 # Data Kependudukan Resmi BPS (2021-2024)
│   └── README_STRUKTUR_DATASET.md                # Dokumentasi Detail Dataset
│
├── .gitignore                                    # Pengecualian file raster besar (>100MB)
└── README.md
```

---

## 🔬 Metodologi & Tiga Pilar Operasional

### 1. Pilar 1: Fisik & Hazard Pesisir
- **Data**: Pengamatan harian 365 hari stasiun GNSS CORS Badan Informasi Geospasial (BIG) tahun 2021.
- **Hasil**: Regresi OLS membuktikan amblesan Pekalongan mencapai **-9,78 cm/tahun** ($R^2 = 0,90$, $p = 3,38 \times 10^{-182}$).

### 2. Pilar 2: Ekologis Mangrove (*Dual-Dataset Validation*)
- **Data**: *Global Mangrove Watch* (GMW v4.1.12) tahun 2021–2024 dan ESA WorldCover 10m.
- **Hasil**: Sensor 10m mendeteksi 126,36 Ha mangrove Pekalongan terfragmentasi menjadi 168 rumpun kecil (< 0,75 Ha) dengan klorofil tajuk anjlok drastis ($\Delta\text{NDVI} = -0,119$).

### 3. Pilar 3: Antropogenik & Kependudukan
- **Data**: Data resmi kependudukan BPS Kabupaten/Kota (2021–2024) dan klasifikasi lahan ESA WorldCover 10m (Class 50: Terbangun, Class 80: Tambak).
- **Hasil**: Semarang-Demak terkunci 70,00% tambak budidaya; Surabaya memiliki konsentrasi terbangun tertinggi (23,50% atau 21.861 Ha).

---

## 🏆 Hasil Peringkat CSPI & Uji Hipotesis Inferensial

- **Analytical Hierarchy Process (AHP)**:
  - Bobot: Amblesan (36,83%), Degradasi NDVI (20,64%), Fragmentasi (20,64%), Terbangun (10,94%), Tambak (10,94%).
  - **Consistency Ratio ($CR$) = 0,0030 (0,30% $\ll$ 10%)** $\to$ Terbukti konsisten.

| Peringkat | Wilayah | Skor CSPI | Kategori Prioritas |
| :---: | :--- | :---: | :--- |
| **1** | **Pekalongan (Jateng)** | **0,8388** | **Prioritas Sangat Tinggi (Episentrum Kritis)** |
| **2** | **Cirebon (Jabar)** | **0,2783** | Prioritas Menengah (Terjepit Parsial) |
| **3** | **Semarang - Demak (Jateng)** | **0,2680** | Prioritas Menengah (Terjepit Parsial) |
| **4** | **Surabaya (Jatim)** | **0,1954** | Prioritas Rendah (Sabuk Kontrol Resilien) |
| **5** | **Jepara Kontrol (Jateng)** | **0,0831** | Prioritas Rendah (Zona Kontrol Stabil) |

- **Uji Kruskal-Wallis ($N = 69.567$)**:
  - $H = 26.667,61$, $p < 0,0001$ (Signifikan Sangat Nyata).
  - Post-Hoc Dunn's Test membuktikan Pekalongan berbeda signifikan terhadap seluruh wilayah ($p < 0,0001$).

---

## 💻 Cara Menjalankan Notebook
1. Pastikan Python 3.9+ telah terinstal beserta dependencies:
   ```bash
   pip install numpy pandas scipy matplotlib tifffile
   ```
2. Buka folder proyek di Jupyter Lab / VS Code dan jalankan notebook secara berurutan:
   - `Codes/notebooks/01_Ekstraksi_Dataset_Fisik_dan_Hazard.ipynb`
   - `Codes/notebooks/02_Ekstraksi_Dataset_Ekologis_Mangrove.ipynb`
   - `Codes/notebooks/03_Ekstraksi_Dataset_Antropogenik_Penduduk.ipynb`
   - `Codes/notebooks/04_Sintesis_Grand_CSPI_dan_Analisis_Statistik.ipynb`
