"""
Sampel validasi visual status tambak (buta: kelas dugaan tidak ditulis ke berkas isian).

Titik kandidat = titik di belakang garis pantai basis (dist_m >= 500) yang kelas Dynamic World dominannya air
pada >= 4 dari 6 tahun, bukan mangrove (GMW 2021/2025, WorldCover 2021), dan punya >= 36 bulan MNDWI teramati.
Strata = pola sementara dari MNDWI bulanan dan tide_coupling (dipakai hanya untuk menyebar sampel):
  aktif (dikeringkan >= 0,5 kali/th, tc <= 0,05), terhubung pasang (< 0,5/th, tc > 0,05),
  bervegetasi (< 0,5/th, tc <= 0,05, NDVI naik > 0,2), tergenang permanen (sisanya < 0,5/th, tc <= 0,05),
  campuran (>= 0,5/th, tc > 0,05). 10 titik per strata, maksimal 1 titik per transek, seed 42.
Klasifikasi resmi dihitung ulang di notebook; berkas ini hanya menentukan titik yang dicek.

Output: dataset/validasi_tambak_ISI_MANUAL.csv, dataset/validasi_tambak_titik.kml
"""
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer

CODE = Path(__file__).resolve().parents[1]
DS = CODE / "dataset"
STEP, LEN_SEA, P = 10, 500, 351
rng = np.random.default_rng(42)

z = np.load(DS / "turunan" / "tensor_profil.npz", allow_pickle=True)
IDS = z["ids"]; N = len(IDS)
NDVI, MNDWI, DW, TIDEC = z["NDVI"], z["MNDWI"], z["DW"], z["TIDEC"]
TH = pd.period_range("2021-01", "2026-08", freq="M").year.to_numpy()
idx = {t: i for i, t in enumerate(IDS)}
TR = pd.read_csv(DS / "transek_params_final.csv").set_index("transek_id").loc[IDS]

wc = pd.read_csv(DS / "worldcover_2021_transek.csv").sort_values(["transek_id", "dist_m"])
mangrove = wc.wc2021.to_numpy().reshape(N, P) == 95
g = pd.read_csv(DS / "gmw_v4112_transek.csv")
for y in (2021, 2025):
    s = g[g[f"gmw{y}"] == 1]
    mangrove[s.transek_id.map(idx).to_numpy(), (s.dist_m // STEP).astype(int).to_numpy()] = True

darat = (np.arange(P) * STEP >= LEN_SEA)[None, :]
kand = darat & ((DW.argmax(-1) == 0).sum(-1) >= 4) & ~mangrove
ii, jj = np.nonzero(kand)
M = MNDWI[ii, jj, :]; V = np.isfinite(M)
nvalid = V.sum(1)
drain = np.array([np.sum((s > 0)[:-1] & ~(s > 0)[1:]) for s in (M[k][V[k]] for k in range(len(ii)))])
drain_th = drain / np.maximum(nvalid / 12, 0.5)
ndvi_y = np.stack([np.nanmedian(NDVI[ii, jj][:, TH == y], 1) for y in (2021, 2026)], 1)
tc = TIDEC[ii, jj]
strata = np.select([(drain_th >= 0.5) & (tc <= 0.05), (drain_th < 0.5) & (tc > 0.05),
                    (drain_th < 0.5) & (tc <= 0.05) & (ndvi_y[:, 1] - ndvi_y[:, 0] > 0.2),
                    (drain_th < 0.5) & (tc <= 0.05)], ["aktif", "pasang", "vegetasi", "permanen"], "campuran")
ok = nvalid >= 36

pilih = []
for s in ["aktif", "pasang", "vegetasi", "permanen", "campuran"]:
    k = np.flatnonzero(ok & (strata == s))
    k = k[rng.permutation(len(k))]
    _, first = np.unique(ii[k], return_index=True)          # maksimal 1 titik per transek
    k = k[np.sort(first)]
    pilih += list(rng.choice(k, size=min(10, len(k)), replace=False))
pilih = np.array(pilih)[rng.permutation(len(pilih))]         # acak urutan supaya strata tidak tertebak

t = TR.iloc[ii[pilih]]
d = jj[pilih] * STEP
x = t.cx.to_numpy() - LEN_SEA * t.ux.to_numpy() + d * t.ux.to_numpy()
y = t.cy.to_numpy() - LEN_SEA * t.uy.to_numpy() + d * t.uy.to_numpy()
lon, lat = Transformer.from_crs("EPSG:32749", 4326, always_xy=True).transform(x, y)

out = pd.DataFrame(dict(id=[f"T{k + 1:02d}" for k in range(len(pilih))], transek_id=t.index, dist_m=d,
                        lat=np.round(lat, 6), lon=np.round(lon, 6), bukan_tambak="", pernah_kering="",
                        pematang_jebol="", bervegetasi="", tanggal_citra_dilihat="", yakin_1_3="", catatan=""))
out.to_csv(DS / "validasi_tambak_ISI_MANUAL.csv", index=False)

pm = "\n".join(f"<Placemark><name>{r.id}</name><description>{r.transek_id}, {r.dist_m} m</description>"
               f"<Point><coordinates>{r.lon},{r.lat},0</coordinates></Point></Placemark>" for r in out.itertuples())
(DS / "validasi_tambak_titik.kml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
    f"<name>Validasi status tambak ({len(out)} titik)</name>\n{pm}\n</Document></kml>\n", encoding="utf-8")
print(f"[OK] {len(out)} titik -> validasi_tambak_ISI_MANUAL.csv + validasi_tambak_titik.kml; "
      f"per wilayah: {t.region_code.value_counts().to_dict()}")
