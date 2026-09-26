"""
Tab 2: Dinamika & Penggerak (SABUK HIJAU).
Menampilkan analisis kausalitas regresi, deret waktu tepi laut bulanan (Sentinel-1/2),
dan penampang melintang tutupan lahan.
"""

import streamlit as st
import pandas as pd
import components as ui
import constants as C
import data as data
import charts as charts

def render():
    ui.section_title("Dinamika Tepi Laut & Kausalitas Penggerak",
                     "Evaluasi empiris pergerakan garis tepi mangrove bulanan dan tekanan lingkungan pemicu coastal squeeze.")

    master = data.master_df()
    y_df = data.y_bulanan_df()
    segmen_gdf = data.segmen_lahan_gdf()

    # --- Temuan Regresi Kausalitas Esai (Tabel Kotak Terpadu) -------------- #
    st.markdown("##### Temuan Kausalitas Penggerak (Model Ekonometrika Spasial)")
    r_cols = st.columns(3)
    for i, col in enumerate(r_cols):
        item = C.REGRESI_FINDINGS[i]
        with col:
            ui.nbox(
                title=f"{item['penggerak']} → {item['respons']}",
                body=f"<b>Pengaruh:</b> {item['koefisien']} ({item['p_value']})<br/><span style='font-size:12px;color:#64748b;'>{item['keterangan']}</span>",
                accent="#0f6e56"
            )

    st.write("")

    # --- Inspektur Mikro per Transek --------------------------------------- #
    st.markdown("##### Inspektur Mikro Profil Ruang & Deret Waktu Transek")
    
    col_sel1, col_sel2 = st.columns([1.2, 2.8])
    with col_sel1:
        # Filter pilihan wilayah untuk menyaring ID transek
        sel_w = st.selectbox("Pilih Wilayah:", C.REGION_NAMES, index=1)
        w_code = C.NAME_TO_CODE[sel_w]
        
        scope_w = master if w_code == "SEMUA" else master[master["wilayah"] == w_code]
        domain_list = scope_w[scope_w["domain_mangrove"] == True]["transek_id"].tolist()
        transek_opts = domain_list if domain_list else scope_w["transek_id"].tolist()

        sel_tid = st.selectbox("Pilih ID Transek:", options=transek_opts, index=0)
        t_row = scope_w[scope_w["transek_id"] == sel_tid].iloc[0]

    with col_sel2:
        sink_yr = t_row.get("tahun_tenggelam_median", None)
        sink_txt = f"{int(sink_yr)}" if pd.notnull(sink_yr) and sink_yr < 2199 else "> 2200"
        ui.nbox(
            title=f"Rapor Evaluasi: {sel_tid} ({sel_w})",
            body=(
                f"<b>Tipologi Intervensi:</b> {t_row.get('rekomendasi', '-')}<br/>"
                f"<b>Defisit Vertikal:</b> {t_row.get('defisit_vertikal_cm_yr', 0):.2f} cm/th | "
                f"<b>Laju Amblesan:</b> {t_row.get('subs_cm_yr', 0):.2f} cm/th | "
                f"<b>Est. Tenggelam:</b> {sink_txt}<br/>"
                f"<b>Ruang Peluang Mundur:</b> {t_row.get('opp_space_m', 0):.0f} m | "
                f"<b>Jarak Penghalang Keras:</b> {t_row.get('jarak_penghalang_m', '-')} m"
            ),
            accent="#0284c7"
        )

    # 1. Grafik Deret Waktu Tepi Bulanan
    fig_ts = charts.plot_timeseries(sel_tid, y_df, t_row)
    st.plotly_chart(fig_ts, use_container_width=True)

    # 2. Penampang Melintang Tutupan Lahan
    fig_cross = charts.plot_cross_section(sel_tid, segmen_gdf)
    st.plotly_chart(fig_cross, use_container_width=True)

    st.write("")

    # --- Distribusi Tipologi Rekomendasi ----------------------------------- #
    st.markdown("##### Sebaran Rekomendasi Intervensi pada Wilayah Ini")
    fig_bar = charts.plot_typology_breakdown(master, w_code)
    st.plotly_chart(fig_bar, use_container_width=True)
