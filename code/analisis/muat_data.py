"""
Pemuat data bersama untuk notebook 01 (eksplorasi) dan 02 (analisis).

Modul ini hanya membaca berkas di code/dataset/ dan menyusunnya menjadi array/tabel berkunci
(transek_id, dist_m). Tidak ada keputusan analisis di sini (ambang, domain, model): semua itu ada di
notebook, sehingga kedua notebook bisa dijalankan sendiri-sendiri tanpa membaca keluaran satu sama lain.
Tensor profil disimpan sebagai cache di dataset/turunan/ supaya pemuatan berikutnya cepat.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer

CODE = Path(__file__).resolve().parents[1]
DS = CODE / "dataset"
GEE = DS / "gee"
TUR = DS / "turunan"

REG = ["PKL", "SEM", "CIR", "SBY", "JPR"]
REG_NAMA = {"PKL": "Pekalongan", "SEM": "Semarang–Demak", "CIR": "Cirebon", "SBY": "Surabaya", "JPR": "Jepara (kontrol)"}
BULAN = pd.period_range("2021-01", "2026-08", freq="M")
T = len(BULAN)
TAHUN = np.arange(2021, 2027)                  # tahunan Dynamic World / genangan; 2026 = Jan-Agu
TH_T = BULAN.year.to_numpy()                   # tahun tiap langkah waktu bulanan
TAHUN_GMW = np.arange(1985, 2026)              # GMW v4.1.12: 41 tahun
STEP, LEN_SEA, P = 10, 500, 351                # titik tiap 10 m; 0 = ujung laut, 500 = garis pantai basis, 3500 = ujung darat
DIST = np.arange(P) * STEP
KELAS_DW = ["water", "trees", "crops", "built", "bare", "floodveg"]
CRS_UTM = "EPSG:32749"
KEY = ["transek_id", "dist_m"]


def _baca_paket(pola, prefix):
    cols, parts = None, []
    for f in sorted(GEE.glob(pola)):
        if cols is None:
            head = pd.read_csv(f, nrows=0).columns
            cols = KEY + [c for c in head if c.split("_")[0] in prefix]
        parts.append(pd.read_csv(f, usecols=cols))
    if not parts:
        return None
    return pd.concat(parts, ignore_index=True).sort_values(KEY, ignore_index=True)


def _tens(df, pre, skala, n):
    c = [f"{pre}_{p.strftime('%Y%m')}" for p in BULAN]
    return (df[c].to_numpy(np.float32) / skala).reshape(n, P, T)


def tensor_profil():
    """Profil bulanan S2/S1 (orbit descending tunggal) dan data statis per titik -> dict array [transek, titik, ...]."""
    f = TUR / "tensor_profil.npz"
    if not f.exists():
        TUR.mkdir(parents=True, exist_ok=True)
        s2 = _baca_paket("profil_s2_*.csv", ["ndvi", "mndwi", "n"])
        s1 = _baca_paket("profil_s1_*.csv", ["vv", "vh"])
        stt = pd.concat([pd.read_csv(x) for x in sorted(GEE.glob("statis_*.csv"))]).sort_values(KEY, ignore_index=True)
        assert (s2[KEY].values == s1[KEY].values).all() and (s2[KEY].values == stt[KEY].values).all()
        ids = s2.transek_id.unique(); n = len(ids)
        dw = np.stack([np.stack([stt[f"dw_{k}_{y}"].to_numpy(np.float32) / 1000 for k in KELAS_DW], -1) for y in TAHUN], 1)
        np.savez(f, ids=ids, NDVI=_tens(s2, "ndvi", 1000, n), MNDWI=_tens(s2, "mndwi", 1000, n),
                 NOBS=_tens(s2, "n_ndvi", 1, n), VV=_tens(s1, "vv", 100, n), VH=_tens(s1, "vh", 100, n),
                 DW=dw.reshape(n, P, len(TAHUN), len(KELAS_DW)),
                 INUND=(stt.inund_freq.to_numpy(np.float32) / 1000).reshape(n, P),
                 INUND_Y=np.stack([stt[f"inund_freq_{y}"].to_numpy(np.float32) / 1000 for y in TAHUN], -1).reshape(n, P, len(TAHUN)),
                 TIDEC=(stt.tide_coupling.to_numpy(np.float32) / 1000).reshape(n, P),
                 ELEV=(stt.elev_glo30_cm.to_numpy(np.float32) / 100).reshape(n, P))
    z = np.load(f, allow_pickle=True)
    return {k: z[k] for k in z.files}


def tensor_s1m(ids):
    """Profil S1 semua orbit (paket profil_s1m): VVD/VHD (descending), VVA/VHA (ascending), dB.
    None bila berkas belum diunduh ke dataset/gee/."""
    f = TUR / "tensor_s1m.npz"
    if not f.exists():
        df = _baca_paket("profil_s1m_*.csv", ["vvd", "vhd", "vva", "vha"])
        if df is None:
            return None
        u = df.transek_id.unique()
        if len(u) != len(ids) or not (u == ids).all():
            raise ValueError(f"profil_s1m belum lengkap: {len(u)} dari {len(ids)} transek")
        n = len(ids)
        np.savez(f, **{k.upper(): _tens(df, k, 100, n) for k in ["vvd", "vhd", "vva", "vha"]})
    z = np.load(f)
    return {k: z[k] for k in z.files}


def transek(ids):
    """Tabel transek: parameter geometri, amblesan InSAR, populasi WorldPop, koordinat pusat (WGS84)."""
    tr = pd.read_csv(DS / "transek_params_final.csv").set_index("transek_id").loc[ids]
    tr = tr.join(pd.read_csv(DS / "subs_insar_transek.csv").set_index("transek_id").drop(columns="region_code"))
    tr = tr.join(pd.read_csv(DS / "pop_worldpop_1km.csv").set_index("transek_id"))
    lon, lat = Transformer.from_crs(CRS_UTM, 4326, always_xy=True).transform(tr.cx.to_numpy(), tr.cy.to_numpy())
    tr["lon"], tr["lat"] = lon, lat
    return tr


def koordinat_titik(tr):
    """lon, lat [transek, titik] setiap titik sampel (ujung laut + dist_m x vektor ke darat)."""
    x = (tr.cx.to_numpy()[:, None] - LEN_SEA * tr.ux.to_numpy()[:, None]) + DIST[None] * tr.ux.to_numpy()[:, None]
    y = (tr.cy.to_numpy()[:, None] - LEN_SEA * tr.uy.to_numpy()[:, None]) + DIST[None] * tr.uy.to_numpy()[:, None]
    lon, lat = Transformer.from_crs(CRS_UTM, 4326, always_xy=True).transform(x.ravel(), y.ravel())
    return lon.reshape(x.shape), lat.reshape(x.shape)


def worldcover(ids):
    """Kode kelas ESA WorldCover 2021 per titik [transek, titik] (95 = mangrove)."""
    wc = pd.read_csv(DS / "worldcover_2021_transek.csv").sort_values(KEY)
    assert (wc.transek_id.to_numpy()[::P] == ids).all()
    return wc.wc2021.to_numpy().reshape(len(ids), P)


def gmw(ids):
    """Sebaran mangrove GMW v4.1.12 per titik per tahun [transek, titik, 41] (bool), 1985-2025."""
    g = pd.read_csv(DS / "gmw_v4112_transek.csv")
    idx = pd.Series(np.arange(len(ids)), index=ids)
    out = np.zeros((len(ids), P, len(TAHUN_GMW)), bool)
    out[idx.loc[g.transek_id].to_numpy(), (g.dist_m // STEP).astype(int).to_numpy()] = \
        g[[f"gmw{y}" for y in TAHUN_GMW]].to_numpy(bool)
    return out


def penghalang():
    """Persilangan penghalang keras: OSM (jalan, rel, tanggul, tol, konstruksi) + struktur baru Dynamic World."""
    return pd.concat([pd.read_csv(DS / "hard_barrier_persilangan.csv"),
                      pd.read_csv(DS / "hard_barrier_dw.csv").drop(columns="lebar_m")], ignore_index=True)


def gnss():
    return pd.read_csv(DS / "gnss_laju_amblesan.csv")


def akuisisi_s1():
    """Daftar akuisisi S1 per wilayah (lintasan, tanggal) untuk menjelaskan pola kekosongan radar."""
    out = []
    for r in REG:
        d = pd.read_csv(DS / f"s1_akuisisi_{r}.csv")
        d["region_code"] = r
        out.append(d)
    d = pd.concat(out, ignore_index=True)
    d["bulan"] = pd.to_datetime(d.time_utc).dt.to_period("M")
    return d


def orbit_transek():
    return pd.read_csv(DS / "s1_orbit_transek.csv").set_index("transek_id")


def validasi_tambak():
    """Isian validasi visual status tambak (dataset/validasi_tambak_ISI_MANUAL.csv); baris kosong dibuang."""
    f = DS / "validasi_tambak_ISI_MANUAL.csv"
    if not f.exists():
        return None
    d = pd.read_csv(f, dtype=str)
    isi = d[["bukan_tambak", "pernah_kering", "pematang_jebol", "bervegetasi"]].notna().any(axis=1)
    return d[isi].reset_index(drop=True)
