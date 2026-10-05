"""
Konstanta & Angka Headline Resmi Esai ASEC 2026 (SABUK HIJAU).
Angka agregat mengacu verbatim pada naskah esai dan penjelasan_analisis.md.
"""

# --- Wilayah Kajian -------------------------------------------------------- #
REGION_NAMES = [
    "Seluruh Pantura (Agregat)",
    "Semarang – Demak",
    "Pekalongan",
    "Cirebon",
    "Surabaya – Madura",
    "Jepara (Kontrol)"
]

NAME_TO_CODE = {
    "Seluruh Pantura (Agregat)": "SEMUA",
    "Semarang – Demak": "SEM",
    "Pekalongan": "PKL",
    "Cirebon": "CIR",
    "Surabaya – Madura": "SBY",
    "Jepara (Kontrol)": "JPR"
}

CODE_TO_NAME = {v: k for k, v in NAME_TO_CODE.items()}

# Batas sebaran transek per kawasan ([[selatan, barat], [utara, timur]]) untuk pembingkaian peta
REGION_BOUNDS = {
    "SEM": [[-6.97, 110.13], [-6.68, 110.64]],
    "PKL": [[-6.92, 109.27], [-6.77, 109.89]],
    "CIR": [[-6.83, 108.47], [-6.45, 109.10]],
    "SBY": [[-7.51, 112.45], [-6.84, 113.36]],
    "JPR": [[-6.69, 110.62], [-6.40, 110.85]],
    "SEMUA": [[-7.51, 108.47], [-6.40, 113.36]]
}

# --- Angka Kunci Riset ---------------------------------------------------- #
N_TRANSEK_TOTAL = 2365
N_DOMAIN_MANGROVE = 920
N_HOTSPOTS_TENGGELAM = 46

# Tahun acuan data (deret Sentinel terakhir)
DATA_PER = "Agustus 2026"

# Horizon analisis esai: tahun tenggelam di atas 2100 ditampilkan sebagai "> 2100"
HORIZON_MAKS = 2100

# Catatan keandalan data per kawasan (Lampiran 1 & 8 esai)
CATATAN_DATA = {
    "PKL": "InSAR 2,4 cm/th lebih rendah dari GNSS (11,6 cm/th), sehingga risiko kemungkinan lebih buruk dari hasil.",
    "SEM": "Amblesan terukur langsung InSAR paling sedikit (34% transek); sisanya diisi dari tetangga.",
    "CIR": "Kelas ORANGE terbanyak; InSAR sesuai GNSS (selisih 0,21 cm/th).",
    "SBY": "Tunggang pasut besar (modal elevasi 123,5 cm): tidak tenggelam sebelum 2100.",
    "JPR": "Kawasan kontrol; hanya 8 transek bermangrove sehingga laju tidak stabil.",
}

# --- Tipologi 4 Kuadran Mangrove Eksisting (V1 Baseline) -------------------- #
TIPOLOGI_ORDER = ["RED", "ORANGE", "YELLOW", "GREEN"]

TIPOLOGI_LABEL = {
    "RED": "RED · Rekayasa Hibrida",
    "ORANGE": "ORANGE · Pembukaan Ruang Mundur Mangrove",
    "YELLOW": "YELLOW · Pengayaan Sabuk Hijau",
    "GREEN": "GREEN · Konservasi Ketat"
}

TIPOLOGI_ACTION = {
    "RED": "Konstruksi penangkap sedimen permeabel (permeable dam bambu) sebelum revegetasi; ruang mundur tertutup infrastruktur.",
    "ORANGE": "Pembukaan pematang tambak terbengkalai di belakang tegakan secara bertahap untuk memfasilitasi migrasi alami ke darat.",
    "YELLOW": "Pengayaan jenis berakar kokoh (Rhizophora mucronata/apiculata) guna meredam hempasan gelombang di bibir penghalang.",
    "GREEN": "Perlindungan kawasan inti mutlak, pengawasan tata ruang, dan pemantauan dinamika tepi berbasis nowcasting."
}

TIPOLOGI_N = {
    "RED": 15,
    "ORANGE": 242,
    "YELLOW": 153,
    "GREEN": 510
}

TIPOLOGI_KM = {
    "RED": 5.5,
    "ORANGE": 69.0,
    "YELLOW": 41.5,
    "GREEN": 124.5
}

# --- 11 Rekomendasi Aksi Lapangan Pesisir (Kanonik) ----------------------- #
REKOMENDASI_11 = [
    "RED · Rekayasa Hibrida",
    "ORANGE · Pembukaan Ruang Mundur Mangrove",
    "YELLOW · Pengayaan Sabuk Hijau",
    "GREEN · Konservasi Ketat",
    "Penangkap Sedimen + Lumpur",
    "Restorasi Hidrologis + Sedimen",
    "Restorasi Hidrologis Tambak",
    "Restorasi Alami Lumpur",
    "Silvofishery Tambak Aktif",
    "Perlindungan Pantai Terbangun",
    "Lahan Darat (Non-Prioritas)"
]

# --- Rekomendasi Pantai Tanpa Mangrove (Notebook Bagian 8.3) -------------- #
# Jenis lahan peluang × ancaman tenggelam sebelum 2100 (P > 0,5), urut sesuai aturan.
AKSI_NONMANGROVE = [
    ("Dataran lumpur", "Tidak", "Restorasi Alami Lumpur", "#14b8a6",
     "Dataran lumpur ≥ 100 m di depan pantai dengan elevasi aman: biarkan mangrove tumbuh alami, bantu penanaman bila perlu."),
    ("Dataran lumpur", "Ya", "Penangkap Sedimen + Lumpur", "#0284c7",
     "Elevasi akan tenggelam: pasang penangkap sedimen (permeable dam) lebih dulu, tanam setelah lumpur meninggi."),
    ("Tambak terbengkalai", "Tidak", "Restorasi Hidrologis Tambak", "#6366f1",
     "Buka pematang/saluran tambak tak terkelola agar pasang surut masuk kembali dan mangrove tumbuh."),
    ("Tambak terbengkalai", "Ya", "Restorasi Hidrologis + Sedimen", "#0ea5e9",
     "Buka aliran pasang surut sekaligus tangkap sedimen karena dasar tambak terancam tenggelam."),
    ("Tambak aktif", "Ya / Tidak", "Silvofishery Tambak Aktif", "#8b5cf6",
     "Tanam mangrove di pematang dan sebagian petak tanpa menghentikan budidaya."),
    ("Pantai terbangun", "Ya / Tidak", "Perlindungan Pantai Terbangun", "#475569",
     "Penghalang ≤ 100 m dari pantai atau ≥ 50% zona 1 km terbangun: perlindungan struktural/hibrida untuk aset."),
    ("Lahan darat lain", "Ya / Tidak", "Lahan Darat (Non-Prioritas)", "#94a3b8",
     "Tidak ada lahan peluang restorasi; bukan prioritas program mangrove."),
]

HOTSPOT_LABELS = {
    "kritis": "Hotspot Tenggelam Padat Penduduk",
    "non_kritis": "Bukan Hotspot"
}
HOTSPOT_DEF = ("klaster Getis-Ord Gi* (FDR 5%) dari peluang tenggelam sebelum 2050 "
               "× jumlah penduduk dalam radius 1 km")

# --- Temuan Regresi Penggerak Perubahan (Tabel 6 & Lampiran 7 Esai) ------- #
REGRESI_FINDINGS = [
    {
        "penggerak": "Amblesan Tanah (InSAR)",
        "respons": "Laju Mundur Tepi Laut",
        "koefisien": "+0,95 m/th per simpangan baku",
        "p_value": "p = 0,008",
        "keterangan": "Searah pada semua variasi spesifikasi (WLS galat baku klaster, Huber, efek tetap kawasan); "
                      "pada laju Sentinel 2021–2026 searah tetapi tidak bermakna (p = 0,144)."
    },
    {
        "penggerak": "Kepadatan Terbangun (Dynamic World)",
        "respons": "Laju Pelebaran Sabuk ke Darat",
        "koefisien": "−1,38 m/th per simpangan baku",
        "p_value": "p = 0,018",
        "keterangan": "Kawasan terbangun tidak memengaruhi tepi laut (p = 0,85), tetapi memperlambat pelebaran sabuk ke darat."
    },
    {
        "penggerak": "Amblesan & Kepadatan Terbangun",
        "respons": "Peluang Kehilangan Total",
        "koefisien": "rasio odds 1,37 dan 1,47 per simpangan baku",
        "p_value": "p = 0,025 dan p < 0,001",
        "keterangan": "Masing-masing menaikkan peluang kehilangan total sekitar 1,4–1,5 kali (regresi logistik, galat baku klaster)."
    }
]
