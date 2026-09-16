# PANDUAN STRUKTUR FOLDER DATASET CSPI PANTURA
**Kompetisi**: ASEC 2026 — Arsen Unair  
**Karakter Waktu Data**: 100% Mematuhi Aturan 5 Tahun Terakhir (Data Observasi Sensor $\ge 2021$)  
**Tim Peneliti**: Mutia & Reno (Universitas Gadjah Mada)  

---

Folder `Dataset/` telah ditata secara rapi, higienis, dan terstandardisasi ke dalam **4 Subfolder Tematik**:

```text
Dataset/
│
├── 01_Fisik_Hazard/
│   ├── GNSS_Amblesan_Tanah_2021_2022/
│   │   ├── stations_information.txt             <- Metadata koordinat seluruh stasiun GNSS
│   │   ├── CPKL_Pekalongan_2021_2022.rneu       <- Observasi mentah Pekalongan (amblas -9.78 cm/th)
│   │   ├── CSEM_Semarang_2021_2022.rneu         <- Observasi mentah Semarang
│   │   ├── CJPR_Jepara_Kontrol_2021_2022.rneu   <- Observasi mentah Jepara (stabil -0.27 cm/th)
│   │   ├── CCIR_Cirebon_2021_2022.rneu          <- Observasi mentah Cirebon Jabar
│   │   ├── CSBY_Surabaya_2021_2022.rneu         <- Observasi mentah Surabaya Jatim
│   │   ├── Data_Harian_2021_Clean/              <- [HASIL NOTEBOOK 01] CSV harian bersih tahun 2021 per stasiun
│   │   └── Arsip_Lengkap_Stasiun_GNSS_Zenodo/   <- Arsip mentah seluruh 41 stasiun Pantura
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
│   ├── Vektor_Mangrove_GMW/
│   │   ├── mangrove_cirebon_jabar_2020.geojson     <- Poligon mangrove Cirebon
│   │   ├── mangrove_pekalongan_jateng_2020.geojson <- Poligon mangrove Pekalongan (-32.2%)
│   │   ├── mangrove_semarang_demak_2020.geojson    <- Poligon mangrove Semarang-Demak (-77.5 ha)
│   │   ├── mangrove_jepara_kontrol_2020.geojson    <- Poligon mangrove Jepara Kontrol
│   │   ├── mangrove_surabaya_jatim_2020.geojson    <- Poligon mangrove Surabaya Delta
│   │   └── gmw_v3_country_statistics_ha.xlsx       <- Rekap statistik mangrove Indonesia
│   │
│   └── Arsip_Mentah_GMW_Global/                 <- Arsip shapefile global GMW 1996, 2010, 2020
│
├── 03_Raster_Satelit_10m_2021_2024/             <- FILE UTAMA MULTIVARIABEL SATELIT GEE (10m, 16 BAND)
│   ├── CSPI_Full_2021_2024_Cirebon_Jabar.tif    <- 16 Band (Elevasi, Slope, Mangrove 2021, Tambak 2021, Built 2021, Pop 2021, S2 2021-2024, Delta)
│   ├── CSPI_Full_2021_2024_Pekalongan_Jateng.tif<- 16 Band
│   ├── CSPI_Full_2021_2024_Semarang_Demak.tif   <- 16 Band
│   ├── CSPI_Full_2021_2024_Jepara_Kontrol.tif   <- 16 Band
│   ├── CSPI_Full_2021_2024_Surabaya_Jatim.tif   <- 16 Band
│   └── Arsip_Lama_7Band/                        <- Arsip raster lama (7 Band)
│
└── 04_Tabel_Ekstraksi_CSV_Excel/
    ├── 01_gnss_subsidence_rate_2021.csv         <- [HASIL NOTEBOOK 01] Rangkuman laju amblesan GNSS 2021
    ├── 02_mangrove_extent_summary.csv           <- Rangkuman luasan tutupan mangrove
    ├── 03_master_sampled_variables_pantura.csv  <- Master sampel titik pesisir
    └── 04_summary_statistik_5_wilayah.csv       <- Rangkuman statistik agregat 5 wilayah
```

---

### Keterangan 16 Band pada File Raster Satelit `.tif` (Folder 03):
Tiap file `.tif` di folder `03_Raster_Satelit_10m_2021_2024/` memiliki 16 layer variabel komposit multi-temporal seragam beresolusi 10 meter (Dtype: `float32`):
1. **Band 0**: `elevation` (Copernicus DEM 30m)
2. **Band 1**: `slope` (Kemiringan lereng dalam derajat)
3. **Band 2**: `mangrove_2021` (ESA WorldCover 10m tahun 2021, Kelas 95 Mangroves)
4. **Band 3**: `tambak_2021` (ESA WorldCover 10m tahun 2021, Kelas 80 Tambak/Air Tergenang)
5. **Band 4**: `terbangun_2021` (ESA WorldCover 10m tahun 2021, Kelas 50 Lahan Terbangun)
6. **Band 5**: `population_2021` (WorldPop 100m, proyeksi resmi BPS laju pertumbuhan 2021)
7. **Band 6**: `ndvi_2021` (Kerapatan kanopi vegetasi Sentinel-2 Mei–Sep 2021)
8. **Band 7**: `ndmi_2021` (Kadar air tajuk & stres genangan Sentinel-2 Mei–Sep 2021)
9. **Band 8**: `ndvi_2022` (Sentinel-2 Mei–Sep 2022)
10. **Band 9**: `ndmi_2022` (Sentinel-2 Mei–Sep 2022)
11. **Band 10**: `ndvi_2023` (Sentinel-2 Mei–Sep 2023)
12. **Band 11**: `ndmi_2023` (Sentinel-2 Mei–Sep 2023)
13. **Band 12**: `ndvi_2024` (Sentinel-2 Mei–Sep 2024, Kondisi Terkini)
14. **Band 13**: `ndmi_2024` (Sentinel-2 Mei–Sep 2024, Kondisi Terkini)
15. **Band 14**: `delta_ndvi_2021_2024` (Laju perubahan kanopi 3 tahun terakhir: $2024 - 2021$)
16. **Band 15**: `delta_ndmi_2021_2024` (Laju perubahan stres hidrologi 3 tahun terakhir: $2024 - 2021$)
