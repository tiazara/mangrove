"""
Tab 1: Peta Spasial & Tipologi Intervensi (SABUK HIJAU).
Arsitektur Pydeck WebGL modern dan berkinerja tinggi, terinspirasi dari Coraly.
Menampilkan kartu penjelas ilmiah, filter interaktif, 4 kartu KPI, peta GPU 50 ms,
legenda kartografis responsif, dan tabel unduh CSV.
"""

import streamlit as st
import pandas as pd
import components as ui
import constants as C
import data as data
import maps as maps
import charts as charts

MODE_LABELS = {
    "tipologi": "Tipologi 4 Kuadran Mangrove (RED, ORANGE, YELLOW, GREEN)",
    "aksi_lengkap": "Rekomendasi Aksi Lapangan (11 Kelas Intervensi)",
    "hotspot": "Hotspot Kritis Tenggelam (< 2050)",
    "subsidence": "Laju Penurunan Tanah InSAR (cm/th)"
}

def render():
    # --- 1. Penjelas Komponen Ilmiah (TDV-Card Style ala Coraly) ---------- #
    ui.component_explainer()
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- 2. Baris Filter & Kontrol Terpadu --------------------------------- #
    f1, f2, f3 = st.columns(3)
    with f1:
        sel_wilayah_name = st.selectbox(
            "Wilayah Koridor Pesisir",
            options=C.REGION_NAMES,
            index=0,
            help="Pilih koridor wilayah untuk memusatkan sudut pandang peta."
        )
        wilayah_code = C.NAME_TO_CODE[sel_wilayah_name]

    with f2:
        sel_mode = st.selectbox(
            "Mode Peta Tematik",
            options=list(MODE_LABELS.keys()),
            format_func=lambda k: MODE_LABELS[k],
            index=0,
            help="Pilih klasifikasi kartografis: 4 Kuadran Mangrove Inti, 11 Aksi Lengkap, Hotspot, atau InSAR."
        )

    with f3:
        sel_basemap = st.selectbox(
            "Tampilan Peta",
            options=["Kanvas Bersih", "Citra Satelit"],
            index=0,
            help="Pilih kanvas putih-abu vector minimalis atau foto satelit resolusi tinggi."
        )

    # --- 3. Kartu KPI Ringkas (Angka Headline Resmi Esai) ----------------- #
    master = data.master_df()
    scope = master if wilayah_code == "SEMUA" else master[master["wilayah"] == wilayah_code]
    domain_scope = scope[scope["domain_mangrove"] == True]

    n_cells = len(scope)
    n_hotspot = int(scope["hotspot_tenggelam"].sum()) if "hotspot_tenggelam" in scope.columns else 0
    subs_val = C.MEDIAN_SUBSIDENCE.get(wilayah_code, 1.45)
    sink_val = C.MEDIAN_SINK_YEAR.get(wilayah_code, "2068")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        ui.kpi(f"{n_cells:,}".replace(",", "."), f"transek dievaluasi ({len(domain_scope)} domain mangrove)")
    with k2:
        ui.kpi(f"{n_hotspot}", "hotspot kritis tenggelam (< 2050)")
    with k3:
        ui.kpi(f"{subs_val:.1f} cm/th", "median laju amblesan InSAR")
    with k4:
        ui.kpi(f"{sink_val}", "median estimasi tahun tenggelam", small=(len(str(sink_val)) > 8))

    st.write("")

    # --- 4. Modul Peta Pydeck (GPU-Accelerated, Instan, Full Width) ------- #
    sub_texts = {
        "tipologi": "Fokus 920 transek domain mangrove aktif dalam 4 kuadran mitigasi: RED, ORANGE, YELLOW, GREEN (garis abu-abu = pesisir non-mangrove).",
        "aksi_lengkap": "Visualisasi komprehensif seluruh 2.365 transek pesisir dengan 11 kelas rekomendasi aksi biofisik spesifik di lapangan.",
        "hotspot": "Titik merah berlingkar putih menandakan 46 transek kritis yang diproyeksikan tenggelam sebelum 2050.",
        "subsidence": "Gradien warna menandakan laju penurunan tanah InSAR dari kuning (< 1 cm/th) hingga merah pekat (> 4 cm/th)."
    }
    ui.mod_title_lg("Peta Spasial Interaktif & Tipologi Mitigasi", sub_texts[sel_mode])

    # Muat geometri garis transek via cached JSON loader
    gj_transek = data.load_transek_geojson()

    deck = maps.build_deck_map(
        wilayah=sel_wilayah_name,
        mode=sel_mode,
        basemap=sel_basemap,
        df_master=master,
        gj_transek=gj_transek
    )

    st.pydeck_chart(deck, use_container_width=True, height=520)

    # --- 5. Legenda Kartografis Responsif Sesuai Mode Peta ----------------- #
    if sel_mode == "tipologi":
        ui.legend([
            ("#b2182b", "RED · Rekayasa Hibrida"),
            ("#ea580c", "ORANGE · Managed Realignment"),
            ("#eab308", "YELLOW · Pengayaan Sabuk Hijau"),
            ("#16a34a", "GREEN · Konservasi Ketat"),
            ("#cbd5e1", "Pesisir Non-Domain Mangrove (1.445 transek)")
        ])
    elif sel_mode == "aksi_lengkap":
        ui.legend([
            ("#b2182b", "RED · Rekayasa Hibrida"),
            ("#ea580c", "ORANGE · Managed Realignment"),
            ("#eab308", "YELLOW · Pengayaan Sabuk Hijau"),
            ("#16a34a", "GREEN · Konservasi Ketat"),
            ("#0284c7", "Penangkap Sedimen + Lumpur"),
            ("#0ea5e9", "Restorasi Hidrologis + Sedimen"),
            ("#6366f1", "Restorasi Hidrologis Tambak"),
            ("#14b8a6", "Restorasi Alami Lumpur"),
            ("#8b5cf6", "Silvofishery Tambak Aktif"),
            ("#475569", "Perlindungan Pantai Terbangun"),
            ("#94a3b8", "Lahan Darat (Non-Prioritas)")
        ])
    elif sel_mode == "hotspot":
        ui.legend([
            ("#dc2626", "Hotspot Kritis Tenggelam (< 2050)"),
            ("#94a3b8", "Transek Pesisir Non-Kritis")
        ])
    elif sel_mode == "subsidence":
        ui.ramp_legend("Rendah (< 1.0 cm/th)", "Kritis (> 4.0 cm/th)")

    # --- 5. Sebaran Analitis Sesuai Mode Peta Tematik (Otomatis Sinkron) ---- #
    st.markdown("<hr>", unsafe_allow_html=True)

    titles_map = {
        "tipologi": (
            "Sebaran Tipologi Mitigasi 4 Kuadran Mangrove",
            f"Distribusi kuantitatif 920 transek mangrove berdasarkan matriks defisit vertikal laut dan restriksi darat di {sel_wilayah_name}."
        ),
        "aksi_lengkap": (
            "Sebaran 11 Rekomendasi Aksi Lapangan Pesisir",
            f"Komposisi tindakan mitigasi fisik komprehensif untuk seluruh 2.365 transek pesisir di {sel_wilayah_name}."
        ),
        "hotspot": (
            "Sebaran Status Kerentanan Tenggelam",
            f"Perbandingan proporsi transek hotspot kritis tenggelam (< 2050) vs transek pesisir non-kritis di {sel_wilayah_name}."
        ),
        "subsidence": (
            "Distribusi Tingkat Laju Penurunan Tanah (InSAR)",
            f"Sebaran transek berdasarkan kelas ambang batas amblesan tanah (kuning < 1 cm/th hingga merah pekat > 4 cm/th) di {sel_wilayah_name}."
        )
    }

    t_title, t_sub = titles_map[sel_mode]
    ui.mod_title_lg(t_title, t_sub)

    fig_breakdown = charts.plot_theme_breakdown(master, wilayah_code, mode=sel_mode)
    st.plotly_chart(fig_breakdown, use_container_width=True, config={"displayModeBar": False, "responsive": True})

    st.write("")

    # --- 6. Tabel Data Transek & Tombol Unduh CSV -------------------------- #
    with st.expander("Lihat & Unduh Data Transek pada Filter Ini", expanded=False):
        cols_show = [
            "transek_id", "wilayah", "rekomendasi", "v_edge_m_yr",
            "subs_cm_yr", "tahun_tenggelam_median", "jarak_penghalang_m", "pop_2026"
        ]
        avail = [c for c in cols_show if c in scope.columns]
        df_display = scope[avail].rename(columns={
            "transek_id": "ID Transek",
            "wilayah": "Wilayah",
            "rekomendasi": "Tipologi Rekomendasi",
            "v_edge_m_yr": "Laju Garis Pantai (m/th)",
            "subs_cm_yr": "Amblesan InSAR (cm/th)",
            "tahun_tenggelam_median": "Estimasi Th Tenggelam",
            "jarak_penghalang_m": "Jarak Penghalang (m)",
            "pop_2026": "Penduduk Terdampak 1km"
        })
        st.dataframe(df_display, use_container_width=True, hide_index=True, height=350)
        
        st.download_button(
            "Unduh Data CSV",
            data=df_display.to_csv(index=False).encode("utf-8"),
            file_name=f"sabuk_hijau_transek_{wilayah_code.lower()}.csv",
            mime="text/csv"
        )
