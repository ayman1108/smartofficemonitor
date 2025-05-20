import csv
from datetime import datetime
import matplotlib.pyplot as plt

timestamps = []
temperatures = []

# קריאת נתונים מקובץ CSV
with open("temperature_log.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        timestamps.append(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
        temperatures.append(float(row["temperature"]))

# ציור הגרף
plt.figure(figsize=(10, 5))
plt.plot(timestamps, temperatures, marker='o', linestyle='-', color='blue', label="Temperature")

# סימון חריגות
for i, temp in enumerate(temperatures):
    print(f"בדיקה: temp={temp}")
    if temp > 0:
        print(f"סימון חריגה: temp={temp} בזמן {timestamps[i]}")
        plt.plot(timestamps[i], temp, marker='o', color='red')
        plt.text(timestamps[i], temp + 0.5, "🔥", color='red', ha='center', fontsize=12)


# עיצוב הגרף
plt.title("Temperature Over Time")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# שמירת גרף לתמונה
plt.savefig("temperature_chart.png")
plt.close()

print("✅ Graph saved as temperature_chart.png with alerts")

