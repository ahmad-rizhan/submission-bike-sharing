# ==========================================================
# =============== FINAL REVISION (DINAMIS) =================
# ==========================================================

st.header("Business Questions & Dynamic Analysis")

st.markdown("""
### Business Questions:
1. Musim apa yang memiliki rata-rata penyewaan tertinggi pada rentang waktu tertentu?
2. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan dalam periode yang dipilih?
""")

# =============================
# FILTER TAMBAHAN (Tanggal, Musim, Cuaca)
# =============================

st.sidebar.header("Filter Lanjutan")

# Pastikan kolom tanggal dalam format datetime
if 'dteday' in df.columns:
    df['dteday'] = pd.to_datetime(df['dteday'])

    min_date = df['dteday'].min()
    max_date = df['dteday'].max()

    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range)
    else:
        start_date, end_date = min_date, max_date
else:
    start_date, end_date = None, None


# Filter musim
season_options = df['season'].unique().tolist()
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=season_options,
    default=season_options
)

# Filter cuaca
weather_options = df['weathersit'].unique().tolist()
selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=weather_options,
    default=weather_options
)

# =============================
# FILTER FINAL DATAFRAME
# =============================

filtered_df_final = df.copy()

if start_date is not None:
    filtered_df_final = filtered_df_final[
        (filtered_df_final['dteday'] >= start_date) &
        (filtered_df_final['dteday'] <= end_date)
    ]

filtered_df_final = filtered_df_final[
    (filtered_df_final['season'].isin(selected_season)) &
    (filtered_df_final['weathersit'].isin(selected_weather))
]

# =============================
# VISUALISASI BISNIS 1 (DINAMIS)
# Rata-rata Penyewaan per Musim
# =============================

st.subheader("Dynamic Analysis: Penyewaan per Musim")

season_dynamic = filtered_df_final.groupby('season')['cnt'].mean().reset_index()

fig_dyn1, ax_dyn1 = plt.subplots(figsize=(6,4))
sns.barplot(data=season_dynamic, x='season', y='cnt', ax=ax_dyn1)
ax_dyn1.set_title("Rata-rata Penyewaan per Musim (Dinamis)")
ax_dyn1.set_xlabel("Musim")
ax_dyn1.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig_dyn1)


# =============================
# VISUALISASI BISNIS 2 (DINAMIS)
# Rata-rata Penyewaan per Cuaca
# =============================

st.subheader("Dynamic Analysis: Penyewaan berdasarkan Cuaca")

weather_dynamic = filtered_df_final.groupby('weathersit')['cnt'].mean().reset_index()

fig_dyn2, ax_dyn2 = plt.subplots(figsize=(6,4))
sns.barplot(data=weather_dynamic, x='weathersit', y='cnt', ax=ax_dyn2)
ax_dyn2.set_title("Rata-rata Penyewaan berdasarkan Cuaca (Dinamis)")
ax_dyn2.set_xlabel("Kondisi Cuaca")
ax_dyn2.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig_dyn2)


# =============================
# METRIK DINAMIS BERDASARKAN FILTER
# =============================

st.subheader("Ringkasan Berdasarkan Filter")

total_dynamic = filtered_df_final['cnt'].sum()
avg_dynamic = filtered_df_final['cnt'].mean()

colA, colB = st.columns(2)
colA.metric("Total Penyewaan (Filtered)", f"{total_dynamic:,.0f}")
colB.metric("Rata-rata Penyewaan (Filtered)", f"{avg_dynamic:,.0f}")
