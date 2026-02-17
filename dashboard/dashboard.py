import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.write("Dashboard analisis penyewaan sepeda periode 2011–2012")

# Load data
df = pd.read_csv("dashboard/main_data.csv")

# Mapping tahun
df['year_label'] = df['yr'].map({0: 2011, 1: 2012})

# ===============================
# FILTER INTERAKTIF
# ===============================
st.sidebar.header("Filter Data")

selected_year = st.sidebar.selectbox(
    "Pilih Tahun:",
    options=df['year_label'].unique()
)

filtered_df = df[df['year_label'] == selected_year]

st.subheader(f"Analisis Tahun {selected_year}")

# ===============================
# Grafik 1: Musim
# ===============================
season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(data=season_avg, x='season', y='cnt', color='steelblue', ax=ax1)
ax1.set_title("Rata-rata Penyewaan Sepeda per Musim")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig1)

# ===============================
# Grafik 2: Cuaca
# ===============================
weather_avg = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(data=weather_avg, x='weathersit', y='cnt', color='steelblue', ax=ax2)
ax2.set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig2)

# ===============================
# Ringkasan Insight
# ===============================
st.markdown("### Insight Utama")
st.markdown("""
1. Musim dengan rata-rata penyewaan tertinggi dapat berbeda tiap tahun.
2. Kondisi cuaca cerah cenderung menghasilkan jumlah penyewaan lebih tinggi.
3. Cuaca buruk seperti hujan atau salju ringan menyebabkan penurunan signifikan.
4. Faktor musim dan cuaca perlu dipertimbangkan dalam perencanaan operasional.
""")
