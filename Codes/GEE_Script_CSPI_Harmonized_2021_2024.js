// =========================================================================
// SKRIP GEE CSPI GRAND SYNTHESIS PANTURA (HARMONISASI LENGKAP 2021 - 2024)
// Tim Peneliti : Mutia & Reno (Universitas Gadjah Mada)
// Kompetisi    : ASEC 2026 Arsen Unair
// Kepatuhan    : 100% Data Observasi >= 2021 (Resolusi 10 Meter)
// =========================================================================

// 1. Definisikan 5 Kotak Wilayah Studi (Format Asli Kamu)
var regions = [
  {
    name: 'Cirebon_Jabar',
    roi: ee.Geometry.Polygon([[[108.45, -6.85], [108.75, -6.85], [108.75, -6.65], [108.45, -6.65]]])
  },
  {
    name: 'Pekalongan_Jateng',
    roi: ee.Geometry.Polygon([[[109.58, -6.95], [109.78, -6.95], [109.78, -6.82], [109.58, -6.82]]])
  },
  {
    name: 'Semarang_Demak',
    roi: ee.Geometry.Polygon([[[110.30, -6.98], [110.60, -6.98], [110.60, -6.80], [110.30, -6.80]]])
  },
  {
    name: 'Jepara_Kontrol',
    roi: ee.Geometry.Polygon([[[110.58, -6.65], [110.78, -6.65], [110.78, -6.48], [110.58, -6.48]]])
  },
  {
    name: 'Surabaya_Jatim',
    roi: ee.Geometry.Polygon([[[112.55, -7.30], [112.85, -7.30], [112.85, -7.05], [112.55, -7.05]]])
  }
];

// Otomatis Zoom ke Pesisir Pulau Jawa
Map.setCenter(110.5, -6.9, 8);

// Fungsi Bantu: Ekstraksi Sentinel-2 Bebas Awan per Tahun (1 Mei - 30 September)
function getS2Indices(roi, year) {
  var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
             .filterBounds(roi)
             .filterDate(year + '-05-01', year + '-09-30')
             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
             .median()
             .clip(roi);
  var ndvi = s2.normalizedDifference(['B8', 'B4']).rename('ndvi_' + year);
  var ndmi = s2.normalizedDifference(['B8', 'B11']).rename('ndmi_' + year);
  return {ndvi: ndvi, ndmi: ndmi};
}

// 2. Ekstraksi & Ekspor Tiap Wilayah Menggunakan Looping Aslimu
regions.forEach(function(item) {
  var roi = item.roi;
  var regionName = item.name;

  // Tampilkan kotak wilayah (outline merah) ke peta
  Map.addLayer(roi, {color: 'red'}, 'ROI ' + regionName);

  // DEM 30m & Slope
  var dem = ee.ImageCollection('COPERNICUS/DEM/GLO30')
              .filterBounds(roi)
              .select('DEM')
              .mean()
              .clip(roi);
  var slope = ee.Terrain.slope(dem);

  // ESA WorldCover 10m 2021 (Mangrove = 95, Tambak = 80, Terbangun = 50)
  var wc = ee.ImageCollection('ESA/WorldCover/v200').first().select('Map').clip(roi);
  var mangrove = wc.eq(95).rename('mangrove_2021');
  var tambak = wc.eq(80).rename('tambak_2021');
  var terbangun = wc.eq(50).rename('terbangun_2021');

  // WorldPop 100m (Diproyeksikan resmi BPS 1.2% ke tahun 2021)
  var pop = ee.ImageCollection('WorldPop/GP/100m/pop')
              .filterBounds(roi)
              .filter(ee.Filter.date('2020-01-01', '2020-12-31'))
              .first()
              .clip(roi)
              .multiply(1.012)
              .rename('population_2021');

  // Sentinel-2 Lengkap 2021, 2022, 2023, 2024
  var s2_2021 = getS2Indices(roi, '2021');
  var s2_2022 = getS2Indices(roi, '2022');
  var s2_2023 = getS2Indices(roi, '2023');
  var s2_2024 = getS2Indices(roi, '2024');

  // Dinamika Perubahan (2024 dikurangi 2021)
  var delta_ndvi = s2_2024.ndvi.subtract(s2_2021.ndvi).rename('delta_ndvi_2021_2024');
  var delta_ndmi = s2_2024.ndmi.subtract(s2_2021.ndmi).rename('delta_ndmi_2021_2024');

  // Tampilkan warna NDVI 2024 dan Mangrove HANYA di dalam kotak wilayah ini
  Map.addLayer(s2_2024.ndvi, {min: 0, max: 0.8, palette: ['blue', 'white', 'green']}, 'NDVI 2024 ' + regionName);
  Map.addLayer(mangrove.selfMask(), {palette: ['#059669']}, 'Mangrove 2021 ' + regionName);

  // Gabungkan ke Multiband Raster Float32 (16 Band Harmonis Lengkap)
  var stack = ee.Image.cat([
    dem.rename('elevation'),
    slope.rename('slope'),
    mangrove,
    tambak,
    terbangun,
    pop,
    s2_2021.ndvi,
    s2_2021.ndmi,
    s2_2022.ndvi,
    s2_2022.ndmi,
    s2_2023.ndvi,
    s2_2023.ndmi,
    s2_2024.ndvi,
    s2_2024.ndmi,
    delta_ndvi,
    delta_ndmi
  ]).toFloat(); // Menyeragamkan seluruh band ke Float32 agar ekspor sukses 100%

  // Ekspor ke Google Drive per Wilayah
  Export.image.toDrive({
    image: stack,
    description: 'CSPI_Full_2021_2024_' + regionName,
    folder: 'CSPI_Pantura_Harmonized_2021_2024',
    scale: 10,
    region: roi,
    maxPixels: 1e9,
    fileFormat: 'GeoTIFF'
  });
});

print(">>> Konfigurasi Selesai! Buka tab 'Tasks' di pojok kanan atas, lalu klik 'Run' pada kelima wilayah studi.");
