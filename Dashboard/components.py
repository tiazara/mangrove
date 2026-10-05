"""
Builder Elemen UI SABUK HIJAU (Kartu KPI, Header Wordmark, Tab Bar, Callout Box, Explainer).
Mengacu verbatim pada pola desain modern Coraly (Daffa Elgo & Mutia).
"""

import streamlit as st
import base64
from pathlib import Path
import theme as theme

def inject_css():
    """Injeksi token desain dan CSS kustom ke halaman Streamlit."""
    st.markdown(f"<style>{theme.build_css()}</style>", unsafe_allow_html=True)

def html(s: str):
    """Shorthand penulisan HTML."""
    st.markdown(s, unsafe_allow_html=True)

def angka(x, dec: int = 0) -> str:
    """Format angka gaya Indonesia: titik pemisah ribuan, koma desimal."""
    if x is None or x != x:
        return "–"
    s = f"{x:,.{dec}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")

def tahun_tenggelam(y, horizon: int = 2100) -> str:
    """Tahun tenggelam median; di luar horizon analisis ditulis '> 2100'."""
    if y is None or y != y or y > horizon:
        return f"> {horizon}"
    return f"{int(round(y))}"

def _get_logo_b64() -> str:
    """Mengambil string base64 logo SABUK HIJAU agar dapat disematkan langsung di HTML."""
    fp = Path(__file__).resolve().parent / "assets" / "logo.png"
    if fp.exists():
        encoded = base64.b64encode(fp.read_bytes()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    return ""

def header_band(tagline_html: str, logo: str = None):
    """Header terpusat: wordmark SABUK HIJAU + logo resmi + tagline resmi esai."""
    logo_b64 = _get_logo_b64()
    if logo_b64 and logo is None:
        logo_markup = f'<img src="{logo_b64}" class="sabuk-logo-img" alt="Logo SABUK HIJAU" />'
    elif logo:
        logo_markup = f'<span class="sabuk-logo">{logo}</span>'
    else:
        logo_markup = '<span class="sabuk-logo">🌿</span>'

    html(
        f"""
        <div class="sabuk-header">
          <div class="wordmark">
            {logo_markup}
            <span class="brand">SABUK HIJAU</span>
          </div>
          <div class="tagline">{tagline_html}</div>
          <div class="tagline" style="font-size:12.5px;opacity:.75;margin-top:4px">Data Sentinel-1/2 hingga Agustus 2026 · 2.365 transek · 5 kawasan Pantura</div>
        </div>
        """
    )

def tab_bar(tabs: list[str], key: str = "active_tab") -> str:
    """Tab bar horizontal berbentuk pil; tab aktif tersimpan di query param URL."""
    qp = st.query_params.get("tab")
    if key not in st.session_state:
        st.session_state[key] = qp if qp in tabs else tabs[0]
    active = st.session_state[key]

    with st.container():
        html('<span class="sabuk-tabmarker"></span>')
        cols = st.columns(len(tabs))
        for i, (col, label) in enumerate(zip(cols, tabs)):
            with col:
                is_active = label == active
                if st.button(
                    label,
                    key=f"{key}_btn_{i}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state[key] = label
                    st.query_params["tab"] = label
                    st.rerun()

    if st.query_params.get("tab") != active:
        st.query_params["tab"] = active
    return active

def tdv_card(color: str, name: str, definition: str):
    """Kartu penjelas narasi ilmiah dengan border atas berwarna khusus."""
    html(
        f"""<div class="tdv-card" style="border-top-color:{color}">
        <div class="tc-name" style="color:{color}">{name}</div>
        <div class="tc-def">{definition}</div></div>"""
    )

def component_explainer():
    """Tiga kartu penjelas pilar Coastal Squeeze (Sumbu Laut, Sumbu Darat, Tipologi)."""
    section_title(
        'Bagaimana "Coastal Squeeze" Dievaluasi?',
        "Setiap ruas pantai 250 m dinilai dari dua tekanan sekaligus, lalu diberi satu dari empat jenis aksi."
    )
    
    c1, c2, c3 = st.columns(3)
    with c1:
        tdv_card(
            "#d85a30",
            "Tekanan Laut: Amblesan & Kenaikan Muka Laut",
            "Amblesan (InSAR 1–15 cm/th di Pantura) ditambah kenaikan muka laut 0,39 cm/th melampaui akresi 0,5 cm/th. "
            "Tekanan tinggi bila peluang tenggelam sebelum 2100 &gt; 0,5. Median tahun tenggelam: Pekalongan 2040, Cirebon 2049, Semarang–Demak 2061."
        )
    with c2:
        tdv_card(
            "#1d9e75",
            "Tekanan Darat: Penghalang Keras & Ruang Mundur",
            "Bangunan, jalan, rel, dan tanggul yang menutup ruang mangrove bermigrasi ke darat. "
            "Tekanan tinggi bila penghalang keras ≤ 500 m di belakang tepi atau transek memotong tol/tanggul laut PSN."
        )
    with c3:
        tdv_card(
            "#0f6e56",
            "Rekomendasi: Laut × Darat",
            "<b>Pantai bermangrove</b> (920 transek): RED rekayasa hibrida · ORANGE buka ruang mundur · "
            "YELLOW pengayaan sabuk hijau · GREEN konservasi ketat (2.000 simulasi Monte Carlo). "
            "<b>Pantai tanpa mangrove</b> (1.445 transek): jenis lahan × ancaman tenggelam → 7 rekomendasi, "
            "mis. penangkap sedimen, restorasi tambak, atau perlindungan pantai terbangun."
        )

def kpi(value: str, unit: str, small: bool = False):
    """Kartu metrik minimalis (angka tebal + keterangan satuan di bawah)."""
    cls = "val sm" if small else "val"
    html(
        f"""
        <div class="kpi-card">
          <div class="{cls}">{value}</div>
          <div class="unit">{unit}</div>
        </div>
        """
    )

def nbox(title: str, body: str, accent: str = None):
    """Kotak narasi bergaris batas samping untuk temuan atau rekomendasi kunci."""
    style = f' style="border-left-color:{accent}"' if accent else ""
    html(
        f"""
        <div class="sabuk-nbox"{style}>
          <div class="nt">{title}</div>
          <div class="nb">{body}</div>
        </div>
        """
    )

def note(body: str):
    """Callout ringkas satu baris untuk batasan ilmiah atau petunjuk operasional."""
    html(f'<div class="note-callout"><span class="note-body">{body}</span></div>')

def section_title(title: str, sub: str = ""):
    """Judul bagian level-2 dengan subjudul penjelas."""
    html(f'<div class="section-title">{title}</div>')
    if sub:
        html(f'<div class="section-sub">{sub}</div>')

def mod_title_lg(title: str, sub: str = ""):
    """Judul modul besar dengan bar aksen hijau di sisi kiri."""
    html(f'<div class="mod-title-lg"><b>{title}</b></div>')
    if sub:
        html(f'<div class="mod-sub">{sub}</div>')

def legend(items: list[tuple[str, str]]):
    """Legenda horizontal berbentuk titik warna dan label teks."""
    rows = "".join(
        f'<span class="legend-item"><span class="dot" style="background:{c}"></span>{lbl}</span>'
        for c, lbl in items
    )
    html(f'<div class="legend-row">{rows}</div>')

def ramp_legend(low="rendah (< 1.0 cm/th)", high="sangat tinggi (> 4.0 cm/th)"):
    """Legenda gradien warna untuk laju amblesan tanah."""
    html(
        f"""<div class="ramp-legend">
        <span class="ramp-end">{low}</span>
        <span class="ramp-bar"></span>
        <span class="ramp-end">{high}</span></div>"""
    )

def tabel_html(header: list[str], rows: list[list[str]], align: list[str] = None, note: str = ""):
    """Tabel ringkas bergaya kartu (rata kanan untuk angka)."""
    align = align or ["left"] * len(header)
    th = "".join(f'<th style="text-align:{a}">{h}</th>' for h, a in zip(header, align))
    tr = "".join(
        "<tr>" + "".join(f'<td style="text-align:{a}">{c}</td>' for c, a in zip(r, align)) + "</tr>"
        for r in rows
    )
    foot = f'<div class="ringkas-note">{note}</div>' if note else ""
    html(f'<div class="ringkas-wrap"><table class="ringkas-tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{foot}</div>')
