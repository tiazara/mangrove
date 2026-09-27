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
    if "ORANGE" in s_upper or "MANAGED REALIGNMENT" in s_upper:
        return "ORANGE · Managed Realignment"
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
def master_df() -> pd.DataFrame:
    """Memuat master data 2.365 transek Pantura dengan rekomendasi kanonik."""
    fp = DIR_DASHBOARD_DATA / "master_transek_pantura.csv"
    df = pd.read_csv(fp)
    if "rekomendasi" in df.columns:
        df["rekomendasi"] = df["rekomendasi"].apply(clean_rekomendasi)
    return df

@st.cache_data(show_spinner=False)
def kamus_df() -> pd.DataFrame:
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
def transek_gdf(wilayah: str = "SEMUA") -> gpd.GeoDataFrame:
    """Memuat garis transek analitis."""
    fp = DIR_DASHBOARD_DATA / "transek.geojson"
    gdf = gpd.read_file(fp)
    if "rekomendasi" in gdf.columns:
        gdf["rekomendasi"] = gdf["rekomendasi"].apply(clean_rekomendasi)
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
def kawasan_gdf(wilayah: str = "SEMUA") -> gpd.GeoDataFrame:
    """Memuat batas ruas kawasan prioritas intervensi."""
    fp = DIR_DASHBOARD_DATA / "kawasan.geojson"
    gdf = gpd.read_file(fp)
    if "rekomendasi" in gdf.columns:
        gdf["rekomendasi"] = gdf["rekomendasi"].apply(clean_rekomendasi)
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

