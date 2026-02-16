import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Bike Sharing Dashboard")

df = pd.read_csv("dashboard/main_data.csv")

st.subheader("Rata-rata Penyewaan Berdasarkan Musim")
season_avg = df.groupby("season")["cnt"].mean().sort_values(ascending=False)

fig1, ax1 = plt.subplots()
sns.barplot(x=season_avg.index, y=season_avg.values, ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
weather_avg = df.groupby("weathersit")["cnt"].mean().sort_values(ascending=False)

fig2, ax2 = plt.subplots()
sns.barplot(x=weather_avg.index, y=weather_avg.values, ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)
