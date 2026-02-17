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

# Ubah kolom tanggal jadi datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# ===============================
# FILTER SIDEBAR (WAJIB DINAMIS)
# ===============================
st.sidebar.header("Filter Data")

min_date = df['dteday'].min()
max_date = df['dteday'].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) &
                     (df['dteday'] <= pd.to_datetime(end_date))]
else:
    filtered_df = df.copy()

# ===============================
# PERTANYAAN 1 – MUSIM
# ===============================
st.subheader("📊 Rata-rata Penyewaan Sepeda per Musim")

season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(data=season_avg, x='season', y='cnt', color='steelblue', ax=ax1)
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig1)

# Insight Dinamis Musim
if not season_avg.empty:
    max_season = season_avg.loc[season_avg['cnt'].idxmax(), 'season']
    min_season = season_avg.loc[season_avg['cnt'].idxmin(), 'season']

    st.markdown("### Insight Musim")
    st.markdown(f"""
    1. Musim dengan rata-rata penyewaan tertinggi adalah **{max_season}**.
    2. Musim dengan rata-rata penyewaan terendah adalah **{min_season}**.
    3. Pola ini menunjukkan adanya pengaruh musiman terhadap permintaan sepeda.
    """)

# ===============================
# PERTANYAAN 2 – CUACA
# ===============================
st.subheader("🌤️ Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")

weather_avg = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(data=weather_avg, x='weathersit', y='cnt', color='steelblue', ax=ax2)
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig2)

# Insight Dinamis Cuaca
if not weather_avg.empty:
    max_weather = weather_avg.loc[weather_avg['cnt'].idxmax(), 'weathersit']
    min_weather = weather_avg.loc[weather_avg['cnt'].idxmin(), 'weathersit']

    st.markdown("### Insight Cuaca")
    st.markdown(f"""
    1. Kondisi cuaca dengan rata-rata penyewaan tertinggi adalah **{max_weather}**.
    2. Kondisi dengan rata-rata penyewaan terendah adalah **{min_weather}**.
    3. Semakin buruk kondisi cuaca, kecenderungan penyewaan sepeda semakin menurun.
    """)

# ===============================
# METRIK TAMBAHAN (BIAR LEBIH KUAT)
# ===============================
st.subheader("📈 Ringkasan Statistik")

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(filtered_df['cnt'].sum()))
col2.metric("Rata-rata Harian", round(filtered_df['cnt'].mean(), 2))
col3.metric("Jumlah Hari", filtered_df['dteday'].nunique())
