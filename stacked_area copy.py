import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from datetime import datetime

# Load the data
df = pd.read_excel('weights.xlsx')
df['Date'] = pd.to_datetime(df['Date'])

st.title('Asset Class Weights Dashboard')

# Month and year selection
st.sidebar.header("Select Date Range")

months = list(range(1, 13))
years = sorted(list(set(df['Date'].dt.year)))

start_year = st.sidebar.selectbox("Start Year", years, index=0)
start_month = st.sidebar.selectbox("Start Month", months, index=0)
end_year = st.sidebar.selectbox("End Year", years, index=len(years)-1)
end_month = st.sidebar.selectbox("End Month", months, index=11)

user_start = datetime(start_year, start_month, 1)
user_end = datetime(end_year, end_month, 28)  # using 28 for safety across months

# Filter data
mask = (df['Date'] >= user_start) & (df['Date'] <= user_end)
df_filtered = df.loc[mask]

classes = ['Public Equity','Hedge Funds','Private Equity','Real Assets','Fixed Income','Cash']
df_plot = df_filtered.set_index('Date')[classes] * 100
dates = df_plot.index
data = [df_plot[asset].values for asset in classes]

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.stackplot(dates, *data, labels=classes, alpha=0.8)
ax.axhline(0, color='black', linewidth=1, linestyle='--')
ax.set_ylabel("Weight (%)")
ax.set_xlabel("Date")
ax.set_title("Asset Class Weights Over Time (Stacked Area, Percentages)")
ax.legend(loc='upper right')
ax.yaxis.set_major_formatter(PercentFormatter())
plt.tight_layout()

st.pyplot(fig)
