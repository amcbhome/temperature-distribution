import streamlit as st
import pandas as pd

st.set_page_config(page_title="Temperature Distribution Snapshot", layout="wide")

st.title("Normal Distribution Snapshot of IoT Data")

# GitHub raw CSV URL (replace with your actual repo and branch)
csv_url = "https://raw.githubusercontent.com/amcbhome/temperature-distribution/0420f5d3237f958c050c9a19b767b2f2e711b3dc/temperature_data.csv"

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

# Display mean and standard deviation
st.subheader("Summary Statistics")
st.write(f"**Mean Temperature:** {mean:.2f} °C")
st.write(f"**Standard Deviation:** {std_dev:.2f}")

# Empirical Rule display
st.subheader("Empirical Rule (68-95-99.7 Rule)")
st.markdown(
    f"""
    - **68%** of data falls within **1 standard deviation**:  
      [{mean - std_dev:.2f} °C, {mean + std_dev:.2f} °C]
    - **95%** of data falls within **2 standard deviations**:  
      [{mean - 2*std_dev:.2f} °C, {mean + 2*std_dev:.2f} °C]
    - **99.7%** of data falls within **3 standard deviations**:  
      [{mean - 3*std_dev:.2f} °C, {mean + 3*std_dev:.2f} °C]
    """
)

# Display how many data points are beyond 3 standard deviations
beyond_3_std = df[(df["temperature"] < mean - 3*std_dev) | (df["temperature"] > mean + 3*std_dev)]
count_beyond_3_std = beyond_3_std.shape[0]

st.subheader("Outliers Beyond 3 Standard Deviations")
st.write(f"**Data points beyond 3 standard deviations:** {count_beyond_3_std} out of {df.shape[0]}")
