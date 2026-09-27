"""
Konfigurasi dan metadata dashboard Coastal Squeeze Pantura Jawa.
Terinspirasi dari Global Mangrove Watch (GMW) dengan standar visual kartografi ilmiah.
"""

from pathlib import Path

# Definisi direktori basis
DIR_DASHBOARD = Path(__file__).resolve().parent
DIR_FIX = DIR_DASHBOARD.parent
DIR_DATASET = DIR_FIX / "Dataset"
DIR_SPATIAL = DIR_FIX / "Spatial_Data"
DIR_SPATIAL_DASHBOARD = DIR_SPATIAL / "Dashboard"
DIR_SPATIAL_LAYERS = DIR_SPATIAL / "Layer_Tambahan"
DIR_OUTPUTS_STAT = DIR_FIX / "Outputs" / "Statistik" / "dashboard"
DIR_DERET_WAKTU = DIR_FIX / "Deret_Waktu"

# Metadata Wilayah Kajian
WILAYAH_INFO = {
    "SEM": {
        "nama": "Semarang – Demak",
        "lat": -6.920,
        "lon": 110.480,
        "zoom": 11,
        "deskripsi": "Kawasan terdampak amblesan parah dan proyek tanggul laut tol (Sayung - Morosari)."
    },
    "PKL": {
        "nama": "Pekalongan",
        "lat": -6.875,
        "lon": 109.680,
        "zoom": 12,
        "deskripsi": "Zona erosi pesisir kritis dengan dinamika akresi lokal pasca-2021."
    },
    "CIR": {
        "nama": "Cirebon",
        "lat": -6.720,
        "lon": 108.620,
        "zoom": 11,
        "deskripsi": "Lanskap tambak pesisir luas dengan ruang peluang pembukaan ruang mundur mangrove."
    },
    "SBY": {
        "nama": "Surabaya – Madura Barat",
        "lat": -7.220,
        "lon": 112.780,
        "zoom": 11,
        "deskripsi": "Kawasan sabuk hijau mangrove luas dengan tekanan konversi terbangun tinggi."
    },
    "JPR": {
        "nama": "Jepara (Kontrol)",
        "lat": -6.560,
        "lon": 110.660,
        "zoom": 12,
        "deskripsi": "Pantai berpasir tanpa tutupan mangrove masif sebagai baseline kontrol."
    },
    "SEMUA": {
        "nama": "Seluruh Pantura Jawa (Pantau Komprehensif)",
        "lat": -6.850,
        "lon": 110.500,
        "zoom": 8,
        "deskripsi": "Agregasi koridor pesisir Pantura Jawa Barat hingga Jawa Timur."
    }
}

# Palet Warna Ilmiah (Standar Kartografi GMW & ASEC)
COLOR_PALETTE = {
    # Mangrove Change (GMW Style)
    "gain": "#2ecc71",           # Hijau muda tegas (penambahan)
    "loss": "#e74c3c",           # Merah tegas (kehilangan)
    "stable": "#16a085",         # Teal / hijau tua (stabil)
    "historical_loss": "#e67e22", # Oranye tua (hilang pra-2021)

    # Mangrove Extent
    "extent": "#00a896",         # Cyan / teal khas Global Mangrove Watch

    # Tipologi Rekomendasi 4 Kuadran
    "RED": "#b2182b",            # Merah gelap (Rekayasa Hibrida)
    "ORANGE": "#f39c12",         # Oranye terang (Pembukaan Ruang Mundur Mangrove)
    "YELLOW": "#f1c40f",         # Kuning (Pengayaan Sabuk Hijau)
    "GREEN": "#27ae60",          # Hijau konservasi (Konservasi Ketat)

    # Lahan & Peluang Restorasi
    "mudflat": "#95a5a6",        # Abu-abu kebiruan (Dataran lumpur)
    "tidal_pond": "#3498db",     # Biru pasut (Tambak terhubung pasang)
    "abandoned_pond": "#8e44ad", # Ungu (Tambak terbengkalai)
    "active_pond": "#2c3e50",    # Abu gelap (Tambak aktif)
    "builtup": "#7f8c8d",        # Abu-abu (Kawasan terbangun)

    # Coastline & Barrier
    "coastline": "#1e293b",      # Slate tua
    "barrier": "#c0392b",        # Garis batas keras penghalang
}
