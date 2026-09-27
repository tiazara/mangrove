"""
SABUK HIJAU — Dashboard Sistem Pendukung Keputusan Mitigasi Coastal Squeeze
dan Alokasi Restorasi Presisi Mangrove Pantura Jawa.
Entry point utama aplikasi Streamlit.
"""

import streamlit as st
import components as ui
import tab_peta as tab_peta
import tab_dinamika as tab_dinamika
import tab_kebijakan as tab_kebijakan

from pathlib import Path
from PIL import Image

# Konfigurasi Halaman & Injeksi Desain Kustom
LOGO_PATH = Path(__file__).resolve().parent / "assets" / "logo.png"
logo_icon = Image.open(LOGO_PATH) if LOGO_PATH.exists() else "🌿"

st.set_page_config(
    page_title="SABUK HIJAU — Pantura Mangrove DSS",
    page_icon=logo_icon,
    layout="wide",
    initial_sidebar_state="collapsed"
)
ui.inject_css()

# --- Header Terpusat (Wordmark SABUK HIJAU + Tagline Resmi Esai) ----------- #
ui.header_band(
    "Nowcasting & Short-Horizon Forecasting Ruang Gerak Mundur Mangrove Pantura Jawa untuk "
    "<em>Pencegahan Coastal Squeeze & Alokasi Restorasi Presisi</em>."
)

# --- Tab Bar Horizontal Berbentuk Pil (Tersimpan di Query Param URL) -------- #
TABS = ["Peta Spasial & Tipologi", "Dinamika & Penggerak", "Rencana Aksi & Simulasi"]
active = ui.tab_bar(TABS)

if active == TABS[0]:
    tab_peta.render()
elif active == TABS[1]:
    tab_dinamika.render()
else:
    tab_kebijakan.render()
