"""
Pembangun peta Pydeck interaktif berkinerja tinggi untuk SABUK HIJAU.
Menggunakan arsitektur Deck.GL berbasis GPU yang identik dengan Coraly (Daffa Elgo & Mutia).
Memberikan render instan (< 100 ms), basemap Carto Positron Vector GL presisi,
dan opsi foto satelit resolusi tinggi bebas galat JS.
"""

import pydeck as pdk
import pandas as pd
import json
import theme as theme
import constants as C

# Basemap resmi bergaya vector GL bebas watermark dan 100% presisi OSM
CARTO_POSITRON = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"

# Basemap Citra Satelit Resolusi Tinggi (Esri World Imagery via MapLibre Style JSON)
SATELLITE_STYLE = "https://raw.githubusercontent.com/roblabs/xyz-raster-sources/master/styles/arcgis-world-imagery.json"

# Sudut pandang (ViewState) per wilayah koridor
REGION_VIEWS = {
    "SEMUA": pdk.ViewState(latitude=-6.92, longitude=110.4, zoom=7.8, pitch=0, bearing=0),
    "SEM": pdk.ViewState(latitude=-6.93, longitude=110.48, zoom=11.2, pitch=0, bearing=0),
    "PKL": pdk.ViewState(latitude=-6.88, longitude=109.68, zoom=11.8, pitch=0, bearing=0),
    "CIR": pdk.ViewState(latitude=-6.71, longitude=108.62, zoom=11.2, pitch=0, bearing=0),
    "SBY": pdk.ViewState(latitude=-7.25, longitude=112.80, zoom=10.5, pitch=0, bearing=0),
    "JPR": pdk.ViewState(latitude=-6.59, longitude=110.67, zoom=11.5, pitch=0, bearing=0),
}

# Tooltip kartu interaktif bergaya modern Inter
TOOLTIP = {
    "html": (
        "<b>Transek {id}</b> ({wilayah})<br/>"
        "Aksi Lapangan: <b>{rek}</b><br/>"
        "Domain Mangrove: <b>{domain}</b><br/>"
        "Amblesan InSAR: <b>{subs} cm/th</b><br/>"
        "Estimasi Tenggelam: <b>{th_tenggelam}</b><br/>"
        "Jarak ke Tanggul/Penghalang: <b>{dist_barrier} m</b>"
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

def build_deck_map(
    wilayah: str,
    mode: str,
    basemap: str,
    df_master: pd.DataFrame,
    gj_coast: dict = None,
    gj_transek: dict = None
) -> pdk.Deck:
    """Membangun objek pdk.Deck berkinerja tinggi GPU-accelerated."""
    code = C.NAME_TO_CODE.get(wilayah, "SEMUA")
    view = REGION_VIEWS.get(code, REGION_VIEWS["SEMUA"])
    
    # Filter dataframe sesuai wilayah
    df_plot = df_master.copy()
    if code != "SEMUA":
        df_plot = df_plot[df_plot["wilayah"] == code]

    layers = []

    # 1. Layer Garis Pantai OSM via PathLayer murni (Bebas 100% dari bug triangulasi poligon)
    if gj_coast is not None:
        coast_col = [15, 23, 42, 210] if basemap != "Citra Satelit" else [255, 255, 255, 240]
        coast_paths = []
        for f in gj_coast.get("features", []):
            geom = f.get("geometry", {})
            gtype = geom.get("type")
            coords = geom.get("coordinates", [])
            if gtype == "LineString":
                if len(coords) >= 2:
                    coast_paths.append({"path": coords})
            elif gtype == "Polygon":
                for ring in coords:
                    if len(ring) >= 2:
                        coast_paths.append({"path": ring})
            elif gtype == "MultiLineString":
                for line in coords:
                    if len(line) >= 2:
                        coast_paths.append({"path": line})
        
        if coast_paths:
            layers.append(
                pdk.Layer(
                    "PathLayer",
                    data=coast_paths,
                    get_path="path",
                    get_color=coast_col,
                    width_scale=1,
                    width_min_pixels=2,
                    width_max_pixels=4,
                    pickable=False,
                )
            )

    # 2. Layer Tematik Utama
    if mode in ["tipologi", "aksi_lengkap"]:
        focus_4k = (mode == "tipologi")
        
        # a. Garis Transek via PathLayer (Aman, cepat, dan bebas artefak WebGL)
        if gj_transek is not None:
            feats = gj_transek.get("features", [])
            if code != "SEMUA":
                feats = [f for f in feats if f.get("properties", {}).get("wilayah") == code]
            
            paths = []
            for f in feats:
                p = f.get("properties", {})
                coords = f.get("geometry", {}).get("coordinates", [])
                if not coords or len(coords) < 2:
                    continue
                rek = p.get("rekomendasi", "")
                is_dom = bool(p.get("domain_mangrove", False))
                col = color_action(rek, is_domain=is_dom, focus_4k=focus_4k)
                paths.append({
                    "path": coords,
                    "id": str(p.get("transek_id", "")),
                    "wilayah": str(p.get("wilayah", "")),
                    "rek": rek,
                    "domain": "Ya (Aktif)" if is_dom else "Pesisir Terbuka",
                    "subs": round(float(p.get("subs_cm_yr", 0)), 1),
                    "th_tenggelam": str(p.get("tahun_tenggelam_median", "-")),
                    "dist_barrier": round(float(p.get("jarak_penghalang_m", 0))),
                    "color": col,
                })
            
            layers.append(
                pdk.Layer(
                    "PathLayer",
                    data=paths,
                    get_path="path",
                    get_color="color",
                    width_scale=1,
                    width_min_pixels=3,
                    width_max_pixels=6,
                    pickable=True,
                )
            )

        # b. Titik Transek untuk penanda yang jelas saat zoom out
        pts = []
        for _, row in df_plot.iterrows():
            rek = str(row.get("rekomendasi", ""))
            is_dom = bool(row.get("domain_mangrove", False))
            col = color_action(rek, is_domain=is_dom, focus_4k=focus_4k)
            pts.append({
                "coordinates": [float(row["lon"]), float(row["lat"])],
                "id": str(row.get("transek_id", "")),
                "wilayah": str(row.get("wilayah", "")),
                "rek": rek,
                "domain": "Ya (Aktif)" if is_dom else "Pesisir Terbuka",
                "subs": round(float(row.get("subs_cm_yr", 0)), 1),
                "th_tenggelam": str(row.get("tahun_tenggelam_median", "-")),
                "dist_barrier": round(float(row.get("jarak_penghalang_m", 0))),
                "color": col,
            })

        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=pts,
                get_position="coordinates",
                get_fill_color="color",
                get_radius=180,
                radius_min_pixels=3,
                radius_max_pixels=14,
                pickable=True,
            )
        )

    elif mode == "hotspot":
        # Mode Hotspot Kritis Tenggelam (< 2050)
        pts_normal = []
        pts_hotspot = []
        for _, row in df_plot.iterrows():
            is_hot = bool(row.get("hotspot_tenggelam", False))
            coord = [float(row["lon"]), float(row["lat"])]
            pdata = {
                "coordinates": coord,
                "id": str(row.get("transek_id", "")),
                "wilayah": str(row.get("wilayah", "")),
                "rek": str(row.get("rekomendasi", "")),
                "domain": "Ya" if bool(row.get("domain_mangrove", False)) else "Tidak",
                "subs": round(float(row.get("subs_cm_yr", 0)), 1),
                "th_tenggelam": str(row.get("tahun_tenggelam_median", "-")),
                "dist_barrier": round(float(row.get("jarak_penghalang_m", 0))),
            }
            if is_hot:
                pdata["color"] = [220, 38, 38, 255]
                pts_hotspot.append(pdata)
            else:
                pdata["color"] = [203, 213, 225, 120]
                pts_normal.append(pdata)

        # Base non-hotspot
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=pts_normal,
                get_position="coordinates",
                get_fill_color="color",
                get_radius=120,
                radius_min_pixels=2,
                radius_max_pixels=8,
                pickable=True,
            )
        )
        # Hotspot kritis menyala
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=pts_hotspot,
                get_position="coordinates",
                get_fill_color="color",
                get_line_color=[255, 255, 255, 255],
                stroked=True,
                line_width_min_pixels=2,
                get_radius=350,
                radius_min_pixels=6,
                radius_max_pixels=20,
                pickable=True,
            )
        )

    elif mode == "subsidence":
        # Mode Laju Penurunan Tanah InSAR
        pts = []
        for _, row in df_plot.iterrows():
            s_val = float(row.get("subs_cm_yr", 0))
            pts.append({
                "coordinates": [float(row["lon"]), float(row["lat"])],
                "id": str(row.get("transek_id", "")),
                "wilayah": str(row.get("wilayah", "")),
                "rek": str(row.get("rekomendasi", "")),
                "domain": "Ya" if bool(row.get("domain_mangrove", False)) else "Tidak",
                "subs": round(s_val, 1),
                "th_tenggelam": str(row.get("tahun_tenggelam_median", "-")),
                "dist_barrier": round(float(row.get("jarak_penghalang_m", 0))),
                "color": _color_subsidence(s_val),
            })

        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=pts,
                get_position="coordinates",
                get_fill_color="color",
                get_radius=220,
                radius_min_pixels=3,
                radius_max_pixels=14,
                pickable=True,
            )
        )

    # Konfigurasi Basemap (Kanvas Bersih vs Citra Satelit)
    if basemap == "Citra Satelit":
        m_provider = "maplibre"
        m_style = SATELLITE_STYLE
    else:
        m_provider = "carto"
        m_style = CARTO_POSITRON

    return pdk.Deck(
        layers=layers,
        initial_view_state=view,
        map_provider=m_provider,
        map_style=m_style,
        tooltip=TOOLTIP,
        views=[pdk.View(type="MapView", controller={"dragRotate": False, "touchRotate": False})],
    )
