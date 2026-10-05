"""
Tab 2: Dinamika & Penggerak (SABUK HIJAU).
Menampilkan perubahan mangrove 2021–2025, temuan regresi penggerak, deret waktu tepi laut
bulanan (Sentinel-1/2) beserta nowcast & ramalan Kalman, dan penampang melintang tutupan lahan.
"""

import streamlit as st
import pandas as pd
import components as ui
import constants as C
import data as data
import charts as charts
import maps as maps
import citra as citra

def render():
    ui.section_title("Dinamika Tepi Laut & Penggerak Perubahan",
                     "Bagaimana mangrove Pantura berubah, apa penyebabnya, dan di mana posisi tepinya saat ini.")

    master = data.master_df()
    y_df = data.y_bulanan_df()
    segmen_gdf = data.segmen_lahan_gdf()

    # --- Perubahan Mangrove 2021–2025 (GMW terkonfirmasi Sentinel) ---------- #
    ui.mod_title_lg("Perubahan Mangrove 2021–2025",
                    "Mangrove Pantura tumbuh ke darat, tetapi tepi lautnya tertekan (GMW 2021 vs 2025, terkonfirmasi sinyal Sentinel-1/2).")
    din = master["dinamika"].astype(str)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        ui.kpi(ui.angka(din.str.startswith("ekspansi").sum()), "transek mengalami ekspansi mangrove")
    with k2:
        ui.kpi(ui.angka(din.str.startswith("kehilangan").sum()), "transek kehilangan mangrove")
    with k3:
        ui.kpi(ui.angka((din == "stabil").sum()), "transek stabil")
    with k4:
        ui.kpi(ui.angka(int(master["kemungkinan_hilang"].sum())),
               f"transek kemungkinan kehilangan tegakan per {C.DATA_PER} (6 bulan terakhir)")

    st.write("")

    # --- Temuan Regresi Penggerak (Tabel 6 Esai) --------------------------- #
    ui.mod_title_lg("Penggerak Perubahan (Regresi dengan Galat Baku Klaster)",
                    "Pengaruh tekanan laut (amblesan) dan tekanan darat (kepadatan terbangun) per simpangan baku.")
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
    ui.mod_title_lg("Inspektur Transek",
                    "Pilih transek untuk melihat status, area yang dipertimbangkan analisis, posisi tepi terkini, "
                    "ramalan, dan profil lahannya. Daftar diurutkan dari yang paling prioritas.")

    col_sel1, col_sel2 = st.columns([1.2, 2.8])
    with col_sel1:
        regions = [r for r in C.REGION_NAMES if r != "Seluruh Pantura (Agregat)"]
        sel_w = st.selectbox("Pilih Wilayah:", regions, index=regions.index("Semarang – Demak"))
        w_code = C.NAME_TO_CODE[sel_w]
        jenis = st.radio("Jenis pantai:", ["Bermangrove", "Tanpa mangrove"], horizontal=True)
        is_dom = jenis == "Bermangrove"

        scope_w = master[(master["wilayah"] == w_code) & (master["domain_mangrove"] == is_dom)].copy()
        if is_dom:
            scope_w = scope_w.sort_values(["hotspot_tenggelam", "P_tenggelam_2050", "transek_id"],
                                          ascending=[False, False, True])
            label = {r.transek_id: f"{r.transek_id} · {r.Intervention_Type}" + (" · hotspot" if r.hotspot_tenggelam else "")
                     for r in scope_w.itertuples()}
        else:
            scope_w = scope_w.sort_values(["P_tenggelam_2100", "transek_id"], ascending=[False, True])
            label = {r.transek_id: f"{r.transek_id} · {r.rekomendasi}" for r in scope_w.itertuples()}
        sel_tid = st.selectbox("Pilih Transek:", options=list(label), format_func=label.get, index=0)
        t_row = scope_w[scope_w["transek_id"] == sel_tid].iloc[0]

    with col_sel2:
        tersensor = bool(t_row.get("B_hard_tersensor", False))
        sumber = {"pantai": "terukur langsung", "darat": "titik darat terdekat",
                  "tetangga": "diisi dari tetangga", "isian": "nilai isian"}.get(str(t_row.get("subs_sumber")), "-")
        laut_txt = (
            f"<b>Tekanan laut:</b> amblesan {ui.angka(t_row.get('subs_cm_yr'), 2)} cm/th ({sumber}) · "
            f"defisit elevasi {ui.angka(t_row.get('defisit_vertikal_cm_yr'), 2)} cm/th · "
            f"P(tenggelam &lt; 2050) {ui.angka(t_row.get('P_tenggelam_2050'), 2)} · "
            f"P(tenggelam &lt; 2100) {ui.angka(t_row.get('P_tenggelam_2100'), 2)} · "
            f"tahun tenggelam median {ui.tahun_tenggelam(t_row.get('tahun_tenggelam_median'))}<br/>"
        )
        if is_dom:
            jarak_txt = "tidak ada dalam 3 km" if tersensor else f"{ui.angka(t_row.get('MS_current_m'), 0)} m dari tepi saat ini"
            hot = " · <b style='color:#dc2626'>hotspot tenggelam padat penduduk</b>" if t_row.get("hotspot_tenggelam") else ""
            body = (
                f"<b>Tipologi:</b> {t_row.get('rekomendasi', '-')} "
                f"(keyakinan {ui.angka(t_row.get('keyakinan_tipologi', float('nan')) * 100, 0)}%; "
                f"RFI {ui.angka(t_row.get('RFI_score'), 2)}){hot}<br/>" + laut_txt +
                f"<b>Tekanan darat:</b> penghalang keras {jarak_txt} · "
                f"ruang peluang mundur {ui.angka(t_row.get('opp_space_m', 0), 0)} m · "
                f"P(tepi mencapai penghalang) 1 th {ui.angka(t_row.get('P_closed_1yr'), 2)}, "
                f"5 th {ui.angka(t_row.get('P_closed_5yr'), 2)}"
            )
        else:
            jarak_txt = "tidak ada dalam 3 km" if tersensor else f"{ui.angka(t_row.get('jarak_penghalang_m'), 0)} m dari garis pantai"
            body = (
                f"<b>Rekomendasi:</b> {t_row.get('rekomendasi', '-')} · jenis lahan <b>{t_row.get('lahan_utama', '-')}</b> · "
                f"status mangrove: {t_row.get('dinamika', '-')}<br/>" + laut_txt +
                f"<b>Lahan peluang:</b> penghalang keras {jarak_txt} · ruang peluang {ui.angka(t_row.get('opp_space_m', 0), 0)} m "
                f"(siap {ui.angka(t_row.get('peluang_siap_m', 0), 0)} m; perlu pengaturan air "
                f"{ui.angka(t_row.get('perlu_pengaturan_air_m', 0), 0)} m; silvofishery {ui.angka(t_row.get('silvofishery_m', 0), 0)} m) · "
                f"dataran lumpur di depan {ui.angka(t_row.get('lumpur_depan_m', 0), 0)} m"
            )
        ui.nbox(title=f"Rapor Transek {sel_tid} ({sel_w})", body=body, accent="#0284c7")

    # Area yang dipertimbangkan analisis untuk transek ini
    ui.mod_title_lg(
        f"Area yang Dipertimbangkan — {sel_tid}",
        "Zona tempat setiap variabel diukur. Koridor bergaris tepi hitam = transek ini (±150 m); pita warna di sampingnya = koridor "
        "transek tetangga yang saling tumpang tindih 50 m. Arahkan kursor ke setiap zona untuk penjelasan."
    )
    deck_area = maps.build_area_map(t_row, master, gj_coast=data.load_coast_geojson())
    st.pydeck_chart(deck_area, use_container_width=True, height=420)
    W = maps.AREA_WARNA
    rgb = lambda c: f"rgb({c[0]},{c[1]},{c[2]})"
    ui.legend([
        (rgb(W["koridor"]), "Koridor ±150 m → median amblesan InSAR"),
        (rgb(W["penduduk"]), "Radius 1 km → jumlah penduduk"),
        (rgb(W["genangan"]), "0–200 m di belakang tepi → frekuensi genangan"),
        (rgb(W["terbangun"]), "0–1 km di belakang tepi → kepadatan terbangun"),
        (rgb(W["tepi"]), "Tepi mangrove / garis pantai acuan"),
        (rgb(W["penghalang"]), "Penghalang keras terdekat"),
    ])

    if not is_dom:
        st.write("")
        _penampang_citra(sel_tid, t_row, is_dom, y_df, segmen_gdf)
        return

    # 1. Grafik Deret Waktu Tepi Bulanan + Nowcast & Ramalan
    v_rate = t_row.get("v_edge_m_yr", None)
    if pd.notnull(v_rate):
        arah = "mundur ke darat" if v_rate > 0 else "maju ke laut" if v_rate < 0 else "diam"
        v_rate_str = f"Laju tepi hasil model: <b>{ui.angka(v_rate, 1)} m/th</b> ({arah})"
    else:
        v_rate_str = "Laju tidak tersedia"
    ui.mod_title_lg(
        f"Posisi Tepi Laut Bulanan & Ramalan — {sel_tid}",
        f"{v_rate_str} · Titik = pengamatan Sentinel-1/2 (Jan 2021 – {C.DATA_PER}); "
        "berlian = nowcast Kalman dengan selang 95%; titik oranye = ramalan 6 dan 12 bulan."
    )
    fig_ts = charts.plot_timeseries(sel_tid, y_df, t_row)
    st.plotly_chart(fig_ts, use_container_width=True, config={"displayModeBar": False, "responsive": True})

    st.write("")

    # 2. Penampang Melintang dari Citra Satelit
    _penampang_citra(sel_tid, t_row, is_dom, y_df, segmen_gdf)


def _penampang_citra(sel_tid: str, t_row: pd.Series, is_dom: bool, y_df: pd.DataFrame, segmen_gdf):
    """Potongan citra satelit sepanjang transek per tahun + klasifikasi tutupan lahan di bawahnya."""
    ui.mod_title_lg(
        f"Penampang Melintang dari Citra Satelit — {sel_tid}",
        "Potongan citra selebar koridor ±150 m sepanjang transek, diputar agar laut di kiri dan darat di kanan. "
        "Bandingkan citra antartahun dengan klasifikasi tutupan lahan di baris terbawah"
        + ("; garis kuning = tepi mangrove terdeteksi pada tahun tersebut." if is_dom else ".")
    )
    with st.spinner("Mengunduh potongan citra satelit…"):
        potongan = citra.potongan_transek(sel_tid)

    tepi = {}
    if is_dom and sel_tid in y_df.index:
        deret = y_df.loc[sel_tid]
        for th in citra.TAHUN_S2:
            kol = [c for c in deret.index if str(c).startswith(str(th))]
            if kol:
                tepi[th] = deret[kol].median()

    b_pos = None
    if not bool(t_row.get("B_hard_tersensor", False)):
        if is_dom and pd.notnull(t_row.get("Y_now_m")) and pd.notnull(t_row.get("MS_current_m")):
            b_pos = t_row["Y_now_m"] + t_row["MS_current_m"]
        elif pd.notnull(t_row.get("jarak_penghalang_m")):
            b_pos = data.GARIS_PANTAI_M + t_row["jarak_penghalang_m"]

    if potongan:
        fig = charts.plot_citra_penampang(sel_tid, potongan, segmen_gdf, tepi, b_pos)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        tahun_txt = ", ".join(str(t) for t in citra.TAHUN_S2)
        st.caption(citra.ATRIBUSI.format(tahun=tahun_txt) +
                   " Tanggal akuisisi citra resolusi tinggi Esri beragam per lokasi; gunakan sebagai konteks visual.")
    else:
        st.info("Citra satelit tidak dapat diunduh saat ini; menampilkan klasifikasi tutupan lahan saja.")
        fig_cross = charts.plot_cross_section(sel_tid, segmen_gdf)
        st.plotly_chart(fig_cross, use_container_width=True, config={"displayModeBar": False, "responsive": True})
