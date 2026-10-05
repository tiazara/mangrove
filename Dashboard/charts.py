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
    - 'hotspot': Hotspot tenggelam padat penduduk (Gi* FDR 5%) vs transek lain
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
                "label": "Hotspot tenggelam padat penduduk",
                "count": n_hot,
                "pct": pct_hot,
                "color": "#dc2626",
                "status": "Prioritas rehabilitasi",
                "keterangan": "Klaster Gi* (FDR 5%) peluang tenggelam < 2050 × penduduk radius 1 km"
            },
            {
                "label": "Bukan hotspot",
                "count": n_safe,
                "pct": pct_safe,
                "color": "#64748b",
                "status": "Bukan klaster risiko × penduduk",
                "keterangan": "Dapat tetap berisiko tenggelam; lihat tipologi aksi"
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
                "keterangan": "Defisit elevasi paling besar; risiko tenggelam tertinggi"
            },
            {
                "label": "2,0 – 4,0 cm/th (Sangat Tinggi)",
                "count": c_stinggi,
                "color": "#dc2626",
                "tingkat": "Sangat Tinggi",
                "keterangan": "Defisit elevasi besar; modal elevasi habis dalam beberapa dekade"
            },
            {
                "label": "1,0 – 2,0 cm/th (Tinggi)",
                "count": c_tinggi,
                "color": "#f97316",
                "tingkat": "Tinggi / Signifikan",
                "keterangan": "Laju amblesan melampaui akresi sedimen alami (0,5 cm/th)"
            },
            {
                "label": "< 1,0 cm/th (Rendah / Relatif Stabil)",
                "count": c_rendah,
                "color": "#eab308",
                "tingkat": "Rendah / Relatif Stabil",
                "keterangan": "Sebagian masih dapat diimbangi akresi alami (0,5 cm/th)"
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

    shown = set()
    for _, row in sub.sort_values("dari_m").iterrows():
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
            legendgroup=l_class,
            showlegend=l_class not in shown
        ))
        shown.add(l_class)

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
        height=190,
        margin=dict(l=15, r=20, t=38, b=30),
        legend=dict(orientation="h", yanchor="top", y=-0.5, xanchor="left", x=0,
                    bgcolor="rgba(0,0,0,0)", font=dict(family=FONT_FAMILY, size=11.5, color="#334155"),
                    traceorder="normal", itemclick=False, itemdoubleclick=False),
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
    """Deret posisi tepi laut bulanan (Jan 2021 – Agu 2026), nowcast Kalman, ramalan 6/12 bulan,
    dan posisi penghalang keras. Posisi diukur dari ujung laut transek (0 m), sehingga
    nilai yang naik berarti tepi mundur ke darat."""
    fig = go.Figure()

    if transek_id not in y_df.index:
        fig.add_annotation(
            text="Deret waktu satelit hanya tersedia untuk transek bermangrove.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(family=FONT_FAMILY, size=12.5, color=theme.TEXT_MUTED)
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=300)
        return fig

    s = y_df.loc[transek_id].dropna()
    dates = pd.PeriodIndex(s.index, freq="M").to_timestamp()
    positions = s.values
    t_now = pd.Timestamp("2026-08-01")

    fig.add_trace(go.Scatter(
        x=dates, y=positions, mode="markers", name="Tepi teramati (Sentinel-1/2)",
        marker=dict(size=5.5, color="#0f766e", line=dict(color="#ffffff", width=0.8)),
        hovertemplate="<b>%{x|%b %Y}</b><br>Posisi tepi: <b>%{y:.0f} m</b><extra></extra>",
        hoverlabel=HOVER_STYLE
    ))

    y_now = master_row.get("Y_now_m", None)
    sd_now = master_row.get("MS_uncertainty", None)
    ms_now = master_row.get("MS_current_m", None)
    ys_extra = list(positions)
    b_pos = None
    if pd.notnull(y_now) and pd.notnull(ms_now) and not bool(master_row.get("B_hard_tersensor", False)):
        b_pos = y_now + ms_now
    if pd.notnull(y_now):
        # Ramalan rerata 6 & 12 bulan = posisi penghalang dikurangi ruang tersisa yang diramalkan
        fc_x, fc_y = [t_now], [y_now]
        for h, col in [(6, "MS_pred_6m"), (12, "MS_pred_12m")]:
            ms_h = master_row.get(col, None)
            if pd.notnull(ms_h) and pd.notnull(ms_now):
                fc_x.append(t_now + pd.DateOffset(months=h))
                fc_y.append(y_now + ms_now - ms_h)
        ys_extra += fc_y
        if pd.notnull(sd_now):
            lo, hi = y_now - 1.96 * sd_now, y_now + 1.96 * sd_now
            ys_extra += [lo, hi]
            fig.add_trace(go.Scatter(
                x=[t_now, t_now], y=[lo, hi], mode="lines", name="Selang 95% nowcast",
                line=dict(color="#f59e0b", width=7), opacity=0.4,
                hovertemplate=f"Selang 95%: {lo:.0f} – {hi:.0f} m<extra></extra>", hoverlabel=HOVER_STYLE
            ))
        n_fc = len(fc_x)
        fig.add_trace(go.Scatter(
            x=fc_x, y=fc_y, mode="lines+markers", name="Nowcast & ramalan 6/12 bln (Kalman)",
            line=dict(color="#d97706", width=2.2, dash="dot"),
            marker=dict(size=[11] + [7] * (n_fc - 1), color="#d97706",
                        symbol=["diamond"] + ["circle"] * (n_fc - 1)),
            hovertemplate="<b>%{x|%b %Y}</b><br>Posisi taksiran: <b>%{y:.0f} m</b><extra></extra>",
            hoverlabel=HOVER_STYLE
        ))

    x_end = t_now + pd.DateOffset(months=13)
    jauh = b_pos is not None and (b_pos - float(np.nanmax(ys_extra))) > 400
    if jauh:
        fig.add_annotation(
            xref="paper", yref="paper", x=0.01, y=0.97, xanchor="left", showarrow=False,
            text=f"Penghalang keras {ms_now:,.0f} m di belakang tepi (di luar skala grafik)".replace(",", "."),
            font=dict(family=FONT_FAMILY, size=11.5, color="#e11d48"),
            bgcolor="rgba(255,255,255,0.9)", bordercolor="#fecdd3", borderwidth=1, borderpad=4
        )
    elif b_pos is not None:
        ys_extra.append(b_pos)
        fig.add_trace(go.Scatter(
            x=[dates.min(), x_end], y=[b_pos, b_pos], mode="lines",
            name=f"Penghalang keras ({ms_now:.0f} m dari tepi)",
            line=dict(color="#e11d48", width=1.8, dash="dash"),
            hovertemplate="Penghalang keras: <b>%{y:.0f} m</b><extra></extra>", hoverlabel=HOVER_STYLE
        ))

    fig.add_trace(go.Scatter(
        x=[dates.min(), x_end], y=[500, 500], mode="lines", name="Garis pantai acuan (500 m)",
        line=dict(color="#94a3b8", width=1.3, dash="dot"),
        hovertemplate="Garis pantai acuan: <b>500 m</b><extra></extra>", hoverlabel=HOVER_STYLE
    ))
    ys_extra.append(500)

    lo_y, hi_y = float(np.nanmin(ys_extra)), float(np.nanmax(ys_extra))
    pad = max(40.0, (hi_y - lo_y) * 0.12)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=330,
        margin=dict(l=60, r=20, t=45, b=25),
        xaxis=dict(showgrid=False, showline=True, linecolor="#cbd5e1", linewidth=1, tickformat="%b %Y",
                   tickfont=dict(family=FONT_FAMILY, size=11, color="#64748b"), title=None),
        yaxis=dict(showgrid=True, gridcolor="rgba(226, 232, 240, 0.7)", gridwidth=0.8, zeroline=False,
                   showline=False, ticksuffix=" m", tickfont=dict(family=FONT_FAMILY, size=11, color="#64748b"),
                   range=[lo_y - pad, hi_y + pad],
                   title=dict(text="jarak dari laut (naik = mundur ke darat)", font=dict(size=11, color="#64748b"))),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)",
                    font=dict(family=FONT_FAMILY, size=11, color="#475569")),
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



WARNA_LAHAN = {
    "mangrove": "#0f766e", "dataran lumpur": "#94a3b8", "tambak terhubung pasang": "#0284c7",
    "tambak mulai bervegetasi": "#0d9488", "tambak tergenang": "#38bdf8", "tambak aktif": "#64748b",
    "sawah": "#f59e0b", "vegetasi darat": "#16a34a", "lahan terbuka": "#cbd5e1",
    "terbangun": "#475569", "terbangun baru": "#e11d48", "perairan": "#2563eb",
}

def plot_citra_penampang(transek_id: str, potongan: list[dict], segmen_df: pd.DataFrame,
                         tepi_tahunan: dict, b_pos: float = None, label_acuan: str = "Garis pantai acuan") -> go.Figure:
    """Penampang melintang dari citra satelit: potongan citra selebar koridor ±150 m disusun per
    sumber/tahun di atas sumbu jarak 0–3.500 m, dengan klasifikasi tutupan lahan di baris terbawah.

    tepi_tahunan: {tahun: posisi tepi median (m)} untuk ditandai pada baris Sentinel-2 tahun tsb.
    """
    fig = go.Figure()
    n = len(potongan)
    tinggi_baris = 0.92
    tickvals, ticktext = [], []

    # 1. Baris citra (atas -> bawah)
    for r, p in enumerate(potongan):
        y_atas = n + 1 - r
        fig.add_layout_image(dict(source=p["uri"], xref="x", yref="y", x=0, y=y_atas, sizex=3500, sizey=tinggi_baris,
                                  xanchor="left", yanchor="top", sizing="stretch", layer="below"))
        tickvals.append(y_atas - tinggi_baris / 2)
        ticktext.append(p["label"].replace("Citra resolusi tinggi (Esri, terkini)", "Resolusi tinggi<br>(Esri)"))
        tahun = p.get("tahun")
        if tahun in tepi_tahunan and pd.notnull(tepi_tahunan[tahun]):
            x_t = tepi_tahunan[tahun]
            fig.add_trace(go.Scatter(
                x=[x_t, x_t], y=[y_atas - tinggi_baris, y_atas], mode="lines",
                line=dict(color="#fde047", width=3), showlegend=tahun == min(tepi_tahunan),
                name="Tepi mangrove terdeteksi (median tahunan)", legendgroup="tepi",
                hovertemplate=f"Tepi mangrove {tahun}: <b>{x_t:.0f} m</b><extra></extra>", hoverlabel=HOVER_STYLE
            ))

    # 2. Baris klasifikasi tutupan lahan
    sub = segmen_df[segmen_df["transek_id"] == transek_id].sort_values("dari_m")
    shown = set()
    for _, row in sub.iterrows():
        kelas = str(row.get("tutupan_lahan", "lainnya")).lower()
        lebar = row["sampai_m"] - row["dari_m"]
        fig.add_trace(go.Bar(
            y=[0.55], x=[lebar], base=[row["dari_m"]], orientation="h", width=0.5,
            marker=dict(color=WARNA_LAHAN.get(kelas, "#94a3b8"), line=dict(width=0)),
            name=kelas.title(), legendgroup=kelas, showlegend=kelas not in shown,
            customdata=[[kelas.title(), row["sampai_m"], lebar]],
            hovertemplate="<b>%{customdata[0]}</b><br>%{base:.0f} – %{customdata[1]:.0f} m (lebar %{customdata[2]:.0f} m)<extra></extra>",
            hoverlabel=HOVER_STYLE
        ))
        shown.add(kelas)
    tickvals.append(0.55)
    ticktext.append("Klasifikasi<br>tutupan lahan")

    # 3. Garis acuan vertikal di seluruh baris
    y_span = [0.25, n + 1.02]
    fig.add_trace(go.Scatter(
        x=[500, 500], y=y_span, mode="lines", line=dict(color="#22d3ee", width=2, dash="dash"),
        name=f"{label_acuan} (500 m)", hovertemplate=f"{label_acuan}: <b>500 m</b><extra></extra>", hoverlabel=HOVER_STYLE
    ))
    if b_pos is not None and pd.notnull(b_pos) and 0 < b_pos < 3500:
        fig.add_trace(go.Scatter(
            x=[b_pos, b_pos], y=y_span, mode="lines", line=dict(color="#e11d48", width=2.2, dash="dash"),
            name=f"Penghalang keras (posisi {b_pos:,.0f} m pada transek)".replace(",", "."),
            hovertemplate=f"Penghalang keras: <b>{b_pos:.0f} m</b> dari ujung laut transek<extra></extra>", hoverlabel=HOVER_STYLE
        ))

    fig.update_layout(
        barmode="overlay",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=int(n * 96 + 150),
        margin=dict(l=10, r=15, t=10, b=30),
        xaxis=dict(range=[0, 3500], tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500],
                   ticktext=["0 m (laut)", "500 m", "1.000 m", "1.500 m", "2.000 m", "2.500 m", "3.000 m", "3.500 m (darat)"],
                   tickfont=dict(family=FONT_FAMILY, size=11, color="#64748b"), showgrid=False, zeroline=False,
                   showline=True, linecolor="#cbd5e1"),
        yaxis=dict(range=[0.2, n + 1.04], tickvals=tickvals, ticktext=ticktext, showgrid=False, zeroline=False,
                   tickfont=dict(family=FONT_FAMILY, size=11.5, color="#334155"), fixedrange=True),
        legend=dict(orientation="h", yanchor="top", y=-0.12, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)",
                    font=dict(family=FONT_FAMILY, size=11.5, color="#334155"), itemclick=False, itemdoubleclick=False),
        font=dict(family=FONT_FAMILY),
    )
    return fig
