import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ... your existing code ...

# Compute mean and std dev from actual data
mean = df["temperature"].mean()
std_dev = df["temperature"].std()

st.subheader("Summary Statistics")
st.write(f"**Mean Temperature:** {mean:.2f} °C")
st.write(f"**Standard Deviation:** {std_dev:.2f}")

# Add normal distribution plot
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
