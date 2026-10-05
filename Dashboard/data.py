"""
Pemuat data spasial dan tabular dengan caching Streamlit untuk performa cepat.
Terhubung langsung ke keluaran analisis di code/analisis/hasil/dashboard/.
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Folder hasil dashboard utama (di code/analisis/hasil/dashboard)
DIR_DASHBOARD_DATA = BASE_DIR / "code" / "analisis" / "hasil" / "dashboard"
if not DIR_DASHBOARD_DATA.exists():
    DIR_DASHBOARD_DATA = BASE_DIR / "Outputs" / "Statistik" / "dashboard"

# Folder layer spasial kartografi tambahan
DIR_SPATIAL_LAYERS = DIR_DASHBOARD_DATA / "layer_tambahan"
if not DIR_SPATIAL_LAYERS.exists():
    DIR_SPATIAL_LAYERS = BASE_DIR / "Spatial_Data" / "Layer_Tambahan"

# Folder deret waktu analitis
DIR_ANALISIS = BASE_DIR / "code" / "analisis" / "hasil" / "analisis"
if not DIR_ANALISIS.exists():
    DIR_ANALISIS = BASE_DIR / "Deret_Waktu"

def clean_rekomendasi(val) -> str:
    """Menstandarkan string rekomendasi ke 11 label kanonik resmi dashboard."""
    if pd.isna(val):
        return "-"
    s = str(val).strip()
    s_upper = s.upper()
    if "RED" in s_upper or "REKAYASA HIBRIDA" in s_upper:
        return "RED · Rekayasa Hibrida"
    if "ORANGE" in s_upper or "MANAGED REALIGNMENT" in s_upper or "RUANG MUNDUR" in s_upper:
        return "ORANGE · Pembukaan Ruang Mundur Mangrove"
    if "YELLOW" in s_upper or "PENGAYAAN" in s_upper:
        return "YELLOW · Pengayaan Sabuk Hijau"
    if "GREEN" in s_upper or "KONSERVASI" in s_upper:
        return "GREEN · Konservasi Ketat"
    if "PENANGKAP SEDIMEN" in s_upper and ("LUMPUR" in s_upper or "DATARAN" in s_upper):
        return "Penangkap Sedimen + Lumpur"
    if "TAMBAK TERBENGKALAI" in s_upper:
        return "Restorasi Hidrologis Tambak"
    if "RESTORASI HIDROLOGIS" in s_upper and "SEDIMEN" in s_upper:
        return "Restorasi Hidrologis + Sedimen"
    if "RESTORASI HIDROLOGIS" in s_upper:
        return "Restorasi Hidrologis Tambak"
    if "RESTORASI ALAMI" in s_upper:
        return "Restorasi Alami Lumpur"
    if "SILVOFISHERY" in s_upper:
        return "Silvofishery Tambak Aktif"
    if "PERLINDUNGAN PANTAI" in s_upper:
        return "Perlindungan Pantai Terbangun"
    if "LAHAN DARAT" in s_upper or "TIDAK PRIORITAS" in s_upper or "NON-PRIORITAS" in s_upper:
        return "Lahan Darat (Non-Prioritas)"
    return s

@st.cache_data(show_spinner=False)
def master_df(cache_version: str = "20260927_v3") -> pd.DataFrame:
    """Memuat master data 2.365 transek Pantura dengan rekomendasi kanonik."""
    fp = DIR_DASHBOARD_DATA / "master_transek_pantura.csv"
    df = pd.read_csv(fp)
    if "rekomendasi" in df.columns:
        df["rekomendasi"] = df["rekomendasi"].apply(clean_rekomendasi)
    if "typ_kawasan" in df.columns:
        df["typ_kawasan"] = df["typ_kawasan"].apply(clean_rekomendasi)
    return df

@st.cache_data(show_spinner=False)
def kamus_df(cache_version: str = "20260927_v3") -> pd.DataFrame:
    """Memuat kamus label kartografis dan definisi peubah."""
    fp = DIR_DASHBOARD_DATA / "kamus_label.csv"
    return pd.read_csv(fp)

@st.cache_data(show_spinner=False)
def y_bulanan_df() -> pd.DataFrame:
    """Memuat matriks posisi tepi laut bulanan Jan 2021 - Agu 2026."""
    fp = DIR_ANALISIS / "Y_bulanan.parquet"
    if not fp.exists():
        fp = BASE_DIR / "code" / "dataset" / "turunan" / "Y_bulanan.parquet"
    if not fp.exists():
        fp = BASE_DIR / "Deret_Waktu" / "Y_bulanan.parquet"
    return pd.read_parquet(fp)

@st.cache_data(show_spinner=False)
def transek_gdf(wilayah: str = "SEMUA", cache_version: str = "20260927_v3") -> gpd.GeoDataFrame:
    """Memuat garis transek analitis."""
    fp = DIR_DASHBOARD_DATA / "transek.geojson"
    gdf = gpd.read_file(fp)
    if "rekomendasi" in gdf.columns:
        gdf["rekomendasi"] = gdf["rekomendasi"].apply(clean_rekomendasi)
    if "typ_kawasan" in gdf.columns:
        gdf["typ_kawasan"] = gdf["typ_kawasan"].apply(clean_rekomendasi)
    if wilayah != "SEMUA" and "wilayah" in gdf.columns:
        gdf = gdf[gdf["wilayah"] == wilayah].copy()
    return gdf

@st.cache_data(show_spinner=False)
def gmw_change_gdf(wilayah: str = "SEMUA") -> gpd.GeoDataFrame:
    """Memuat poligon dinamika perubahan GMW (gain, loss, stable)."""
    fp = DIR_SPATIAL_LAYERS / "mangrove_gmw_perubahan_2021_2025.geojson"
    gdf = gpd.read_file(fp)
    if wilayah != "SEMUA" and "wilayah" in gdf.columns:
        gdf = gdf[gdf["wilayah"] == wilayah].copy()
    return gdf

@st.cache_data(show_spinner=False)
def garis_pantai_gdf(wilayah: str = "SEMUA") -> gpd.GeoDataFrame:
    """Memuat garis pantai acuan OSM."""
    fp = DIR_SPATIAL_LAYERS / "garis_pantai_osm.geojson"
    gdf = gpd.read_file(fp)
    if wilayah != "SEMUA" and "wilayah" in gdf.columns:
        gdf = gdf[gdf["wilayah"] == wilayah].copy()
    return gdf

@st.cache_data(show_spinner=False)
def amblesan_gdf(wilayah: str = "SEMUA") -> gpd.GeoDataFrame:
    """Memuat grid 500m laju penurunan tanah InSAR."""
    fp = DIR_SPATIAL_LAYERS / "amblesan_insar_ohenhen_grid500m.geojson"
    gdf = gpd.read_file(fp)
    if wilayah != "SEMUA" and "wilayah" in gdf.columns:
        gdf = gdf[gdf["wilayah"] == wilayah].copy()
    return gdf

@st.cache_data(show_spinner=False)
def penghalang_gdf(wilayah: str = "SEMUA") -> gpd.GeoDataFrame:
    """Memuat garis penghalang keras (jalan arteri, tol tanggul laut, rel)."""
    fp = DIR_SPATIAL_LAYERS / "penghalang_osm_garis.geojson"
    gdf = gpd.read_file(fp)
    if wilayah != "SEMUA" and "wilayah" in gdf.columns:
        gdf = gdf[gdf["wilayah"] == wilayah].copy()
    return gdf

@st.cache_data(show_spinner=False)
def kawasan_gdf(wilayah: str = "SEMUA", cache_version: str = "20260927_v3") -> gpd.GeoDataFrame:
    """Memuat batas ruas kawasan prioritas intervensi."""
    fp = DIR_DASHBOARD_DATA / "kawasan.geojson"
    gdf = gpd.read_file(fp)
    if "rekomendasi" in gdf.columns:
        gdf["rekomendasi"] = gdf["rekomendasi"].apply(clean_rekomendasi)
    if "typ_kawasan" in gdf.columns:
        gdf["typ_kawasan"] = gdf["typ_kawasan"].apply(clean_rekomendasi)
    if wilayah != "SEMUA" and "wilayah" in gdf.columns:
        gdf = gdf[gdf["wilayah"] == wilayah].copy()
    return gdf

@st.cache_data(show_spinner=False)
def segmen_lahan_gdf(wilayah: str = "SEMUA") -> gpd.GeoDataFrame:
    """Memuat segmen tutupan lahan untuk profil penampang melintang."""
    fp = DIR_DASHBOARD_DATA / "segmen_lahan.geojson"
    gdf = gpd.read_file(fp)
    if wilayah != "SEMUA" and "wilayah" in gdf.columns:
        gdf = gdf[gdf["wilayah"] == wilayah].copy()
    return gdf

@st.cache_data(show_spinner=False)
def load_coast_geojson() -> dict:
    """Memuat GeoJSON garis pantai OSM murni untuk Pydeck."""
    fp = DIR_SPATIAL_LAYERS / "garis_pantai_osm.geojson"
    if fp.exists():
        import json
        return json.loads(fp.read_text(encoding="utf-8"))
    return None

@st.cache_data(show_spinner=False)
def load_transek_geojson() -> dict:
    """Memuat GeoJSON garis transek analitis untuk Pydeck dengan rekomendasi kanonik."""
    fp = DIR_DASHBOARD_DATA / "transek.geojson"
    if fp.exists():
        import json
        gj = json.loads(fp.read_text(encoding="utf-8"))
        for f in gj.get("features", []):
            props = f.get("properties", {})
            if "rekomendasi" in props:
                props["rekomendasi"] = clean_rekomendasi(props["rekomendasi"])
        return gj
    return None


# --- Penduduk Terpapar Tanpa Hitung Ganda --------------------------------- #
# pop_2026 per transek adalah jumlah penduduk radius 1 km; transek berjarak 250 m
# sehingga radiusnya saling tumpang tindih. Penjumlahan langsung menghitung orang
# yang sama berkali-kali. Fungsi di bawah menggabungkan (union) seluruh radius
# lebih dulu, lalu memotongnya dengan grid WorldPop 1 km secara proporsional luas.
CRS_METER = 32749  # UTM 49S, mencakup seluruh Pantura (108–114° BT)
RADIUS_POP_M = 1000

@st.cache_resource(show_spinner=False)
def _grid_penduduk() -> gpd.GeoDataFrame:
    fp = DIR_SPATIAL_LAYERS / "penduduk_worldpop2026_grid1km.geojson"
    g = gpd.read_file(fp).to_crs(CRS_METER)
    g["luas_sel"] = g.area
    return g[["penduduk", "luas_sel", "geometry"]]

@st.cache_resource(show_spinner=False)
def _titik_transek() -> gpd.GeoSeries:
    m = master_df()
    pts = gpd.GeoSeries(gpd.points_from_xy(m["lon"], m["lat"]), index=m["transek_id"], crs=4326)
    return pts.to_crs(CRS_METER)

def _penduduk_dalam(geom) -> float:
    grid = _grid_penduduk()
    area = gpd.GeoDataFrame(geometry=[geom], crs=CRS_METER)
    x = gpd.overlay(grid, area, how="intersection", keep_geom_type=True)
    return float((x["penduduk"] * x.area / x["luas_sel"]).sum())

@st.cache_data(show_spinner=False)
def penduduk_unik(transek_ids: tuple) -> float:
    """Jumlah penduduk unik dalam radius 1 km dari sekumpulan transek (tanpa hitung ganda)."""
    if not transek_ids:
        return 0.0
    pts = _titik_transek().loc[list(transek_ids)]
    return _penduduk_dalam(pts.buffer(RADIUS_POP_M).union_all())

@st.cache_data(show_spinner=False)
def penduduk_unik_per_kawasan(cache_version: str = "v1") -> pd.Series:
    """Penduduk unik radius 1 km per kawasan program (indeks kawasan_id)."""
    m = master_df()
    pts = _titik_transek()
    buf = gpd.GeoDataFrame(
        {"kawasan_id": m["kawasan_id"].to_numpy()},
        geometry=pts.loc[m["transek_id"]].buffer(RADIUS_POP_M).to_numpy(), crs=CRS_METER
    ).dissolve(by="kawasan_id").reset_index()
    x = gpd.overlay(_grid_penduduk(), buf, how="intersection", keep_geom_type=True)
    x["jiwa"] = x["penduduk"] * x.area / x["luas_sel"]
    return x.groupby("kawasan_id")["jiwa"].sum()

# --- Simulasi Monte Carlo Tipologi (Replikasi Persis Notebook Bagian 8.2) --- #
# Draw acak memakai seed dan urutan yang sama dengan notebook analisis, sehingga
# parameter dasar (akresi 0,5; SLR 0,39; horizon 2100; penghalang 500 m)
# menghasilkan tipologi yang identik dengan esai (15 / 242 / 153 / 510).
N_SIM = 2000
SLR_SD = 0.04
SIGMA_B = 10.0
URUT_TIPE = ["RED", "ORANGE", "YELLOW", "GREEN"]

@st.cache_resource(show_spinner=False)
def _draw_monte_carlo():
    import numpy as np
    d = master_df()
    d = d[d["domain_mangrove"] == True].reset_index(drop=True)
    nd = len(d)
    rng = np.random.default_rng(8)
    sig_d = np.sqrt(d["subs_sigma"].to_numpy() ** 2 + SLR_SD ** 2)
    sub_s = d["subs_cm_yr"].to_numpy()[:, None] + sig_d[:, None] * rng.standard_normal((nd, N_SIM))
    sd_ms = np.sqrt(d["MS_uncertainty"].to_numpy() ** 2 + SIGMA_B ** 2)
    ms_s = d["MS_current_m"].to_numpy()[:, None] + sd_ms[:, None] * rng.standard_normal((nd, N_SIM))
    return d, sub_s.astype("float32"), ms_s.astype("float32")

@st.cache_data(show_spinner=False)
def simulasi_tipologi(akresi: float, slr: float, horizon: int, ms_dekat: float) -> pd.DataFrame:
    """Tipologi Monte Carlo seluruh transek bermangrove untuk satu skenario parameter."""
    import numpy as np
    d, sub_s, ms_s = _draw_monte_carlo()
    ambang = np.nan_to_num(d["modal_elevasi_cm"].to_numpy() / (horizon - 2026), nan=0.0)[:, None]
    laut = (sub_s + slr - akresi) >= ambang
    darat = ((ms_s <= ms_dekat) & ~d["B_hard_tersensor"].to_numpy()[:, None]) | d["PSN_overlap"].to_numpy()[:, None]
    pk = np.stack([(laut & darat).mean(1), (laut & ~darat).mean(1),
                   (~laut & darat).mean(1), (~laut & ~darat).mean(1)], 1)
    out = d[["transek_id", "wilayah", "Intervention_Type"]].copy()
    out["sim_type"] = np.array(URUT_TIPE)[pk.argmax(1)]
    out["sim_yakin"] = pk.max(1)
    return out

# --- Jejak Analisis Transek (Koridor ±150 m) ------------------------------ #
# Amblesan per transek = median titik InSAR dalam koridor ±150 m di sepanjang transek
# 3.500 m (0 m = laut, 500 m = garis pantai, 3.500 m = darat). Transek berjarak 250 m,
# sehingga koridor yang bersebelahan saling tumpang tindih 50 m.
KORIDOR_M = 150
PANJANG_TRANSEK_M = 3500
GARIS_PANTAI_M = 500

@st.cache_resource(show_spinner=False)
def _garis_transek_meter() -> gpd.GeoSeries:
    g = transek_gdf()
    return gpd.GeoSeries(g.geometry.to_numpy(), index=g["transek_id"].to_numpy(), crs=4326).to_crs(CRS_METER)

@st.cache_data(show_spinner=False)
def koridor_transek(cache_version: str = "v1") -> dict:
    """Poligon koridor ±150 m per transek (lon/lat) untuk PolygonLayer."""
    garis = _garis_transek_meter()
    poli = garis.buffer(KORIDOR_M, cap_style="flat").to_crs(4326)
    return {tid: [list(map(list, p.exterior.coords))] for tid, p in poli.items()}

def titik_pada_transek(transek_id: str, jarak_m: float) -> list:
    """Koordinat [lon, lat] titik pada jarak tertentu dari ujung laut transek."""
    garis = _garis_transek_meter().loc[transek_id]
    p = garis.interpolate(min(max(jarak_m, 0), PANJANG_TRANSEK_M))
    q = gpd.GeoSeries([p], crs=CRS_METER).to_crs(4326).iloc[0]
    return [q.x, q.y]

def ruas_pada_transek(transek_id: str, dari_m: float, sampai_m: float) -> list:
    return [titik_pada_transek(transek_id, dari_m), titik_pada_transek(transek_id, sampai_m)]

def lingkaran(lon: float, lat: float, radius_m: float) -> list:
    """Poligon lingkaran (lon/lat) berjari-jari tertentu di sekitar satu titik."""
    c = gpd.GeoSeries(gpd.points_from_xy([lon], [lat]), crs=4326).to_crs(CRS_METER).buffer(radius_m, 48)
    return [list(map(list, c.to_crs(4326).iloc[0].exterior.coords))]
