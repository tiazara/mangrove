"""
Grafik visualisasi analitis Plotly untuk SABUK HIJAU.
Ditema agar selaras dengan palet warna kartografis theme.py.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import theme as theme

TEMPLATE = "plotly_white"

def plot_timeseries(transek_id: str, y_df: pd.DataFrame, master_row: pd.Series) -> go.Figure:
    """Grafik deret waktu posisi tepi laut bulanan Jan 2021 - Agu 2026."""
    fig = go.Figure()

    if transek_id not in y_df.index:
        fig.add_annotation(
            text="Deret waktu tidak tersedia untuk transek non-domain.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color=theme.TEXT_MUTED)
        )
        fig.update_layout(template=TEMPLATE, height=320)
        return fig

    s = y_df.loc[transek_id].dropna()
    dates = pd.to_datetime(s.index)
    positions = s.values

    # Observasi Tepi Laut Bulanan (Sentinel-1/2)
    fig.add_trace(go.Scatter(
        x=dates,
        y=positions,
        mode="lines+markers",
        name="Posisi Tepi Teramati",
        line=dict(color="#0284c7", width=2),
        marker=dict(size=4.5, color="#0369a1"),
        hovertemplate="%{x|%b %Y}: %{y:.1f} m<extra></extra>"
    ))

    # Garis Batas Penghalang Keras (Hard Barrier)
    jarak_barrier = master_row.get("jarak_penghalang_m", None)
    y_now = master_row.get("Y_now_m", None)
    if pd.notnull(jarak_barrier) and pd.notnull(y_now):
        b_pos = y_now + jarak_barrier
        fig.add_trace(go.Scatter(
            x=[dates.min(), dates.max()],
            y=[b_pos, b_pos],
            mode="lines",
            name=f"Penghalang Keras ({b_pos:.0f} m)",
            line=dict(color="#dc2626", width=2, dash="dash"),
            hovertemplate=f"Penghalang Keras: {b_pos:.0f} m<extra></extra>"
        ))

    # Garis Pantai Basis (500 m)
    fig.add_trace(go.Scatter(
        x=[dates.min(), dates.max()],
        y=[500, 500],
        mode="lines",
        name="Garis Pantai (500 m)",
        line=dict(color="#64748b", width=1.2, dash="dot"),
        hovertemplate="Garis Pantai Basis: 500 m<extra></extra>"
    ))

    v_rate = master_row.get("v_edge_m_yr", np.nan)
    v_info = f"Laju Pergerakan Tepi: {v_rate:+.1f} m/tahun" if pd.notnull(v_rate) else ""

    fig.update_layout(
        title=dict(
            text=f"Deret Waktu Posisi Tepi Laut — Transek {transek_id} ({v_info})",
            font=dict(size=14, color=theme.TEXT)
        ),
        xaxis=dict(title="Waktu Observasi", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="Jarak dari Ujung Laut (m)", showgrid=True, gridcolor="#f1f5f9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
        template=TEMPLATE,
        height=320,
        margin=dict(l=40, r=20, t=45, b=35)
    )
    return fig

def plot_cross_section(transek_id: str, segmen_df: pd.DataFrame) -> go.Figure:
    """Diagram profil penampang melintang tutupan lahan (0m laut -> 3500m darat)."""
    fig = go.Figure()
    sub = segmen_df[segmen_df["transek_id"] == transek_id]
    if sub.empty:
        fig.add_annotation(
            text="Profil penampang segmen tidak ditemukan.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color=theme.TEXT_MUTED)
        )
        fig.update_layout(template=TEMPLATE, height=160)
        return fig

    color_map = {
        "mangrove": theme.COLOR_STABLE,
        "dataran lumpur": "#94a3b8",
        "tambak terhubung pasang": "#0284c7",
        "tambak mulai bervegetasi": "#38bdf8",
        "tambak tergenang": "#818cf8",
        "tambak aktif": "#64748b",
        "sawah": "#f59e0b",
        "vegetasi darat": "#15803d",
        "lahan terbuka": "#cbd5e1",
        "terbangun": "#475569",
        "terbangun baru": "#dc2626",
        "perairan": "#3b82f6"
    }

    for _, row in sub.iterrows():
        d_from = row.get("dari_m", 0)
        d_to = row.get("sampai_m", 0)
        l_class = str(row.get("tutupan_lahan", "Lainnya")).lower()
        bar_color = color_map.get(l_class, "#94a3b8")

        fig.add_trace(go.Bar(
            y=["Profil"],
            x=[d_to - d_from],
            base=[d_from],
            orientation="h",
            name=l_class.title(),
            marker=dict(color=bar_color),
            hovertemplate=f"{l_class.title()}: {d_from:.0f}m - {d_to:.0f}m<extra></extra>",
            showlegend=False
        ))

    fig.add_vline(x=500, line_dash="dash", line_color="#0f172a", line_width=1.5,
                  annotation_text="Garis Pantai (500 m)", annotation_position="top")

    fig.update_layout(
        barmode="stack",
        xaxis=dict(title="Jarak dari Ujung Laut ke Daratan (meter)", range=[0, 3500], showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(showticklabels=False),
        title=dict(text=f"Penampang Melintang Lahan — Transek {transek_id}", font=dict(size=13, color=theme.TEXT)),
        template=TEMPLATE,
        height=170,
        margin=dict(l=40, r=20, t=35, b=35)
    )
    return fig

def plot_typology_breakdown(df: pd.DataFrame, wilayah: str) -> go.Figure:
    """Diagram batang distribusi tipologi rekomendasi presisi."""
    sub = df if wilayah == "SEMUA" else df[df["wilayah"] == wilayah]
    counts = sub["rekomendasi"].value_counts().reset_index()
    counts.columns = ["Rekomendasi", "Jumlah"]

    fig = px.bar(
        counts.head(7),
        x="Jumlah",
        y="Rekomendasi",
        orientation="h",
        template=TEMPLATE,
        color="Jumlah",
        color_continuous_scale=["#99f6e4", "#0f766e", "#042f2e"]
    )
    fig.update_layout(
        height=260,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Jumlah Transek",
        yaxis_title="",
        yaxis=dict(autorange="reversed")
    )
    return fig
