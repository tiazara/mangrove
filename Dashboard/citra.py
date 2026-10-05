"""
Potongan citra satelit sepanjang transek (penampang melintang visual) untuk SABUK HIJAU.
Tile XYZ diunduh, digabung, lalu dipotong dan diputar sehingga 0 m (laut) di kiri dan
3.500 m (darat) di kanan, selaras dengan sumbu jarak transek pada grafik.

Sumber citra:
- Sentinel-2 cloudless tahunan (EOX IT Services GmbH; contains modified Copernicus Sentinel data)
- Esri World Imagery (resolusi tinggi, tanggal akuisisi beragam)
"""

import io
import math
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import streamlit as st
from PIL import Image
from shapely.geometry import Polygon, box

import data as data

R_BUMI = 6378137.0
ORIGIN = math.pi * R_BUMI
LEBAR_SETENGAH_M = data.KORIDOR_M      # potongan selebar koridor analisis (±150 m)
LEBAR_PX = 1400                         # 3.500 m -> 2,5 m per piksel

SUMBER = {
    "esri": ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 16),
    "s2": ("https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-{tahun}_3857/default/GoogleMapsCompatible/{z}/{y}/{x}.jpg", 14),
}
TAHUN_S2 = [2021, 2023, 2025]
ATRIBUSI = ("Citra: Sentinel-2 cloudless {tahun} by EOX IT Services GmbH (contains modified Copernicus Sentinel data); "
            "Esri World Imagery (Maxar, Earthstar Geographics).")

def _merc(lon: float, lat: float) -> tuple[float, float]:
    return R_BUMI * math.radians(lon), R_BUMI * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

def _unduh(url: str) -> Image.Image:
    req = urllib.request.Request(url, headers={"User-Agent": "sabuk-hijau-dashboard"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")

def _potong(garis_lonlat: list, url_tpl: str, z: int) -> Image.Image:
    """Potongan citra terputar sepanjang transek, lebar ±LEBAR_SETENGAH_M."""
    (lo0, la0), (lo1, la1) = garis_lonlat[0], garis_lonlat[-1]
    ax, ay = _merc(lo0, la0)
    bx, by = _merc(lo1, la1)
    skala = 1 / math.cos(math.radians((la0 + la1) / 2))     # meter tanah -> meter Mercator
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L                    # arah laut -> darat
    px, py = -uy, ux                                         # arah tegak lurus
    hw = LEBAR_SETENGAH_M * skala
    koridor = Polygon([(ax + hw * px, ay + hw * py), (bx + hw * px, by + hw * py),
                       (bx - hw * px, by - hw * py), (ax - hw * px, ay - hw * py)])

    res = 2 * ORIGIN / (256 * 2 ** z)
    x0, y0, x1, y1 = koridor.bounds
    tx0, tx1 = int((x0 + ORIGIN) / res // 256), int((x1 + ORIGIN) / res // 256)
    ty0, ty1 = int((ORIGIN - y1) / res // 256), int((ORIGIN - y0) / res // 256)
    # Hanya tile yang benar-benar memotong koridor
    tiles = [
        (tx, ty) for tx in range(tx0, tx1 + 1) for ty in range(ty0, ty1 + 1)
        if koridor.intersects(box(tx * 256 * res - ORIGIN, ORIGIN - (ty + 1) * 256 * res,
                                  (tx + 1) * 256 * res - ORIGIN, ORIGIN - ty * 256 * res))
    ]
    with ThreadPoolExecutor(8) as ex:
        imgs = list(ex.map(lambda t: _unduh(url_tpl.format(z=z, x=t[0], y=t[1])), tiles))
    mosaik = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256), (200, 200, 200))
    for (tx, ty), im in zip(tiles, imgs):
        mosaik.paste(im.resize((256, 256)), ((tx - tx0) * 256, (ty - ty0) * 256))

    tinggi_px = int(round(LEBAR_PX * 2 * LEBAR_SETENGAH_M / data.PANJANG_TRANSEK_M))
    su, sv = L / LEBAR_PX, 2 * hw / tinggi_px
    mx0 = (ax + hw * px + ORIGIN) / res - tx0 * 256
    my0 = (ORIGIN - (ay + hw * py)) / res - ty0 * 256
    # piksel keluaran (i, j) -> piksel mosaik: baris 0 = sisi +tegak lurus
    koef = (su * ux / res, -sv * px / res, mx0, -su * uy / res, sv * py / res, my0)
    return mosaik.transform((LEBAR_PX, tinggi_px), Image.AFFINE, koef, resample=Image.BICUBIC)

def _jpeg_uri(img: Image.Image) -> str:
    import base64
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

@st.cache_data(show_spinner=False, ttl=7 * 24 * 3600, max_entries=300)
def potongan_transek(transek_id: str) -> list[dict]:
    """Daftar potongan citra (label, data URI) untuk satu transek; kosong bila gagal diunduh."""
    garis = data.load_transek_geojson()
    feat = next((f for f in garis["features"] if f["properties"].get("transek_id") == transek_id), None)
    if feat is None:
        return []
    coords = feat["geometry"]["coordinates"]
    lapis = [("Citra resolusi tinggi (Esri, terkini)", "esri", SUMBER["esri"][0], SUMBER["esri"][1], None)]
    lapis += [(f"Sentinel-2 {t}", "s2", SUMBER["s2"][0].replace("{tahun}", str(t)), SUMBER["s2"][1], t) for t in TAHUN_S2]

    def satu(item):
        label, jenis, url, z, tahun = item
        try:
            return {"label": label, "jenis": jenis, "tahun": tahun, "uri": _jpeg_uri(_potong(coords, url, z))}
        except Exception:
            return None

    with ThreadPoolExecutor(4) as ex:
        hasil = list(ex.map(satu, lapis))
    return [h for h in hasil if h is not None]
