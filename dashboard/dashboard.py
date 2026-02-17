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

# Pastikan kolom tanggal dalam format datetime (AMAN)
if 'dteday' in df.columns:
    df['dteday'] = pd.to_datetime(df['dteday'])

# Mapping tahun
year_map = {0: 2011, 1: 2012}

# =============================
# SIDEBAR FILTER (ASLI)
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
# VISUALISASI 1 (ASLI)
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
# VISUALISASI 2 (ASLI)
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
# VISUALISASI 3 (ASLI)
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
# VISUALISASI 4 (ASLI)
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
# KESIMPULAN (ASLI)
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
# ================= TAMBAHAN DINAMIS FINAL =================
# ==========================================================

st.header("Business Questions & Dynamic Analysis")

st.markdown("""
### Business Questions:
1. Musim apa yang memiliki rata-rata penyewaan tertinggi pada rentang waktu tertentu?
2. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan dalam periode yang dipilih?
""")

st.sidebar.header("Filter Tambahan (Dinamis)")

# Filter tanggal
if 'dteday' in df.columns:
    min_date = df['dteday'].min()
    max_date = df['dteday'].max()

    start_date, end_date = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date]
    )
else:
    start_date, end_date = None, None

# Filter musim
season_list = df['season'].unique().tolist()
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    season_list,
    default=season_list
)

# Filter cuaca
weather_list = df['weathersit'].unique().tolist()
selected_weather = st.sidebar.multiselect(
    "Pilih Cuaca",
    weather_list,
    default=weather_list
)

# Data dinamis final
filtered_df_dynamic = df.copy()

if start_date is not None:
    filtered_df_dynamic = filtered_df_dynamic[
        (filtered_df_dynamic['dteday'] >= pd.to_datetime(start_date)) &
        (filtered_df_dynamic['dteday'] <= pd.to_datetime(end_date))
    ]

filtered_df_dynamic = filtered_df_dynamic[
    filtered_df_dynamic['season'].isin(selected_season)
]

filtered_df_dynamic = filtered_df_dynamic[
    filtered_df_dynamic['weathersit'].isin(selected_weather)
]

# Visualisasi dinamis 1
st.subheader("Dynamic: Rata-rata Penyewaan per Musim")

season_dynamic = filtered_df_dynamic.groupby('season')['cnt'].mean().reset_index()

fig_dyn1, ax_dyn1 = plt.subplots()
sns.barplot(data=season_dynamic, x='season', y='cnt', ax=ax_dyn1)
st.pyplot(fig_dyn1)

# Visualisasi dinamis 2
st.subheader("Dynamic: Rata-rata Penyewaan per Cuaca")

weather_dynamic = filtered_df_dynamic.groupby('weathersit')['cnt'].mean().reset_index()

fig_dyn2, ax_dyn2 = plt.subplots()
sns.barplot(data=weather_dynamic, x='weathersit', y='cnt', ax=ax_dyn2)
st.pyplot(fig_dyn2)
