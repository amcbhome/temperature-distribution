import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.set_page_config(page_title="Temperature Distribution Snapshot", layout="wide")

st.title("Normal Distribution Snapshot of IoT Data")

# GitHub raw CSV URL (replace with your actual repo and branch)
csv_url = "https://raw.githubusercontent.com/amcbhome/temperature-distribution/0420f5d3237f958c050c9a19b767b2f2e711b3dc/temperature_data.csv"

try:
    df = pd.read_csv(csv_url)
    st.write("✅ Data loaded. Columns in CSV: ", df.columns.tolist())
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

if df.empty:
    st.warning("No data available yet.")
    st.stop()

if "temperature" not in df.columns:
    st.error("❌ 'temperature' column not found in the CSV file. Columns present: " + str(df.columns.tolist()))
    st.stop()

# Compute mean and std dev from actual data
mean = df["temperature"].mean()
std_dev = df["temperature"].std()
count = df["temperature"].count()
min_temp = df["temperature"].min()
max_temp = df["temperature"].max()
median_temp = df["temperature"].median()

# Display summary statistics, including the number of data points
st.subheader("Summary Statistics")
st.write(f"**Number of Data Points:** {count}")
st.write(f"**Mean Temperature:** {mean:.2f} °C")
st.write(f"**Median Temperature:** {median_temp:.2f} °C")
st.write(f"**Min Temperature:** {min_temp:.2f} °C")
st.write(f"**Max Temperature:** {max_temp:.2f} °C")
st.write(f"**Standard Deviation:** {std_dev:.2f}")

# Normal distribution plot
st.subheader("Normal Distribution Plot of Temperature Data")

fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(df["temperature"], kde=False, stat="density", bins=30, ax=ax, color="skyblue", label="Data Histogram")

# Plot the fitted normal curve
xmin, xmax = ax.get_xlim()
x = np.linspace(xmin, xmax, 100)
p = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-(x - mean)**2 / (2 * std_dev**2))
ax.plot(x, p, 'r', linewidth=2, label="Normal Curve (fit)")

ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("Density")
ax.set_title("Temperature Data & Fitted Normal Distribution")
ax.legend()

st.pyplot(fig)

# Compute and display skewness
skewness = df["temperature"].skew()
st.subheader("Skewness of Temperature Data")
st.write(f"**Skewness:** {skewness:.2f}")

if abs(skewness) < 0.5:
    st.info("The dataset is fairly symmetric (low skew).")
elif skewness > 0.5:
    st.info("The dataset is positively skewed (tail to the right).")
elif skewness < -0.5:
    st.info("The dataset is negatively skewed (tail to the left).")

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

# Display time stamps for readings within 3 standard deviations
within_3_std = df[(df["temperature"] >= mean - 3*std_dev) & (df["temperature"] <= mean + 3*std_dev)]

st.subheader("Time Stamps for Readings Within 3 Standard Deviations")
if "timestamp" in within_3_std.columns:
    st.dataframe(within_3_std[["timestamp", "temperature"]])
else:
    st.info("No 'timestamp' column found in the data.")
