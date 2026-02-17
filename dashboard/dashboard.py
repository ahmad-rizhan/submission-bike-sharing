import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.write("Dashboard analisis penyewaan sepeda periode 2011–2012")

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("main_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# ==============================
# SIDEBAR FILTER
# ==============================
st.sidebar.header("Filter Data")

min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = df[
        (df['dteday'] >= start_date) &
        (df['dteday'] <= end_date)
    ]
else:
    filtered_df = df.copy()

# ==============================
# VISUALISASI 1
# RATA-RATA PENYEWAAN PER MUSIM
# ==============================
st.subheader("Rata-rata Penyewaan Sepeda per Musim")

season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()

plt.figure(figsize=(8,5))
sns.barplot(data=season_avg, x='season', y='cnt', color='steelblue')
plt.title("Rata-rata Penyewaan Sepeda per Musim")
plt.xlabel("Musim")
plt.ylabel("Rata-rata Penyewaan")
st.pyplot(plt)

# Insight Dinamis
if not season_avg.empty:
    highest = season_avg.loc[season_avg['cnt'].idxmax()]
    lowest = season_avg.loc[season_avg['cnt'].idxmin()]

    st.markdown("### Insight:")
    st.write(f"1. Musim dengan rata-rata penyewaan tertinggi adalah **{highest['season']}**.")
    st.write(f"2. Musim dengan rata-rata penyewaan terendah adalah **{lowest['season']}**.")
    st.write("3. Pola musiman menunjukkan adanya pengaruh musim terhadap tingkat permintaan sepeda.")

# ==============================
# VISUALISASI 2
# RATA-RATA PENYEWAAN BERDASARKAN CUACA
# ==============================
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

weather_avg = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()

plt.figure(figsize=(8,5))
sns.barplot(data=weather_avg, x='weathersit', y='cnt', color='steelblue')
plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Rata-rata Penyewaan")
st.pyplot(plt)

# Insight Dinamis
if not weather_avg.empty:
    highest_weather = weather_avg.loc[weather_avg['cnt'].idxmax()]
    lowest_weather = weather_avg.loc[weather_avg['cnt'].idxmin()]

    st.markdown("### Insight:")
    st.write(f"1. Kondisi cuaca dengan rata-rata penyewaan tertinggi adalah **{highest_weather['weathersit']}**.")
    st.write(f"2. Kondisi cuaca dengan rata-rata penyewaan terendah adalah **{lowest_weather['weathersit']}**.")
    st.write("3. Semakin buruk kondisi cuaca, cenderung semakin rendah jumlah penyewaan sepeda.")

# ==============================
# CONCLUSION DINAMIS
# ==============================
st.subheader("Kesimpulan")

if not season_avg.empty and not weather_avg.empty:
    st.write("Berdasarkan filter tanggal yang dipilih:")
    st.write(f"- Musim paling tinggi: **{highest['season']}**")
    st.write(f"- Cuaca paling tinggi: **{highest_weather['weathersit']}**")
    st.write("Hal ini menunjukkan faktor lingkungan seperti musim dan cuaca sangat memengaruhi tingkat penyewaan sepeda.")
