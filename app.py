from flask import Flask, render_template_string, send_file
from datetime import datetime
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from mqtt_listener import start_mqtt

# הפעלת ה-MQTT listener וקבלת התור (buffer)
mqtt_client, data_buffer = start_mqtt()

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Environment Dashboard</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body { font-family: Arial; text-align: center; margin: 40px; }
        img { width: 80%%; max-width: 800px; border: 1px solid #ccc; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); }
        .tabs { margin-bottom: 20px; }
        .tabs a {
            display: inline-block;
            margin: 0 10px;
            padding: 8px 16px;
            background-color: #f0f0f0;
            text-decoration: none;
            color: black;
            border-radius: 5px;
        }
        .tabs a.active {
            background-color: #007BFF;
            color: white;
        }
    </style>
</head>
<body>
    <h1>Live Environment Dashboard</h1>
    <div class="tabs">
        <a href="/" class="{{ 'active' if chart_type == 'temperature' else '' }}">Temperature</a>
        <a href="/humidity" class="{{ 'active' if chart_type == 'humidity' else '' }}">Humidity</a>
    </div>
    <img src="{{ chart_src }}" alt="Chart">
    <p><small>Refreshing every 10 seconds...</small></p>
</body>
</html>
"""

@app.route("/")
def temperature_index():
    return render_template_string(HTML_TEMPLATE, chart_type="temperature", chart_src="/chart.png")

@app.route("/humidity")
def humidity_index():
    return render_template_string(HTML_TEMPLATE, chart_type="humidity", chart_src="/humidity_chart.png")

@app.route("/chart.png")
def chart():
    timestamps = []
    temperatures = []
    for row in list(data_buffer):
        try:
            timestamps.append(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
            temperatures.append(float(row["temperature"]))
        except:
            continue

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temperatures, marker='o', linestyle='-')
    plt.title("Temperature Over Time")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

@app.route("/humidity_chart.png")
def humidity_chart():
    timestamps = []
    humidities = []
    for row in list(data_buffer):
        try:
            timestamps.append(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
            humidities.append(float(row["humidity"]))
        except:
            continue

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, humidities, marker='o', linestyle='-', color='green')
    plt.title("Humidity Over Time")
    plt.xlabel("Time")
    plt.ylabel("Humidity (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
