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

# Koordinat pembingkaian peta (fit_bounds: [[south, west], [north, east]])
REGION_BOUNDS = {
    "SEM": [[-7.02, 110.38], [-6.84, 110.58]],
    "PKL": [[-6.93, 109.61], [-6.83, 109.75]],
    "CIR": [[-6.84, 108.48], [-6.58, 108.76]],
    "SBY": [[-7.40, 112.66], [-7.10, 112.95]],
    "JPR": [[-6.70, 110.58], [-6.48, 110.76]],
    "SEMUA": [[-7.45, 108.40], [-6.45, 113.00]]
}

# --- Angka Kunci Riset ---------------------------------------------------- #
N_TRANSEK_TOTAL = 2365
N_DOMAIN_MANGROVE = 920
N_HOTSPOTS_TENGGELAM = 46

# Median Amblesan InSAR (cm/tahun)
MEDIAN_SUBSIDENCE = {
    "SEMUA": 1.45,
    "SEM": 4.80,
    "PKL": 3.90,
    "CIR": 2.70,
    "SBY": 0.85,
    "JPR": 0.25
}

# Median Estimasi Tahun Tenggelam (Monte Carlo 2.000 iterasi)
MEDIAN_SINK_YEAR = {
    "PKL": "2040",
    "CIR": "2049",
    "SEM": "2061",
    "SBY": "> 2200",
    "JPR": "> 2200",
    "SEMUA": "2068"
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

HOTSPOT_LABELS = {
    "kritis": "Hotspot Kritis Tenggelam (< 2050)",
    "non_kritis": "Transek Pesisir Non-Kritis"
}

# --- Temuan Regresi Kausalitas Penggerak (Esai Bagian 6) -------------------- #
REGRESI_FINDINGS = [
    {
        "penggerak": "Amblesan Tanah (InSAR)",
        "respons": "Laju Tepi Laut Mundur (Erosi)",
        "koefisien": "+0,95 m/th per SD",
        "p_value": "p = 0,008",
        "keterangan": "Terbukti kokoh pada seluruh spesifikasi WLS klaster, Huber robust, dan SIMEX."
    },
    {
        "penggerak": "Kawasan Terbangun (DW)",
        "respons": "Laju Pelebaran Sabuk Mangrove",
        "koefisien": "−1,40 m/th per SD",
        "p_value": "p = 0,018",
        "keterangan": "Infrastruktur keras menahan ruang ekspansi mangrove ke arah daratan."
    },
    {
        "penggerak": "Amblesan + Terbangun",
        "respons": "Peluang Kehilangan Tegakan Total",
        "koefisien": "+37% & +47% per SD",
        "p_value": "p < 0,01",
        "keterangan": "Interaksi ganda kedua tekanan melipatgandakan risiko kepunahan tegakan lokal."
    }
]
