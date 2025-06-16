import paho.mqtt.client as mqtt
import json
from collections import deque
import ssl

# ===== AWS IoT Core Configuration =====
ENDPOINT = "azpmiseaxivxk-ats.iot.eu-north-1.amazonaws.com"
PORT = 8883
TOPIC = "office/temperature"
CLIENT_ID = "OfficeSensor1Subscriber"

# ===== Certificate Files =====
CA_PATH = "certs/AmazonRootCA1.pem"
CERT_PATH = "certs/OfficeSensor1.cert.pem"
KEY_PATH = "certs/OfficeSensor1.private.key"

# ===== Shared Message Buffer =====
data_buffer = deque(maxlen=300)

# Internal state to prevent duplicate subscriptions
_connected_once = False

def on_message(client, userdata, msg):
    try:
        print("📥 Raw message received:", msg.payload.decode())
        payload = json.loads(msg.payload.decode())
        timestamp = payload.get("timestamp")
        temp = payload.get("temp")
        hum = payload.get("hum")

        if timestamp and temp is not None and hum is not None:
            data_point = {
                "timestamp": timestamp,
                "temperature": temp,
                "humidity": hum
            }
            data_buffer.append(data_point)
            print("📊 Buffer size:", len(data_buffer))


            if temp > 30:
                print(f"🚨 High Temperature Alert: {temp}°C at {timestamp}")
            if hum < 35:
                print(f"💧 Low Humidity Alert: {hum}% at {timestamp}")

            print("✅ Received:", data_point)
        else:
            print("⚠️ Missing fields in payload:", payload)

    except Exception as e:
        print("❌ Failed to parse message:", e)


def on_connect(client, userdata, flags, rc):
    global _connected_once
    if rc == 0 and not _connected_once:
        print("🔌 Connected with code", rc)
        client.subscribe(TOPIC)
        print(f"📡 Subscribed to topic: '{TOPIC}'")
        _connected_once = True
    elif rc != 0:
        print("❌ Connection failed with code", rc)


def start_mqtt():
    client = mqtt.Client(client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_set(
        ca_certs=CA_PATH,
        certfile=CERT_PATH,
        keyfile=KEY_PATH,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )

    client.connect(ENDPOINT, PORT)
    print(f"🚀 MQTT Listener connecting to AWS IoT Core at {ENDPOINT}:{PORT}...")
    client.loop_start()  # <-- loop_forever blocks; loop_start is non-blocking
    return client, data_buffer


# Optional: allow running as standalone script for testing
if __name__ == "__main__":
    client, _ = start_mqtt()
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Shutting down MQTT client.")
        client.loop_stop()
        client.disconnect()
