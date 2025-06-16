import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv("temperature_log.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Plot
plt.figure(figsize=(14, 6))
plt.plot(df["timestamp"], df["humidity"], marker="o", linestyle="-", label="Humidity", color='blue')

# Check if the latest humidity is still low
latest = df.iloc[-1]
if latest["humidity"] < 35:
    # Plot only the latest alert
    plt.scatter(latest["timestamp"], latest["humidity"], color='red', label="Low Humidity Alert")
    plt.text(latest["timestamp"], latest["humidity"] + 1, "💧", color='red', ha='center', fontsize=12)

# Styling
plt.xlabel("Time")
plt.ylabel("Humidity (%)")
plt.title("Humidity Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save
plt.savefig("humidity_chart.png")
plt.close()
