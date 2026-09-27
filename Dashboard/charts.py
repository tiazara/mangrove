"""
Grafik visualisasi analitis Plotly untuk SABUK HIJAU.
Dirancang dengan standar visual modern ala Coraly:
- Latar transparan (paper_bgcolor & plot_bgcolor = rgba(0,0,0,0))
- Tipografi Inter institusional
- Hover tooltip elegan gelap kontras (#04342c)
- Bebas dari elemen 'default plotly' (axis lines/gridlines kaku disederhanakan)
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import theme as theme

FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"

HOVER_STYLE = dict(
    bgcolor="#04342c",
    font_family=FONT_FAMILY,
    font_size=12.5,
    font_color="#ffffff",
    bordercolor="#0f6e56"
)

def plot_theme_breakdown(df: pd.DataFrame, wilayah: str = "SEMUA", mode: str = "tipologi") -> go.Figure:
    """Diagram batang horizontal adaptif ala Coraly yang otomatis sinkron dengan Mode Peta Tematik.
    
    Mode:
    - 'tipologi': Fokus Tipologi 4 Kuadran Mangrove (GREEN, ORANGE, YELLOW, RED)
    - 'aksi_lengkap': 11 Rekomendasi Aksi Lapangan Pesisir Komprehensif
    - 'hotspot': Perbandingan Hotspot Kritis (< 2050) vs Pesisir Adaptif
    - 'subsidence': Distribusi 5 Tingkat Amblesan Tanah InSAR (<0.5 hingga >4 cm/th)
    """
    sub = df if wilayah == "SEMUA" else df[df["wilayah"] == wilayah]

    if mode in ("tipologi", "4k"):
        # 1. Mode Fokus 4 Kuadran Mangrove (Domain Mangrove Aktif)
        m_sub = sub[sub["domain_mangrove"] == True]
        total_m = len(m_sub)

        quad_defs = [
            {
                "code": "GREEN",
                "label": "GREEN · Konservasi Ketat",
                "color": "#16a34a",
                "matriks": "Tekanan Laut Rendah × Tekanan Darat Rendah",
                "pedoman": "Zona lindung inti berdaya lentur alami tinggi"
            },
            {
                "code": "ORANGE",
                "label": "ORANGE · Pembukaan Ruang Mundur Mangrove",
                "color": "#ea580c",
                "matriks": "Tekanan Laut Tinggi × Tekanan Darat Rendah",
                "pedoman": "Pembukaan ruang mundur (jebol pematang tambak terbengkalai)"
            },
            {
                "code": "YELLOW",
                "label": "YELLOW · Pengayaan Sabuk Hijau",
                "color": "#eab308",
                "matriks": "Tekanan Laut Rendah × Tekanan Darat Tinggi",
                "pedoman": "Pengayaan jenis perakaran kokoh (Rhizophora/Avicennia)"
            },
            {
                "code": "RED",
                "label": "RED · Rekayasa Hibrida",
                "color": "#b2182b",
                "matriks": "Tekanan Laut Tinggi × Tekanan Darat Tinggi",
                "pedoman": "Struktur hibrida penangkap sedimen (permeable dam)"
            },
        ]

        items = []
        for q in quad_defs:
            cnt = int((m_sub["Intervention_Type"] == q["code"]).sum())
            pct = (cnt / total_m * 100) if total_m > 0 else 0
            items.append({
                "label": q["label"],
                "count": cnt,
                "pct": pct,
                "color": q["color"],
                "matriks": q["matriks"],
                "pedoman": q["pedoman"]
            })

        items = sorted(items, key=lambda x: x["count"], reverse=True)
        y_labels = [it["label"] for it in items]
        x_vals = [it["count"] for it in items]
        colors = [it["color"] for it in items]
        customdata = [[it["label"], it["matriks"], it["pedoman"], it["pct"]] for it in items]
        max_val = max(x_vals) if x_vals else 100

        hovertemplate = (
            "<b>%{customdata[0]}</b><br>"
            "Matriks Esai: <i>%{customdata[1]}</i><br>"
            "Pedoman Mitigasi: %{customdata[2]}<br>"
            "Jumlah: <b>%{x:,} transek</b> (%{customdata[3]:.1f}%)"
            "<extra></extra>"
        )

    elif mode == "hotspot":
        # 2. Mode Hotspot Kritis Tenggelam (< 2050) vs Transek Pesisir Non-Kritis
        total_all = len(sub)
        n_hot = int(sub["hotspot_tenggelam"].sum()) if "hotspot_tenggelam" in sub.columns else 0
        n_safe = total_all - n_hot
        pct_hot = (n_hot / total_all * 100) if total_all else 0
        pct_safe = (n_safe / total_all * 100) if total_all else 0

        items = [
            {
                "label": "Hotspot Kritis Tenggelam (< 2050)",
                "count": n_hot,
                "pct": pct_hot,
                "color": "#dc2626",
                "status": "Darurat / Amblesan Ekstrem",
                "keterangan": "Diproyeksikan tenggelam permanen sebelum 2050 tanpa intervensi"
            },
            {
                "label": "Transek Pesisir Non-Kritis",
                "count": n_safe,
                "pct": pct_safe,
                "color": "#64748b",
                "status": "Relatif Bertahan",
                "keterangan": "Batas ketahanan elevasi melampaui horizon perencanaan 2050"
            }
        ]

        items = sorted(items, key=lambda x: x["count"], reverse=True)
        y_labels = [it["label"] for it in items]
        x_vals = [it["count"] for it in items]
        colors = [it["color"] for it in items]
        customdata = [[it["label"], it["status"], it["keterangan"], it["pct"]] for it in items]
        max_val = max(x_vals) if x_vals else 100

        hovertemplate = (
            "<b>%{customdata[0]}</b><br>"
            "Status: <b>%{customdata[1]}</b><br>"
            "Keterangan: %{customdata[2]}<br>"
            "Jumlah: <b>%{x:,} transek</b> (%{customdata[3]:.1f}%)"
            "<extra></extra>"
        )

    elif mode == "subsidence":
        # 3. Mode Laju Penurunan Tanah InSAR (4 Kelas Ambang Batas Ilmiah, Severity-First)
        total_all = len(sub)
        s = sub["subs_cm_yr"]

        c_ekstrem = int((s >= 4.0).sum())
        c_stinggi = int(((s >= 2.0) & (s < 4.0)).sum())
        c_tinggi = int(((s >= 1.0) & (s < 2.0)).sum())
        c_rendah = int((s < 1.0).sum())

        subs_defs = [
            {
                "label": "> 4,0 cm/th (Ekstrem / Darurat)",
                "count": c_ekstrem,
                "color": "#7f0000",
                "tingkat": "Ekstrem / Darurat Amblesan",
                "keterangan": "Defisit elevasi vertikal akut, risiko tenggelam permanen tertinggi"
            },
            {
                "label": "2,0 – 4,0 cm/th (Sangat Tinggi)",
                "count": c_stinggi,
                "color": "#dc2626",
                "tingkat": "Sangat Tinggi",
                "keterangan": "Penurunan tanah masif yang mengunci ruang adaptasi mangrove"
            },
            {
                "label": "1,0 – 2,0 cm/th (Tinggi / Signifikan)",
                "count": c_tinggi,
                "color": "#f97316",
                "tingkat": "Tinggi / Signifikan",
                "keterangan": "Laju amblesan tanah melampaui kemampuan akresi sedimen alami"
            },
            {
                "label": "< 1,0 cm/th (Rendah / Relatif Stabil)",
                "count": c_rendah,
                "color": "#eab308",
                "tingkat": "Rendah / Relatif Stabil",
                "keterangan": "Kondisi amblesan relatif mampu diimbangi proses akresi alami habitat"
            }
        ]

        # Diurutkan berdasarkan tingkat keparahan (Severity-First: Ekstrem -> Rendah)
        y_labels = [it["label"] for it in subs_defs]
        x_vals = [it["count"] for it in subs_defs]
        colors = [it["color"] for it in subs_defs]
        customdata = [[it["label"], it["tingkat"], it["keterangan"], (it["count"] / total_all * 100) if total_all else 0] for it in subs_defs]
        max_val = max(x_vals) if x_vals else 100

        hovertemplate = (
            "<b>%{customdata[0]}</b><br>"
            "Klasifikasi: <b>%{customdata[1]}</b><br>"
            "Karakteristik: <i>%{customdata[2]}</i><br>"
            "Jumlah: <b>%{x:,} transek</b> (%{customdata[3]:.1f}%)"
            "<extra></extra>"
        )

    else:
        # 4. Mode Rekomendasi Aksi Lapangan (11 Aksi Lapangan Pesisir)
        counts = sub["rekomendasi"].value_counts().reset_index()
        counts.columns = ["Rekomendasi", "Jumlah"]
        counts = counts.sort_values(by="Jumlah", ascending=False)
        total_all = len(sub)

        action_colors = {
            "RED · Rekayasa Hibrida": "#b2182b",
            "ORANGE · Pembukaan Ruang Mundur Mangrove": "#ea580c",
            "YELLOW · Pengayaan Sabuk Hijau": "#eab308",
            "GREEN · Konservasi Ketat": "#16a34a",
            "Penangkap Sedimen + Lumpur": "#0284c7",
            "Restorasi Hidrologis + Sedimen": "#0ea5e9",
            "Restorasi Hidrologis Tambak": "#6366f1",
            "Restorasi Alami Lumpur": "#14b8a6",
            "Silvofishery Tambak Aktif": "#8b5cf6",
            "Perlindungan Pantai Terbangun": "#475569",
            "Lahan Darat (Non-Prioritas)": "#94a3b8"
        }

        def get_color(name: str):
            if name in action_colors:
                return action_colors[name]
            for k, c in action_colors.items():
                if k.lower() in name.lower():
                    return c
            return "#0f6e56"

        y_labels = counts["Rekomendasi"].tolist()
        x_vals = counts["Jumlah"].tolist()
        colors = [get_color(lbl) for lbl in y_labels]
        customdata = [[lbl, (val / total_all * 100) if total_all else 0] for lbl, val in zip(y_labels, x_vals)]
        max_val = max(x_vals) if x_vals else 100

        hovertemplate = (
            "<b>%{customdata[0]}</b><br>"
            "Jumlah Transek: <b>%{x:,}</b> (%{customdata[1]:.1f}%)"
            "<extra></extra>"
        )

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=y_labels,
        x=x_vals,
        orientation="h",
        marker=dict(
            color=colors,
            cornerradius=4,
            line=dict(width=0)
        ),
        text=[f"{int(v):,}".replace(",", ".") for v in x_vals],
        texttemplate="<b>%{text}</b>",
        textposition="outside",
        textfont=dict(family=FONT_FAMILY, size=13, color="#0f172a"),
        cliponaxis=False,
        customdata=customdata,
        hovertemplate=hovertemplate,
        hoverlabel=HOVER_STYLE
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=max(160, len(y_labels) * 36 + 25),
        margin=dict(l=10, r=45, t=10, b=10),
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            showticklabels=False,
            title=None,
            range=[0, max_val * 1.15]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            ticks="",
            tickfont=dict(family=FONT_FAMILY, size=13, color="#1e293b"),
            autorange="reversed"
        ),
        font=dict(family=FONT_FAMILY)
    )
    return fig

def plot_typology_breakdown(df: pd.DataFrame, wilayah: str = "SEMUA", mode: str = "4k") -> go.Figure:
    """Wrapper kompatibilitas untuk plot_theme_breakdown."""
    return plot_theme_breakdown(df, wilayah, mode=mode)


def plot_cross_section(transek_id: str, segmen_df: pd.DataFrame) -> go.Figure:
    """Diagram profil pita (ribbon) penampang melintang tutupan lahan (0 m laut -> 3.500 m darat).
    
    Karakteristik Coraly:
    - Pita ramping horizontal (height ~130px) tanpa chrome default Plotly
    - Garis batas pantai 500 m yang elegan dengan floating badge penanda di atas pita
    - Ticks sumbu X halus dengan penamaan titik penting (Laut, Pantai, Darat)
    - Hover tooltip interaktif memuat rentang meter dan jenis tutupan lahan
    """
    fig = go.Figure()
    sub = segmen_df[segmen_df["transek_id"] == transek_id]
    if sub.empty:
        fig.add_annotation(
            text="Profil penampang segmen tidak ditemukan untuk transek ini.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(family=FONT_FAMILY, size=12.5, color=theme.TEXT_MUTED)
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=125)
        return fig

    color_map = {
        "mangrove": "#0f766e",                  # Deep teal
        "dataran lumpur": "#94a3b8",            # Slate neutral
        "tambak terhubung pasang": "#0284c7",   # Sky blue
        "tambak mulai bervegetasi": "#0d9488",  # Teal accent
        "tambak tergenang": "#38bdf8",          # Cyan
        "tambak aktif": "#64748b",              # Muted slate
        "sawah": "#f59e0b",                     # Amber warm
        "vegetasi darat": "#16a34a",            # Forest green
        "lahan terbuka": "#cbd5e1",             # Light grey
        "terbangun": "#475569",                 # Slate dark
        "terbangun baru": "#e11d48",            # Rose alert
        "perairan": "#2563eb"                   # Marine blue
    }

    for _, row in sub.iterrows():
        d_from = row.get("dari_m", 0)
        d_to = row.get("sampai_m", 0)
        l_class = str(row.get("tutupan_lahan", "Lainnya")).lower()
        bar_color = color_map.get(l_class, "#94a3b8")
        width = d_to - d_from

        fig.add_trace(go.Bar(
            y=["Profil"],
            x=[width],
            base=[d_from],
            orientation="h",
            name=l_class.title(),
            marker=dict(
                color=bar_color,
                line=dict(color="rgba(255,255,255,0.35)", width=0.5)
            ),
            customdata=[[l_class.title(), d_to, width]],
            hovertemplate="<b>%{customdata[0]}</b><br>Rentang: %{base:.0f} m – %{customdata[1]:.0f} m (Lebar: %{customdata[2]:.0f} m)<extra></extra>",
            hoverlabel=HOVER_STYLE,
            showlegend=False
        ))

    # Garis Pantai Basis (500 m) — Garis vertikal putus-putus
    fig.add_vline(
        x=500,
        line_dash="dash",
        line_color="#0f172a",
        line_width=1.5
    )

    # Floating Badge Penanda Garis Pantai di atas pita (tidak nabrak bar)
    fig.add_annotation(
        x=500,
        y=1.28,
        yref="paper",
        text="<b>Garis Pantai (500 m)</b>",
        showarrow=False,
        xanchor="center",
        font=dict(family=FONT_FAMILY, size=10.5, color="#0f172a"),
        bgcolor="rgba(255, 255, 255, 0.95)",
        bordercolor="#cbd5e1",
        borderwidth=1,
        borderpad=4
    )

    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=130,
        margin=dict(l=15, r=20, t=38, b=30),
        xaxis=dict(
            range=[0, 3500],
            tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500],
            ticktext=["0 m (Laut)", "500 m (Pantai)", "1.000 m", "1.500 m", "2.000 m", "2.500 m", "3.000 m", "3.500 m (Darat)"],
            tickfont=dict(family=FONT_FAMILY, size=11, color="#64748b"),
            showgrid=False,
            showline=True,
            linecolor="#cbd5e1",
            linewidth=1,
            title=None
        ),
        yaxis=dict(visible=False),
        font=dict(family=FONT_FAMILY)
    )
    return fig


def plot_timeseries(transek_id: str, y_df: pd.DataFrame, master_row: pd.Series) -> go.Figure:
    """Grafik deret waktu posisi tepi laut bulanan Jan 2021 - Agu 2026 ala Coraly.
    
    Karakteristik Coraly:
    - Kurva garis teal halus (#0f766e) dengan area bayangan lembut (soft fill)
    - Penghalang keras ditampilkan dengan garis putus-putus merah modern (#e11d48)
    - Garis acuan pantai 500 m dengan garis titik-titik abu-abu
    - Gridline horizontal super subtle (#f1f5f9), tanpa grid vertikal yang mengganggu
    - Legenda horizontal di kanan atas, bebas dari frame kotak kaku
    """
    fig = go.Figure()

    if transek_id not in y_df.index:
        fig.add_annotation(
            text="Deret waktu satelit tidak tersedia untuk transek non-domain.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(family=FONT_FAMILY, size=12.5, color=theme.TEXT_MUTED)
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=280)
        return fig

    s = y_df.loc[transek_id].dropna()
    dates = pd.to_datetime(s.index)
    positions = s.values

    # 1. Observasi Tepi Laut Bulanan (Sentinel-1/2)
    fig.add_trace(go.Scatter(
        x=dates,
        y=positions,
        mode="lines+markers",
        name="Posisi Tepi Teramati",
        line=dict(color="#0f766e", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(15, 118, 110, 0.06)",
        marker=dict(size=4.5, color="#0f766e", line=dict(color="#ffffff", width=1)),
        hovertemplate="<b>%{x|%b %Y}</b><br>Posisi Garis Tepi: <b>%{y:.1f} m</b><extra></extra>",
        hoverlabel=HOVER_STYLE
    ))

    # 2. Garis Batas Penghalang Keras (Hard Barrier)
    jarak_barrier = master_row.get("jarak_penghalang_m", None)
    y_now = master_row.get("Y_now_m", None)
    if pd.notnull(jarak_barrier) and pd.notnull(y_now):
        b_pos = y_now + jarak_barrier
        fig.add_trace(go.Scatter(
            x=[dates.min(), dates.max()],
            y=[b_pos, b_pos],
            mode="lines",
            name=f"Penghalang Keras ({b_pos:.0f} m)",
            line=dict(color="#e11d48", width=1.8, dash="dash"),
            hovertemplate="Penghalang Keras: <b>%{y:.0f} m</b><extra></extra>",
            hoverlabel=HOVER_STYLE
        ))

    # 3. Garis Pantai Basis (500 m)
    fig.add_trace(go.Scatter(
        x=[dates.min(), dates.max()],
        y=[500, 500],
        mode="lines",
        name="Garis Pantai Basis (500 m)",
        line=dict(color="#94a3b8", width=1.3, dash="dot"),
        hovertemplate="Garis Pantai Basis: <b>500 m</b><extra></extra>",
        hoverlabel=HOVER_STYLE
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(l=45, r=20, t=15, b=25),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor="#cbd5e1",
            linewidth=1,
            tickformat="%b %Y",
            tickfont=dict(family=FONT_FAMILY, size=11, color="#64748b"),
            title=None
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(226, 232, 240, 0.7)",
            gridwidth=0.8,
            zeroline=False,
            showline=False,
            ticksuffix=" m",
            tickfont=dict(family=FONT_FAMILY, size=11, color="#64748b"),
            title=None
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(family=FONT_FAMILY, size=11, color="#475569")
        ),
        font=dict(family=FONT_FAMILY)
    )
    return fig

def plot_scenario_comparison(domain_df: pd.DataFrame) -> go.Figure:
    """Diagram batang horizontal komparatif ala Coraly: Baseline vs Skenario What-If.
    
    Menampilkan pergeseran kuadran 920 transek mangrove secara berdampingan:
    - RED · Rekayasa Hibrida
    - ORANGE · Pembukaan Ruang Mundur Mangrove
    - YELLOW · Pengayaan Sabuk Hijau
    - GREEN · Konservasi Ketat
    """
    total_m = len(domain_df)
    quads = [
        ("RED", "RED · Rekayasa Hibrida", "#b2182b"),
        ("ORANGE", "ORANGE · Pembukaan Ruang Mundur Mangrove", "#ea580c"),
        ("YELLOW", "YELLOW · Pengayaan Sabuk Hijau", "#eab308"),
        ("GREEN", "GREEN · Konservasi Ketat", "#16a34a"),
    ]
    
    y_labels = [q[1] for q in quads]
    
    # Baseline
    cnt_orig = [int((domain_df["Intervention_Type"] == q[0]).sum()) for q in quads]
    pct_orig = [(c / total_m * 100) if total_m else 0 for c in cnt_orig]
    
    # Skenario
    cnt_sim = [int((domain_df["sim_type"] == q[0]).sum()) for q in quads]
    pct_sim = [(c / total_m * 100) if total_m else 0 for c in cnt_sim]
    
    fig = go.Figure()
    
    # Trace 1: Baseline (Eksisting) - Batang abu-abu kebiruan netral
    fig.add_trace(go.Bar(
        y=y_labels,
        x=cnt_orig,
        name="Baseline (Kondisi Saat Ini)",
        orientation="h",
        marker=dict(
            color="#94a3b8",
            cornerradius=4,
            line=dict(width=0)
        ),
        text=[f"{v:,}".replace(",", ".") for v in cnt_orig],
        texttemplate="<b>%{text}</b>",
        textposition="outside",
        textfont=dict(family=FONT_FAMILY, size=12, color="#475569"),
        cliponaxis=False,
        customdata=pct_orig,
        hovertemplate=(
            "<b>Baseline Saat Ini</b><br>"
            "Tipologi: <b>%{y}</b><br>"
            "Jumlah Transek: <b>%{x:,}</b> (%{customdata:.1f}%)"
            "<extra></extra>"
        ),
        hoverlabel=HOVER_STYLE
    ))
    
    # Trace 2: Skenario Simulasi - Batang berwarna kuadran solid
    colors_sim = [q[2] for q in quads]
    fig.add_trace(go.Bar(
        y=y_labels,
        x=cnt_sim,
        name="Hasil Skenario Simulasi",
        orientation="h",
        marker=dict(
            color=colors_sim,
            cornerradius=4,
            line=dict(width=0)
        ),
        text=[f"{v:,}".replace(",", ".") for v in cnt_sim],
        texttemplate="<b>%{text}</b>",
        textposition="outside",
        textfont=dict(family=FONT_FAMILY, size=12, color="#0f172a"),
        cliponaxis=False,
        customdata=pct_sim,
        hovertemplate=(
            "<b>Hasil Skenario Simulasi</b><br>"
            "Tipologi: <b>%{y}</b><br>"
            "Jumlah Transek: <b>%{x:,}</b> (%{customdata:.1f}%)"
            "<extra></extra>"
        ),
        hoverlabel=HOVER_STYLE
    ))
    
    max_val = max(max(cnt_orig), max(cnt_sim)) if (cnt_orig and cnt_sim) else 500
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=270,
        margin=dict(l=10, r=45, t=10, b=25),
        barmode="group",
        bargap=0.28,
        bargroupgap=0.12,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            showticklabels=False,
            title=None,
            range=[0, max_val * 1.18]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            ticks="",
            tickfont=dict(family=FONT_FAMILY, size=12.5, color="#1e293b"),
            autorange="reversed"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(family=FONT_FAMILY, size=12, color="#334155")
        ),
        font=dict(family=FONT_FAMILY)
    )
    return fig

