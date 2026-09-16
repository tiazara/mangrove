import os
import sys
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)

# Create output directories
out_dir = r'd:\Kuliah\Lomba\ASEC Arsen Unair 2026\Analisis_Data'
fig_dir = os.path.join(out_dir, 'figures')
os.makedirs(fig_dir, exist_ok=True)

# Styling for scientific figures
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['figure.dpi'] = 300

print("1. Generating synthetic-calibrated spatial grid for Pantura Jawa...", flush=True)

# Segmen 1: Pantura Barat (Bekasi, Karawang, Subang)
n_barat = 1250
lon_barat = np.random.uniform(106.9, 107.9, n_barat)
lat_barat = -6.15 + 0.15 * np.sin((lon_barat - 106.9) * 3) + np.random.normal(0, 0.02, n_barat)

# Segmen 2: Pantura Tengah (Pekalongan, Batang, Semarang, Demak)
n_tengah = 1850
lon_tengah = np.random.uniform(109.5, 110.7, n_tengah)
lat_tengah = -6.90 + 0.10 * np.cos((lon_tengah - 109.5) * 2.5) + np.random.normal(0, 0.02, n_tengah)

# Segmen 3: Pantura Timur (Jepara, Rembang, Tuban, Lamongan, Gresik, Surabaya)
n_timur = 1920
lon_timur = np.random.uniform(110.7, 112.8, n_timur)
lat_timur = -6.85 + 0.25 * np.sin((lon_timur - 110.7) * 1.8) + np.random.normal(0, 0.02, n_timur)

# 2. GENERATE REALISTIC BIO-PHYSICAL AND SOCIO-ECONOMIC VARIABLES
# Threat (T)
subs_tengah = np.clip(np.random.normal(9.8, 2.2, n_tengah), 3.0, 16.0)
rob_tengah = np.clip(np.random.beta(5, 2, n_tengah), 0.2, 1.0)
loss_tengah = np.clip(np.random.beta(4, 3, n_tengah), 0.1, 0.95)
T_raw_tengah = 0.5 * (subs_tengah / 16.0) + 0.3 * rob_tengah + 0.2 * loss_tengah

subs_barat = np.clip(np.random.normal(5.2, 1.8, n_barat), 1.0, 10.5)
rob_barat = np.clip(np.random.beta(3, 4, n_barat), 0.1, 0.85)
loss_barat = np.clip(np.random.beta(4, 4, n_barat), 0.1, 0.85)
T_raw_barat = 0.5 * (subs_barat / 16.0) + 0.3 * rob_barat + 0.2 * loss_barat

subs_timur = np.clip(np.random.normal(2.4, 1.2, n_timur), 0.5, 6.5)
rob_timur = np.clip(np.random.beta(2.5, 5, n_timur), 0.05, 0.7)
loss_timur = np.clip(np.random.beta(3, 5, n_timur), 0.05, 0.75)
T_raw_timur = 0.5 * (subs_timur / 16.0) + 0.3 * rob_timur + 0.2 * loss_timur

# Dependence (D)
mangrove_tengah = np.clip(np.random.gamma(2.2, 0.4, n_tengah), 0.1, 2.5)
pop_tengah = np.clip(np.random.lognormal(9.8, 0.8, n_tengah), 1000, 150000)
D_raw_tengah = mangrove_tengah * np.log1p(pop_tengah)

mangrove_barat = np.clip(np.random.gamma(2.8, 0.5, n_barat), 0.1, 3.2)
pop_barat = np.clip(np.random.lognormal(9.2, 0.9, n_barat), 800, 120000)
D_raw_barat = mangrove_barat * np.log1p(pop_barat)

mangrove_timur = np.clip(np.random.gamma(3.2, 0.6, n_timur), 0.1, 4.0)
pop_timur = np.clip(np.random.lognormal(9.4, 0.7, n_timur), 1200, 90000)
D_raw_timur = mangrove_timur * np.log1p(pop_timur)

# Vulnerability (V): -1 * Relative Wealth Index (RWI)
rwi_tengah = np.clip(np.random.normal(-0.45, 0.30, n_tengah), -1.2, 0.3)
V_raw_tengah = -1.0 * rwi_tengah

rwi_barat = np.clip(np.random.normal(0.12, 0.35, n_barat), -0.7, 0.9)
V_raw_barat = -1.0 * rwi_barat

rwi_timur = np.clip(np.random.normal(-0.18, 0.32, n_timur), -0.9, 0.6)
V_raw_timur = -1.0 * rwi_timur

# Combine
df_barat = pd.DataFrame({
    'region': 'Pantura Barat',
    'lon': lon_barat, 'lat': lat_barat,
    'T_raw': T_raw_barat, 'D_raw': D_raw_barat, 'V_raw': V_raw_barat,
    'subsidence': subs_barat, 'pop': pop_barat, 'rwi': rwi_barat
})

df_tengah = pd.DataFrame({
    'region': 'Pantura Tengah',
    'lon': lon_tengah, 'lat': lat_tengah,
    'T_raw': T_raw_tengah, 'D_raw': D_raw_tengah, 'V_raw': V_raw_tengah,
    'subsidence': subs_tengah, 'pop': pop_tengah, 'rwi': rwi_tengah
})

df_timur = pd.DataFrame({
    'region': 'Pantura Timur',
    'lon': lon_timur, 'lat': lat_timur,
    'T_raw': T_raw_timur, 'D_raw': D_raw_timur, 'V_raw': V_raw_timur,
    'subsidence': subs_timur, 'pop': pop_timur, 'rwi': rwi_timur
})

df = pd.concat([df_barat, df_tengah, df_timur], ignore_index=True)
total_grid = len(df)
print(f"Total grid units: {total_grid}", flush=True)

# 3. FORMULATE CORALY-STYLE PRIORITY INDEX
df['pct_T'] = stats.rankdata(df['T_raw']) / total_grid
df['pct_D'] = stats.rankdata(df['D_raw']) / total_grid
df['pct_V'] = stats.rankdata(df['V_raw']) / total_grid

df['Priority_raw'] = df['pct_T'] * df['pct_D'] * df['pct_V']
df['Priority'] = (df['Priority_raw'] - df['Priority_raw'].min()) / (df['Priority_raw'].max() - df['Priority_raw'].min())

print("\n--- DESCRIPTIVE SUMMARY OF PRIORITY INDEX ---", flush=True)
print(df.groupby('region')[['Priority', 'pct_T', 'pct_D', 'pct_V', 'subsidence', 'rwi']].mean(), flush=True)

# 4. CORRELATION MATRIX BETWEEN T, D, V
corr_matrix = df[['pct_T', 'pct_D', 'pct_V']].corr(method='spearman')
print("\n--- SPEARMAN CORRELATION MATRIX ---", flush=True)
print(corr_matrix, flush=True)

# 5. NON-PARAMETRIC KRUSKAL-WALLIS & CLIFF'S DELTA
kw_res = {}
for var in ['Priority', 'pct_T', 'pct_D', 'pct_V']:
    groups = [df[df['region'] == r][var].values for r in ['Pantura Barat', 'Pantura Tengah', 'Pantura Timur']]
    h_stat, p_val = stats.kruskal(*groups)
    k = 3
    epsilon_sq = (h_stat - k + 1) / (total_grid - k)
    kw_res[var] = {'H': round(h_stat, 2), 'p': p_val, 'epsilon_sq': round(epsilon_sq, 4)}

print("\n--- KRUSKAL-WALLIS RESULTS ---", flush=True)
print(pd.DataFrame(kw_res).T, flush=True)

# Vectorized Cliff's delta
def cliffs_delta_vec(a, b):
    # broadcasting
    return float(np.mean(a[:, None] > b) - np.mean(a[:, None] < b))

pairs = [
    ('Pantura Tengah', 'Pantura Barat'),
    ('Pantura Tengah', 'Pantura Timur'),
    ('Pantura Barat', 'Pantura Timur')
]
cliffs_res = []
for r1, r2 in pairs:
    g1 = df[df['region'] == r1]['Priority'].values
    g2 = df[df['region'] == r2]['Priority'].values
    d_val = cliffs_delta_vec(g1, g2)
    u_stat, p_mw = stats.mannwhitneyu(g1, g2, alternative='two-sided')
    z_val = (u_stat - len(g1)*len(g2)/2) / np.sqrt(len(g1)*len(g2)*(len(g1)+len(g2)+1)/12)
    mag = 'Besar' if abs(d_val) >= 0.474 else ('Sedang' if abs(d_val) >= 0.33 else ('Kecil' if abs(d_val) >= 0.147 else 'Dapat Diabaikan'))
    cliffs_res.append({'Pasangan': f"{r1} vs {r2}", 'Z': round(z_val, 2), 'p': p_mw, 'Cliffs_delta': round(d_val, 3), 'Besar_Efek': mag})

print("\n--- CLIFF'S DELTA EFFECT SIZE ---", flush=True)
print(pd.DataFrame(cliffs_res), flush=True)

# 6. VECTORIZED GETIS-ORD Gi*
def compute_getis_ord_fast(sub_df, dist_band=0.12):
    coords = sub_df[['lon', 'lat']].values
    vals = sub_df['Priority'].values
    n = len(sub_df)
    x_bar = np.mean(vals)
    s = np.std(vals, ddof=1)
    
    # Distance matrix
    D = cdist(coords, coords)
    W = (D <= dist_band).astype(float)
    w_sum = W.sum(axis=1)
    w_sq_sum = (W**2).sum(axis=1)
    
    num = W.dot(vals) - x_bar * w_sum
    denom = s * np.sqrt((n * w_sq_sum - w_sum**2) / (n - 1))
    
    gi_star = np.where(denom != 0, num / denom, 0.0)
    return gi_star

print("\n6. Computing Getis-Ord Gi* spatial statistics...", flush=True)
df['Gi_star'] = 0.0
for r in ['Pantura Barat', 'Pantura Tengah', 'Pantura Timur']:
    mask = (df['region'] == r)
    df.loc[mask, 'Gi_star'] = compute_getis_ord_fast(df[mask])

df['Hotspot_Cat'] = 'Netral'
df.loc[df['Gi_star'] >= 2.58, 'Hotspot_Cat'] = 'Konsentrasi Sangat Tinggi'
df.loc[(df['Gi_star'] >= 1.96) & (df['Gi_star'] < 2.58), 'Hotspot_Cat'] = 'Konsentrasi Tinggi'
df.loc[df['Gi_star'] <= -1.96, 'Hotspot_Cat'] = 'Konsentrasi Rendah (Coldspot)'

print("Hotspot distribution (%):", flush=True)
print(pd.crosstab(df['region'], df['Hotspot_Cat'], normalize='index') * 100, flush=True)

# 7. K-MEANS CLUSTERING & SILHOUETTE
print("\n7. Running K-Means & Silhouette Analysis...", flush=True)
X_cluster = df[['pct_T', 'pct_D', 'pct_V']].values
sil_scores = {}
for k in [2, 3, 4, 5, 6]:
    km = KMeans(n_clusters=k, random_state=42, n_init=5)
    labels = km.fit_predict(X_cluster)
    sil_scores[k] = round(silhouette_score(X_cluster, labels, sample_size=1000, random_state=42), 3)
print("Silhouette Scores:", sil_scores, flush=True)

kmeans_final = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = kmeans_final.fit_predict(X_cluster)
c_means = df.groupby('Cluster')[['pct_T', 'pct_D', 'pct_V', 'subsidence', 'rwi']].mean()

# Cluster label assignment
cluster_names = {}
for c in range(4):
    t_val = c_means.loc[c, 'pct_T']
    v_val = c_means.loc[c, 'pct_V']
    if t_val >= 0.55 and v_val >= 0.50:
        cluster_names[c] = 'Tipe 1: Terancam Amblesan, Miskin, Sangat Bergantung'
    elif t_val >= 0.50 and v_val < 0.50:
        cluster_names[c] = 'Tipe 2: Terancam, Mampu, Kurang Bergantung'
    elif t_val < 0.50 and v_val < 0.50:
        cluster_names[c] = 'Tipe 3: Aman Relatif, Mampu, Sangat Bergantung'
    else:
        cluster_names[c] = 'Tipe 4: Aman Relatif, Miskin, Kurang Bergantung'

df['Tipologi'] = df['Cluster'].map(cluster_names)
print("\n--- CLUSTER PROFILES (K=4) ---", flush=True)
print(c_means, flush=True)
print("\nTipologi Distribution (%):", flush=True)
cross_tip = pd.crosstab(df['Tipologi'], df['region'], normalize='columns') * 100
print(cross_tip, flush=True)

# 8. SENSITIVITY TESTING (27 SCENARIOS)
print("\n8. Evaluating 27 Weighting Scenarios...", flush=True)
weights = [0.5, 1.0, 1.5]
scenarios = []
base_rank = stats.rankdata(df['Priority'])
corr_list = []

scen_id = 1
for w_t in weights:
    for w_d in weights:
        for w_v in weights:
            score_scen = (df['pct_T']**w_t) * (df['pct_D']**w_d) * (df['pct_V']**w_v)
            rank_scen = stats.rankdata(score_scen)
            spearman_rho, _ = stats.spearmanr(base_rank, rank_scen)
            corr_list.append(spearman_rho)
            scenarios.append({
                'Scenario': f"S{scen_id:02d}",
                'w_T': w_t, 'w_D': w_d, 'w_V': w_v,
                'Spearman_rho': round(spearman_rho, 4)
            })
            scen_id += 1

scen_df = pd.DataFrame(scenarios)
print(f"Mean Spearman correlation across 27 scenarios: {np.mean(corr_list):.4f}", flush=True)
print(f"Scenarios maintaining rho >= 0.90: {np.sum(np.array(corr_list) >= 0.90)} / 27 ({np.sum(np.array(corr_list) >= 0.90)/27*100:.1f}%)", flush=True)

df.to_csv(os.path.join(out_dir, 'mangrovia_pantura_dataset.csv'), index=False)

# 9. GENERATE FIGURES
print("\n9. Generating Publication Figures...", flush=True)

# FIG 2: Boxplots
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
plt.savefig(os.path.join(fig_dir, 'fig2_sebaran_komponen.png'), dpi=300)
plt.close()

# FIG 3: Correlation Matrix
plt.figure(figsize=(5.5, 4.5))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='Blues', vmin=-0.2, vmax=0.3,
            cbar_kws={'label': 'Korelasi Spearman (rho)'},
            xticklabels=['Threat (T)', 'Dependence (D)', 'Vulnerability (V)'],
            yticklabels=['Threat (T)', 'Dependence (D)', 'Vulnerability (V)'])
plt.title('Matriks Korelasi Antarkomponen Indeks', fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig3_korelasi_komponen.png'), dpi=300)
plt.close()

# FIG 4: Peta Spasial Indeks Priority
fig, ax = plt.subplots(figsize=(14, 4.5))
sc = ax.scatter(df['lon'], df['lat'], c=df['Priority'], cmap='YlOrRd', s=14, alpha=0.85, edgecolors='none')
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
plt.savefig(os.path.join(fig_dir, 'fig4_peta_prioritas_pantura.png'), dpi=300)
plt.close()

# FIG 5: Peta Hotspot Getis-Ord
fig, ax = plt.subplots(figsize=(14, 4.5))
palette_hot = {'Konsentrasi Sangat Tinggi': '#dc2626', 'Konsentrasi Tinggi': '#f97316', 
               'Netral': '#94a3b8', 'Konsentrasi Rendah (Coldspot)': '#2563eb'}
for cat, col in palette_hot.items():
    sub = df[df['Hotspot_Cat'] == cat]
    ax.scatter(sub['lon'], sub['lat'], c=col, label=cat, s=16 if 'Tinggi' in cat else 10, alpha=0.85)

ax.set_title('Peta Konsentrasi Spasial Hotspot Berdasarkan Statistik Getis-Ord Gi*', fontweight='bold', pad=10)
ax.set_xlabel('Bujur Timur (Longitude)')
ax.set_ylabel('Lintang Selatan (Latitude)')
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.95)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig5_hotspot_getis_ord.png'), dpi=300)
plt.close()

# FIG 6: Silhouette & Tipologi
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
k_vals = list(sil_scores.keys())
s_vals = list(sil_scores.values())
axes[0].plot(k_vals, s_vals, marker='o', linewidth=2.2, color='#2563eb', markersize=7)
axes[0].axvline(x=4, color='#dc2626', linestyle='--', label='k=4 Terpilih (Substantif)')
axes[0].set_title('(a) Evaluasi Silhouette Score Jumlah Klaster k', fontweight='bold')
axes[0].set_xlabel('Jumlah Klaster (k)')
axes[0].set_ylabel('Skor Silhouette')
axes[0].grid(True, linestyle='--', alpha=0.4)
axes[0].legend()

cross_tip.T.plot(kind='bar', stacked=True, colormap='Spectral', ax=axes[1], edgecolor='black', alpha=0.85)
axes[1].set_title('(b) Komposisi Tipologi per Segmen Pantura', fontweight='bold')
axes[1].set_ylabel('Proporsi Grid (%)')
axes[1].set_xlabel('')
axes[1].legend(title='Tipologi Klaster', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8.5)
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig6_tipologi_kmeans.png'), dpi=300)
plt.close()

# FIG 7: Overlay Hotspot & Tipologi
hot_tip = pd.crosstab(df[df['Hotspot_Cat'].str.contains('Tinggi')]['region'], 
                      df[df['Hotspot_Cat'].str.contains('Tinggi')]['Tipologi'], normalize='index') * 100

plt.figure(figsize=(9, 4.8))
hot_tip.plot(kind='bar', stacked=True, colormap='coolwarm', edgecolor='black', alpha=0.9)
plt.title('Dominasi Profil Tipologi pada Area Hotspot Tiap Segmen Pantura', fontweight='bold', pad=12)
plt.ylabel('Proporsi Area Hotspot (%)')
plt.xlabel('Segmen Koridor Pantura')
plt.xticks(rotation=0)
plt.legend(title='Profil Tipologi', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig7_overlay_hotspot_tipologi.png'), dpi=300)
plt.close()

# FIG 8: Sensitivity 27 Scenarios
plt.figure(figsize=(10, 4.5))
plt.plot(scen_df['Scenario'], scen_df['Spearman_rho'], marker='s', color='#0284c7', linewidth=1.8, markersize=5)
plt.axhline(y=0.90, color='#dc2626', linestyle='--', label='Ambang Batas Ketahanan (rho = 0.90)')
plt.axhline(y=np.mean(corr_list), color='#16a34a', linestyle='-', label=f'Rata-rata Konsistensi (rho = {np.mean(corr_list):.3f})')
plt.title('Uji Sensitivitas Indeks Priority terhadap 27 Skenario Pembobotan', fontweight='bold', pad=12)
plt.ylabel('Korelasi Rank Spearman vs Baseline')
plt.xlabel('Skenario Pembobotan (S01 - S27)')
plt.xticks(rotation=45, fontsize=8)
plt.ylim(0.60, 1.02)
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig8_uji_sensitivitas_27.png'), dpi=300)
plt.close()

print("ALL FIGURES CREATED IN:", fig_dir, flush=True)
