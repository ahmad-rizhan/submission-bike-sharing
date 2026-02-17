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

if 'dteday' in df.columns:
    df['dteday'] = pd.to_datetime(df['dteday'])

year_map = {0: 2011, 1: 2012}

# =============================
# SIDEBAR FILTER
# =============================
st.sidebar.header("Filter Data")

# Tahun
selected_year_label = st.sidebar.selectbox(
    "Pilih Tahun",
    options=list(year_map.values())
)

selected_year_code = [k for k, v in year_map.items() if v == selected_year_label][0]

# Tanggal
if 'dteday' in df.columns:
    min_date = df['dteday'].min()
    max_date = df['dteday'].max()

    start_date, end_date = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date]
    )
else:
    start_date, end_date = None, None

# Musim
season_list = df['season'].unique().tolist()
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    season_list,
    default=season_list
)

# Cuaca
weather_list = df['weathersit'].unique().tolist()
selected_weather = st.sidebar.multiselect(
    "Pilih Cuaca",
    weather_list,
    default=weather_list
)

# =============================
# FILTER DATA
# =============================
filtered_df = df.copy()

filtered_df = filtered_df[filtered_df['yr'] == selected_year_code]

if start_date is not None:
    filtered_df = filtered_df[
        (filtered_df['dteday'] >= pd.to_datetime(start_date)) &
        (filtered_df['dteday'] <= pd.to_datetime(end_date))
    ]

filtered_df = filtered_df[
    filtered_df['season'].isin(selected_season)
]

filtered_df = filtered_df[
    filtered_df['weathersit'].isin(selected_weather)
]

st.subheader(f"Analisis Tahun {selected_year_label}")

# =============================
# CEK DATA KOSONG
# =============================
if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih. Silakan ubah filter.")
else:

    # =============================
    # VISUALISASI 1
    # =============================
    season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()

    fig1, ax1 = plt.subplots(figsize=(6,4))
    sns.barplot(data=season_avg, x='season', y='cnt', color='steelblue', ax=ax1)
    ax1.set_title("Rata-rata Penyewaan Sepeda per Musim")
    st.pyplot(fig1)

    # =============================
    # VISUALISASI 2
    # =============================
    weather_avg = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(6,4))
    sns.barplot(data=weather_avg, x='weathersit', y='cnt', color='steelblue', ax=ax2)
    ax2.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
    st.pyplot(fig2)

    # =============================
    # VISUALISASI 3
    # =============================
    if 'dteday' in filtered_df.columns:
        trend_data = filtered_df.sort_values('dteday')

        fig3, ax3 = plt.subplots(figsize=(8,4))
        ax3.plot(trend_data['dteday'], trend_data['cnt'])
        ax3.set_title("Tren Penyewaan Harian")
        st.pyplot(fig3)

    # =============================
    # VISUALISASI 4 (AMAN)
    # =============================
    if not filtered_df['temp'].empty:
        filtered_df['temp_category'] = pd.cut(
            filtered_df['temp'],
            bins=3,
            labels=['Low', 'Medium', 'High']
        )

        temp_avg = filtered_df.groupby('temp_category')['cnt'].mean().reset_index()

        fig4, ax4 = plt.subplots(figsize=(6,4))
        sns.barplot(data=temp_avg, x='temp_category', y='cnt', color='steelblue', ax=ax4)
        ax4.set_title("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
        st.pyplot(fig4)

# =============================
# KESIMPULAN
# =============================
st.header("Kesimpulan")

st.markdown("""
Dashboard bersifat dinamis dan seluruh visualisasi akan berubah sesuai filter tahun, tanggal, musim, dan cuaca.
Jika filter menghasilkan data kosong, sistem akan menampilkan peringatan.
""")
