# PANDUAN STRUKTUR FOLDER DATASET CSPI PANTURA
**Kompetisi**: Airlangga Statistics Essay Competition (ASEC) 2026 — Arsen Unair  
**Karakter Waktu Data**: 100% Mematuhi Aturan 5 Tahun Terakhir (Data Observasi Sensor $\ge 2021$, rentang 2021–2024)  
**Tim Peneliti**: Mutia & Reno (Universitas Gadjah Mada)  
**Terakhir Diperbarui**: September 2026  

---

Folder `Dataset/` dirancang secara komprehensif, modular, higienis, dan terstandardisasi untuk mendukung reproduksibilitas analisis sintesis **Coastal Squeeze Priority Index (CSPI)** pada 5 *nodes* pesisir Pantura Jawa: **Cirebon (Jabar), Pekalongan (Jateng), Semarang–Demak (Jateng), Jepara Kontrol (Jateng), dan Surabaya (Jatim)**.

Berikut adalah diagram hierarki direktori lengkap dan terkini:

```text
Dataset/
│
├── 01_Fisik_Hazard/
│   ├── GNSS_Amblesan_Tanah_2021_2022/
│   │   ├── stations_information.txt             <- Metadata koordinat dan profil 41 stasiun GNSS CORS Pantura
│   │   ├── CCIR_Cirebon_2021_2022.rneu          <- Observasi harian koordinat rneu stasiun Cirebon (CCIR/CCPK)
│   │   ├── CPKL_Pekalongan_2021_2022.rneu       <- Observasi harian Pekalongan (laju amblesan kritis -9.78 cm/th)
│   │   ├── CSEM_Semarang_2021_2022.rneu         <- Observasi harian Semarang (laju amblesan -4.50 cm/th)
│   │   ├── CJPR_Jepara_Kontrol_2021_2022.rneu   <- Observasi harian Jepara Kontrol (stabil -0.27 cm/th)
│   │   ├── CSBY_Surabaya_2021_2022.rneu         <- Observasi harian Surabaya (laju amblesan -0.74 cm/th)
│   │   ├── Data_Harian_2021_Clean/              <- [OUTPUT NOTEBOOK 01] CSV harian bersih tahun 2021 per stasiun
│   │   │   ├── GNSS_Clean_2021_CCIR_Cirebon.csv
│   │   │   ├── GNSS_Clean_2021_CPKL_Pekalongan.csv
│   │   │   ├── GNSS_Clean_2021_CSEM_Semarang.csv
│   │   │   ├── GNSS_Clean_2021_CJPR_Jepara.csv
│   │   │   └── GNSS_Clean_2021_CSBY_Surabaya.csv
│   │   └── Arsip_Lengkap_Stasiun_GNSS_Zenodo/   <- Arsip mentah seluruh 41 stasiun GNSS Pantura Jawa
│   │
│   └── Garis_Pantai_Coastline/
│       ├── coastline_cirebon_jabar.geojson      <- Garis pantai Cirebon WGS84
│       ├── coastline_pekalongan_jateng.geojson  <- Garis pantai Pekalongan WGS84
│       ├── coastline_semarang_demak.geojson     <- Garis pantai Semarang-Demak WGS84
│       ├── coastline_jepara_kontrol.geojson     <- Garis pantai Jepara WGS84
│       ├── coastline_surabaya_jatim.geojson     <- Garis pantai Surabaya WGS84
│       └── Arsip_Mentah_OSM_Global/             <- Arsip shapefile global OpenStreetMap
│
├── 02_Ekologis_Mangrove/
│   ├── GMW_v4112_Annual_1985_2025/              <- [CORE NOTEBOOK 02] Raster GMW v4.1.12 Tahunan (2021–2024)
│   │   ├── GMW_S07E108_v4112_mng_*.tif          <- Tile ubin pesisir Cirebon Jawa Barat
│   │   ├── GMW_S07E109_v4112_mng_*.tif          <- Tile ubin pesisir Pekalongan Jawa Tengah
│   │   ├── GMW_S07E110_v4112_mng_*.tif          <- Tile ubin pesisir Semarang–Demak & Jepara
│   │   └── GMW_S08E112_v4112_mng_*.tif          <- Tile ubin pesisir Surabaya Jawa Timur
│   ├── Vektor_Mangrove_GMW/
│   │   ├── mangrove_cirebon_jabar_2020.geojson     <- Poligon mangrove Cirebon
│   │   ├── mangrove_pekalongan_jateng_2020.geojson <- Poligon mangrove Pekalongan
│   │   ├── mangrove_semarang_demak_2020.geojson    <- Poligon mangrove Semarang-Demak
│   │   ├── mangrove_jepara_kontrol_2020.geojson    <- Poligon mangrove Jepara Kontrol
│   │   ├── mangrove_surabaya_jatim_2020.geojson    <- Poligon mangrove Surabaya Delta
│   │   └── gmw_v3_country_statistics_ha.xlsx       <- Rekap statistik nasional mangrove Indonesia
│   └── Arsip_Mentah_GMW_Global/                 <- Arsip shapefile global GMW v3 (1996, 2010, 2020)
│
├── 03_Raster_Satelit_10m_2021_2024/             <- MASTER DATASET SATELIT GEE (Resolusi 10 Meter, 16 Band Float32)
│   ├── CSPI_Full_2021_2024_Cirebon_Jabar.tif    <- 16 Band Multitemporal (376 MB)
│   ├── CSPI_Full_2021_2024_Pekalongan_Jateng.tif<- 16 Band Multitemporal (164 MB)
│   ├── CSPI_Full_2021_2024_Semarang_Demak.tif   <- 16 Band Multitemporal (323 MB)
│   ├── CSPI_Full_2021_2024_Jepara_Kontrol.tif   <- 16 Band Multitemporal (210 MB)
│   ├── CSPI_Full_2021_2024_Surabaya_Jatim.tif   <- 16 Band Multitemporal (483 MB)
│   └── Arsip_Lama_7Band/                        <- Arsip raster iterasi awal (7 Band)
│
├── 04_Tabel_Ekstraksi_CSV_Excel/                <- [OUTPUT EKSTRAKSI LENGKAP 4 NOTEBOOK]
│   ├── 01_gnss_subsidence_rate_2021.csv         <- [Notebook 01] Regresi laju amblesan GNSS CORS (mm/th & cm/th)
│   ├── 02_gmw_annual_mangrove_extent_2021_2024.csv <- [Notebook 02] Luas mangrove tahunan GMW v4.1.12 (2021-2024)
│   ├── 02_mangrove_extent_and_health_2021_2024.csv <- [Notebook 02] Metrik kanopi Sentinel-2 (NDVI, NDMI, Luas Patch)
│   ├── 02_mangrove_extent_summary.csv           <- [Notebook 02] Ringkasan fragmen poligon mangrove
│   ├── 03_antropogenik_dan_demografi_2021_2024.csv <- [Notebook 03] Barrier squeeze (Terbangun, Tambak, Populasi BPS)
│   ├── 03_master_sampled_variables_pantura.csv  <- [Notebook 03] Master geospasial sampel piksel pesisir Pantura (5 MB)
│   ├── 04_master_sintesis_cspi_pantura_2021_2024.csv <- [Notebook 04] Grand Sintesis Skor CSPI & Sub-Indeks 5 Wilayah
│   └── 04_summary_statistik_5_wilayah.csv       <- [Notebook 04] Ringkasan statistik agregat komparatif 5 wilayah
│
└── Penduduk/                                    <- DATA RESMI BPS JAWA BARAT, JAWA TENGAH, & JAWA TIMUR (2021–2024)
    ├── _Jumlah Penduduk menurut Kabupaten_Kota dan Kelompok Umur, 2021.csv
    ├── _Jumlah Penduduk menurut Kabupaten_Kota dan Kelompok Umur, 2022.csv
    ├── _Jumlah Penduduk menurut Kabupaten_Kota dan Kelompok Umur, 2023.csv
    ├── _Jumlah Penduduk menurut Kabupaten_Kota dan Kelompok Umur, 2024.csv
    ├── Penduduk, Laju Pertumbuhan Penduduk, ... Provinsi Jawa Barat, 2021-2023.xlsx
    ├── Penduduk, Laju Pertumbuhan Penduduk, ... Provinsi Jawa Tengah, 2021-2023.xlsx
    ├── Penduduk, Laju Pertumbuhan Penduduk, ... Provinsi Jawa Timur, 2021-2023.xlsx
    └── Penduduk, Laju Pertumbuhan Penduduk, ... 2024.xlsx
```

---

## Spesifikasi 16 Band pada File Master Raster Satelit `.tif` (Folder 03)

Seluruh file GeoTIFF di dalam `03_Raster_Satelit_10m_2021_2024/` diekspor langsung melalui *cloud-computing platform* Google Earth Engine menggunakan skrip [Codes/GEE_Script_CSPI_Harmonized_2021_2024.js](file:///d:/Kuliah/Lomba/ASEC%20Arsen%20Unair%202026/Codes/GEE_Script_CSPI_Harmonized_2021_2024.js) dengan resolusi spasial seragam **10 meter** dan tipe data **`Float32`**:

| Band Index | Nama Band | Sumber Satelit / Sensor | Deskripsi & Satuan |
| :---: | :--- | :--- | :--- |
| **0** | `elevation` | Copernicus DEM GLO-30 (30 m resampled to 10 m) | Elevasi topografi di atas permukaan laut (meter DPL) |
| **1** | `slope` | Diturunkan dari Copernicus DEM (`ee.Terrain.slope`) | Kemiringan lereng pesisir (derajat, $0^\circ - 90^\circ$) |
| **2** | `mangrove_2021` | ESA WorldCover 10m v200 (Kelas 95) | Masking biner tutupan mangrove ($1 = \text{Mangrove}$, $0 = \text{Lainnya}$) |
| **3** | `tambak_2021` | ESA WorldCover 10m v200 (Kelas 80) | Barrier akuakultur/tambak air tergenang ($1 = \text{Tambak}$, $0 = \text{Lainnya}$) |
| **4** | `terbangun_2021`| ESA WorldCover 10m v200 (Kelas 50) | Barrier antropogenik lahan terbangun/urban ($1 = \text{Built-up}$, $0 = \text{Lainnya}$) |
| **5** | `population_2021`| WorldPop 100m terkoreksi laju BPS | Estimasi densitas penduduk spasial tahun 2021 (jiwa per piksel) |
| **6** | `ndvi_2021` | Sentinel-2 MSI Level-2A (SR) Komposit Kemarau 2021 | Indeks vegetasi kehijauan kanopi: $(B8 - B4) / (B8 + B4)$ |
| **7** | `ndmi_2021` | Sentinel-2 MSI Level-2A (SR) Komposit Kemarau 2021 | Indeks kelembapan & kadar air tajuk: $(B8 - B11) / (B8 + B11)$ |
| **8** | `ndvi_2022` | Sentinel-2 MSI Level-2A (SR) Komposit Kemarau 2022 | Indeks kehijauan kanopi tahun 2022 |
| **9** | `ndmi_2022` | Sentinel-2 MSI Level-2A (SR) Komposit Kemarau 2022 | Indeks kadar air tajuk tahun 2022 |
| **10** | `ndvi_2023` | Sentinel-2 MSI Level-2A (SR) Komposit Kemarau 2023 | Indeks kehijauan kanopi tahun 2023 |
| **11** | `ndmi_2023` | Sentinel-2 MSI Level-2A (SR) Komposit Kemarau 2023 | Indeks kadar air tajuk tahun 2023 |
| **12** | `ndvi_2024` | Sentinel-2 MSI Level-2A (SR) Komposit Kemarau 2024 | Indeks kehijauan kanopi kondisi terkini tahun 2024 |
| **13** | `ndmi_2024` | Sentinel-2 MSI Level-2A (SR) Komposit Kemarau 2024 | Indeks kadar air tajuk kondisi terkini tahun 2024 |
| **14** | `delta_ndvi_2021_2024` | Selisih Temporal Komposit: $NDVI_{2024} - NDVI_{2021}$ | Tren laju dinamika kesehatan kanopi 3 tahun terakhir |
| **15** | `delta_ndmi_2021_2024` | Selisih Temporal Komposit: $NDMI_{2024} - NDMI_{2021}$ | Tren laju dinamika stres hidrologi tajuk 3 tahun terakhir |

---

## Ringkasan Hasil Ekstraksi Utama per Node Pantura

Berdasarkan dataset ekstraksi terpadu pada `04_Tabel_Ekstraksi_CSV_Excel/04_master_sintesis_cspi_pantura_2021_2024.csv`:

1. **Pekalongan (Jateng)**:
   - Amblesan Tanah: **-9.78 cm/tahun** ($R^2 = 0.999$, $p < 0.001$, kritis).
   - Barrier Lahan: Total barrier **59.23%** (Tambak 39.35% + Terbangun 19.87%).
   - Dinamika Mangrove (GMW): **-10.02 Ha (-15.4%)** dalam 3 tahun (2021: 65.07 Ha $\to$ 2024: 55.05 Ha).
   - **Skor CSPI: 0.8388** *(Prioritas Sangat Tinggi / Critical Squeeze Epicenter)*.

2. **Cirebon (Jabar)**:
   - Amblesan Tanah: **-1.22 cm/tahun**.
   - Barrier Lahan: Total barrier **55.02%** (Tambak 40.19% + Terbangun 14.83%).
   - Dinamika Mangrove (GMW): Penurunan **-10.59 Ha (-8.2%)** (2021: 128.60 Ha $\to$ 2024: 118.01 Ha).
   - **Skor CSPI: 0.2783** *(Prioritas Sedang / Fragmented Aquaculture Buffer)*.

3. **Semarang–Demak (Jateng)**:
   - Amblesan Tanah: **-4.50 cm/tahun** (Signifikan, $p < 0.001$).
   - Barrier Lahan: Total barrier tertinggi Pantura **79.57%** (Didominasi Tambak 70.00% + Terbangun 9.57%).
   - Dinamika Mangrove (GMW): Penurunan **-12.78 Ha (-8.5%)** (2021: 149.99 Ha $\to$ 2024: 137.21 Ha).
   - **Skor CSPI: 0.2680** *(Prioritas Sedang / Aquaculture-Dominated Squeeze)*.

4. **Surabaya (Jatim)**:
   - Amblesan Tanah: **-0.74 cm/tahun** (Relatif stabil).
   - Barrier Lahan: Total barrier **55.79%** (Terbangun tinggi 23.50% + Tambak 32.29%).
   - Dinamika Mangrove (GMW): Paling stabil dan luas, ekspansi **+12.63 Ha (+0.8%)** (2021: 1,607.72 Ha $\to$ 2024: 1,620.35 Ha).
   - **Skor CSPI: 0.1954** *(Prioritas Rendah / Resilient Delta Belt)*.

5. **Jepara Kontrol (Jateng)**:
   - Amblesan Tanah: **-0.27 cm/tahun** (Baseline kontrol geologis stabil).
   - Barrier Lahan: Total barrier terendah **48.61%** (Tambak 40.81% + Terbangun 7.81%).
   - Dinamika Mangrove (GMW): Stabil **-0.66 Ha (-1.2%)** (2021: 54.26 Ha $\to$ 2024: 53.60 Ha).
   - **Skor CSPI: 0.0831** *(Prioritas Rendah / Baseline Control)*.
