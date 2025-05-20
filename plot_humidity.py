import matplotlib.pyplot as plt
import pandas as pd

# קריאת הקובץ
df = pd.read_csv("temperature_log.csv")

# המרת עמודת הזמן לפורמט תאריך-שעה
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ציור הגרף
plt.figure(figsize=(14, 6))
plt.plot(df["timestamp"], df["humidity"], marker="o", linestyle="-", label="Humidity", color='blue')

# סימון חריגות (לחות < 35%)
alerts = df[df["humidity"] < 35]
plt.scatter(alerts["timestamp"], alerts["humidity"], color='red', label="Low Humidity Alert")

# הוספת טקסט 💧 על הנקודות החריגות
for i, row in alerts.iterrows():
    plt.text(row["timestamp"], row["humidity"] + 1, "💧", color='red', ha='center', fontsize=12)

# עיצוב הגרף
plt.xlabel("Time")
plt.ylabel("Humidity (%)")
plt.title("Humidity Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# שמירת הגרף
plt.savefig("humidity_chart.png")
plt.close()
