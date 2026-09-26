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

def render():
    ui.section_title("Rencana Aksi Presisi & Simulasi Kebijakan",
                     "Pedoman intervensi fisik terpadu per ruas kawasan pesisir (≥ 500 m) dan pengujian sensitivitas mitigasi.")

    master = data.master_df()
    kawasan = data.kawasan_gdf()

    # --- 4 Kotak Panduan Aksi Teknis (Verbatim Esai) ----------------------- #
    st.markdown("##### Pedoman Operasional Intervensi 4 Kuadran")
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

    # --- Tabel Matriks Rencana Aksi Kawasan --------------------------------- #
    st.markdown("##### Matriks Kawasan Prioritas Intervensi Pesisir")

    f_col1, f_col2 = st.columns([1.5, 2.5])
    with f_col1:
        rek_list = ["Semua Rekomendasi"] + sorted(kawasan["rekomendasi"].unique().tolist())
        sel_rek = st.selectbox("Saring berdasarkan Rekomendasi:", rek_list)

    filtered_kawasan = kawasan if sel_rek == "Semua Rekomendasi" else kawasan[kawasan["rekomendasi"] == sel_rek]

    tot_km = filtered_kawasan["panjang_km"].sum() if "panjang_km" in filtered_kawasan.columns else 0
    tot_pop = filtered_kawasan["pop"].sum() if "pop" in filtered_kawasan.columns else 0

    with f_col2:
        st.markdown(
            f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px 14px; font-size:13px; color:#334155; margin-top:14px;">
              <b>Total Ruas:</b> {len(filtered_kawasan)} kawasan | 
              <b>Panjang Garis Pantai:</b> {tot_km:.1f} km | 
              <b>Penduduk Terlindungi:</b> {int(tot_pop):,} jiwa
            </div>
            """,
            unsafe_allow_html=True
        )

    cols_show = ["kawasan_id", "wilayah", "rekomendasi", "panjang_km", "transek", "pop", "hotspot"]
    avail_cols = [c for c in cols_show if c in filtered_kawasan.columns]
    df_table = filtered_kawasan[avail_cols].rename(columns={
        "kawasan_id": "ID Kawasan",
        "wilayah": "Wilayah",
        "rekomendasi": "Rekomendasi Kebijakan",
        "panjang_km": "Panjang (km)",
        "transek": "Jumlah Transek",
        "pop": "Populasi 1km",
        "hotspot": "Hotspot Tenggelam"
    })

    st.dataframe(df_table, use_container_width=True, hide_index=True)

    csv_data = df_table.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Unduh Tabel Rencana Aksi (CSV)",
        data=csv_data,
        file_name="rencana_aksi_sabuk_hijau_pantura.csv",
        mime="text/csv",
        help="Ekspor matriks rencana aksi untuk pelaporan dinas atau Bappeda"
    )

    st.markdown("---")

    # --- Simulator Skenario Kebijakan Interaktif --------------------------- #
    st.markdown("##### Simulator 'What-If': Respons Akresi Sedimen & Horizon Waktu")
    st.caption("Eksplorasi pergeseran risiko bila intervensi penangkap sedimen diterapkan atau horizon perencanaan diubah.")

    p1, p2, p3 = st.columns(3)
    with p1:
        akresi_sim = st.slider("Laju Akresi Sedimen (cm/th):", 0.2, 2.0, 0.5, 0.1,
                               help="Nilai baseline Pb-210 = 0,5 cm/th. Nilai > 1,0 cm/th = penangkap sedimen intensif.")
    with p2:
        horizon_sim = st.radio("Horizon Waktu Target:", [2050, 2100], index=1, horizontal=True)
    with p3:
        buka_tambak = st.checkbox("Buka Pematang Tambak (Realignment)", value=True)

    # Hitung dampak skenario
    domain_df = master[master["domain_mangrove"] == True].copy()
    defisit_sim = domain_df["subs_cm_yr"] + 0.39 - akresi_sim
    elevasi = domain_df["modal_elevasi_cm"].fillna(100.0)

    ratio = elevasi / defisit_sim.replace(0, 0.001)
    tahun_sim = (2026.0 + ratio).clip(lower=2026, upper=2200)

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

    res1, res2 = st.columns(2)
    with res1:
        st.markdown("**Distribusi Eksisting (Baseline Pb-210, Horizon 2100)**")
        st.dataframe(domain_df["Intervention_Type"].value_counts().reset_index().rename(
            columns={"Intervention_Type": "Tipologi", "count": "Jumlah Transek"}), use_container_width=True, hide_index=True)

    with res2:
        st.markdown(f"**Distribusi Skenario (Akresi {akresi_sim:.1f} cm/th, Horizon {horizon_sim})**")
        st.dataframe(domain_df["sim_type"].value_counts().reset_index().rename(
            columns={"sim_type": "Tipologi Skenario", "count": "Jumlah Transek"}), use_container_width=True, hide_index=True)

    n_red_orig = (domain_df["Intervention_Type"] == "RED").sum()
    n_red_new = (domain_df["sim_type"] == "RED").sum()
    diff_red = n_red_new - n_red_orig

    if diff_red < 0:
        ui.note(f"<b>Hasil Skenario:</b> Peningkatan akresi ke {akresi_sim:.1f} cm/th berhasil membebaskan {abs(diff_red)} transek dari zona bahaya kritis (RED).")
    elif diff_red > 0:
        ui.note(f"<b>Hasil Skenario:</b> Horizon atau restriksi yang lebih ketat menambah {diff_red} transek ke dalam status prioritas darurat (RED).")
    else:
        ui.note("<b>Hasil Skenario:</b> Jumlah transek berstatus risiko tertinggi (RED) relatif stabil pada skenario ini.")
