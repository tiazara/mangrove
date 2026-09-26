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

# Konfigurasi Halaman & Injeksi Desain Kustom
st.set_page_config(
    page_title="SABUK HIJAU — Pantura Mangrove DSS",
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
