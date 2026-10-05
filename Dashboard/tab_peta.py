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
    "aksi_lengkap": "Rekomendasi Aksi Seluruh Pantai (11 kelas)",
    "tipologi": "Tipologi Pantai Bermangrove saja (4 kelas)",
    "hotspot": "Hotspot Tenggelam Padat Penduduk (46 transek)",
    "subsidence": "Laju Penurunan Tanah InSAR (cm/th)"
}

def render():
    # --- 1. Penjelas Komponen Ilmiah (TDV-Card Style ala Coraly) ---------- #
    ui.component_explainer()
    st.write("")
    ringkasan_kawasan()
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
            help="Rekomendasi seluruh pantai (bermangrove + tanpa mangrove), tipologi bermangrove saja, hotspot, atau amblesan InSAR."
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
    n_hotspot = int(scope["hotspot_tenggelam"].sum())
    subs_med = domain_scope["subs_cm_yr"].median()
    pct_terukur = (scope["subs_sumber"] == "pantai").mean() * 100

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        ui.kpi(ui.angka(n_cells), f"transek dievaluasi ({ui.angka(len(domain_scope))} bermangrove)")
    with k2:
        ui.kpi(f"{n_hotspot}", "hotspot tenggelam padat penduduk")
    with k3:
        ui.kpi(f"{ui.angka(subs_med, 2)} cm/th",
               f"median amblesan InSAR transek bermangrove ({ui.angka(pct_terukur)}% transek terukur langsung)")
    with k4:
        if wilayah_code == "SEMUA":
            ui.kpi("2040–2061", "median tahun tenggelam tegakan di 3 kawasan terancam (PKL · CIR · SEM)", small=True)
        else:
            th = domain_scope["tahun_tenggelam_median"].median()
            ui.kpi(ui.tahun_tenggelam(th), "median tahun tenggelam tegakan mangrove")

    st.write("")

    # --- 4. Modul Peta Pydeck (GPU-Accelerated, Instan, Full Width) ------- #
    sub_texts = {
        "tipologi": "Hanya 920 transek bermangrove yang diwarnai sesuai tipologinya; abu-abu = pantai tanpa mangrove.",
        "aksi_lengkap": "Seluruh 2.365 transek: 4 tipologi untuk pantai bermangrove dan 7 rekomendasi untuk pantai tanpa mangrove.",
        "hotspot": f"Titik merah = {C.HOTSPOT_DEF}. Seluruhnya berada di Cirebon, Semarang–Demak, dan Pekalongan.",
        "subsidence": "Gradien warna menandakan laju penurunan tanah InSAR dari kuning (< 1 cm/th) hingga merah pekat (> 4 cm/th)."
    }
    ui.mod_title_lg(
        "Peta Rekomendasi per Transek",
        sub_texts[sel_mode] + " Setiap pita = koridor analisis ±150 m × 3,5 km (laut → darat); "
        "koridor bersebelahan tumpang tindih 50 m. Arahkan kursor untuk detail, gulir untuk memperbesar."
    )

    # Muat geometri garis pantai & transek via cached JSON loader
    gj_coast = data.load_coast_geojson()
    gj_transek = data.load_transek_geojson()

    deck = maps.build_deck_map(
        wilayah=sel_wilayah_name,
        mode=sel_mode,
        basemap=sel_basemap,
        df_master=master,
        gj_coast=gj_coast,
        gj_transek=gj_transek
    )

    st.pydeck_chart(deck, use_container_width=True, height=520)

    # --- 5. Legenda Kartografis Responsif Sesuai Mode Peta ----------------- #
    if sel_mode == "tipologi":
        ui.legend([
            ("#b2182b", "RED · Rekayasa Hibrida"),
            ("#ea580c", "ORANGE · Pembukaan Ruang Mundur Mangrove"),
            ("#eab308", "YELLOW · Pengayaan Sabuk Hijau"),
            ("#16a34a", "GREEN · Konservasi Ketat"),
            ("#cbd5e1", "Pantai tanpa mangrove (1.445 transek)")
        ])
    elif sel_mode == "aksi_lengkap":
        ui.html('<div class="legend-head">Pantai bermangrove</div>')
        ui.legend([
            ("#b2182b", "RED · Rekayasa Hibrida"),
            ("#ea580c", "ORANGE · Pembukaan Ruang Mundur Mangrove"),
            ("#eab308", "YELLOW · Pengayaan Sabuk Hijau"),
            ("#16a34a", "GREEN · Konservasi Ketat"),
        ])
        ui.html('<div class="legend-head">Pantai tanpa mangrove</div>')
        ui.legend([
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
            ("#dc2626", "Hotspot tenggelam padat penduduk"),
            ("#cbd5e1", "Bukan hotspot")
        ])
    elif sel_mode == "subsidence":
        ui.ramp_legend("Rendah (< 1,0 cm/th)", "Kritis (> 4,0 cm/th)")

    # --- 5. Sebaran Analitis Sesuai Mode Peta Tematik (Otomatis Sinkron) ---- #
    st.markdown("<hr>", unsafe_allow_html=True)

    titles_map = {
        "tipologi": (
            "Sebaran Tipologi Aksi Transek Bermangrove",
            f"Jumlah transek bermangrove per jenis aksi di {sel_wilayah_name}."
        ),
        "aksi_lengkap": (
            "Sebaran Rekomendasi Seluruh Pantai",
            f"Jumlah transek per rekomendasi (bermangrove dan tanpa mangrove) di {sel_wilayah_name}."
        ),
        "hotspot": (
            "Sebaran Hotspot Tenggelam Padat Penduduk",
            f"Jumlah transek hotspot ({C.HOTSPOT_DEF}) dibanding transek lain di {sel_wilayah_name}."
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
            "transek_id", "wilayah", "lat", "lon", "rekomendasi", "keyakinan_tipologi", "RFI_score",
            "P_tenggelam_2050", "P_tenggelam_2100", "tahun_tenggelam_median",
            "subs_cm_yr", "subs_sumber", "v_edge_m_yr", "jarak_penghalang_m", "hotspot_tenggelam", "pop_2026"
        ]
        avail = [c for c in cols_show if c in scope.columns]
        df_display = scope[avail].rename(columns={
            "transek_id": "ID Transek",
            "wilayah": "Wilayah",
            "lat": "Lintang", "lon": "Bujur",
            "rekomendasi": "Rekomendasi",
            "keyakinan_tipologi": "Keyakinan Kelas",
            "RFI_score": "RFI",
            "P_tenggelam_2050": "P(tenggelam < 2050)",
            "P_tenggelam_2100": "P(tenggelam < 2100)",
            "tahun_tenggelam_median": "Tahun Tenggelam (median)",
            "subs_cm_yr": "Amblesan InSAR (cm/th)",
            "subs_sumber": "Sumber Amblesan",
            "v_edge_m_yr": "Laju Tepi Laut (m/th, + = mundur)",
            "jarak_penghalang_m": "Jarak Penghalang Keras (m)",
            "hotspot_tenggelam": "Hotspot",
            "pop_2026": "Penduduk Radius 1 km"
        })
        st.dataframe(df_display, use_container_width=True, hide_index=True, height=350)
        st.caption("Penduduk radius 1 km per transek saling tumpang tindih antartransek; jangan dijumlahkan.")
        
        st.download_button(
            "Unduh Data CSV",
            data=df_display.to_csv(index=False).encode("utf-8"),
            file_name=f"sabuk_hijau_transek_{wilayah_code.lower()}.csv",
            mime="text/csv"
        )


def ringkasan_kawasan():
    """Tabel perbandingan lima kawasan: risiko, tipologi, prioritas, dan catatan keandalan data."""
    master = data.master_df()
    kawasan = data.kawasan_gdf()
    ui.mod_title_lg(
        "Perbandingan Antarkawasan",
        "Ringkasan lima kawasan studi, diurutkan dari yang paling cepat kehilangan modal elevasi."
    )
    warna = {"RED": "#b2182b", "ORANGE": "#ea580c", "YELLOW": "#ca8a04", "GREEN": "#16a34a"}
    rows = []
    for kode in ["PKL", "CIR", "SEM", "SBY", "JPR"]:
        sub = master[master["wilayah"] == kode]
        dom = sub[sub["domain_mangrove"] == True]
        tipe = dom["Intervention_Type"].value_counts()
        chips = " ".join(
            f'<span class="chip" style="background:{warna[t]}">{int(tipe.get(t, 0))}</span>' for t in C.TIPOLOGI_ORDER
        )
        km_orange = kawasan[(kawasan["wilayah"] == kode) & kawasan["rekomendasi"].str.startswith("ORANGE")]["panjang_km"].sum()
        rows.append([
            f"<b>{C.CODE_TO_NAME[kode]}</b>",
            f"{ui.angka(len(sub))} ({ui.angka(len(dom))})",
            ui.angka(dom["subs_cm_yr"].median(), 2),
            f"<b>{ui.tahun_tenggelam(dom['tahun_tenggelam_median'].median())}</b>",
            chips,
            ui.angka(km_orange, 1),
            str(int(sub["hotspot_tenggelam"].sum())),
            f'<span class="catatan">{C.CATATAN_DATA[kode]}</span>',
        ])
    ui.tabel_html(
        ["Kawasan", "Transek (bermangrove)", "Amblesan median bermangrove (cm/th)", "Tahun tenggelam tegakan",
         "RED · ORANGE · YELLOW · GREEN", "Kawasan ORANGE (km)", "Hotspot", "Catatan keandalan data"],
        rows,
        align=["left", "right", "right", "right", "left", "right", "right", "left"],
        note="Amblesan dan tahun tenggelam = median transek bermangrove; tahun tenggelam dari simulasi Monte Carlo (akresi 0,5 cm/th; SLR 0,39 cm/th). "
             "Kawasan ORANGE = panjang ruas program pembukaan ruang mundur."
    )
