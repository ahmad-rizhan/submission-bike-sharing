import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.write("Dashboard analisis penyewaan sepeda periode 2011–2012")

# =========================
# LOAD DATA (AMAN & KONSISTEN)
# =========================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "main_data.csv")

df = pd.read_csv(DATA_PATH)
df['dteday'] = pd.to_datetime(df['dteday'])

# =========================
# FILTER SIDEBAR
# =========================
st.sidebar.header("Filter Data")

min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[
    (df['dteday'] >= pd.to_datetime(start_date)) &
    (df['dteday'] <= pd.to_datetime(end_date))
]

# =========================
# VISUALISASI 1: MUSIM
# =========================
st.subheader("Rata-rata Penyewaan Sepeda per Musim")

season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()

plt.figure(figsize=(8,5))
sns.barplot(data=season_avg, x='season', y='cnt', color='steelblue')
plt.title("Rata-rata Penyewaan Sepeda per Musim")
plt.xlabel("Musim")
plt.ylabel("Rata-rata Penyewaan")
st.pyplot(plt)

if not season_avg.empty:
    highest_season = season_avg.loc[season_avg['cnt'].idxmax()]
    lowest_season = season_avg.loc[season_avg['cnt'].idxmin()]

    st.markdown("### Insight Musim")
    st.write(f"- Musim tertinggi: **{highest_season['season']}**")
    st.write(f"- Musim terendah: **{lowest_season['season']}**")
    st.write("Permintaan sepeda dipengaruhi oleh pola musiman.")

# =========================
# VISUALISASI 2: CUACA
# =========================
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

weather_avg = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()

plt.figure(figsize=(8,5))
sns.barplot(data=weather_avg, x='weathersit', y='cnt', color='steelblue')
plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Rata-rata Penyewaan")
st.pyplot(plt)

if not weather_avg.empty:
    highest_weather = weather_avg.loc[weather_avg['cnt'].idxmax()]
    lowest_weather = weather_avg.loc[weather_avg['cnt'].idxmin()]

    st.markdown("### Insight Cuaca")
    st.write(f"- Cuaca tertinggi: **{highest_weather['weathersit']}**")
    st.write(f"- Cuaca terendah: **{lowest_weather['weathersit']}**")
    st.write("Semakin buruk cuaca, rata-rata penyewaan cenderung menurun.")

# =========================
# KESIMPULAN DINAMIS
# =========================
st.subheader("Kesimpulan")

if not season_avg.empty and not weather_avg.empty:
    st.write("Berdasarkan rentang tanggal yang dipilih:")
    st.write(f"- Musim paling tinggi: **{highest_season['season']}**")
    st.write(f"- Cuaca paling tinggi: **{highest_weather['weathersit']}**")
    st.write("Faktor musim dan cuaca memiliki pengaruh signifikan terhadap tingkat penyewaan sepeda.")
