"""
Tab 3: Rencana Aksi & Simulator Kebijakan (SABUK HIJAU).
Menyediakan matriks kawasan prioritas terpadu, unduhan rencana aksi CSV,
dan simulator interaktif 'What-If' akresi sedimen dan horizon waktu.
"""

import streamlit as st
import pandas as pd
import components as ui
import constants as C
import data as data
import theme as theme
import charts as charts

def render():
    ui.section_title("Rencana Aksi Presisi & Simulasi Kebijakan",
                     "Pedoman intervensi fisik terpadu per ruas kawasan pesisir (≥ 500 m) dan pengujian sensitivitas mitigasi.")

    master = data.master_df()
    kawasan = data.kawasan_gdf()

    # --- 1. Pedoman Operasional Intervensi 4 Kuadran (N-Box Berwarna) ------ #
    ui.mod_title_lg(
        "Pedoman Operasional Intervensi 4 Kuadran",
        "Panduan tindakan mitigasi fisik spesifik per kuadran matriks defisit vertikal laut dan restriksi lateral darat."
    )
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    colors = [theme.COLOR_RED, theme.COLOR_ORANGE, theme.COLOR_YELLOW, theme.COLOR_GREEN]

    for i, code in enumerate(C.TIPOLOGI_ORDER):
        col = [q_col1, q_col2, q_col3, q_col4][i]
        with col:
            ui.nbox(
                title=f"{C.TIPOLOGI_LABEL[code]} ({C.TIPOLOGI_KM[code]} km)",
                body=f"<span style='font-size:12.5px;color:#334155;'>{C.TIPOLOGI_ACTION[code]}</span>",
                accent=colors[i]
            )

    st.write("")
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- 2. Tabel Matriks Rencana Aksi Kawasan (Filter Ganda & KPI) -------- #
    ui.mod_title_lg(
        "Matriks Kawasan Prioritas Intervensi Pesisir",
        "Rencana penanganan terpadu per ruas garis pantai kontinu (≥ 500 m) hasil agregasi spasial transek analitis."
    )

    f_col1, f_col2 = st.columns([1.2, 1.8])
    with f_col1:
        sel_w_name = st.selectbox(
            "Wilayah Koridor Pesisir:",
            options=C.REGION_NAMES,
            index=0,
            help="Saring ruas kawasan prioritas berdasarkan koridor wilayah."
        )
        w_code = C.NAME_TO_CODE[sel_w_name]

    with f_col2:
        rek_list = ["Semua Rekomendasi"] + sorted(kawasan["rekomendasi"].unique().tolist())
        sel_rek = st.selectbox(
            "Rekomendasi Kebijakan:",
            options=rek_list,
            index=0,
            help="Saring ruas berdasarkan klasifikasi tindakan aksi lapangan."
        )

    # Terapkan filter ganda
    filtered_kawasan = kawasan.copy()
    if w_code != "SEMUA":
        filtered_kawasan = filtered_kawasan[filtered_kawasan["wilayah"] == w_code]
    if sel_rek != "Semua Rekomendasi":
        filtered_kawasan = filtered_kawasan[filtered_kawasan["rekomendasi"] == sel_rek]

    tot_km = filtered_kawasan["panjang_km"].sum() if "panjang_km" in filtered_kawasan.columns else 0
    tot_pop = filtered_kawasan["pop"].sum() if "pop" in filtered_kawasan.columns else 0
    tot_ruas = len(filtered_kawasan)

    # 3 Kartu Metrik Ringkas ala Coraly
    k1, k2, k3 = st.columns(3)
    with k1:
        ui.kpi(f"{tot_ruas:,}".replace(",", "."), "ruas kawasan prioritas")
    with k2:
        ui.kpi(f"{tot_km:.1f} km", "panjang garis pantai intervensi")
    with k3:
        ui.kpi(f"{int(tot_pop):,}".replace(",", "."), "estimasi penduduk terlindungi (jiwa)")

    st.write("")

    cols_show = ["kawasan_id", "wilayah", "rekomendasi", "panjang_km", "transek", "pop", "hotspot"]
    avail_cols = [c for c in cols_show if c in filtered_kawasan.columns]
    
    df_table = filtered_kawasan[avail_cols].copy()
    # Map kode wilayah ke nama lengkap jika ada
    if "wilayah" in df_table.columns:
        df_table["wilayah"] = df_table["wilayah"].map(lambda x: C.CODE_TO_NAME.get(x, x))
    if "hotspot" in df_table.columns:
        df_table["hotspot"] = df_table["hotspot"].map(lambda x: "Kritis (< 2050)" if x and x > 0 else "Non-Kritis")
    if "panjang_km" in df_table.columns:
        df_table["panjang_km"] = df_table["panjang_km"].round(2)
    if "pop" in df_table.columns:
        df_table["pop"] = df_table["pop"].round(0).astype(int)

    df_table = df_table.rename(columns={
        "kawasan_id": "ID Kawasan",
        "wilayah": "Koridor Wilayah",
        "rekomendasi": "Rekomendasi Kebijakan",
        "panjang_km": "Panjang (km)",
        "transek": "Jumlah Transek",
        "pop": "Populasi 1km (Jiwa)",
        "hotspot": "Status Hotspot"
    })

    st.dataframe(df_table, use_container_width=True, hide_index=True)

    csv_data = df_table.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Unduh Tabel Rencana Aksi Kawasan (CSV)",
        data=csv_data,
        file_name="rencana_aksi_sabuk_hijau_pantura.csv",
        mime="text/csv",
        help="Ekspor matriks rencana aksi untuk pelaporan dinas atau Bappeda"
    )

    st.write("")
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- 3. Simulator Skenario Kebijakan Interaktif (Grafik Dinamis + Delta) #
    ui.mod_title_lg(
        "Simulator 'What-If': Uji Sensitivitas Intervensi & Horizon Waktu",
        "Eksplorasi pergeseran risiko dan alokasi kuadran saat laju akresi sedimen ditingkatkan atau horizon waktu diubah."
    )

    f_sim1, f_sim2, f_sim3, f_sim4 = st.columns([1.2, 1.3, 0.9, 1.1])
    with f_sim1:
        sel_w_sim = st.selectbox(
            "Wilayah Simulasi:",
            options=C.REGION_NAMES,
            index=0,
            help="Pilih koridor wilayah untuk mensimulasikan dampak akresi sedimen secara spesifik atau agregat seluruh Pantura."
        )
        w_code_sim = C.NAME_TO_CODE[sel_w_sim]
    with f_sim2:
        akresi_sim = st.slider(
            "Laju Akresi Sedimen (cm/th):",
            min_value=0.2, max_value=2.0, value=0.5, step=0.1,
            help="Nilai baseline Pb-210 = 0,5 cm/th. Nilai > 1,0 cm/th mengasumsikan pembangunan penangkap sedimen intensif (permeable dam)."
        )
    with f_sim3:
        horizon_sim = st.radio(
            "Target Horizon:",
            options=[2050, 2100],
            index=1,
            horizontal=True,
            help="Tahun batas evaluasi daya tahan elevasi mangrove terhadap kenaikan muka air laut dan amblesan tanah."
        )
    with f_sim4:
        st.write("")
        buka_tambak = st.checkbox(
            "Buka Pematang Tambak",
            value=True,
            help="Fasilitasi pembukaan pematang tambak terbengkalai di belakang tegakan untuk memperluas ruang mundur alami (Managed Realignment)."
        )

    # Filter domain mangrove sesuai wilayah simulasi terpilih
    domain_df = master[master["domain_mangrove"] == True].copy()
    if w_code_sim != "SEMUA":
        domain_df = domain_df[domain_df["wilayah"] == w_code_sim]

    # Rumus Ilmiah Esai: Defisit D = S + SLR - A
    # S = subs_cm_yr, SLR = 0.39 cm/th, A = akresi_sim
    # Waktu hingga tenggelam: T = (0.5 * R) / D
    import numpy as np
    defisit_sim = domain_df["subs_cm_yr"] + 0.39 - akresi_sim
    elevasi = domain_df["modal_elevasi_cm"].fillna(100.0)

    # Jika D <= 0 (akresi >= amblesan + SLR), mangrove tidak tenggelam (T -> 2200 / aman)
    # Jika D > 0, tahun tenggelam = 2026 + (elevasi / defisit_sim)
    tahun_sim = np.where(defisit_sim <= 0, 2200.0, 2026.0 + (elevasi / defisit_sim.replace(0, 0.001)))
    tahun_sim = np.clip(tahun_sim, 2026.0, 2200.0)

    terancam = tahun_sim < horizon_sim
    if buka_tambak:
        barrier_dekat = domain_df["jarak_penghalang_m"] <= 500.0
    else:
        barrier_dekat = (domain_df["jarak_penghalang_m"] <= 500.0) | (domain_df["lahan_utama"] == "tambak aktif")

    sim_types = []
    for s, b in zip(terancam, barrier_dekat):
        if s and b: sim_types.append("RED")
        elif s and not b: sim_types.append("ORANGE")
        elif not s and b: sim_types.append("YELLOW")
        else: sim_types.append("GREEN")

    domain_df["sim_type"] = sim_types

    # Grafik Batang Horizontal Komparatif: Baseline vs Skenario
    fig_sim = charts.plot_scenario_comparison(domain_df)
    st.plotly_chart(fig_sim, use_container_width=True, config={"displayModeBar": False, "responsive": True})

    # Hitung Delta Perubahan Kuadran
    n_red_orig = int((domain_df["Intervention_Type"] == "RED").sum())
    n_red_new = int((domain_df["sim_type"] == "RED").sum())
    diff_red = n_red_new - n_red_orig

    n_orange_orig = int((domain_df["Intervention_Type"] == "ORANGE").sum())
    n_orange_new = int((domain_df["sim_type"] == "ORANGE").sum())
    diff_orange = n_orange_new - n_orange_orig

    n_green_orig = int((domain_df["Intervention_Type"] == "GREEN").sum())
    n_green_new = int((domain_df["sim_type"] == "GREEN").sum())
    diff_green = n_green_new - n_green_orig

    # Tiga Kartu Delta Metrik
    d1, d2, d3 = st.columns(3)
    with d1:
        str_r = f"{diff_red:+d} transek" if diff_red != 0 else "0 transek"
        ui.kpi(str_r, f"perubahan status RED (kritis: {n_red_new})")
    with d2:
        str_o = f"{diff_orange:+d} transek" if diff_orange != 0 else "0 transek"
        ui.kpi(str_o, f"perubahan status ORANGE (mundur: {n_orange_new})")
    with d3:
        str_g = f"{diff_green:+d} transek" if diff_green != 0 else "0 transek"
        ui.kpi(str_g, f"perubahan zona GREEN (lestari: {n_green_new})")

    st.write("")

    scope_lbl = f"di {sel_w_sim}"
    if diff_red < 0:
        ui.note(
            f"<b>Hasil Skenario ({sel_w_sim}):</b> Peningkatan laju akresi sedimen ke <b>{akresi_sim:.1f} cm/th</b> berhasil "
            f"membebaskan <b>{abs(diff_red)} transek</b> dari zona prioritas darurat (RED). "
            f"Kawasan berdaya lentur tinggi (GREEN) kini mencakup <b>{n_green_new} transek</b>."
        )
    elif diff_red > 0:
        ui.note(
            f"<b>Hasil Skenario ({sel_w_sim}):</b> Horizon waktu atau batasan ruang darat yang lebih ketat menambah <b>{diff_red} transek</b> "
            f"ke dalam zona bahaya kritis (RED), menuntut akselerasi pembangunan struktur penangkap sedimen."
        )
    else:
        ui.note(
            f"<b>Hasil Skenario ({sel_w_sim}):</b> Jumlah transek berstatus darurat (RED) relatif seimbang pada konfigurasi parameter ini "
            f"({n_red_new} transek)."
        )

