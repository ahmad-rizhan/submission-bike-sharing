import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# KONFIGURASI AWAL
# ===============================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.write("Dashboard analisis penyewaan sepeda periode 2011–2012")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("dashboard/main_data.csv")

# ===============================
# FILTER SIDEBAR
# ===============================
st.sidebar.header("Filter Data")

year_option = st.sidebar.selectbox(
    "Pilih Tahun",
    options=df['yr'].unique()
)

filtered_df = df[df['yr'] == year_option]

# Ubah label tahun agar lebih jelas
year_label = "2011" if year_option == 0 else "2012"

st.subheader(f"Analisis Tahun {year_label}")

# ===============================
# VISUALISASI 1: MUSIM
# ===============================
season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()

plt.figure(figsize=(8,5))
sns.barplot(data=season_avg, x='season', y='cnt', color='steelblue')
plt.title('Rata-rata Penyewaan Sepeda per Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Penyewaan')
st.pyplot(plt)

# Insight Musim (Dinamis)
highest_season = season_avg.loc[season_avg['cnt'].idxmax(), 'season']
lowest_season = season_avg.loc[season_avg['cnt'].idxmin(), 'season']

st.markdown("### Insight Musim:")
st.markdown(f"""
1. Musim dengan rata-rata penyewaan tertinggi adalah **{highest_season}**.
2. Musim dengan rata-rata penyewaan terendah adalah **{lowest_season}**.
3. Terdapat pola musiman yang mempengaruhi tingkat penggunaan sepeda.
4. Strategi operasional perlu difokuskan pada musim dengan permintaan tertinggi.
""")

# ===============================
# VISUALISASI 2: KONDISI CUACA
# ===============================
weather_avg = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()

plt.figure(figsize=(8,5))
sns.barplot(data=weather_avg, x='weathersit', y='cnt', color='steelblue')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Rata-rata Penyewaan')
st.pyplot(plt)

# Insight Cuaca (Dinamis)
highest_weather = weather_avg.loc[weather_avg['cnt'].idxmax(), 'weathersit']
lowest_weather = weather_avg.loc[weather_avg['cnt'].idxmin(), 'weathersit']

st.markdown("### Insight Cuaca:")
st.markdown(f"""
1. Kondisi cuaca dengan rata-rata penyewaan tertinggi adalah **{highest_weather}**.
2. Kondisi cuaca dengan rata-rata penyewaan terendah adalah **{lowest_weather}**.
3. Semakin buruk kondisi cuaca, semakin rendah tingkat penyewaan sepeda.
4. Perencanaan kapasitas layanan perlu mempertimbangkan faktor cuaca.
""")

# ===============================
# VISUALISASI 3: KATEGORI SUHU (BINNING)
# ===============================
filtered_df['temp_category'] = pd.cut(
    filtered_df['temp'],
    bins=3,
    labels=['Low', 'Medium', 'High']
)

temp_avg = filtered_df.groupby('temp_category')['cnt'].mean().reset_index()

plt.figure(figsize=(8,5))
sns.barplot(data=temp_avg, x='temp_category', y='cnt', color='steelblue')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu')
plt.xlabel('Kategori Suhu')
plt.ylabel('Rata-rata Penyewaan')
st.pyplot(plt)

# Insight Suhu
highest_temp = temp_avg.loc[temp_avg['cnt'].idxmax(), 'temp_category']
lowest_temp = temp_avg.loc[temp_avg['cnt'].idxmin(), 'temp_category']

st.markdown("### Insight Suhu:")
st.markdown(f"""
1. Kategori suhu dengan rata-rata penyewaan tertinggi adalah **{highest_temp}**.
2. Kategori suhu dengan rata-rata penyewaan terendah adalah **{lowest_temp}**.
3. Suhu yang lebih tinggi cenderung meningkatkan jumlah penyewaan sepeda.
4. Faktor suhu perlu dipertimbangkan dalam strategi operasional layanan.
""")

# ===============================
# KESIMPULAN
# ===============================
st.markdown("## 📌 Conclusion")

st.markdown(f"""
1. Pada tahun {year_label}, musim dan kondisi cuaca terbukti mempengaruhi tingkat penyewaan sepeda.
2. Musim dengan permintaan tertinggi memerlukan kesiapan operasional yang lebih optimal.
3. Kondisi cuaca buruk dan suhu rendah cenderung menurunkan tingkat penggunaan sepeda.
4. Faktor lingkungan seperti musim, cuaca, dan suhu memiliki peran penting dalam menentukan strategi operasional layanan penyewaan sepeda.
""")
