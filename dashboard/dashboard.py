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
# VISUALISASI 4
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

# ==========================================================
# ================== TAMBAHAN FITUR ========================
# ==========================================================

# =============================
# KPI SUMMARY
# =============================
st.header("Ringkasan Statistik")

total_rent = filtered_df['cnt'].sum()
avg_rent = filtered_df['cnt'].mean()
max_rent = filtered_df['cnt'].max()
min_rent = filtered_df['cnt'].min()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Penyewaan", f"{total_rent:,.0f}")
col2.metric("Rata-rata Harian", f"{avg_rent:,.0f}")
col3.metric("Penyewaan Tertinggi", f"{max_rent:,.0f}")
col4.metric("Penyewaan Terendah", f"{min_rent:,.0f}")

# =============================
# Growth Rate Antar Tahun
# =============================
st.header("Analisis Pertumbuhan")

year_comparison = df.groupby('yr')['cnt'].mean().reset_index()

avg_2011 = year_comparison[year_comparison['yr'] == 0]['cnt'].values[0]
avg_2012 = year_comparison[year_comparison['yr'] == 1]['cnt'].values[0]

growth_rate = ((avg_2012 - avg_2011) / avg_2011) * 100

st.metric("Pertumbuhan 2012 vs 2011", f"{growth_rate:.2f}%")

# =============================
# Tren Penyewaan Harian
# =============================
st.header("Tren Penyewaan Harian")

if 'dteday' in filtered_df.columns:
    filtered_df['dteday'] = pd.to_datetime(filtered_df['dteday'])
    trend_data = filtered_df.sort_values('dteday')

    fig_trend, ax_trend = plt.subplots(figsize=(8,4))
    ax_trend.plot(trend_data['dteday'], trend_data['cnt'])
    ax_trend.set_title("Tren Penyewaan Harian")
    ax_trend.set_xlabel("Tanggal")
    ax_trend.set_ylabel("Jumlah Penyewaan")

    st.pyplot(fig_trend)

# =============================
# Korelasi Antar Variabel
# =============================
st.header("Analisis Korelasi")

numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64'])
correlation = numeric_cols.corr()

fig_corr, ax_corr = plt.subplots(figsize=(8,6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax_corr)

st.pyplot(fig_corr)

# =============================
# Download Data
# =============================
st.header("Unduh Data yang Difilter")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Data CSV",
    data=csv,
    file_name=f"filtered_data_{selected_year_label}.csv",
    mime="text/csv"
)
