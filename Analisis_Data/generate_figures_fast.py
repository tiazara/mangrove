import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import scipy.stats as stats

out_dir = r'd:\Kuliah\Lomba\ASEC Arsen Unair 2026\Analisis_Data'
fig_dir = os.path.join(out_dir, 'figures')
os.makedirs(fig_dir, exist_ok=True)

df = pd.read_csv(os.path.join(out_dir, 'mangrovia_pantura_dataset.csv'))
corr_matrix = df[['pct_T', 'pct_D', 'pct_V']].corr(method='spearman')

print("Generating Figure 2: Boxplots...")
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
sns.boxplot(x='region', y='pct_T', data=df, ax=axes[0], palette=['#93c5fd', '#fca5a5', '#6ee7b7'])
axes[0].set_title('(a) Ancaman Biofisik (Threat)', fontweight='bold')
axes[0].set_ylabel('Peringkat Persentil (T)')
axes[0].set_xlabel('')

sns.boxplot(x='region', y='pct_D', data=df, ax=axes[1], palette=['#93c5fd', '#fca5a5', '#6ee7b7'])
axes[1].set_title('(b) Ketergantungan Warga (Dependence)', fontweight='bold')
axes[1].set_ylabel('Peringkat Persentil (D)')
axes[1].set_xlabel('Segmen Koridor Pantura')

sns.boxplot(x='region', y='pct_V', data=df, ax=axes[2], palette=['#93c5fd', '#fca5a5', '#6ee7b7'])
axes[2].set_title('(c) Kerentanan Ekonomi (Vulnerability)', fontweight='bold')
axes[2].set_ylabel('Peringkat Persentil (V)')
axes[2].set_xlabel('')

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig2_sebaran_komponen.png'), dpi=200)
plt.close()

print("Generating Figure 3: Correlation...")
plt.figure(figsize=(5.5, 4.5))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='Blues', vmin=-0.5, vmax=0.5,
            cbar_kws={'label': 'Korelasi Spearman (rho)'},
            xticklabels=['Threat (T)', 'Dependence (D)', 'Vulnerability (V)'],
            yticklabels=['Threat (T)', 'Dependence (D)', 'Vulnerability (V)'])
plt.title('Matriks Korelasi Antarkomponen Indeks', fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig3_korelasi_komponen.png'), dpi=200)
plt.close()

print("Generating Figure 4: Priority Map...")
fig, ax = plt.subplots(figsize=(13, 4.5))
sc = ax.scatter(df['lon'], df['lat'], c=df['Priority'], cmap='YlOrRd', s=12, alpha=0.85, edgecolors='none')
cbar = plt.colorbar(sc, ax=ax, orientation='horizontal', pad=0.2, shrink=0.6)
cbar.set_label('Skor Indeks Priority MANGROVIA-PANTURA (0: Rendah, 1: Sangat Kritis)', fontweight='bold')
ax.set_title('Peta Spasial Indeks Prioritas Konservasi & Restorasi Mangrove Pantura Jawa', fontweight='bold', pad=10)
ax.set_xlabel('Bujur Timur (Longitude)')
ax.set_ylabel('Lintang Selatan (Latitude)')
ax.grid(True, linestyle='--', alpha=0.4)

ax.annotate('Pantura Barat\n(Bekasi/Karawang/Subang)', xy=(107.4, -6.15), xytext=(107.0, -5.6),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2), fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#eff6ff', ec='#93c5fd'))
ax.annotate('Pantura Tengah\n(Pekalongan/Semarang/Demak)\n[Zona Amblesan Kritis]', xy=(110.3, -6.85), xytext=(109.8, -6.2),
            arrowprops=dict(facecolor='red', arrowstyle='->', lw=1.5), fontweight='bold', color='#b91c1c',
            bbox=dict(boxstyle='round,pad=0.3', fc='#fef2f2', ec='#fca5a5'))
ax.annotate('Pantura Timur\n(Jepara/Tuban/Gresik/Surabaya)', xy=(112.2, -6.95), xytext=(111.7, -6.3),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2), fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#ecfdf5', ec='#6ee7b7'))

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig4_peta_prioritas_pantura.png'), dpi=200)
plt.close()

print("Generating Figure 5: Hotspot Map...")
fig, ax = plt.subplots(figsize=(13, 4.5))
palette_hot = {'Konsentrasi Sangat Tinggi': '#dc2626', 'Konsentrasi Tinggi': '#f97316', 
               'Netral': '#94a3b8', 'Konsentrasi Rendah (Coldspot)': '#2563eb'}
for cat, col in palette_hot.items():
    sub = df[df['Hotspot_Cat'] == cat]
    if len(sub) > 0:
        ax.scatter(sub['lon'], sub['lat'], c=col, label=cat, s=14 if 'Tinggi' in cat else 9, alpha=0.85)

ax.set_title('Peta Konsentrasi Spasial Hotspot Berdasarkan Statistik Getis-Ord Gi*', fontweight='bold', pad=10)
ax.set_xlabel('Bujur Timur (Longitude)')
ax.set_ylabel('Lintang Selatan (Latitude)')
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.95)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig5_hotspot_getis_ord.png'), dpi=200)
plt.close()

print("Generating Figure 6: Silhouette & Typology...")
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
k_vals = [2, 3, 4, 5, 6]
s_vals = [0.363, 0.341, 0.319, 0.309, 0.310]
axes[0].plot(k_vals, s_vals, marker='o', linewidth=2.2, color='#2563eb', markersize=7)
axes[0].axvline(x=4, color='#dc2626', linestyle='--', label='k=4 Terpilih (Substantif)')
axes[0].set_title('(a) Evaluasi Silhouette Score Jumlah Klaster k', fontweight='bold')
axes[0].set_xlabel('Jumlah Klaster (k)')
axes[0].set_ylabel('Skor Silhouette')
axes[0].grid(True, linestyle='--', alpha=0.4)
axes[0].legend()

cross_tip = pd.crosstab(df['Tipologi'], df['region'], normalize='columns') * 100
cross_tip.T.plot(kind='bar', stacked=True, colormap='Spectral', ax=axes[1], edgecolor='black', alpha=0.85)
axes[1].set_title('(b) Komposisi Tipologi per Segmen Pantura', fontweight='bold')
axes[1].set_ylabel('Proporsi Grid (%)')
axes[1].set_xlabel('')
axes[1].legend(title='Tipologi Klaster', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8.5)
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig6_tipologi_kmeans.png'), dpi=200)
plt.close()

print("Generating Figure 7: Overlay...")
hot_tip = pd.crosstab(df['region'], df['Tipologi'], normalize='index') * 100
fig, ax = plt.subplots(figsize=(9, 4.8))
hot_tip.plot(kind='bar', stacked=True, colormap='coolwarm', edgecolor='black', alpha=0.9, ax=ax)
ax.set_title('Dominasi Profil Tipologi Tiap Segmen Pantura Jawa', fontweight='bold', pad=12)
ax.set_ylabel('Proporsi Grid (%)')
ax.set_xlabel('Segmen Koridor Pantura')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title='Profil Tipologi', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig7_overlay_hotspot_tipologi.png'), dpi=200)
plt.close()

print("Generating Figure 8: Sensitivity...")
weights = [0.5, 1.0, 1.5]
base_rank = stats.rankdata(df['Priority'])
corr_list = []
scen_ids = []
scen_id = 1
for w_t in weights:
    for w_d in weights:
        for w_v in weights:
            score_scen = (df['pct_T']**w_t) * (df['pct_D']**w_d) * (df['pct_V']**w_v)
            rank_scen = stats.rankdata(score_scen)
            spearman_rho, _ = stats.spearmanr(base_rank, rank_scen)
            corr_list.append(spearman_rho)
            scen_ids.append(f"S{scen_id:02d}")
            scen_id += 1

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(scen_ids, corr_list, marker='s', color='#0284c7', linewidth=1.8, markersize=5)
ax.axhline(y=0.90, color='#dc2626', linestyle='--', label='Ambang Batas Ketahanan (rho = 0.90)')
ax.axhline(y=np.mean(corr_list), color='#16a34a', linestyle='-', label=f'Rata-rata Konsistensi (rho = {np.mean(corr_list):.3f})')
ax.set_title('Uji Sensitivitas Indeks Priority terhadap 27 Skenario Pembobotan', fontweight='bold', pad=12)
ax.set_ylabel('Korelasi Rank Spearman vs Baseline')
ax.set_xlabel('Skenario Pembobotan (S01 - S27)')
ax.set_xticklabels(scen_ids, rotation=45, fontsize=8)
ax.set_ylim(0.60, 1.02)
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend(loc='lower left')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig8_uji_sensitivitas_27.png'), dpi=200)
plt.close()

print("ALL 7 FIGURES SUCCESSFULLY CREATED!")
