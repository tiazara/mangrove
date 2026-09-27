"""
Script untuk menghasilkan Gambar 1: Alur Analisis Sistem Pendukung Keputusan SABUK HIJAU.
Kualitas publikasi 300 DPI untuk esai ilmiah ASEC 2026.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

def draw_flowchart():
    fig, ax = plt.subplots(figsize=(15.5, 11.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor("#ffffff")
    fig.patch.set_facecolor("#ffffff")
    ax.axis("off")

    # Palet warna institusional
    c_blue = "#0284c7"     # Tahap 1: Data & Unit
    c_teal = "#0d9488"     # Tahap 2: Pemrosesan
    c_green = "#16a34a"    # Tahap 3: Perubahan (Apa & Mengapa)
    c_amber = "#d97706"    # Tahap 4: Risiko & Prioritas
    c_emerald = "#0f6e56"  # Tahap 5: DSS SABUK HIJAU
    c_purple = "#7c3aed"   # Evaluasi Menyeluruh

    def draw_card(x, y, w, h, title, subtitle, items, border_color, fill_color="#f8fafc", badge_text=""):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.008,rounding_size=0.015",
            linewidth=1.3, edgecolor=border_color, facecolor=fill_color, zorder=2
        )
        ax.add_patch(rect)
        
        header_h = 0.038
        header_rect = patches.FancyBboxPatch(
            (x, y + h - header_h), w, header_h,
            boxstyle="round,pad=0.006,rounding_size=0.012",
            linewidth=0, facecolor=border_color, zorder=3
        )
        ax.add_patch(header_rect)
        
        # Title text
        ax.text(x + 0.012, y + h - 0.019, title, fontsize=9.2, fontweight="bold", color="#ffffff", va="center", zorder=4)
        
        # Badge text
        if badge_text:
            ax.text(x + w - 0.012, y + h - 0.019, badge_text, fontsize=7.5, fontweight="bold", color="#ffffff", ha="right", va="center", zorder=4)

        # Subtitle
        cur_y = y + h - header_h - 0.022
        if subtitle:
            ax.text(x + 0.012, cur_y, subtitle, fontsize=8.4, fontweight="bold", fontstyle="italic", color="#0f172a", va="center", zorder=4)
            cur_y -= 0.021
            
        # Items bullet
        for it in items:
            ax.text(x + 0.012, cur_y, it, fontsize=7.6, color="#334155", va="center", zorder=4)
            cur_y -= 0.0185

    w_main = 0.55
    x_main = 0.025
    w_eval = 0.33
    x_eval = 0.645

    # --- Box 1: Kawasan, Unit, dan Data (2.2.1) ---
    draw_card(
        x=x_main, y=0.815, w=w_main, h=0.150,
        title="2.2.1 Kawasan Studi, Unit Analisis, dan Fusi Data Multi-Sumber",
        subtitle="Fondasi Pengukuran Spasial 1-Dimensi Pantai",
        items=[
            "• 5 Lanskap Arketipe: Pekalongan (Ekstrem), Semarang–Demak (PSN), Cirebon (Tambak), SBY (Delta), Jepara (Kontrol)",
            "• Unit Analisis: N = 2.365 transek ortogonal (spasi 250 m, panjang 3.500 m [500 m laut, 3.000 m darat], EPSG:32749)",
            "• Satelit & Sensor: Sentinel-1 SAR (VV/VH 10 m), Sentinel-2 (NDVI/MNDWI 10 m), Dynamic World, GMW (2000–2025)",
            "• Geodesi & Fisik: InSAR Jawa (75 m), GNSS CORS BIG harian, Copernicus DEM (30 m), EOT20 Pasut, WorldPop 100 m"
        ],
        border_color=c_blue, fill_color="#f0f9ff", badge_text="INPUT DATA"
    )

    # --- Box 2: Pemrosesan Data (2.2.2) ---
    draw_card(
        x=x_main, y=0.620, w=w_main, h=0.150,
        title="2.2.2 Pemrosesan Data & Konstruksi Variabel Ruang",
        subtitle="Standardisasi & Ekstraksi Sepanjang Sumbu Transek",
        items=[
            "• Domain Mangrove Aktif: Penapisan 920 transek terkonfirmasi (rangkaian ≥ 30 m GMW/WorldCover + validasi spektral S2)",
            "• Tepi Laut Bulanan Y(i,t): Ambang ganda adaptif (NDVI > 0,4 & VH > -14 dB) dengan filter Hampel 7-bulan bebas awan",
            "• Penghalang Keras B(i): Titik darat permanen (Dynamic World built stabil 2 thn, tanggul, jalan arteri Pantura, tol PSN)",
            "• Tutupan Lahan & Ruang Peluang: Klasifikasi 4 status tambak (MNDWI bulanan), jendela hidroperiode, & penghalang fungsional"
        ],
        border_color=c_teal, fill_color="#f0fdfa", badge_text="PEMROSESAN"
    )

    # --- Box 3: Analisis Perubahan Mangrove (2.2.3) ---
    draw_card(
        x=x_main, y=0.425, w=w_main, h=0.150,
        title="2.2.3 Analisis Perubahan Mangrove",
        subtitle="Pertanyaan 1 & 2: \"Apa yang terjadi pada mangrove dan mengapa?\"",
        items=[
            "• Apa yang Terjadi: Tren jangka panjang Theil–Sen (laju tepi v & laju lebar w) + Model State-Space M2 (AR(1) Kalman Filter)",
            "• Nowcasting & Forecasting: Estimasi posisi tepi kini t serta proyeksi t+6 dan t+12 bulan + kerucut ketidakpastian (±1,96σ)",
            "• Mengapa Terjadi: Model Dua Bagian (WLS, Huber Robust, Efek Tetap Lanskap) membedakan efek amblesan,",
            "  frekuensi genangan rob, dan kepadatan bangunan + Koreksi kesalahan pengukuran kovariat dengan SIMEX"
        ],
        border_color=c_green, fill_color="#f0fdf4", badge_text="DIAGNOSIS & KAUSALITAS"
    )

    # --- Box 4: Analisis Risiko & Prioritas (2.2.4) ---
    draw_card(
        x=x_main, y=0.230, w=w_main, h=0.150,
        title="2.2.4 Analisis Risiko dan Penentuan Prioritas",
        subtitle="Pertanyaan 3 & 4: \"Apa yang akan terjadi dan apa yang harus dilakukan?\"",
        items=[
            "• Risiko Vertikal: Defisit D = Subs + SLR - A & Simulasi Monte Carlo 2.000 ulangan waktu tenggelam (P(tenggelam < 2050/2100))",
            "• Risiko Horizontal: Peluang penutupan ruang gerak P(Closed_h) (1 & 5 tahun) + Indeks Kelayakan Restorasi (RFI)",
            "• Matriks Tipologi 4 Kuadran: RED (Rekayasa Hibrida), ORANGE (Managed Realignment), YELLOW (Pengayaan), GREEN (Konservasi)",
            "• Spasial Hotspot & Kawasan: Indeks keterpaparan penduduk PERI, klaster Getis-Ord Gi* (FDR 5%), agregasi kawasan ≥ 500 m"
        ],
        border_color=c_amber, fill_color="#fffbeb", badge_text="PRESIKRIPSI MITIGASI"
    )

    # --- Box 5: Sistem Pendukung Keputusan (2.4) ---
    draw_card(
        x=x_main, y=0.040, w=w_main, h=0.145,
        title="2.4 Sistem Pendukung Keputusan (Layer SABUK HIJAU)",
        subtitle="Hilirisasi Kebijakan: Platform DSS Pesisir Pantura Interaktif",
        items=[
            "• Peta Spasial WebGL Interaktif: Eksplorasi 4 kuadran mitigasi & 11 aksi lapangan (2.365 transek) secepat 50 ms GPU",
            "• Inspektur Mikro & Simulator What-If: Eksplorasi cross-section 1D, grafik deret waktu bulanan, & uji skenario akresi sedimen",
            "• Ekspor Rencana Aksi Kawasan: Tabel data terstruktur CSV untuk dokumen perencanaan RTRW Provinsi dan alokasi anggaran APBN/D"
        ],
        border_color=c_emerald, fill_color="#ecfdf5", badge_text="OUTPUT SISTEM (DSS)"
    )

    # --- Box Kanan: Evaluasi (2.2.5) ---
    draw_card(
        x=x_eval, y=0.230, w=w_eval, h=0.540,
        title="2.2.5 Lapisan Evaluasi Menyeluruh",
        subtitle="Pertanyaan 5: \"Seberapa yakin kita terhadap jawabannya?\"",
        items=[
            "Validasi Data (Tingkat 1):",
            "• Kalibrasi InSAR vs GNSS CORS (regresi siklus sinus-kosinus)",
            "• Validasi tepi Sentinel vs GMW 2025 (median selisih 20 m, ρ = 0,88)",
            "",
            "Validasi Model (Tingkat 2):",
            "• Backtest Rolling-Origin peramalan k-step (t+6 dan t+12 bulan)",
            "• Evaluasi CRPS & interval 95% vs Persistensi & Gradient Boosting",
            "• Uji signifikansi beda skor CRPS dengan block-bootstrap spasial",
            "",
            "Ketahanan Kesimpulan (Tingkat 3):",
            "• 36 Skenario Kombinasi Parameter (ambang NDVI, Built, spasi transek)",
            "• Uji sensitivitas batas akresi (0,2–1,5 cm/th) & horizon (2050 vs 2100)",
            "• Uji permutasi 1.000 bobot acak Dirichlet indeks RFI",
            "• Evaluasi Irisan Jaccard (zona RED ∪ ORANGE & Hotspot stabil > 85%)"
        ],
        border_color=c_purple, fill_color="#faf5ff", badge_text="VALIDASI TRIPEL"
    )

    # Panah alur vertikal utama
    arrow_props = dict(arrowstyle="-|>", linewidth=2, color="#475569", mutation_scale=14, zorder=5)
    
    # 1 -> 2 (Gap: 0.770 s.d. 0.815)
    ax.annotate("", xy=(x_main + w_main/2, 0.770), xytext=(x_main + w_main/2, 0.815), arrowprops=arrow_props)
    ax.text(x_main + w_main/2 + 0.012, 0.792, "Ekstraksi Titik 10 m", fontsize=7.2, color="#475569", fontweight="bold", va="center")

    # 2 -> 3 (Gap: 0.575 s.d. 0.620)
    ax.annotate("", xy=(x_main + w_main/2, 0.575), xytext=(x_main + w_main/2, 0.620), arrowprops=arrow_props)
    ax.text(x_main + w_main/2 + 0.012, 0.597, "Variabel Terukur per Transek", fontsize=7.2, color="#475569", fontweight="bold", va="center")

    # 3 -> 4 (Gap: 0.380 s.d. 0.425)
    ax.annotate("", xy=(x_main + w_main/2, 0.380), xytext=(x_main + w_main/2, 0.425), arrowprops=arrow_props)
    ax.text(x_main + w_main/2 + 0.012, 0.402, "Nowcast & Parameter Kausal", fontsize=7.2, color="#475569", fontweight="bold", va="center")

    # 4 -> 5 (Gap: 0.185 s.d. 0.230)
    ax.annotate("", xy=(x_main + w_main/2, 0.185), xytext=(x_main + w_main/2, 0.230), arrowprops=arrow_props)
    ax.text(x_main + w_main/2 + 0.012, 0.207, "Matriks Kuadran & Kawasan Prioritas", fontsize=7.2, color="#475569", fontweight="bold", va="center")

    # Panah evaluasi putus-putus horizontal di celah 0.575 s.d. 0.645
    dash_arrow = dict(arrowstyle="-|>", linestyle="dashed", linewidth=1.5, color=c_purple, mutation_scale=12, zorder=5)
    
    # Ke Tahap 2 (Validasi Data)
    ax.annotate("", xy=(x_main + w_main, 0.695), xytext=(x_eval, 0.695), arrowprops=dash_arrow)
    ax.text((x_main + w_main + x_eval)/2, 0.710, "Validasi Data", fontsize=7.2, color=c_purple, fontweight="bold", ha="center")

    # Ke Tahap 3 (Validasi Model)
    ax.annotate("", xy=(x_main + w_main, 0.500), xytext=(x_eval, 0.500), arrowprops=dash_arrow)
    ax.text((x_main + w_main + x_eval)/2, 0.515, "Validasi Model", fontsize=7.2, color=c_purple, fontweight="bold", ha="center")

    # Ke Tahap 4 (Ketahanan Kesimpulan)
    ax.annotate("", xy=(x_main + w_main, 0.305), xytext=(x_eval, 0.305), arrowprops=dash_arrow)
    ax.text((x_main + w_main + x_eval)/2, 0.320, "Uji Ketahanan", fontsize=7.2, color=c_purple, fontweight="bold", ha="center")

    ax.text(0.5, 0.015, "Gambar 1. Rantai Logika Analisis dan Kerangka Kerja Sistem Pendukung Keputusan SABUK HIJAU.",
            fontsize=10.2, fontweight="bold", color="#0f172a", ha="center")

    out_path = Path(r"d:\Kuliah\Lomba\ASEC Arsen Unair 2026\mangrove\gambar_1_alur_analisis.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Perfect clean flowchart regenerated at:", out_path)

if __name__ == "__main__":
    draw_flowchart()
