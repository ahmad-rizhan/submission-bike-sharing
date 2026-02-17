import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================
# Konfigurasi halaman
# =============================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.write("Dashboard analisis penyewaan sepeda periode 2011–2012")

# =============================
# Load Data
# =============================
df = pd.read_csv("dashboard/main_data.csv")

# Mapping tahun
year_map = {0: 2011, 1: 2012}

# =============================
# SIDEBAR FILTER
# =============================
st.sidebar.header("Filter Data")

selected_year_label = st.sidebar.selectbox(
    "Pilih Tahun",
    options=list(year_map.values())
)

selected_year_code = [k for k, v in year_map.items() if v == selected_year_label][0]

filtered_df = df[df['yr'] == selected_year_code]

st.subheader(f"Analisis Tahun {selected_year_label}")

# =============================
# VISUALISASI 1
# Rata-rata Penyewaan per Musim
# =============================
season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(6,4))
sns.barplot(data=season_avg, x='season', y='cnt', color='steelblue', ax=ax1)
ax1.set_title("Rata-rata Penyewaan Sepeda per Musim")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig1)

st.markdown("""
**Insight:**
1. Musim dengan rata-rata penyewaan tertinggi menunjukkan periode permintaan paling kuat.
2. Musim dengan rata-rata terendah perlu strategi promosi atau efisiensi operasional.
3. Pola musiman berpengaruh terhadap tingkat penggunaan layanan.
""")

# =============================
# VISUALISASI 2
# Rata-rata Penyewaan berdasarkan Cuaca
# =============================
weather_avg = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(6,4))
sns.barplot(data=weather_avg, x='weathersit', y='cnt', color='steelblue', ax=ax2)
ax2.set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig2)

st.markdown("""
**Insight:**
1. Cuaca cerah cenderung meningkatkan jumlah penyewaan sepeda.
2. Kondisi cuaca buruk menyebabkan penurunan signifikan pada penggunaan sepeda.
3. Faktor cuaca perlu dipertimbangkan dalam perencanaan kapasitas layanan.
""")

# =============================
# VISUALISASI 3
# Rata-rata Penyewaan per Tahun
# =============================
yearly_avg = df.groupby('yr')['cnt'].mean().reset_index()
yearly_avg['yr'] = yearly_avg['yr'].map(year_map)

fig3, ax3 = plt.subplots(figsize=(6,4))
sns.barplot(data=yearly_avg, x='yr', y='cnt', color='steelblue', ax=ax3)
ax3.set_title("Rata-rata Penyewaan Sepeda per Tahun")
ax3.set_xlabel("Tahun")
ax3.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig3)

st.markdown("""
**Insight:**
1. Terdapat perbedaan rata-rata penyewaan antara tahun 2011 dan 2012.
2. Tahun dengan nilai lebih tinggi menunjukkan peningkatan minat atau pertumbuhan penggunaan.
3. Hal ini mengindikasikan adanya tren peningkatan penggunaan layanan.
""")

# =============================
# VISUALISASI 4 (Analisis Lanjutan)
# Kategori Suhu (Binning)
# =============================
filtered_df['temp_category'] = pd.cut(
    filtered_df['temp'],
    bins=3,
    labels=['Low', 'Medium', 'High']
)

temp_avg = filtered_df.groupby('temp_category')['cnt'].mean().reset_index()

fig4, ax4 = plt.subplots(figsize=(6,4))
sns.barplot(data=temp_avg, x='temp_category', y='cnt', color='steelblue', ax=ax4)
ax4.set_title("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
ax4.set_xlabel("Kategori Suhu")
ax4.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig4)

st.markdown("""
**Insight (Analisis Lanjutan):**
1. Suhu yang lebih tinggi cenderung menghasilkan rata-rata penyewaan lebih besar.
2. Suhu rendah menunjukkan tingkat penggunaan yang lebih rendah.
3. Faktor suhu menjadi variabel penting dalam pola penggunaan sepeda.
""")

# =============================
# KESIMPULAN
# =============================
st.header("Kesimpulan")

st.markdown("""
1. Musim memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda.
2. Kondisi cuaca memengaruhi tingkat penggunaan layanan secara langsung.
3. Terdapat peningkatan rata-rata penyewaan dari tahun 2011 ke 2012.
4. Suhu yang lebih tinggi berkorelasi dengan peningkatan penggunaan sepeda.
5. Faktor lingkungan (musim, cuaca, suhu) berperan penting dalam perencanaan operasional layanan.
""")
