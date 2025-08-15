import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

st.set_page_config(page_title="Temperature Distribution Snapshot", layout="wide")

st.title("Normal Distribution Snapshot of IoT Data")

# Auto-refresh every 30 seconds
# st_autorefresh = st.experimental_rerun  # old approach, replaced with this:
st_autorefresh = st.autorefresh(interval=30_000, key="data_refresh")

# GitHub raw CSV URL (replace with your actual repo and branch)
csv_url = "https://raw.githubusercontent.com/amcbhome/temperature-distribution/main/temperature_data.csv"

try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

if df.empty:
    st.warning("No data available yet.")
    st.stop()

# Compute mean and std dev from actual data
mean = df["temperature"].mean()
std_dev = df["temperature"].std()

# Create normal curve
x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
y = norm.pdf(x, mean, std_dev)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, color='black', linewidth=2, label='Normal Distribution')

# Shade 95% range
lower_bound = mean - 2*std_dev
upper_bound = mean + 2*std_dev
x_fill = np.linspace(lower_bound, upper_bound, 500)
ax.fill_between(x_fill, norm.pdf(x_fill, mean, std_dev),
                alpha=0.3, color='lightgreen', label='95% range')

# Plot actual data points
temps = df["temperature"].values
y_points = norm.pdf(temps, mean, std_dev)
ax.scatter(temps, y_points, color='red', zorder=5, label='Data points')

# Labels
ax.set_title("Temperature Distribution Snapshot", fontsize=16)
ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("Probability Density")
ax.legend()
ax.grid(True)

st.pyplot(fig)
