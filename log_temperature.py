import csv
import json
from datetime import datetime
import paho.mqtt.client as mqtt

CSV_FILENAME = "temperature_log.csv"

def log_to_csv(temp, hum):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILENAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([now, temp, hum])
        print(f"[{now}] Logged temperature: {temp}°C, humidity: {hum}%")

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    log_to_csv(data["temperature"], data["humidity"])

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("office/temperature")

MQTT_BROKER = "localhost"
MQTT_PORT = 1883

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# יצירת קובץ CSV עם כותרות אם לא קיים
try:
    with open(CSV_FILENAME, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature", "humidity"])
        print("Created CSV file with headers.")
except FileExistsError:
    print("CSV already exists. Appending...")

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()
