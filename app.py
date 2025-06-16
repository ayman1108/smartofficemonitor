import os
from flask import Flask, jsonify, render_template_string, request
from collections import deque

# Correctly import shared buffer from mqtt_listener
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    from mqtt_listener import start_mqtt
    mqtt_client, data_buffer = start_mqtt()
else:
    from mqtt_listener import data_buffer  # share buffer without reinitializing MQTT
app = Flask(__name__)


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Live Environment Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; margin: 40px; }
    #plotly-chart { width: 90%%; max-width: 1000px; margin: auto; }
    #alert {
      background-color: rgba(255, 0, 0, 0.75);
      color: white;
      padding: 10px 20px;
      border-radius: 5px;
      font-size: 18px;
      font-weight: bold;
      display: none;
      margin: 10px auto;
      width: fit-content;
    }
    .tabs {
      margin-bottom: 20px;
    }
    .tabs button {
      padding: 10px 20px;
      margin: 0 10px;
      font-size: 16px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    .tabs .active {
      background-color: #007BFF;
      color: white;
    }
    .tabs .inactive {
      background-color: #f0f0f0;
      color: black;
    }
  </style>
</head>
<body>
  <h1>Live Environment Dashboard</h1>
  <div class="tabs">
    <button id="btn-temp" class="active" onclick="switchTab('temperature')">Temperature</button>
    <button id="btn-humid" class="inactive" onclick="switchTab('humidity')">Humidity</button>
  </div>
  <div id="alert"></div>
  <div id="plotly-chart"></div>
  <p>Refreshing every 10 seconds...</p>

  <script>
    let currentTab = "temperature";

    function refreshPlot() {
      fetch("/api/data/" + currentTab)
        .then(res => res.json())
        .then(data => {
          const trace = {
            x: data.timestamps,
            y: data.values,
            mode: 'lines+markers',
            type: 'scatter',
            line: { color: currentTab === 'temperature' ? 'blue' : 'green' }
          };
          const layout = {
            title: (currentTab === "temperature" ? "Temperature" : "Humidity") + " Over Time",
            xaxis: { title: "Time" },
            yaxis: { title: currentTab === "temperature" ? "Temperature (°C)" : "Humidity (%)" }
          };
          Plotly.newPlot('plotly-chart', [trace], layout);
        });
    }

    function refreshAlert() {
      const alertDiv = document.getElementById("alert");

      fetch("/alert?tab=" + currentTab)
        .then(response => response.json())
        .then(data => {
          if (data.alert && data.alert !== "") {
            alertDiv.textContent = data.alert;
            alertDiv.style.display = "block";
          } else {
            alertDiv.style.display = "none";
          }
        });
    }

    function switchTab(tab) {
      currentTab = tab;
      refreshPlot();
      refreshAlert();
      document.getElementById("btn-temp").className = (tab === "temperature") ? "active" : "inactive";
      document.getElementById("btn-humid").className = (tab === "humidity") ? "active" : "inactive";
    }

    window.onload = function () {
      refreshPlot();
      refreshAlert();
      setInterval(refreshPlot, 10000);
      setInterval(refreshAlert, 5000);
    };
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route("/alert")
def alert():
    tab = request.args.get("tab", "temperature")
    try:
        last_row = list(data_buffer)[-1]
        if tab == "temperature":
            temp = float(last_row["temperature"])
            if temp > 30:
                return jsonify({"alert": "⚠️ טמפרטורה גבוהה! הפעלת מאוורר."})
        elif tab == "humidity":
            humidity = float(last_row["humidity"])
            if humidity < 35 or humidity > 55:
                return jsonify({"alert": "💧 לחות חריגה! פתח חלון או הפעל יבשן."})
    except:
        pass
    return jsonify({"alert": ""})


@app.route("/api/data/<string:data_type>")
def get_data(data_type):
    timestamps, values = [], []
    key = "temperature" if data_type == "temperature" else "humidity"
    for row in list(data_buffer):
        try:
            timestamps.append(row["timestamp"])
            values.append(float(row[key]))
        except:
            continue
    return jsonify({"timestamps": timestamps, "values": values})

if __name__ == "__main__":
    app.run(debug=True)
