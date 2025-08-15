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
