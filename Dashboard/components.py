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
        "Indeks kerentanan dan alokasi mitigasi ditentukan oleh interaksi defisit vertikal laut dan restriksi lateral darat."
    )
    
    c1, c2, c3 = st.columns(3)
    with c1:
        tdv_card(
            "#d85a30",
            "Sumbu Laut: Amblesan & Kenaikan Muka Air Laut",
            "Laju penurunan tanah (InSAR hingga 4,8 cm/th) & kenaikan muka laut memicu defisit elevasi vertikal dan risiko tenggelam permanen sebelum 2050 (median th 2068)."
        )
    with c2:
        tdv_card(
            "#1d9e75",
            "Sumbu Darat: Penghalang Keras & Ruang Mundur",
            "Jarak ke infrastruktur keras buatan manusia (tanggul laut, jalan arteri Pantura, pematang tambak) membatasi ruang akomodasi alami (buffer kritis 500 m)."
        )
    with c3:
        tdv_card(
            "#0f6e56",
            "Tipologi 4 Kuadran: Keputusan Mitigasi Presisi",
            "Klasifikasi spasial transek menjadi 4 aksi prioritas: RED · Rekayasa Hibrida, ORANGE · Managed Realignment, YELLOW · Pengayaan Sabuk Hijau, & GREEN · Konservasi Ketat."
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
