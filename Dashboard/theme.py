"""
Token Desain SABUK HIJAU (Warna, Tipografi, Spasi).
Sumber tunggal yang dibaca Python dan diinjeksi ke assets/style.css via build_css().
"""

from pathlib import Path

# --- Warna Chrome & Layout ------------------------------------------------- #
CANVAS = "#f4f6f8"
CARD = "#ffffff"
CARD_BORDER = "#d9e5e6"
TEXT = "#0f172a"
TEXT_SECONDARY = "#475569"
TEXT_MUTED = "#94a3b8"
BRAND = "#0f6e56"
BRAND_DARK = "#085041"
HEADER_TINT = "#e6f4f1"

# --- Palet Warna Kartografi (Mangrove & Pesisir) ---------------------------- #
# Dinamika Perubahan Mangrove (GMW Style)
COLOR_GAIN = "#2ecc71"           # Hijau cerah (penambahan/akresi)
COLOR_LOSS = "#e74c3c"           # Merah tegas (kehilangan/tenggelam)
COLOR_STABLE = "#0f766e"         # Teal gelap (stabil)
COLOR_HISTORICAL = "#d97706"     # Oranye kecokelatan (hilang pra-2021)

# Tipologi 4 Kuadran Intervensi Presisi
COLOR_RED = "#b2182b"            # Rekayasa Hibrida (permeable dam)
COLOR_ORANGE = "#ea580c"         # Managed Realignment (buka pematang tambak)
COLOR_YELLOW = "#eab308"         # Pengayaan Sabuk Hijau (spesies akar kokoh)
COLOR_GREEN = "#16a34a"          # Konservasi Ketat (zona lindung inti)

# Garis Pantai & Penghalang
COLOR_COASTLINE = "#1e293b"      # Garis pantai acuan
COLOR_BARRIER = "#dc2626"        # Penghalang keras (jalan, tanggul, tol)

# --- Skala Tipografi Institusional ----------------------------------------- #
H1, H2, H3, BODY = 26, 20, 16.5, 15

def build_css() -> str:
    """Membaca style.css dan mengganti placeholder {{TOKEN}} dengan nilai aktual."""
    css_path = Path(__file__).parent / "assets" / "style.css"
    raw = css_path.read_text(encoding="utf-8")
    tokens = {
        "CANVAS": CANVAS, "CARD": CARD, "CARD_BORDER": CARD_BORDER,
        "TEXT": TEXT, "TEXT_SECONDARY": TEXT_SECONDARY, "TEXT_MUTED": TEXT_MUTED,
        "BRAND": BRAND, "BRAND_DARK": BRAND_DARK, "HEADER_TINT": HEADER_TINT,
        "H1": f"{H1}px", "H2": f"{H2}px", "H3": f"{H3}px", "BODY": f"{BODY}px",
    }
    for k, v in tokens.items():
        raw = raw.replace(f"{{{{{k}}}}}", v)
    return raw
