import csv
from datetime import datetime
import matplotlib.pyplot as plt

timestamps = []
temperatures = []

# Read from CSV
with open("temperature_log.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        timestamps.append(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
        temperatures.append(float(row["temperature"]))

# Plot base line
plt.figure(figsize=(10, 5))
plt.plot(timestamps, temperatures, marker='o', linestyle='-', color='blue', label="Temperature")

# Check latest value only
latest_temp = temperatures[-1]
latest_time = timestamps[-1]

print(f"בדיקה: temp={latest_temp}")
if latest_temp > 30:
    print(f"🔥 סימון חריגה: temp={latest_temp} בזמן {latest_time}")
    plt.plot(latest_time, latest_temp, marker='o', color='red')
    plt.text(latest_time, latest_temp + 0.5, "🔥", color='red', ha='center', fontsize=12)

# Styling
plt.title("Temperature Over Time")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
plt.savefig("temperature_chart.png")
plt.close()

print("✅ Graph saved as temperature_chart.png with conditional alert")
