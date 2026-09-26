# DOKUMEN PETUNJUK DETAIL ANALISIS & SPESIFIKASI PEMROGRAMAN PYTHON

**Judul Proyek**: Nowcasting & Short-Horizon Forecasting Ruang Gerak Mundur (Migration Space) Mangrove Berbasis Transek Pesisir Pantura Jawa Barat–Jawa Tengah untuk Pencegahan Coastal Squeeze dan Alokasi Restorasi Presisi  
**Target Output**: Airlangga Statistics Essay Competition (ASEC) 2026  
**Format Dokumen**: Technical Reference & Implementation Blueprint  

---

## 1. Maksud, Tujuan, dan Cakupan Wilayah

### 1.1 Tujuan Utama
Membangun *pipeline* analisis spasial-temporal berbasis statistik dan *remote sensing* di Python untuk:
1. **Nowcasting & Short-Horizon Forecasting**: Memetakan posisi tepi mangrove ($Y_{i,t}$) dan sisa ruang gerak mundur (*migration space*, $MS_{i,t}$) secara *near real-time* (per bulan) serta memproyeksikan lintasannya dalam horizon pendek (3 bulan, 6 bulan, hingga 1–2 tahun) menggunakan *State-Space Model / Kalman Filter* lengkap dengan *uncertainty cone*.
2. **Dekomposisi Dua Tekanan Simultan (*Dual-Pressure Framework*)**: Mengkuantifikasi interaksi antara **Tekanan Sisi Laut** (*seaward risk*: laju amblesan tanah $Subs_i$, frekuensi rob/genangan $Inund_i$) dan **Tekanan Sisi Darat** (*landward resistance*: infrastruktur keras buatan manusia vs. tambak pesisir non-aktif).
3. **Pencegahan Coastal Squeeze & Identifikasi Ruang Peluang**: Membedakan penghalang keras permanen (*hard barrier* / jalan/tanggul PSN) dengan penghalang lunak reversible (*soft barrier* / tambak *idle*) guna mengukur ruang ekspansi restorasi (*opportunity/expansion space*).
4. **Restoration Feasibility Index (RFI) & Exceedance Probability**: Menghitung probabilitas penutupan ruang gerak ($P(\text{Closed})$) serta mengidentifikasi transek yang memiliki viabilitas tinggi untuk *Managed Realignment* dan *Nature-based Solutions* (NbS).
5. **Kerangka Intervensi Preskriptif Multi-Skala**: Menghasilkan sistem pendukung keputusan spasial yang menetapkan intervensi tepat sasaran di tingkat makro (APBN/RTRW via klaster Getis-Ord $\text{Gi}^*$) dan tingkat mikro per transek 250m (*Hybrid Engineering*, *Managed Realignment*, *Assisted Regeneration*, *Strict Conservation*).

### 1.2 Desain Sampling Wilayah & Generalisasi Makro (Representative Coastal Archetypes)
Penelitian ini mengadopsi **Desain Stratifikasi Tipologi Pesisir (*Representative Coastal Archetypes / End-Member Design*)** pada **5 Lanskap Representatif Pantura**, bukan *convenience sampling*. Kelima situs ini dipilih secara purposif untuk mencakup keseluruhan spektrum variabilitas kovariat biofisik dan antropogenik (*full covariate support*):
1. **Pekalongan (Jateng) — *Ujung Ekstrem Bahaya Laut (*Extreme Seaward Risk*)***: Episentrum amblesan tanah terparah (GNSS CPKL $-11,6$ cm/tahun; InSAR di stasiun $-9,2$ cm/tahun; 10% transek tercepat $\le -6,8$ cm/tahun) dan genangan rob permanen masif.
2. **Semarang-Demak (Jateng) — *Benturan Infrastruktur Keras (*Hard Infrastructure Collision*)***: Interseksi proyek strategis nasional (Tol Semarang-Demak & Tanggul Laut terpadu) yang memotong ruang mundur alami pada zona amblesan tinggi (InSAR per transek: median $-2,6$ cm/tahun, 10% transek tercepat $\le -7,9$ cm/tahun).
3. **Cirebon (Jabar) — *Peluang Managed Realignment (*Soft Barrier Archetype*)***: Didominasi tambak pesisir marjinal/terlantar yang luas di daratan dengan amblesan sedang, mewakili potensi ekspansi ruang mangrove terbesar.
4. **Jepara (Jateng) — *Kontrol Negatif Alami (*Baseline / Counterfactual*)***: Area stabil dengan amblesan tanah mendekati nol (median InSAR per transek $-0,08$ cm/tahun; GNSS CJPR $-0,27$ cm/tahun) dan tekanan antropogenik rendah; berfungsi krusial membuktikan validitas kausal (bahwa penyempitan ruang di lokasi lain bukan sekadar noise iklim global).
5. **Surabaya (Jatim) — *Lanskap Delta Perkotaan (*Urban Estuary Archetype*)***: Estuari padat permukiman megapolitan dengan tekanan struktur keras perkotaan.

* **Defensibilitas Generalisasi ke Koridor Makro Pantura (*Covariate-Based Transferability*)**:
  Model statistika (laju penutupan $v_i$, State-Space Kalman Filter, dan RFI) dibangun berbasis **kovariat biofisik kontinu** ($Subs_i, Inund_i, DEM_i, Built_i$), bukan berbasis label wilayah administratif. Wilayah Pantura lainnya (seperti Kab. Brebes, Tegal, Batang, dan Kendal) secara karakteristik biofisik berada dalam domain interpolasi di antara Cirebon, Pekalongan, dan Semarang. Oleh karena itu, parameter model dan fungsi transfernya memiliki **validitas inferensial yang kokoh (*transferable*)** untuk merepresentasikan seluruh koridor pesisir Pantura.

### 1.3 Rentang Temporal & Proyeksi Spasial
* **Rentang Data Observasi Historis**: 1 Januari 2021 – 31 Agustus 2026 (komposit median bulanan, T = 68 bulan; tanggal potong data = awal bulan berjalan saat pipeline dijalankan; memenuhi kaidah data $\ge 2021$).
* **Horizon Prediksi Jangka Pendek (*Near-Term Forecast*)**: $t+6\text{ bulan}$ dan $t+12\text{ bulan}$ (hingga horizon 2 tahun) untuk deteksi dini akselerasi penyempitan (*accelerating squeeze*).
* **Proyeksi Geospasial**: Wajib diseragamkan ke `EPSG:32749` (**UTM Zone 49S - WGS 84 / Southern Hemisphere**; seluruh lokasi studi 108,5–113,3° BT berada di zona 49) agar seluruh perhitungan jarak horizontal ($MS_{i,t}$, jarak tambak, mundur tepi) terukur tepat dalam satuan meter planar murni.

---

## 2. Unit Observasi & Garis Basis Transek

Unit analisis statistik yang digunakan adalah **Transek Tegak Lurus Garis Pantai ($i$)**, bukan agregasi wilayah administratif:
* **Spasi Antartransek**: 250 meter sepanjang garis arah pantai (garis pantai OSM yang disederhanakan menjadi ruas lurus/sektor) pada 5 lanskap arketipe. Titik sampel sepanjang transek berjarak 10 meter (351 titik per transek).
* **Panjang Transek**: 3.500 meter (500 meter ke arah laut, 3.000 meter ke arah darat dari garis pantai basis). Panjang ke darat dipilih agar transek mencakup sabuk tambak hingga penghalang keras: median jarak garis pantai ke tol/jalan arteri/tanggul (OSM) ±3 km (Pekalongan 3,0 km; Semarang–Demak 3,4 km).
* **Orientasi Transek**: tegak lurus garis arah yang dihaluskan (jendela ±4,5 km). Transek sejajar di ruas lurus dan berputar bertahap (kipas) di tikungan. Transek yang memotong transek lain dibuang (tikungan tajam, perbatasan wilayah), sehingga setiap lokasi pantai hanya diobservasi satu kali dan tidak ada informasi ganda antarwilayah.
* **Cakupan & Celah**: ruas pantai tanpa transek > 750 m (umumnya muara sungai, pelabuhan, dan tikungan delta) dicatat pada `celah_pantai.geojson`. Ruas ini **tidak dinilai** dan tidak diinterpolasi; persentase cakupan pantai per wilayah dilaporkan sebagai keterbatasan.
* **Transek Multi-Persilangan**: transek yang memotong garis pantai lebih dari sekali (spit, muara, tambak jebol) ditandai `n_silang_pantai > 1`. Transek ini tetap dipakai, dan hasil dihitung ulang tanpa transek tersebut sebagai uji sensitivitas (Bagian 7).
* **Profil Transek**: Setiap transek menjadi sumbu 1-dimensi tempat profil elevasi, NDVI, SAR backscatter, dan tutupan lahan diekstrak secara konsisten.
* **Ukuran Sampel & Kekuatan Statistik (*Statistical Power*)**:
  * Garis pantai pada 5 lanskap arketipe menghasilkan **$N \approx 2.365$ transek**.
  * Dengan $T = 68$ time-steps (komposit bulanan Januari 2021 – Agustus 2026), diperoleh total **$N \times T \approx 160.800$ titik observasi spasial-temporal**.
  * Ukuran sampel ini menjamin derajat kebebasan (*degrees of freedom*) yang sangat masif untuk konvergensi estimasi parameter *State-Space Kalman Filter*, *Random Forest*, dan regresi laju.

---

## 3. Sumber Data, Sensor Satelit, & Variabel Ekstraksi

Seluruh data bersifat *open-source* dan dapat diakses publik ($\ge 2021$):

| Kategori Data | Source / Platform / Band GEE | Resolusi Spasial/Temporal | Variabel Ekstraksi | Peran dalam Model 2 Tekanan & Restorasi |
| :--- | :--- | :--- | :--- | :--- |
| **Sentinel-2 MSI (L2A)** | `COPERNICUS/S2_SR_HARMONIZED`<br>B8 (NIR), B4 (Red), B11 (SWIR1) | 10 meter / Komposit Median Bulanan | $\text{NDVI} = \frac{\text{B8}-\text{B4}}{\text{B8}+\text{B4}}$<br>$\text{NDMO} = \frac{\text{B8}-\text{B11}}{\text{B8}+\text{B11}}$ | Deteksi batas tepi luar mangrove ($Y_{i,t}$) dan kesehatan kanopi vegetasi pesisir. |
| **Sentinel-1 SAR (GRD)** | `COPERNICUS/S1_GRD`<br>VV, VH (IW mode, Descending) | 10 meter / Komposit Median Bulanan (orbit descending) | Backscatter VH ($\text{dB}$), VV ($\text{dB}$), Rasio $\text{VH}/\text{VV}$ | Deteksi batas mangrove tembus awan/air keruh & kuantifikasi *Hydroperiod* (proksi frekuensi genangan rob / Tekanan Laut). |
| **Dynamic World V1** | `GOOGLE/DYNAMICWORLD/V1`<br>Class `built`, `water`, `crops`, `bare` | 10 meter / Daily | Probabilitas piksel terbangun ($\tau_{\text{built}}$) & piksel perairan/tambak | Pembeda **Hard Barrier** (bangunan/jalan permanen) vs **Soft Barrier** (tambak/lahan marginal daratan). |
| **Copernicus DEM** | `COPERNICUS/DEM/GLO30`<br>Band `DEM` | 30 meter / Statis | Elevasi ($Z$), Slope ($\theta$), Diskontinuitas kontur ($\Delta Z$) | Penentu batas tanggul fisik darat, serta verifikasi elevasi intertidal untuk kesesuaian tumbuh mangrove baru. |
| **InSAR Sentinel-1 Jawa** | Ohenhen dkk. (2026), *Sci. Adv.* 12:eaec0172; Zenodo 10.5281/zenodo.15786356 | 75 meter / laju rata-rata 2017–2023 (vertikal, IGS14) | Laju Amblesan Tanah **per transek** ($Subs_i$, $\text{cm/tahun}$): median VLM dalam koridor ±150 m | Penggerak utama laju penyempitan ruang dari sisi laut (*Seaward Hazard*). |
| **Observasi GNSS** | Stasiun BIG (`CPKL`, `CSEM`, `CJPR`, `CCIR`, `CSBY`); Zenodo 10.5281/zenodo.7775016 | Point Data / Deret Harian 2010–2021 | Laju vertikal stasiun | **Validasi** InSAR di lokasi stasiun (bukan nilai per wilayah). |
| **Raster Multiband Workspace** | Folder `Dataset/03_Raster_Satelit_10m_2021_2024/` (16 Band) | 10 meter | Band `Mangrove 2021`, `Tambak 2021`, `Built 2021`, `Pop 2021`, S2 time-series | Basis ekstraksi cepat luas tambak eksisting dan batas infrastruktur di sepanjang transek. |
| **Footprint PSN & RTRW** | Vector GeoJSON/SHP (KemenATR/KKP) | Vektor Poligon | Tapak Proyek Tol & Tanggul Laut | Flagging tumpang tindih infrastruktur keras strategis nasional. |
| **Populasi Terpapar** | WorldPop / LandScan | 100 meter / Tahunan | Jumlah Penduduk ($Pop_i$) radius 1 km | Pembobotan indeks risiko keterpaparan manusia ($\text{PERI}_i$). |

---

## 4. Alur Pemrosesan Kode Python (Workflow Modul)

```
========================================================================================
ALUR PIPELINE PYTHON (NOWCASTING, FORECASTING & PRESCRIPTIVE RESTORATION)
========================================================================================

[Modul 01: Preprocessing & Grid Transek]
├─ Import Garis Pantai Basis (GeoJSON Pantura Jabar–Jateng)
├─ Generate Transek Ortogonal (Spasi 250m, Panjang 3.500m [500 laut + 3.000 darat], EPSG:32749) via GeoPandas/Shapely
└─ Panggil GEE API / Baca Raster 16-Band -> Ekstraksi Profil Spasial per Transek
│
▼
[Modul 02: Ekstraksi Batas & Dekomposisi 2 Tekanan]
├─ Deteksi Tepi Mangrove Terluar (Y_i,t) via Threshold Dinamis NDVI + VH Backscatter
├─ Deteksi Hard Barrier (B_i^hard) via Dynamic World Built (tau_built > 0.5) / Tanggul PSN
├─ Deteksi Soft Barrier & Opportunity Space (B_i^soft) via Poligon/Band Tambak & Lahan Terbuka
├─ Hitung Migration Space Keras: MS_i,t^hard = |B_i^hard - Y_i,t|
└─ Hitung Ruang Peluang Restorasi Ekspansi: Space_opp,i = |B_i^hard - B_i^soft|
│
▼
[Modul 03: Nowcasting & Short-Horizon Forecasting Engine]
├─ Model A: OLS Linear Drift Baseline
├─ Model B: Spatio-Temporal Random Forest / Gradient Boosting
├─ Model C (Model Utama): State-Space Local Level Model dengan Kalman Filter
│   ├─ Filter Nowcasting: Estimasi Y_hat_i,t dan varians posterior sigma²_Y,i,t
│   └─ K-Step Ahead Forecasting: Proyeksi posisi tepi t+6 bulan & t+12 bulan + Uncertainty Cone
└─ Validasi Kinerja: RMSE, MAE, dan CRPS (Continuous Ranked Probability Score)
│
▼
[Modul 04: Pemodelan Laju 2 Tekanan & Restoration Feasibility Index (RFI)]
├─ Model Laju Mundur v_i (m/tahun) = f(Subs_i, Inund_i, Slope_i)
├─ Propagasi Ketidakpastian: sigma²_MS,i = sigma²_Y,i,t + sigma²_B,i
├─ Hitung P(Closed_k): Probabilitas MS <= 0 dalam horizon 1 tahun dan 5 tahun
└─ Hitung RFI_i (Restoration Feasibility Index) berbasis kesesuaian hidro-topografi & ruang tambak
│
▼
[Modul 05: Kerangka Intervensi Preskriptif Multi-Skala]
├─ Level Makro: Population-Exposed Risk Index (PERI_i) & Hotspot Spatial Getis-Ord Gi* (DistanceBand 1.000 m)
├─ Level Mikro: Matriks Klasifikasi 4-Tipologi Solusi Preskriptif:
│   ├─ Tipologi 1 (RED): Hybrid Engineering (Green-Gray / Permeable Dam) pada Squeeze Akut
│   ├─ Tipologi 2 (ORANGE): Managed Realignment (Buka Tambak Idle untuk Ekspansi Darat)
│   ├─ Tipologi 3 (YELLOW): Assisted Regeneration & Pengkayaan Sabuk Hijau Penahan Erosi
│   └─ Tipologi 4 (GREEN): Strict Conservation & Perlindungan Legal Kawasan Inti
├─ Agregasi Transek -> Kawasan Prioritas (modus 5 transek, celah > 1 km memutus kawasan, panjang minimum 1 km)
├─ Uji Sensitivitas 36 Skenario Parameter (Spearman Rank Correlation rho > 0.90)
└─ Export Master Output: master_transek_pantura.csv & GeoJSON Intervensi Pesisir
```

---

## 5. Rincian Metodologi Statistik & Formula Matematika

### 5.1 Penentuan Posisi Tepi ($Y_{i,t}$) & Dual-Barrier ($B_i^{\text{hard}}, B_i^{\text{soft}}$)
Pada transek $i$ dan waktu $t$:
* **Posisi Tepi Terluar Mangrove ($Y_{i,t}$)** dihitung dari titik terjauh ke arah laut yang memenuhi kriteria ganda kanopi mangrove:
  $$\text{Mangrove}_{i,x,t} = (\text{NDVI}_{i,x,t} > \tau_{\text{veg}}) \quad \land \quad (\text{VH}_{i,x,t} > \tau_{\text{SAR}})$$
  di mana $\tau_{\text{veg}} = 0,4$ dan $\tau_{\text{SAR}} = -14\text{ dB}$.
* **Hard Barrier ($B_i^{\text{hard}}$)**: Titik darat terdekat yang berupa struktur permanen tak tertembus:
  $$\text{HardBarrier}_{i,x} = (P(\text{built})_{i,x} > 0,5) \quad \lor \quad (\text{Tapak PSN}_{i,x} = \text{True}) \quad \lor \quad (\Delta \text{DEM}_{i,x} > 1,5\text{ m})$$
* **Soft Opportunity Barrier ($B_i^{\text{soft}}$)**: Titik awal batas tambak pesisir non-aktif atau lahan terbuka marjinal di darat:
  $$\text{SoftBarrier}_{i,x} = (P(\text{water/bare})_{i,x} > 0,4) \quad \land \quad (\text{Elevasi}_{i,x} \in [0,5\text{ m}, 2,0\text{ m}])$$
* **Migration Space Riil & Ruang Peluang Restorasi**:
  $$MS_{i,t}^{\text{hard}} = |B_i^{\text{hard}} - Y_{i,t}|, \qquad \text{Space}_{\text{opp},i} = |B_i^{\text{hard}} - B_i^{\text{soft}}|$$

### 5.2 Nowcasting & Short-Horizon Forecasting Engine (Kalman Filter)
Menggunakan model *State-Space Local Linear Trend* per transek:

$$\begin{aligned}
\text{Persamaan Observasi:} &\quad y_{i,t} = \mu_{i,t} + \epsilon_{i,t}, \quad &\epsilon_{i,t} \sim \mathcal{N}(0, \sigma_\epsilon^2) \\
\text{Persamaan Level (Posisi):} &\quad \mu_{i,t} = \mu_{i,t-1} + \beta_{i,t-1} + \eta_{i,t}, \quad &\eta_{i,t} \sim \mathcal{N}(0, \sigma_\eta^2) \\
\text{Persamaan Slope (Laju):} &\quad \beta_{i,t} = \beta_{i,t-1} + \zeta_{i,t}, \quad &\zeta_{i,t} \sim \mathcal{N}(0, \sigma_\zeta^2)
\end{aligned}$$

* **Nowcasting ($t$)**: Menghasilkan posisi tepi terhaluskan $\hat{\mu}_{i,t}$ bebas gangguan pasang surut/awan beserta varians posterior $P_{i,t|t}$.
* **Short-Horizon Forecasting ($t+k$, di mana $k \in \{6\text{ bulan}, 12\text{ bulan}\}$)**:
  $$\hat{y}_{i, t+k \mid t} = \hat{\mu}_{i,t} + k \cdot \hat{\beta}_{i,t}$$
  $$\text{Var}(\hat{y}_{i, t+k \mid t}) = P_{i,t|t} + k^2 \cdot \text{Var}(\hat{\beta}_{i,t}) + k \cdot \sigma_\eta^2$$
  *Pita Ketidakpastian (Uncertainty Cone)*: $\hat{y}_{i, t+k \mid t} \pm 1,96 \sqrt{\text{Var}(\hat{y}_{i, t+k \mid t})}$.

### 5.3 Dekomposisi 2 Tekanan & Bayesian Exceedance Probability
Laju penyempitan ruang gerak ($v_i$, meter/tahun) dimodelkan dari dua sisi tekanan:
$$v_i = \gamma_0 + \underbrace{\gamma_1 \cdot Subs_i + \gamma_2 \cdot Inund_i}_{\text{Tekanan Sisi Laut}} + \underbrace{\gamma_3 \cdot BuiltDensity_i}_{\text{Tekanan Sisi Darat}} + u_i$$

Probabilitas ruang gerak tertutup habis ($P(\text{Closed}_h)$) dalam horizon $h$ tahun (misal $h=1$ tahun untuk jangka pendek, $h=5$ tahun untuk jangka menengah):
$$P(MS_{i, t+h} \le 0 \mid \mathcal{D}) = \Phi \left( \frac{0 - (MS_{i,t}^{\text{hard}} - h \cdot v_i)}{\sqrt{\sigma_{MS,i}^2 + h^2 \cdot \sigma_{v,i}^2}} \right)$$

### 5.4 Restoration Feasibility Index (RFI)
Untuk menentukan apakah suatu transek layak menjadi target peningkatan/restorasi mangrove (bukan lokasi sia-sia):
$$\text{RFI}_i = w_1 \cdot \text{Norm}(\text{Space}_{\text{opp},i}) + w_2 \cdot \text{HydroSuitability}_i - w_3 \cdot \text{Norm}(|Subs_i|) - w_4 \cdot \text{Norm}(P(\text{Closed}_1)_i)$$
* Skor $\text{RFI}_i \in [0, 1]$ tinggi menandakan bahwa di daratan terdapat tambak *idle* luas dengan kemiringan pasang-surut ideal dan tingkat amblesan yang masih bisa ditoleransi oleh mangrove perintis.

---

## 6. Kerangka Intervensi Preskriptif Multi-Skala

### 6.1 Skala Makro / Global (Alokasi Kebijakan Provinsi & Nasional)
* **Population-Exposed Risk Index**:
  $$\text{PERI}_i = P(\text{Closed}_5)_i \times \log_{10}(Pop_i + 1)$$
* **Analisis Klaster Spasial Getis-Ord $\text{Gi}^*$**:
  Mendeteksi koridor pesisir Pantura yang menjadi *Hotspot* multisektoral (tingkat keterancaman ekologis tinggi bersanding dengan kepadatan pemukiman tinggi). Koridor ini menjadi dasar usulan alokasi anggaran penanganan pesisir terpadu pada revisi RTRW Provinsi dan Rencana Aksi Nasional Adaptasi Perubahan Iklim.
  * *Matriks bobot*: `DistanceBand` biner pada titik pusat transek dengan ambang **1.000 m** (±4 transek tetangga di setiap sisi). Dengan ambang ini, transek di seberang celah > 1 km (muara, pelabuhan) tidak saling bertetangga, sehingga hotspot tidak "melompati" celah.
  * Transek tanpa tetangga dalam 1.000 m (isolat) tidak diberi nilai $\text{Gi}^*$ dan dilaporkan terpisah.
  * Koridor hotspot = rangkaian transek berurutan dengan $z_{\text{Gi}^*} > 1{,}96$, dibentuk dengan aturan penggabungan yang sama dengan Bagian 6.3.

### 6.2 Skala Mikro / Lokal: Matriks Tipologi 4-Aksi Intervensi Presisi (per Transek 250m)

```
                            TEKANAN SISI LAUT (Subsidence & Rob Ekstrem)
                                 TINGGI                     RENDAH
                     +---------------------------+---------------------------+
                     | TIPOLOGI 1: RED FLAG      | TIPOLOGI 3: YELLOW FLAG   |
         TINGGI      | HYBRID ENGINEERING        | URBAN BUFFER & ENRICHMENT |
                     | Tanggul Permeabel Bambu   | Pengkayaan Sabuk Hijau    |
TEKANAN  (Hard Built | + Penanaman Berundak      | Penahan Erosi & Gelombang |
SISI     / PSN)      +---------------------------+---------------------------+
DARAT                | TIPOLOGI 2: ORANGE FLAG   | TIPOLOGI 4: GREEN FLAG    |
         RENDAH      | MANAGED REALIGNMENT       | STRICT CONSERVATION       |
         (Tambak     | Pembukaan Pematang Tambak | Perlindungan Kawasan Inti |
         / Lahan Idle| untuk Ekspansi Daratan    | & Refugia Alami           |
                     +---------------------------+---------------------------+
```

1. **TIPOLOGI 1: RED FLAG (Hybrid Engineering / Coastal Defense)**
   * *Kriteria*: $P(\text{Closed}_1) > 0,60$, Beririsan dengan infrastruktur keras/PSN, laju amblesan tinggi.
   * *Tindakan Preskriptif*: Penanaman mangrove konvensional **dilarang** karena pasti mati tersapu ombak/terbenam rob. Wajib dibangun struktur pelindung peredam gelombang permeabel (*permeable bamboo/brushwood breakwater*) di sisi depan untuk menjebak sedimen sebelum revegetasi bertahap.
2. **TIPOLOGI 2: ORANGE FLAG (Managed Realignment - Target Utama Peningkatan Mangrove)**
   * *Kriteria*: $P(\text{Closed}_5) > 0,70$, $\text{RFI}_i > 0,60$, daratan didominasi tambak non-aktif (*Soft Barrier*).
   * *Tindakan Preskriptif*: **Lokasi paling tepat sasaran untuk program restorasi mangrove nasional**. Rekomendasi teknis berupa pembukaan saluran pematang tambak secara terkontrol agar pasang surut masuk alami (*hydrological restoration*), memberikan ruang ekspansi ke arah darat.
3. **TIPOLOGI 3: YELLOW FLAG (Assisted Regeneration & Buffer)**
   * *Kriteria*: $MS_{i,t} < 50\text{ m}$, tekanan laut rendah/sedang, di darat terdapat permukiman lokal.
   * *Tindakan Preskriptif*: Pengkayaan tegakan (*enrichment planting*) jenis berakar kokoh (*Rhizophora mucronata*) untuk mempertahankan dinding penahan erosi alami.
4. **TIPOLOGI 4: GREEN FLAG (Strict Conservation & Natural Expansion)**
   * *Kriteria*: $MS_{i,t} \ge 50\text{ m}$, $P(\text{Closed}_5) < 0,25$, dinamika sedimentasi positif.
   * *Tindakan Preskriptif*: Penetapan status suaka konservasi ketat (*non-take zone*) dan pemantauan berkala via sistem *nowcasting*.

### 6.3 Pembentukan Kawasan Prioritas (Agregasi Transek → Segmen Pantai)

Tipologi dan indeks dihitung **per transek**. Untuk peta kebijakan, transek bertetangga digabung menjadi **kawasan** (segmen pantai) dengan aturan berikut:

1. **Urutan sepanjang pantai.** Transek diurutkan sepanjang garis arah (urutan `transek_id` dalam wilayah). Dua transek berurutan dianggap **bersambung** bila jarak titik pusatnya ≤ 1.000 m.
2. **Celah.** Celah ≤ 1 km (≤ 3 transek hilang) dijembatani. Celah > 1 km **memutus** rangkaian, dan ruas pantai tersebut ditampilkan sebagai *tidak dinilai* (abu-abu), tanpa interpolasi.
3. **Penghalusan.** Dalam setiap rangkaian bersambung, tipologi tiap transek diganti dengan **modus** jendela 5 transek (±2 tetangga, ±500 m). Tujuannya menghilangkan pola selang-seling (misalnya RED–YELLOW–RED) akibat derau pengukuran. Bila modus seri, dipakai kelas dengan tingkat keparahan tertinggi (RED > ORANGE > YELLOW > GREEN) sebagai prinsip kehati-hatian.
4. **Pembentukan kawasan.** Transek berurutan dengan tipologi hasil penghalusan yang sama digabung menjadi satu kawasan (`kawasan_id`).
5. **Panjang minimum.** Kawasan yang lebih pendek dari **4 transek (1 km)** dilebur ke kawasan tetangga yang lebih panjang (bila sama panjang, ke kelas yang lebih parah). Langkah ini diulang sampai tidak ada kawasan di bawah panjang minimum. Rangkaian yang secara keseluruhan < 1 km dipertahankan apa adanya.
6. **Atribut kawasan.** Panjang (km), jumlah transek, tipologi, median $P(\text{Closed}_5)$, median RFI, total populasi terpapar, dan proporsi transek dengan `n_silang_pantai > 1`.

Nilai per transek tetap tersimpan untuk skala mikro; kawasan dipakai untuk komunikasi kebijakan pada skala kilometer. Parameter jendela (5 transek) dan panjang minimum (1 km) ikut diuji di Bagian 7.

---

## 7. Uji Sensitivitas & Ketahanan Model (36 Skenario)

Untuk memastikan bahwa penetapan status intervensi tidak bias terhadap pemilihan *threshold* teknis, dilakukan simulasi pada **36 kombinasi parameter**:
1. Ambang batas NDVI ($\tau_{\text{veg}}$): 0,3 | 0,4 | 0,5
2. Ambang batas Built ($\tau_{\text{built}}$): 0,4 | 0,5 | 0,6
3. Spasi Transek: 200 m | 250 m | 300 m | 350 m

*Uji tambahan (di luar 36 kombinasi)*: (a) analisis tanpa transek `n_silang_pantai > 1`; (b) jendela penghalusan kawasan 3 | 5 | 7 transek dan panjang minimum kawasan 0,5 | 1 | 2 km, dievaluasi dengan kesamaan peta kawasan (proporsi panjang pantai dengan tipologi sama).

*Evaluasi Ketahanan*: Menghitung koefisien korelasi rank Spearman ($\rho$) terhadap urutan peringkat prioritas transek. Nilai $\rho > 0,90$ membuktikan kestabilan model statistik terhadap variasi parameter.

---

## 8. Spesifikasi Kode Python (Blueprint Implementasi)

### 8.1 Library Dependencies
```python
# Analisis Geospasial
import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point

# Pemodelan Statistika & Peramalan
from pykalman import KalmanFilter
import statsmodels.api as sm
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import norm, spearmanr

# Spasial Klaster
from esda.getisord import G_Local
from libpysal.weights import DistanceBand

# Visualisasi
import matplotlib.pyplot as plt
import seaborn as sns
```

### 8.2 Struktur Fungsi Utama

```python
# ==============================================================================
# MODUL 01: INISIALISASI TRANSEK PESISIR ORTOGONAL (EPSG:32749)
# ==============================================================================
# Diimplementasikan di data_acquisition/02_buat_transek.py -> dataset/transek_params_final.csv
# (transek_id, region_code, sektor, cx, cy, ux, uy, n_silang_pantai, tide_zone).
def generate_coastal_transects(coastline_gdf, spacing=250, length_sea=500, length_land=3000):
    """
    Menghasilkan transek tegak lurus garis arah pantai yang dihaluskan, koordinat planar UTM Zone 49S.
    """
    transects = []
    # Stasiun tiap 250 m -> normal garis arah terhalus -> bentangkan 500m laut & 3000m darat
    return gpd.GeoDataFrame(transects, crs="EPSG:32749")

# ==============================================================================
# MODUL 02: DUAL-BARRIER & EDGE DETECTION
# ==============================================================================
def detect_edges_and_barriers(profile_df, tau_veg=0.4, tau_sar=-14.0, tau_built=0.5):
    """
    Mendeteksi posisi tepi mangrove (Y_i,t), hard barrier permanen (B_hard), 
    dan soft barrier tambak/lahan marginal (B_soft).
    """
    # Y_i,t: titik terluar laut dengan NDVI > tau_veg dan VH > tau_sar
    # B_hard: titik darat pertama dengan P_built > tau_built atau tanggul PSN
    # B_soft: titik darat pertama dengan kelas tambak / elevasi intertidal
    pass

# ==============================================================================
# MODUL 03: STATE-SPACE KALMAN FILTER FOR NOWCASTING & SHORT FORECAST
# ==============================================================================
def run_kalman_nowcast_and_forecast(y_series, forecast_steps=[12, 24]):
    """
    Menjalankan Kalman Filter untuk nowcasting t dan short-horizon forecast (6-12 bulan).
    1 step = komposit 15 hari -> 12 steps = 6 bulan, 24 steps = 12 bulan.
    """
    kf = KalmanFilter(
        initial_state_mean=[y_series.iloc[0], 0],
        transition_matrices=[[1, 1], [0, 1]],
        observation_matrices=[[1, 0]],
        n_dim_obs=1
    )
    state_means, state_covs = kf.filter(y_series.values)
    
    current_pos = state_means[-1, 0]
    current_vel = state_means[-1, 1]
    current_var = state_covs[-1, 0, 0]
    
    forecasts = {}
    for step in forecast_steps:
        pred_pos = current_pos + (step * current_vel)
        pred_var = current_var + (step * state_covs[-1, 1, 1])
        forecasts[step] = (pred_pos, np.sqrt(pred_var))
        
    return current_pos, np.sqrt(current_var), forecasts

# ==============================================================================
# MODUL 04: RESTORATION FEASIBILITY & EXCEEDANCE PROBABILITY
# ==============================================================================
def calculate_rfi_and_exceedance(ms_current, ms_forecast_6m, opp_space, subsidence, inundation):
    """
    Menghitung probabilitas penutupan ruang dan Indeks Kelayakan Restorasi (RFI).
    """
    # Probabilitas ruang habis jika MS <= 0
    p_closed_1yr = norm.cdf(0, loc=ms_forecast_6m[0], scale=ms_forecast_6m[1])
    
    # RFI: Skalasi ruang tambak darat dikurangi faktor bahaya abrasi/amblesan
    rfi_score = (opp_space / 500.0) * 0.4 + (1 - p_closed_1yr) * 0.3 - (abs(subsidence) / 15.0) * 0.3
    rfi_score = np.clip(rfi_score, 0.0, 1.0)
    return p_closed_1yr, rfi_score

# ==============================================================================
# MODUL 05: PRESCRIPTIVE INTERVENTION CLASSIFICATION
# ==============================================================================
def assign_prescriptive_intervention(row):
    """
    Menetapkan klasifikasi 4-Tipologi Tindakan Pesisir.
    """
    if row['P_closed_1yr'] > 0.60 and row['PSN_overlap']:
        return "RED FLAG - Hybrid Engineering (Permeable Dams)"
    elif row['RFI_score'] > 0.60 and row['opp_space_m'] > 100:
        return "ORANGE FLAG - Managed Realignment (Restorasi Tambak)"
    elif row['MS_current_m'] < 50:
        return "YELLOW FLAG - Assisted Regeneration & Greenbelt"
    else:
        return "GREEN FLAG - Strict Conservation"


SEVERITY = {"RED": 4, "ORANGE": 3, "YELLOW": 2, "GREEN": 1}

def build_priority_zones(df, gap_m=1000, window=5, min_len=4):
    """
    Agregasi tipologi per transek menjadi kawasan (Bagian 6.3).
    df: satu baris per transek dengan kolom transek_id, region_code, cx, cy,
        typ (RED/ORANGE/YELLOW/GREEN).
    """
    df = df.sort_values(["region_code", "transek_id"]).copy()
    step = np.hypot(df.cx.diff(), df.cy.diff())
    df["run_id"] = ((df.region_code != df.region_code.shift()) | (step > gap_m)).cumsum()

    def smooth(typ):
        # modus jendela; seri -> kelas paling parah
        half = window // 2
        out = []
        for k in range(len(typ)):
            c = pd.Series(typ[max(0, k - half):k + half + 1]).value_counts()
            out.append(max(c[c == c.max()].index, key=SEVERITY.get))
        return out

    def merge_short(typ):
        typ = list(typ)
        while True:
            blocks = []                                   # [awal, akhir (eksklusif), kelas]
            for k, c in enumerate(typ):
                if blocks and blocks[-1][2] == c:
                    blocks[-1][1] = k + 1
                else:
                    blocks.append([k, k + 1, c])
            short = [b for b in blocks if b[1] - b[0] < min_len]
            if len(blocks) == 1 or not short:
                return typ
            b = min(short, key=lambda x: x[1] - x[0])     # lebur blok terpendek dulu
            i = blocks.index(b)
            nb = [blocks[j] for j in (i - 1, i + 1) if 0 <= j < len(blocks)]
            tgt = max(nb, key=lambda x: (x[1] - x[0], SEVERITY[x[2]]))
            typ[b[0]:b[1]] = [tgt[2]] * (b[1] - b[0])

    df["typ_smooth"] = df.groupby("run_id").typ.transform(lambda t: smooth(list(t)))
    df["typ_kawasan"] = df.groupby("run_id").typ_smooth.transform(merge_short)
    change = (df.run_id != df.run_id.shift()) | (df.typ_kawasan != df.typ_kawasan.shift())
    df["kawasan_id"] = df.region_code + "_K" + change.cumsum().astype(str).str.zfill(3)
    return df
```

---

## 9. Format Master Dataset Output (`master_transek_pantura.csv`)

| Nama Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `transek_id` | String | ID Unik Transek (contoh: `TRS_PKL_0012`) |
| `kab_kota` | String | Wilayah Administrasi Kabupaten/Kota |
| `lat` / `lon` | Float | Koordinat Titik Tengah Transek (WGS84) |
| `MS_current_m` | Float | Jarak Migration Space Terkini terhadap Hard Barrier (meter) |
| `MS_uncertainty` | Float | Ketidakpastian Posterior Kalman Filter ($\sigma_{MS}$, meter) |
| `MS_pred_6m` | Float | Proyeksi Posisi Ruang Gerak 6 Bulan ke Depan (meter) |
| `MS_pred_12m` | Float | Proyeksi Posisi Ruang Gerak 12 Bulan ke Depan (meter) |
| `opp_space_m` | Float | Luas/Jarak Ruang Peluang Tambak/Lahan Idle di Darat (meter) |
| `v_closure_m_yr` | Float | Laju Penyempitan Ruang Gerak (meter/tahun) |
| `P_closed_1yr` | Float | Probabilitas Ruang Habis dalam Horizon Pendek 1 Tahun |
| `P_closed_5yr` | Float | Probabilitas Ruang Habis dalam Horizon 5 Tahun |
| `RFI_score` | Float | Skor Indeks Kelayakan Restorasi ($[0, 1]$) |
| `PERI_index` | Float | Indeks Risiko Keterpaparan Populasi Manusia |
| `Gi_Zscore` | Float | Nilai Signifikansi Spasial Hotspot Getis-Ord $\text{Gi}^*$ (DistanceBand 1.000 m; kosong bila isolat) |
| `n_silang_pantai` | Integer | Jumlah persilangan transek dengan garis pantai (> 1 = spit/muara/tambak jebol) |
| `PSN_overlap` | Boolean | True jika transek memotong tapak proyek tanggul/tol laut |
| `Intervention_Type`| String | Tipologi Tindakan Preskriptif per transek (Red/Orange/Yellow/Green) |
| `kawasan_id` | String | ID kawasan prioritas hasil agregasi (Bagian 6.3) |
| `typ_kawasan` | String | Tipologi kawasan setelah penghalusan & panjang minimum |

---

