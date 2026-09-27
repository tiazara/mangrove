# SABUK HIJAU — Pantura Mangrove Decision Support System (DSS)
> **Sistem Pendukung Keputusan Berbasis Fusi Data Multi-Sumber dan Pemodelan Probabilistik untuk Prioritas Mitigasi *Coastal Squeeze* Mangrove Pantura**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pydeck WebGL](https://img.shields.io/badge/Pydeck-GPU_WebGL-47A248?style=flat&logo=webgl&logoColor=white)](https://deckgl.readthedocs.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Modern_Theme-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)

Aplikasi Web Sistem Pendukung Keputusan (*Decision Support System* / DSS) Spasial Interaktif untuk **Nowcasting & Short-Horizon Forecasting Ruang Gerak Mundur Mangrove Pantura Jawa** guna pencegahan fenomena *coastal squeeze* dan alokasi restorasi presisi multi-koridor.

*Karya esai ilmiah untuk kompetisi **Airlangga Statistics Essay Competition (ASEC) 2026 — Arsen Unair**.*

---

## 1. Ikhtisar Ilmiah

Hutan mangrove di pesisir utara Jawa (Pantura) mengalami ancaman ganda yang dikenal sebagai **coastal squeeze**:
1. **Sumbu Laut (Tekanan Vertikal)**: Amblesan tanah (*land subsidence* hingga 4,8 cm/th menurut InSAR) dipadu kenaikan muka laut memicu defisit elevasi yang mengancam menenggelamkan tegakan mangrove secara permanen sebelum 2050 (median tahun 2068).
2. **Sumbu Darat (Restriksi Lateral)**: Infrastruktur keras buatan manusia (jalan arteri Pantura, jalan tol tanggul laut, pemukiman, serta pematang tambak beton) berjarak dekat ($\le 500\text{ m}$) di belakang tegakan, mengunci ruang akomodasi alami mangrove untuk bermigrasi mundur ke darat.

Dashboard ini menyatukan pemodelan *state-space* (Filter Kalman pada deret waktu Sentinel-1/2), analisis laju InSAR 2017–2023, data pasang surut global EOT20, serta inventarisasi tutupan lahan Dynamic World & GMW ke dalam antarmuka interaktif institusional.

---

## 2. Struktur Modul & Berkas

Arsitektur kode dirancang modular, berkinerja tinggi, dan mengadopsi standar visual modern:

```
Dashboard/
├── app.py                  # Entrypoint aplikasi Streamlit (Header terpusat & Pill Tab Navigation)
├── theme.py                # Desain token (Warna institusional, Tipografi Inter, build_css)
├── components.py           # Komponen UI (Header band, KPI cards, Title modules, N-box, Note callout)
├── constants.py            # Konstanta headline resmi esai, kamus wilayah, 4 kuadran, 11 rekomendasi
├── data.py                 # Pemuat data spasial & tabular dengan st.cache_data (CSV, GeoJSON, Parquet)
├── maps.py                 # Pembangun peta Pydeck WebGL GPU-accelerated (Carto Positron & Satelit Esri)
├── charts.py               # Generator visualisasi analitis Plotly (Timeseries, Cross-section, Grouped Bar)
├── tab_peta.py             # Tab 1: Peta Spasial & Tipologi Intervensi
├── tab_dinamika.py         # Tab 2: Dinamika Tepi Laut & Kausalitas Penggerak
├── tab_kebijakan.py        # Tab 3: Rencana Aksi Presisi & Simulator Kebijakan What-If
├── assets/
│   └── style.css           # Lembar gaya CSS terpadu (Typography, Controls, Responsi)
├── requirements.txt        # Daftar dependensi Python
└── README.md               # Dokumentasi teknis sistem
```

---

## 3. Fitur Utama per Tab

### Tab 1: Peta Spasial & Tipologi Intervensi
* **Peta WebGL Berkinerja Tinggi (GPU-Accelerated 50 ms)**:
  * Visualisasi garis pantai acuan OSM dan 2.365 transek analitis dengan transisi instan antar-wilayah.
  * Pilihan basemap: **Kanvas Bersih** (*Carto Positron minimalis*) dan **Citra Satelit** (*Esri World Imagery resolusi tinggi*).
* **4 Mode Peta Tematik Otomatis Sinkron**:
  1. *Tipologi 4 Kuadran Mangrove*: Fokus 920 transek domain mangrove aktif (RED, ORANGE, YELLOW, GREEN).
  2. *Rekomendasi Aksi Lapangan*: Komposisi menyeluruh 11 rekomendasi intervensi biofisik pesisir Pantura.
  3. *Hotspot Kritis Tenggelam (< 2050)*: Penandaan 46 transek darurat amblesan ekstrem vs transek non-kritis.
  4. *Laju Penurunan Tanah InSAR*: Gradien termal laju amblesan tanah (< 1,0 hingga > 4,0 cm/th).
* **Sebaran Analitis Responsif**: Diagram batang horizontal adaptif dengan hover tooltip gelap kontras (`#04342c`).
* **Inspeksi & Ekspor Data**: Filter data transek dan tombol unduh CSV interaktif.

### Tab 2: Dinamika Tepi Laut & Kausalitas Penggerak
* **Temuan Model Ekonometrika Spasial**: Ringkasan empiris regresi WLS klaster, Huber robust, dan SIMEX terkait pengaruh defisit vertikal dan restriksi lateral terhadap pergerakan mangrove.
* **Inspektur Mikro per Transek**:
  * *Rapor Evaluasi Komprehensif*: Menampilkan tipologi intervensi, laju amblesan, estimasi tahun tenggelam, ruang mundur, dan jarak penghalang.
  * *Deret Waktu Posisi Tepi Bulanan*: Visualisasi posisi tepi laut bulanan Jan 2021 – Agu 2026 hasil ekstraksi Sentinel-1/2 beserta estimasi tren laju pergerakan ($v_{\text{edge}}$).
  * *Penampang Melintang Lahan*: Profil gradien tutupan lahan dari 0 m (laut lepas), 500 m (garis pantai basis), hingga 3.500 m (pedalaman darat) lengkap dengan penanda floating badge.

### Tab 3: Rencana Aksi Presisi & Simulator Kebijakan What-If
* **Pedoman Operasional Intervensi 4 Kuadran**: Kartu panduan aksi teknis per kuadran lengkap dengan panjang garis pantai terdampak.
* **Matriks Kawasan Prioritas (259 Ruas Kawasan Intervensi)**:
  * Hasil peleburan spasial transek bersebelahan dengan rekomendasi seragam ($\ge 500\text{ m}$).
  * Dilengkapi filter ganda (*Wilayah Koridor* & *Rekomendasi Kebijakan*) serta 3 kartu KPI (Total Ruas, Panjang Pantai, Penduduk Terlindungi).
  * Tombol ekspor rencana aksi tabular CSV untuk pelaporan dinas/Bappeda.
* **Simulator Kebijakan Interaktif "What-If"**:
  * Pengujian sensitivitas laju akresi sedimen penangkap lumpur ($A = 0{,}2 - 2{,}0\text{ cm/th}$), horizon target waktu (2050 vs 2100), dan opsi pembukaan pematang tambak (*Managed Realignment*).
  * Dilengkapi **Dropdown Wilayah Mandiri** untuk simulasi skala makro Pantura maupun koridor lokal.
  * **Grafik Batang Komparatif (*Grouped Bar Chart*)**: Membandingkan secara langsung kondisi Baseline Eksisting vs Hasil Skenario Simulasi, didukung kartu metrik delta pergeseran risiko.

---

## 4. Klasifikasi Kartografis & Penamaan Kanonik

Sistem menggunakan penamaan resmi yang seragam di seluruh peta, grafik, legenda, dan tabel:

### A. Tipologi 4 Kuadran Mangrove (920 Transek Domain Mangrove)
* **`RED · Rekayasa Hibrida`** (`#b2182b`): Tekanan laut tinggi $\times$ tekanan darat tinggi. Butuh struktur permeable dam bambu.
* **`ORANGE · Managed Realignment`** (`#ea580c`): Tekanan laut tinggi $\times$ tekanan darat rendah. Pembukaan pematang tambak untuk ruang migrasi darat.
* **`YELLOW · Pengayaan Sabuk Hijau`** (`#eab308`): Tekanan laut rendah $\times$ tekanan darat tinggi. Pengayaan jenis akar tunjang/kokoh pelindung aset.
* **`GREEN · Konservasi Ketat`** (`#16a34a`): Tekanan laut rendah $\times$ tekanan darat rendah. Zona lindung mandiri berdaya lentur alami tinggi.

### B. 11 Rekomendasi Aksi Lapangan Pesisir (2.365 Transek Pantura)
1. `GREEN · Konservasi Ketat` (510 transek)
2. `Perlindungan Pantai Terbangun` (486 transek)
3. `Restorasi Alami Lumpur` (460 transek)
4. `ORANGE · Managed Realignment` (242 transek)
5. `Restorasi Hidrologis + Sedimen` (187 transek)
6. `YELLOW · Pengayaan Sabuk Hijau` (153 transek)
7. `Lahan Darat (Non-Prioritas)` (132 transek)
8. `Penangkap Sedimen + Lumpur` (125 transek)
9. `Silvofishery Tambak Aktif` (45 transek)
10. `RED · Rekayasa Hibrida` (15 transek)
11. `Restorasi Hidrologis Tambak` (10 transek)

### C. Status Kerentanan Hotspot
* **`Hotspot Kritis Tenggelam (< 2050)`** (`#dc2626`): 46 transek darurat elevasi kritis.
* **`Transek Pesisir Non-Kritis`** (`#64748b` / `#94a3b8`): Pesisir berdaya tahan melampaui horizon 2050.

---

## 5. Cara Instalasi & Menjalankan Lokal

### Prasyarat
* Python versi 3.10 atau lebih baru.
* Git.

### Langkah Instalasi
1. Kloning repositori ini atau navigasikan ke direktori proyek:
   ```bash
   cd mangrove/Dashboard
   ```

2. Buat dan aktifkan lingkungan virtual (disarankan):
   ```bash
   python -m venv venv
   # Di Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # Di Linux/macOS:
   source venv/bin/activate
   ```

3. Instal pustaka dependensi yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app.py
   ```

Dashboard akan otomatis terbuka di peramban web pada alamat `http://localhost:8501`.

---

## 6. Sitasi & Sumber Data Terbuka

* **Global Mangrove Watch (GMW v4.0)**: Bunting et al. (2022).
* **Laju Amblesan InSAR**: Ohenhen et al. (2024), dikalibrasi stasiun GNSS Susilo et al. (2023).
* **Kenaikan Muka Air Laut (SLR)**: Kismawardhani et al. (2018) & Altimetri AVISO.
* **Akresi Sedimen Pb-210**: Murdiyarso et al. (2018) & Lovelock et al. (2015).
* **Infrastruktur & Batas Pesisir**: OpenStreetMap (OSM) via Overpass API.
* **Tutupan Lahan Dinamis**: Dynamic World & WorldCover via Google Earth Engine (GEE).
* **Model Pasang Surut Global**: Empirical Ocean Tide model (EOT20; Hart-Davis et al., 2021).
* **Kepadatan Penduduk**: WorldPop 100m Resolution (2026 projection).

---

*Dikembangkan untuk Airlangga Statistics Essay Competition (ASEC) 2026.*
