# Panduan Lengkap Akuisisi Data CSPI Pantura Jawa
**Kompetisi**: Airlangga Statistics Essay Competition (ASEC) 2026 — Arsen Unair  
**Topik**: *Coastal Squeeze Priority Index* (CSPI) untuk Konservasi Mangrove Pantura Jawa  
**Penyusun**: Tim Mutia & Reno (UGM)  

---

## 1. Matriks Kebutuhan Data (Data Requirement Matrix)

Seluruh data yang digunakan dalam analisis CSPI adalah **100% data terbuka (Open Source)** sesuai dengan regulasi ASEC 2026.

| No | Nama Dataset | Penyedia / Institusi | Variabel yang Diekstrak | Resolusi Spasial & Format | Rentang Waktu (Epoch) | Guna / Fungsi dalam CSPI |
|---|---|---|---|---|---|---|
| **1** | **Global Mangrove Watch (GMW)** | UNEP-WCMC & JAXA | • Luasan mangrove historis<br>• Laju kehilangan mangrove (%/th) | Vektor Polygon (Shapefile / GeoJSON) | 1996, 2010, 2016, 2020 (Multi-dekade) | **Dimensi Ekologis**: Menghitung tren kehilangan kanopi mangrove via Mann-Kendall & Sen's Slope. |
| **2** | **Sentinel-2 MSI Level-2A** | European Space Agency (Copernicus) | • Indeks Vegetasi (NDVI)<br>• Indeks Kelembapan (NDMI) | Raster 10 m (GeoTIFF, Band 4, 8, 11) | 2023–2024 (Komposit bebas awan <10%) | **Dimensi Ekologis**: Mengukur kerapatan kanopi dan tingkat stres fisiologis mangrove akibat intrusi/genangan. |
| **3** | **DEMNAS (Digital Elevation Model Nasional)** | Badan Informasi Geospasial (BIG) | • Elevasi buffer darat (m)<br>• Kemiringan lereng (*slope*, %) | Raster 0,27 arcsecond (~8,1 meter) GeoTIFF | Pemutakhiran terkini (Baseline nasional) | **Dimensi Antropogenik**: Mengukur ketersediaan ruang akomodasi alami daratan (*accommodation space* untuk migrasi mundur). |
| **4** | **ESA WorldCover 10 m** | European Space Agency (ESA) | • Proporsi tambak/air tergenang (%)<br>• Proporsi area terbangun (%) | Raster 10 m (GeoTIFF) | 2021 (v200) | **Dimensi Antropogenik**: Mengidentifikasi hambatan fisik buatan (*hard barriers*) yang memblokir mangrove. |
| **5** | **WorldPop Indonesia** | WorldPop (Univ. of Southampton) | • Kepadatan penduduk pesisir (jiwa/pixel 100m) | Raster 100 m (GeoTIFF) | 2020 (Constrained) | **Dimensi Antropogenik**: Menilai intensitas tekanan antropogenik di zona penyangga pesisir. |
| **6** | **Garis Pantai & Shoreline Change** | CoastSat (Python) / Ina-Geoportal BIG | • Posisi garis pantai multi-waktu<br>• End Point Rate (EPR, m/th)<br>• Linear Regression Rate (LRR, m/th) | Vektor Garis & Transekt 100–250 m | 2015 s.d. 2024/2026 | **Dimensi Fisik**: Mengukur laju kemunduran pantai akibat abrasi dan gelombang laut. |
| **7** | **Laju Amblesan Tanah (Land Subsidence)** | PATGL Badan Geologi ESDM & Publikasi InSAR (BRIN/ITB) | • Laju penurunan muka tanah (*subsidence rate*, cm/th) | Titik/Vektor diinterpolasi Kriging ke Raster 30 m | 2015–2024 (Rerata dekade terakhir) | **Dimensi Fisik (KUNCI)**: Mengukur laju tenggelamnya substrat mangrove yang memperparah genangan pasang surut. |
| **8** | **Kenaikan Muka Laut (Relative Sea Level Rise)** | Copernicus Marine Service (CMEMS) / AVISO | • Laju kenaikan muka laut absolut (mm/th)<br>• Sea Level Anomaly (SLA) | Gridded altimetri 0.25° | 1993–2024 | **Dimensi Fisik**: Komponen pemicu *seaward pressure* saat digabungkan dengan amblesan lokal. |

---

## 2. Rincian Data & Panduan Cara Unduh (Step-by-Step)

### A. Data Ekologis: Global Mangrove Watch (GMW v3.0)
* **Deskripsi**: Peta sebaran dan luasan hutan mangrove global resolusi 25 meter dari satelit ALOS PALSAR dan Landsat.
* **Guna dalam CSPI**: Menghitung luasan historis mangrove pada tiap segmen transekt, mendeteksi area deforestasi/kematian mangrove, dan menghitung Sen's slope laju penyusutan mangrove.
* **Direct Link & Cara Unduh**:
  1. Kunjungi portal resmi UNEP-WCMC:  
     👉 [UNEP-WCMC GMW Dataset](https://data.unep-wcmc.org/datasets/45)
  2. Klik tombol biru **"Download Dataset"**.
  3. Pilih format **Shapefile (.zip)** atau **GeoPackage**.
  4. Didalam file zip terdapat folder tahun: `gmw_v3_1996`, `gmw_v3_2010`, `gmw_v3_2016`, `gmw_v3_2020`.
  5. *Alternatif Cepat*: Menggunakan repositori Zenodo resmi: [Zenodo GMW v3.0](https://zenodo.org/records/6894273).

---

### B. Data Fisik: DEMNAS (Digital Elevation Model Nasional) BIG
* **Deskripsi**: DEM resmi Indonesia dari Badan Informasi Geospasial dengan resolusi spasial ultra-tinggi (~8,1 meter per piksel) menggunakan integrasi IFSAR, Terrasar-X, dan ALOS PALSAR. Jauh lebih presisi dari SRTM 30 m untuk pesisir Pantura yang sangat landai.
* **Guna dalam CSPI**: 
  1. Menghitung kelerengan (*slope*) zona buffer darat 500 m – 1 km di belakang mangrove. Jika lereng landai (<2°) dan elevasi <1 m DPL, mangrove punya potensi mundur (migrasi darat). Jika lereng terjal atau terhalang tanggul, ruang akomodasi = 0 (*squeezed*).
* **Direct Link & Cara Unduh**:
  1. Buka portal resmi Ina-Geoportal:  
     👉 [Portal DEMNAS BIG](https://tanahair.indonesia.go.id/demnas/#/)
  2. Lakukan login gratis (bisa daftar akun dalam 1 menit).
  3. Klik menu **"Download DEMNAS"** di bilah navigasi atas.
  4. Arahkan peta ke pesisir Jawa Tengah (Demak – Semarang – Pekalongan).
  5. Klik pada grid kotak lembar peta wilayah kajian:
     - **Semarang & Demak**: Lembar `DEMNAS_1409-11` s.d. `DEMNAS_1409-14`.
     - **Pekalongan**: Lembar `DEMNAS_1309-64` s.d. `DEMNAS_1409-41`.
  6. Klik tombol **"Unduh"** (File langsung terunduh dalam format `.tif` GeoTIFF).

---

### C. Data Antropogenik: ESA WorldCover 10 m (2021)
* **Deskripsi**: Peta tutupan lahan global resolusi tinggi 10 meter hasil klasifikasi satelit Sentinel-1 dan Sentinel-2 oleh European Space Agency (ESA).
* **Guna dalam CSPI**:
  1. Mengekstrak tutupan lahan di zona penyangga darat 500 m – 1 km di belakang mangrove.
  2. Menghitung persentase **Kelas 80 (Permanent water bodies / tambak intensif)** dan **Kelas 50 (Built-up / permukiman & industri pesisir)** sebagai indikator rintangan keras manusia (*hard barrier*).
* **Direct Link & Cara Unduh**:
  1. Akses portal data resmi ESA WorldCover:  
     👉 [ESA WorldCover Data Access](https://esa-worldcover.org/en/data-access)
  2. Buka tab **"AWS S3 / Zenodo Direct Download"** atau via Zenodo:  
     👉 [Zenodo ESA WorldCover 2021 v200](https://zenodo.org/records/7254221)
  3. Cari nama tile untuk wilayah Jawa Tengah (koordinat sekitar S07 E110):
     - File: `ESA_WorldCover_10m_2021_v200_S09E108_MAP.tif` (area Jawa Barat - Tengah)
     - File: `ESA_WorldCover_10m_2021_v200_S09E111_MAP.tif` (area Jawa Tengah - Timur)
  4. Klik langsung nama file `.tif` tersebut untuk direct download.

---

### D. Data Antropogenik: WorldPop Indonesia 100m (Kepadatan Penduduk)
* **Deskripsi**: Estimasi jumlah penduduk berbasis raster resolusi 100 meter yang disesuaikan dengan data sensus BPS dan bangunan pemukiman (constrained).
* **Guna dalam CSPI**: Menilai beban antropogenik di pesisir (tekanan eksploitasi air tanah dan konversi lahan).
* **Direct Download Link**:
  - Link Halaman: [WorldPop Summary ID 44750](https://hub.worldpop.org/geodata/summary?id=44750)
  - **Direct Download Link (File GeoTIFF, ~65 MB)**:  
    👉 `https://data.worldpop.org/GIS/Population/Global_2000_2020_100m/2020/IDN/idn_ppp_2020_100m_constrained.tif`  
    *(Tinggal copy-paste link ini ke browser atau download manager untuk langsung mengunduh file TIFF).*

---

### E. Data Ekologis: Citra Satelit Sentinel-2 (NDVI & NDMI)
* **Deskripsi**: Citra multispektral 10 m untuk analisis kanopi mangrove.
  - $\text{NDVI} = \frac{\text{B8} - \text{B4}}{\text{B8} + \text{B4}}$ (Kerapatan kanopi hijau).
  - $\text{NDMI} = \frac{\text{B8} - \text{B11}}{\text{B8} + \text{B11}}$ (Kandungan air dan kelembapan tajuk).
* **Guna dalam CSPI**: Mengukur vitalitas dan degradasi kanopi mangrove di tiap segmen transekt.
* **Cara Unduh via Copernicus Browser**:
  1. Kunjungi portal resmi: 👉 [Copernicus Data Space Browser](https://browser.dataspace.copernicus.eu/)
  2. Buat akun gratis dan login.
  3. Kotak pencarian: ketik `Semarang, Indonesia` atau `Demak, Indonesia`.
  4. Di bilah kiri, centang **Sentinel-2 L2A**.
  5. Filter tanggal: **01 Juni 2024 s.d. 30 September 2024** (pilih musim kemarau agar bebas awan < 10%).
  6. Pilih citra terbaik (cloud cover terendah), klik tab **Download** untuk mengunduh Band 4 (Red), Band 8 (NIR), dan Band 11 (SWIR).
  7. *Tips Cepat*: Menggunakan script Python GEE (disediakan di Bagian 3) agar tidak perlu mengunduh gigabyte citra mentah.

---

### F. Data Fisik: Laju Amblesan Tanah (Land Subsidence)
* **Deskripsi**: Data kecepatan penurunan tanah di Pantura Jawa (cm/tahun).
* **Sumber Kredibel & Open-Access**:
  1. **Laporan & Publikasi PATGL Badan Geologi Kementerian ESDM**:
     - Publikasi resmi Kementerian ESDM: [Kajian Amblesan Pesisir Utara Jawa Tengah](https://esdm.go.id/id/media-center/arsip-berita/ini-penyebab-terjadinya-penurunan-tanah-di-pesisir-utara-jawa-tengah)
  2. **Data Ground-Truth & InSAR Publikasi Ilmiah (BRIN / ITB / Open Data)**:
     - Rerata laju penurunan tanah per kawasan (2018–2024):
       * **Kecamatan Sayung & Sriwulan (Demak)**: $10{,}5 \text{ s.d. } 16{,}2\text{ cm/tahun}$
       * **Semarang Utara & Genuk**: $7{,}8 \text{ s.d. } 13{,}5\text{ cm/tahun}$
       * **Pekalongan Utara (Tirto & Wonokerto)**: $6{,}2 \text{ s.d. } 12{,}0\text{ cm/tahun}$
       * **Jepara & Kendal**: $1{,}0 \text{ s.d. } 3{,}5\text{ cm/tahun}$
  3. **Cara Penggunaan**: Titik-titik laju amblesan dari stasiun GNSS geodetik Badan Geologi dan sampel titik InSAR literatur dimasukkan ke QGIS/Python, lalu dibuatkan raster interpolasi kontinu menggunakan metode **Ordinary Kriging** atau **Inverse Distance Weighted (IDW)** dengan grid 30 meter.

---

### G. Data Fisik: Perubahan Garis Pantai & CoastSat
* **Deskripsi**: Ekstraksi garis pantai multi-temporal dari citra satelit resolusi menengah untuk menghitung laju abrasi/akresi (*End Point Rate* / *Linear Regression Rate*).
* **Toolkit Open-Source (Python)**:
  - Repositori GitHub: 👉 [kvos/CoastSat](https://github.com/kvos/CoastSat)
  - CoastSat mengambil citra Sentinel-2 / Landsat otomatis via Google Earth Engine API, mendeteksi garis air pada skala sub-piksel menggunakan MNDWI, dan menghitung pergeseran garis pantai pada transekt yang ditentukan.
* **Alternatif Format Vektor Siap Pakai**:
  - Garis Pantai Indonesia (GPI) multi-tahun dari [Ina-Geoportal TanahAir BIG](https://tanahair.indonesia.go.id/portal-web).

---

## 3. Jalur Cepat (Pro-Tip): Skrip Otomasi Google Earth Engine (GEE)

Untuk menghemat waktu kamu dan Mutia (agar tidak perlu mengunduh file bergiga-giga dan menghabiskan kuota atau memori laptop), seluruh ekstraksi variabel raster (GMW, ESA WorldCover, NDVI/NDMI Sentinel-2, dan Copernicus DEM) dapat diproses dan diekspor dalam 1 kali jalan menggunakan skrip Google Earth Engine berikut:

```javascript
// =========================================================================
// SKRIP EKSTRAKSI VARIABEL CSPI PANTURA JAWA TENGAH (DEMAK - SEMARANG)
// Buka di: https://code.earthengine.google.com/
// =========================================================================

// 1. Definisikan Wilayah Kajian (Pesisir Demak - Semarang)
var roi = ee.Geometry.Polygon([
  [[110.30, -6.98],
   [110.60, -6.98],
   [110.60, -6.80],
   [110.30, -6.80]]
]);
Map.centerObject(roi, 11);

// 2. Data Elevasi: Copernicus DEM 30m
var dem = ee.ImageCollection('COPERNICUS/DEM/GLO30')
            .filterBounds(roi)
            .select('DEM')
            .mean()
            .clip(roi);
var slope = ee.Terrain.slope(dem);

// 3. Tutupan Lahan: ESA WorldCover 10m (2021)
var worldcover = ee.ImageCollection('ESA/WorldCover/v200')
                   .first()
                   .select('Map')
                   .clip(roi);
// Masking Tambak/Air (80) dan Pemukiman/Terbangun (50)
var tambak = worldcover.eq(80).rename('tambak');
var terbangun = worldcover.eq(50).rename('terbangun');

// 4. Mangrove: Global Mangrove Watch 2020
// Mengambil dataset komunitas GMW
var gmw2020 = ee.ImageCollection("projects/sat-io/open-datasets/GMW/GMW_2020_v3")
                .mosaic()
                .clip(roi)
                .rename('mangrove_gmw');

// 5. Kesehatan Kanopi: Sentinel-2 L2A Bebas Awan (2024)
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
           .filterBounds(roi)
           .filterDate('2024-05-01', '2024-09-30')
           .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
           .median()
           .clip(roi);

var ndvi = s2.normalizedDifference(['B8', 'B4']).rename('ndvi');
var ndmi = s2.normalizedDifference(['B8', 'B11']).rename('ndmi');

// 6. Visualisasi di Map Canvas
Map.addLayer(dem, {min: 0, max: 20, palette: ['blue', 'green', 'yellow']}, 'DEM 30m');
Map.addLayer(worldcover, {}, 'ESA WorldCover 10m');
Map.addLayer(ndvi, {min: 0, max: 0.8, palette: ['white', 'yellow', 'green']}, 'NDVI Mangrove 2024');

// 7. Ekspor Hasil Komposit Variabel ke Google Drive
var stack = ee.Image.cat([dem.rename('elevation'), slope.rename('slope'), tambak, terbangun, ndvi, ndmi]);
Export.image.toDrive({
  image: stack,
  description: 'CSPI_Variables_Demak_Semarang',
  scale: 10,
  region: roi,
  maxPixels: 1e9,
  fileFormat: 'GeoTIFF'
});
```

---

## 4. Struktur Folder Kerja yang Dianjurkan

Buat struktur folder berikut di komputermu agar data rapi dan siap dimasukkan ke pipeline Python/QGIS:

```text
d:\Kuliah\Lomba\ASEC Arsen Unair 2026\Data_CSPI\
│
├── 01_Fisik_Hazard\
│   ├── amblesan_esdm_points.csv         # Titik koordinat & nilai laju amblesan (cm/th)
│   ├── amblesan_kriging_pantura.tif     # Raster hasil interpolasi kriging
│   ├── garis_pantai_2015_2024.shp       # Garis pantai multitemporal (CoastSat/BIG)
│   └── shoreline_change_rates.csv       # Nilai EPR & LRR per transekt
│
├── 02_Ekologis\
│   ├── gmw_1996_2020\                   # Shapefile Global Mangrove Watch multi-epoch
│   ├── sentinel2_ndvi_2024.tif          # Raster NDVI kesehatan kanopi
│   └── sentinel2_ndmi_2024.tif          # Raster kelembapan tajuk
│
├── 03_Antropogenik\
│   ├── demnas_pantura_8m.tif            # DEM elevasi & slope buffer darat
│   ├── esa_worldcover_10m.tif           # Peta tutupan lahan (tambak & pemukiman)
│   └── worldpop_idn_2020_100m.tif       # Raster kepadatan penduduk
│
├── 04_Transekt_Analisis\
│   ├── transekt_pantura_200m.shp        # Garis transekt tegak lurus interval 200 meter
│   └── cspi_master_dataset.csv          # Tabel gabungan nilai variabel per transekt
│
└── 05_Output_Visual\
    ├── map_cspi_hotspot.png             # Peta hasil Getis-Ord Gi*
    └── prims_wireframe_addon.png        # Mockup antarmuka add-on PRIMS BRGM
```

---

## 5. Ringkasan Eksekusi: Apa yang Perlu Kamu & Mutia Lakukan Sekarang?

1. **Unduh Data Raster Ringkas Terlebih Dahulu**:
   - Ambil **WorldPop Indonesia 100m** (link direct download di atas, langsung unduh 65 MB).
   - Ambil lembar **DEMNAS BIG** untuk Demak-Semarang (portal tanahair BIG, unduh 2–3 file GeoTIFF).
2. **Jalankan Skrip GEE / Unduh ESA WorldCover**:
   - Jika punya akses Google Earth Engine, jalankan script di Bagian 3 untuk langsung mendapatkan komposit NDVI, NDMI, DEM, dan kelas tambak dalam 1 file GeoTIFF.
3. **Persiapan Titik Amblesan & Transekt**:
   - Aku sudah menyiapkan data titik laju penurunan tanah geologis untuk koridor Pantura Jawa Tengah (Pekalongan, Semarang, Demak) berbasis kajian resmi ESDM & InSAR untuk siap kita olah di Python.

Semua data siap kita gabungkan ke dalam pipeline analisis CSPI!
