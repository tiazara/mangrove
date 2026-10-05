"""
Tab 3: Rencana Aksi & Simulator Kebijakan (SABUK HIJAU).
Menyediakan matriks kawasan program yang diurutkan berdasarkan prioritas, unduhan rencana aksi CSV,
dan simulator 'What-If' yang menjalankan ulang Monte Carlo tipologi esai.
"""

import streamlit as st
import pandas as pd
import components as ui
import constants as C
import data as data
import theme as theme
import charts as charts

# Parameter skenario dasar esai (Bagian 2.2.4)
DASAR = dict(akresi=0.5, slr=0.39, horizon=2100, ms_dekat=500)

@st.cache_data(show_spinner=False)
def _tabel_kawasan(cache_version: str = "v3") -> pd.DataFrame:
    """Kawasan program diperkaya dengan risiko, kelayakan, koordinat, dan penduduk unik."""
    master = data.master_df()
    kaw = pd.DataFrame(data.kawasan_gdf().drop(columns="geometry"))
    agg = master.groupby("kawasan_id").agg(
        p_tgl_2100=("P_tenggelam_2100", "median"),
        p_tgl_2050=("P_tenggelam_2050", "median"),
        rfi=("RFI_score", "median"),
        n_hotspot=("hotspot_tenggelam", "sum"),
        lat=("lat", "mean"), lon=("lon", "mean"),
    )
    kaw = kaw.join(agg, on="kawasan_id")
    kaw["pop_unik"] = kaw["kawasan_id"].map(data.penduduk_unik_per_kawasan()).fillna(0)
    # Urutan prioritas: hotspot tenggelam -> peluang tenggelam 2100 -> kelayakan restorasi (RFI)
    kaw["_p_urut"] = kaw["p_tgl_2100"].round(2)
    kaw = kaw.sort_values(["n_hotspot", "_p_urut", "rfi"], ascending=[False, False, False]).reset_index(drop=True)
    return kaw

def render():
    ui.section_title("Rencana Aksi & Simulasi Kebijakan",
                     "Di mana harus bertindak lebih dulu, apa tindakannya, dan seberapa peka hasilnya terhadap asumsi.")

    master = data.master_df()

    # --- 1. Pedoman Operasional Intervensi 4 Tipologi ---------------------- #
    ui.mod_title_lg(
        "Pedoman Aksi Pantai Bermangrove (920 transek)",
        "Tipologi laut × darat; angka dalam kurung = panjang kawasan program dan jumlah transek."
    )
    q_cols = st.columns(4)
    colors = [theme.COLOR_RED, theme.COLOR_ORANGE, theme.COLOR_YELLOW, theme.COLOR_GREEN]
    for i, code in enumerate(C.TIPOLOGI_ORDER):
        with q_cols[i]:
            ui.nbox(
                title=f"{C.TIPOLOGI_LABEL[code]} ({ui.angka(C.TIPOLOGI_KM[code], 1)} km · {C.TIPOLOGI_N[code]} transek)",
                body=f"<span style='font-size:12.5px;color:#334155;'>{C.TIPOLOGI_ACTION[code]}</span>",
                accent=colors[i]
            )

    st.write("")
    pedoman_tanpa_mangrove(master)

    st.write("")
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- 2. Matriks Kawasan Prioritas -------------------------------------- #
    ui.mod_title_lg(
        "Daftar Kawasan Program Berdasarkan Prioritas",
        "Ruas pantai bersebelahan dengan rekomendasi sama digabung menjadi kawasan program. "
        "Urutan: jumlah hotspot tenggelam → peluang tenggelam sebelum 2100 → kelayakan restorasi (RFI)."
    )

    kaw = _tabel_kawasan()
    f_col1, f_col2 = st.columns([1.2, 1.8])
    with f_col1:
        sel_w_name = st.selectbox("Wilayah:", options=C.REGION_NAMES, index=0,
                                  help="Saring kawasan program berdasarkan wilayah studi.")
        w_code = C.NAME_TO_CODE[sel_w_name]
    with f_col2:
        rek_list = ["Semua Rekomendasi"] + [r for r in C.REKOMENDASI_11 if r in set(kaw["rekomendasi"])]
        sel_rek = st.selectbox("Rekomendasi:", options=rek_list, index=0,
                               help="Saring kawasan berdasarkan jenis tindakan lapangan.")

    filt = kaw.copy()
    if w_code != "SEMUA":
        filt = filt[filt["wilayah"] == w_code]
    if sel_rek != "Semua Rekomendasi":
        filt = filt[filt["rekomendasi"] == sel_rek]

    ids_filt = tuple(sorted(master[master["kawasan_id"].isin(filt["kawasan_id"])]["transek_id"]))
    pop_total = data.penduduk_unik(ids_filt)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        ui.kpi(ui.angka(len(filt)), "kawasan program")
    with k2:
        ui.kpi(f"{ui.angka(filt['panjang_km'].sum(), 1)} km", "panjang garis pantai")
    with k3:
        ui.kpi(ui.angka(int(filt["n_hotspot"].sum())), "transek hotspot tenggelam padat penduduk")
    with k4:
        ui.kpi(ui.angka(round(pop_total, -2)), "penduduk terpapar dalam radius 1 km (jiwa unik)")

    st.write("")

    tbl = pd.DataFrame({
        "Peringkat": range(1, len(filt) + 1),
        "ID Kawasan": filt["kawasan_id"].to_numpy(),
        "Wilayah": filt["wilayah"].map(C.CODE_TO_NAME).to_numpy(),
        "Rekomendasi": filt["rekomendasi"].to_numpy(),
        "Hotspot (transek)": filt["n_hotspot"].astype(int).to_numpy(),
        "P(tenggelam < 2100)": filt["p_tgl_2100"].round(2).to_numpy(),
        "RFI": filt["rfi"].round(2).to_numpy(),
        "Panjang (km)": filt["panjang_km"].round(2).to_numpy(),
        "Transek": filt["transek"].astype(int).to_numpy(),
        "Penduduk Terpapar 1 km": filt["pop_unik"].round(0).astype(int).to_numpy(),
        "Lintang": filt["lat"].round(5).to_numpy(),
        "Bujur": filt["lon"].round(5).to_numpy(),
    })
    st.dataframe(
        tbl, use_container_width=True, hide_index=True, height=390,
        column_config={
            "P(tenggelam < 2100)": st.column_config.ProgressColumn(format="%.2f", min_value=0, max_value=1),
            "RFI": st.column_config.ProgressColumn("RFI (kelayakan)", format="%.2f", min_value=0, max_value=1),
            "Panjang (km)": st.column_config.NumberColumn(format="%.2f"),
            "Penduduk Terpapar 1 km": st.column_config.NumberColumn(format="localized"),
            "Lintang": st.column_config.NumberColumn(format="%.5f"),
            "Bujur": st.column_config.NumberColumn(format="%.5f"),
        }
    )
    st.caption("RFI = Restoration Feasibility Index (rerata peringkat ruang peluang, kesesuaian genangan, rendahnya amblesan, "
               "dan porsi tambak terbengkalai). Koordinat = titik tengah kawasan, dapat disalin ke Google Maps/GPS.")

    st.download_button(
        label="Unduh Daftar Kawasan Prioritas (CSV)",
        data=tbl.to_csv(index=False).encode("utf-8"),
        file_name="kawasan_prioritas_sabuk_hijau.csv",
        mime="text/csv",
        help="Ekspor daftar kawasan untuk pelaporan dinas atau Bappeda"
    )

    st.write("")
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- 3. Simulator Skenario (Monte Carlo Esai) -------------------------- #
    ui.mod_title_lg(
        "Simulator 'What-If': Seberapa Peka Tipologi terhadap Asumsi?",
        "Menjalankan ulang 2.000 simulasi Monte Carlo tipologi esai dengan parameter pilihan Anda. "
        "Pada parameter dasar (akresi 0,5 · SLR 0,39 · 2100 · 500 m) hasilnya identik dengan esai."
    )

    f1, f2, f3, f4, f5 = st.columns([1.2, 1.2, 1.2, 0.9, 1.1])
    with f1:
        sel_w_sim = st.selectbox("Wilayah Simulasi:", options=C.REGION_NAMES, index=0)
        w_code_sim = C.NAME_TO_CODE[sel_w_sim]
    with f2:
        akresi_sim = st.slider(
            "Akresi sedimen (cm/th):", min_value=0.2, max_value=1.5, value=DASAR["akresi"], step=0.1,
            help="Dasar 0,5 cm/th (Pb-210). Nilai lebih tinggi mencerminkan skenario penangkap sedimen. "
                 "Rentang 0,2–1,5 sesuai uji ketahanan esai."
        )
    with f3:
        slr_sim = st.slider(
            "Kenaikan muka laut (cm/th):", min_value=0.0, max_value=0.5, value=DASAR["slr"], step=0.01,
            help="Dasar 0,39 cm/th (altimetri Laut Jawa). Rentang uji esai 0–0,5."
        )
    with f4:
        horizon_sim = st.radio("Horizon:", options=[2050, 2100], index=1, horizontal=True,
                               help="Tekanan laut tinggi = peluang tenggelam sebelum tahun ini > 0,5.")
    with f5:
        ms_dekat_sim = st.select_slider(
            "Penghalang dianggap dekat (m):", options=[250, 500, 1000], value=DASAR["ms_dekat"],
            help="Tekanan darat tinggi bila penghalang keras berada dalam jarak ini di belakang tepi."
        )

    sim = data.simulasi_tipologi(round(akresi_sim, 2), round(slr_sim, 2), int(horizon_sim), float(ms_dekat_sim))
    if w_code_sim != "SEMUA":
        sim = sim[sim["wilayah"] == w_code_sim]

    fig_sim = charts.plot_scenario_comparison(sim)
    st.plotly_chart(fig_sim, use_container_width=True, config={"displayModeBar": False, "responsive": True})

    base = sim["Intervention_Type"].value_counts()
    new = sim["sim_type"].value_counts()
    d_cols = st.columns(4)
    for col, t in zip(d_cols, C.TIPOLOGI_ORDER):
        diff = int(new.get(t, 0)) - int(base.get(t, 0))
        with col:
            ui.kpi(f"{diff:+d}" if diff else "0", f"perubahan {t} (dasar {int(base.get(t, 0))} → {int(new.get(t, 0))})")

    st.write("")
    berubah = sim[sim["sim_type"] != sim["Intervention_Type"]]
    is_dasar = (round(akresi_sim, 2) == DASAR["akresi"] and round(slr_sim, 2) == DASAR["slr"]
                and int(horizon_sim) == DASAR["horizon"] and int(ms_dekat_sim) == DASAR["ms_dekat"])
    jaccard_ro = _jaccard(sim)
    if is_dasar:
        ui.note(f"<b>Skenario dasar esai ({sel_w_sim}).</b> Ubah parameter di atas untuk melihat transek mana yang berpindah kelas.")
    elif berubah.empty:
        ui.note(f"<b>Hasil ({sel_w_sim}):</b> tidak ada transek yang berpindah kelas. Tipologi tahan terhadap perubahan asumsi ini.")
    else:
        per_w = berubah.groupby("wilayah").size().sort_values(ascending=False)
        rincian = ", ".join(f"{C.CODE_TO_NAME[w]} {n}" for w, n in per_w.items())
        ui.note(
            f"<b>Hasil ({sel_w_sim}):</b> {len(berubah)} dari {len(sim)} transek bermangrove "
            f"({ui.angka(len(berubah) / max(len(sim), 1) * 100, 1)}%; ±{ui.angka(len(berubah) * 0.25, 2)} km pantai) berpindah kelas. "
            f"Kesamaan himpunan RED ∪ ORANGE dengan skenario dasar (Jaccard) = {ui.angka(jaccard_ro, 2)}. "
            f"Perpindahan terbanyak: {rincian}."
        )
        with st.expander("Lihat transek yang berpindah kelas"):
            tb = berubah.merge(master[["transek_id", "lat", "lon", "kawasan_id"]], on="transek_id")
            tb = tb.rename(columns={"transek_id": "ID Transek", "wilayah": "Wilayah", "Intervention_Type": "Kelas Dasar",
                                    "sim_type": "Kelas Skenario", "sim_yakin": "Keyakinan Skenario",
                                    "kawasan_id": "Kawasan", "lat": "Lintang", "lon": "Bujur"})
            tb["Keyakinan Skenario"] = tb["Keyakinan Skenario"].round(2)
            st.dataframe(tb, use_container_width=True, hide_index=True, height=300)

def pedoman_tanpa_mangrove(master: pd.DataFrame):
    """Tabel aturan + besaran 7 rekomendasi pantai tanpa mangrove (Lampiran 6 esai)."""
    ui.mod_title_lg(
        "Pedoman Aksi Pantai Tanpa Mangrove (1.445 transek)",
        "Ditentukan dari jenis lahan peluang × ancaman tenggelam sebelum 2100 (peluang &gt; 0,5)."
    )
    kaw = data.kawasan_gdf()
    non = master[master["domain_mangrove"] != True]
    rows = []
    for lahan, ancam, rek, warna, aksi in C.AKSI_NONMANGROVE:
        km = kaw[kaw["rekomendasi"] == rek]["panjang_km"].sum()
        n = int((non["rekomendasi"] == rek).sum())
        rows.append([
            lahan, ancam,
            f'<span class="dot" style="background:{warna};display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px"></span><b>{rek}</b>',
            ui.angka(n), ui.angka(km, 2),
            f'<span class="catatan">{aksi}</span>',
        ])
    ui.tabel_html(
        ["Jenis lahan", "Terancam tenggelam", "Rekomendasi", "Transek", "Panjang (km)", "Tindakan"],
        rows, align=["left", "left", "left", "right", "right", "left"],
        note="Dua rekomendasi penangkap sedimen (±74 km) adalah ruas terancam tenggelam yang perlu menaikkan elevasi "
             "sebelum penanaman, terutama di Pekalongan, Semarang–Demak, dan Cirebon."
    )
    with st.expander("Panjang per kawasan (km)"):
        tb = (kaw[kaw["rekomendasi"].isin([a[2] for a in C.AKSI_NONMANGROVE])]
              .pivot_table(index="rekomendasi", columns="wilayah", values="panjang_km", aggfunc="sum", fill_value=0)
              .reindex(index=[a[2] for a in C.AKSI_NONMANGROVE], columns=["PKL", "SEM", "CIR", "SBY", "JPR"], fill_value=0))
        tb.columns = [C.CODE_TO_NAME[c] for c in tb.columns]
        tb["Total"] = tb.sum(axis=1)
        st.dataframe(tb.round(2), use_container_width=True)

def _jaccard(sim: pd.DataFrame) -> float:
    a = sim["Intervention_Type"].isin(["RED", "ORANGE"])
    b = sim["sim_type"].isin(["RED", "ORANGE"])
    union = (a | b).sum()
    return float((a & b).sum() / union) if union else 1.0
