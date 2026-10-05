"""
Pembangun peta Pydeck interaktif berkinerja tinggi untuk SABUK HIJAU.
Menggunakan arsitektur Deck.GL berbasis GPU yang identik dengan Coraly (Daffa Elgo & Mutia).
Memberikan render instan (< 100 ms), basemap Carto Positron Vector GL presisi,
dan opsi foto satelit resolusi tinggi bebas galat JS.
"""

import pydeck as pdk
import pandas as pd
import json
import math
import components as ui
import data as data
import theme as theme
import constants as C

# Basemap resmi bergaya vector GL bebas watermark dan 100% presisi OSM
CARTO_POSITRON = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"

# Basemap Citra Satelit Resolusi Tinggi (Esri World Imagery via MapLibre Style JSON)
SATELLITE_STYLE = "https://raw.githubusercontent.com/roblabs/xyz-raster-sources/master/styles/arcgis-world-imagery.json"

# Sudut pandang (ViewState) per wilayah dihitung dari batas sebaran transek agar
# seluruh kawasan masuk bingkai (lebar peta minimum diasumsikan ~900 x 500 px).
def _view_dari_batas(bounds, w_px=900, h_px=500, pad=1.15) -> pdk.ViewState:
    (s_, w_), (n_, e_) = bounds
    dlon, dlat = (e_ - w_) * pad, (n_ - s_) * pad
    zoom = min(math.log2(w_px * 360 / (512 * dlon)), math.log2(h_px * 360 / (512 * dlat)))
    return pdk.ViewState(latitude=(s_ + n_) / 2, longitude=(w_ + e_) / 2, zoom=round(zoom, 2), pitch=0, bearing=0)

REGION_VIEWS = {k: _view_dari_batas(v) for k, v in C.REGION_BOUNDS.items()}

# Tooltip kartu interaktif bergaya modern Inter
TOOLTIP = {
    "html": (
        "<b>Transek {id}</b> ({wilayah})<br/>"
        "Aksi Lapangan: <b>{rek}</b><br/>"
        "Bermangrove: <b>{domain}</b><br/>"
        "Amblesan InSAR: <b>{subs} cm/th</b><br/>"
        "Tahun tenggelam (median): <b>{th_tenggelam}</b><br/>"
        "Penghalang keras di belakang tepi: <b>{dist_barrier} m</b>"
    ),
    "style": {
        "backgroundColor": "#ffffff",
        "color": "#0f172a",
        "border": "0.5px solid #d9e5e6",
        "borderRadius": "8px",
        "padding": "8px 12px",
        "fontFamily": "Inter, sans-serif",
        "fontSize": "12px",
        "boxShadow": "0 2px 4px rgba(0,0,0,0.08)",
    },
}

def _jarak_txt(jarak, tersensor) -> str:
    """Jarak penghalang keras; tersensor berarti tidak ada penghalang dalam 3 km."""
    if bool(tersensor) or jarak is None or jarak != jarak:
        return "> 3.000"
    return ui.angka(float(jarak), 0)

def color_action(rek: str, is_domain: bool = True, focus_4k: bool = False) -> list[int]:
    """
    Pemetaan warna komprehensif untuk 10 kelas rekomendasi kanonik.
    """
    r = str(rek).upper()
    
    # 1. Empat Kuadran Utama Mangrove (Warna Menyala Berkarakter)
    if "RED" in r or "REKAYASA HIBRIDA" in r:
        return [178, 24, 43, 245]         # Merah Tua Pekat (RED · Rekayasa Hibrida)
    elif "ORANGE" in r or "MANAGED REALIGNMENT" in r or "RUANG MUNDUR" in r:
        return [234, 88, 12, 240]        # Oranye Menyala (ORANGE · Pembukaan Ruang Mundur Mangrove)
    elif "YELLOW" in r or "PENGAYAAN" in r:
        return [234, 179, 8, 240]        # Kuning Emas (YELLOW · Pengayaan Sabuk Hijau)
    elif "GREEN" in r or "KONSERVASI" in r:
        return [22, 163, 74, 240]         # Hijau Emerald (GREEN · Konservasi Ketat)
        
    # Jika mode adalah Fokus 4 Kuadran Mangrove murni, garis non-domain dibuat abu-abu lembut
    if focus_4k and not is_domain:
        return [203, 213, 225, 90]
        
    # 2. Rekomendasi Lapangan Pesisir Lengkap (11 Aksi)
    if "PENANGKAP SEDIMEN" in r and "LUMPUR" in r:
        return [2, 132, 199, 230]        # Biru Laut (Penangkap Sedimen + Lumpur)
    elif "RESTORASI HIDROLOGIS" in r and "SEDIMEN" in r:
        return [14, 165, 233, 230]       # Biru Langit (Restorasi Hidrologis + Sedimen)
    elif "RESTORASI HIDROLOGIS" in r or "TAMBAK TERBENGKALAI" in r:
        return [99, 102, 241, 230]       # Indigo (Restorasi Hidrologis Tambak)
    elif "RESTORASI ALAMI" in r:
        return [20, 184, 166, 230]       # Pirus / Teal (Restorasi Alami Lumpur)
    elif "SILVOFISHERY" in r:
        return [139, 92, 246, 230]       # Ungu (Silvofishery Tambak Aktif)
    elif "PERLINDUNGAN PANTAI" in r:
        return [71, 85, 105, 230]        # Slate / Abu-abu Gelap (Perlindungan Pantai Terbangun)
    elif "LAHAN DARAT" in r or "NON-PRIORITAS" in r:
        return [148, 163, 184, 160]      # Abu-abu Netral (Lahan Darat (Non-Prioritas))
    else:
        return [100, 116, 139, 180]

def _color_subsidence(val: float) -> list[int]:
    """Ramp warna laju amblesan tanah InSAR (kuning ke merah tua)."""
    if val >= 4.0:
        return [127, 0, 0, 240]
    elif val >= 2.0:
        return [220, 38, 38, 230]
    elif val >= 1.0:
        return [249, 115, 22, 220]
    elif val >= 0.5:
        return [250, 204, 21, 210]
    else:
        return [254, 240, 138, 200]

def _layer_garis_pantai(gj_coast: dict, basemap: str):
    """Garis pantai OSM via PathLayer murni (bebas bug triangulasi poligon)."""
    if gj_coast is None:
        return None
    coast_col = [15, 23, 42, 210] if basemap != "Citra Satelit" else [255, 255, 255, 240]
    coast_paths = []
    for f in gj_coast.get("features", []):
        geom = f.get("geometry", {})
        gtype, coords = geom.get("type"), geom.get("coordinates", [])
        if gtype == "LineString":
            parts = [coords]
        elif gtype in ("Polygon", "MultiLineString"):
            parts = coords
        else:
            parts = []
        coast_paths += [{"path": p} for p in parts if len(p) >= 2]
    if not coast_paths:
        return None
    return pdk.Layer("PathLayer", data=coast_paths, get_path="path", get_color=coast_col,
                     width_scale=1, width_min_pixels=1.5, width_max_pixels=3, pickable=False)

def _warna_transek(row, mode: str) -> list[int]:
    is_dom = bool(row.get("domain_mangrove", False))
    if mode == "hotspot":
        return [220, 38, 38, 210] if bool(row.get("hotspot_tenggelam", False)) else [148, 163, 184, 70]
    if mode == "subsidence":
        return _color_subsidence(float(row.get("subs_cm_yr", 0) or 0))
    return color_action(str(row.get("rekomendasi", "")), is_domain=is_dom, focus_4k=(mode == "tipologi"))

def _basemap(basemap: str):
    if basemap == "Citra Satelit":
        return "maplibre", SATELLITE_STYLE
    return "carto", CARTO_POSITRON

def build_deck_map(
    wilayah: str,
    mode: str,
    basemap: str,
    df_master: pd.DataFrame,
    gj_coast: dict = None,
    gj_transek: dict = None
) -> pdk.Deck:
    """Peta transek sebagai koridor analisis ±150 m × 3,5 km (laut → darat).

    Koridor bersebelahan saling tumpang tindih 50 m (jarak transek 250 m), sehingga pantai
    tampil sebagai sabuk menerus dan bagian yang dipertimbangkan dua transek tampak lebih pekat.
    """
    code = C.NAME_TO_CODE.get(wilayah, "SEMUA")
    view = REGION_VIEWS.get(code, REGION_VIEWS["SEMUA"])
    df_plot = df_master if code == "SEMUA" else df_master[df_master["wilayah"] == code]
    koridor = data.koridor_transek()

    recs = []
    for row in df_plot.to_dict("records"):
        tid = row["transek_id"]
        if tid not in koridor:
            continue
        recs.append({
            "polygon": koridor[tid],
            "id": tid,
            "wilayah": C.CODE_TO_NAME.get(row.get("wilayah"), row.get("wilayah")),
            "rek": str(row.get("rekomendasi", "")),
            "domain": "Ya" if bool(row.get("domain_mangrove", False)) else "Tidak",
            "subs": ui.angka(float(row.get("subs_cm_yr", 0) or 0), 1),
            "th_tenggelam": ui.tahun_tenggelam(row.get("tahun_tenggelam_median")),
            "dist_barrier": _jarak_txt(row.get("jarak_penghalang_m"), row.get("B_hard_tersensor")),
            "color": (warna := _warna_transek(row, mode)),
            "line": warna[:3] + [min(255, warna[3] + 60)],
            "_urut": 1 if (mode == "hotspot" and row.get("hotspot_tenggelam")) or
                          (mode == "tipologi" and row.get("domain_mangrove")) else 0,
        })
    # Kelas yang ditonjolkan digambar terakhir agar berada di atas
    recs.sort(key=lambda r: r["_urut"])

    layers = []
    coast = _layer_garis_pantai(gj_coast, basemap)
    if coast is not None:
        layers.append(coast)
    layers.append(pdk.Layer(
        "PolygonLayer",
        data=recs,
        get_polygon="polygon",
        get_fill_color="color",
        get_line_color="line",
        line_width_min_pixels=1,
        line_width_max_pixels=1.5,
        stroked=True,
        filled=True,
        pickable=True,
        auto_highlight=True,
        highlight_color=[15, 23, 42, 120],
    ))

    provider, style = _basemap(basemap)
    return pdk.Deck(
        layers=layers,
        initial_view_state=view,
        map_provider=provider,
        map_style=style,
        tooltip=TOOLTIP,
        views=[pdk.View(type="MapView", controller={"dragRotate": False, "touchRotate": False})],
    )


# --- Peta Area Pertimbangan Satu Transek ------------------------------------ #
AREA_WARNA = {
    "koridor": [17, 24, 39],
    "penduduk": [124, 58, 237],
    "terbangun": [71, 85, 105],
    "genangan": [14, 165, 233],
    "tepi": [15, 118, 110],
    "penghalang": [225, 29, 72],
    "transek": [15, 23, 42],
}

def build_area_map(row: pd.Series, df_master: pd.DataFrame, basemap: str = "Kanvas Bersih",
                   gj_coast: dict = None) -> pdk.Deck:
    """Peta zona yang dipakai analisis untuk satu transek beserta transek tetangganya."""
    tid = row["transek_id"]
    koridor = data.koridor_transek()
    is_dom = bool(row.get("domain_mangrove", False))
    # Posisi acuan (m dari ujung laut): tepi mangrove terkini atau garis pantai
    acuan = float(row["Y_now_m"]) if is_dom and pd.notnull(row.get("Y_now_m")) else data.GARIS_PANTAI_M
    nama_acuan = "Tepi mangrove terkini (nowcast)" if is_dom else "Garis pantai acuan"

    # Transek tetangga ±3 km (koridor saling tumpang tindih)
    sekitar = df_master[(df_master["wilayah"] == row["wilayah"]) &
                        ((df_master["lat"] - row["lat"]).abs() < 0.03) &
                        ((df_master["lon"] - row["lon"]).abs() < 0.03)]
    tetangga = []
    for r in sekitar.to_dict("records"):
        if r["transek_id"] == tid or r["transek_id"] not in koridor:
            continue
        col = color_action(str(r.get("rekomendasi", "")), is_domain=bool(r.get("domain_mangrove")))
        tetangga.append({"polygon": koridor[r["transek_id"]], "color": col[:3] + [70],
                         "nama": f"Transek tetangga {r['transek_id']}",
                         "ket": f"{r.get('rekomendasi', '-')} · koridornya tumpang tindih 50 m dengan transek sebelahnya"})

    zona_poli = [
        {"polygon": data.lingkaran(row["lon"], row["lat"], data.RADIUS_POP_M),
         "color": AREA_WARNA["penduduk"] + [22], "line": AREA_WARNA["penduduk"] + [230],
         "nama": "Radius penduduk 1 km",
         "ket": f"Penduduk WorldPop yang dihitung untuk transek ini: {ui.angka(row.get('pop_2026', 0))} jiwa"},
        {"polygon": koridor[tid], "color": AREA_WARNA["koridor"] + [45], "line": AREA_WARNA["koridor"] + [255],
         "nama": "Koridor transek ±150 m × 3,5 km",
         "ket": f"Median titik InSAR di koridor ini = amblesan {ui.angka(row.get('subs_cm_yr', 0), 2)} cm/th"},
    ]

    ruas = [
        {"path": data.ruas_pada_transek(tid, 0, data.PANJANG_TRANSEK_M), "color": AREA_WARNA["transek"] + [200], "w": 6,
         "nama": "Garis transek", "ket": "0 m (laut) → 500 m (garis pantai) → 3.500 m (darat), titik pengamatan tiap 10 m"},
        {"path": data.ruas_pada_transek(tid, acuan, acuan + 1000), "color": AREA_WARNA["terbangun"] + [210], "w": 46,
         "nama": "Zona kepadatan terbangun 0–1 km",
         "ket": "Rerata peluang terbangun Dynamic World di belakang tepi (tekanan darat)"},
        {"path": data.ruas_pada_transek(tid, acuan, acuan + 200), "color": AREA_WARNA["genangan"] + [235], "w": 90,
         "nama": "Zona frekuensi genangan 0–200 m",
         "ket": "Proporsi citra radar Sentinel-1 yang tergenang di belakang tepi (tekanan laut)"},
    ]

    titik = [{"position": data.titik_pada_transek(tid, acuan), "color": AREA_WARNA["tepi"] + [255],
              "nama": nama_acuan, "ket": f"{ui.angka(acuan, 0)} m dari ujung laut transek"}]
    if not bool(row.get("B_hard_tersensor", False)) and pd.notnull(row.get("jarak_penghalang_m")):
        jarak = float(row["MS_current_m"]) if is_dom and pd.notnull(row.get("MS_current_m")) else float(row["jarak_penghalang_m"])
        titik.append({"position": data.titik_pada_transek(tid, acuan + jarak), "color": AREA_WARNA["penghalang"] + [255],
                      "nama": "Penghalang keras terdekat",
                      "ket": f"{ui.angka(jarak, 0)} m di belakang {nama_acuan.lower()}"})

    layers = []
    coast = _layer_garis_pantai(gj_coast, basemap)
    if coast is not None:
        layers.append(coast)
    layers += [
        pdk.Layer("PolygonLayer", data=tetangga, get_polygon="polygon", get_fill_color="color",
                  get_line_color=[255, 255, 255, 160], line_width_min_pixels=0.6, stroked=True, pickable=True),
        pdk.Layer("PolygonLayer", data=zona_poli, get_polygon="polygon", get_fill_color="color",
                  get_line_color="line", line_width_min_pixels=2.5, stroked=True, pickable=True),
        pdk.Layer("PathLayer", data=ruas, get_path="path", get_color="color", get_width="w",
                  width_min_pixels=2, pickable=True),
        pdk.Layer("ScatterplotLayer", data=titik, get_position="position", get_fill_color="color",
                  get_line_color=[255, 255, 255, 255], stroked=True, line_width_min_pixels=2,
                  get_radius=45, radius_min_pixels=6, radius_max_pixels=12, pickable=True),
    ]

    pusat = data.titik_pada_transek(tid, 1500)
    provider, style = _basemap(basemap)
    return pdk.Deck(
        layers=layers,
        initial_view_state=pdk.ViewState(longitude=pusat[0], latitude=pusat[1], zoom=13.1, pitch=0, bearing=0),
        map_provider=provider,
        map_style=style,
        tooltip={"html": "<b>{nama}</b><br/>{ket}", "style": TOOLTIP["style"]},
        views=[pdk.View(type="MapView", controller={"dragRotate": False, "touchRotate": False})],
    )
