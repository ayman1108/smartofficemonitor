import paho.mqtt.client as mqtt
import ssl
import time
import datetime
import random
import json

ENDPOINT = "azpmiseaxivxk-ats.iot.eu-north-1.amazonaws.com"
PORT = 8883
TOPIC = "office/temperature"
CLIENT_ID = "OfficeSensor1Publisher"

CA_PATH = "certs/AmazonRootCA1.pem"
CERT_PATH = "certs/OfficeSensor1.cert.pem"
KEY_PATH = "certs/OfficeSensor1.private.key"

is_connected = False

def on_connect(client, userdata, flags, rc):
    global is_connected
    if rc == 0:
        print("✅ Connected to AWS IoT Core successfully")
        is_connected = True
    else:
        print(f"❌ Failed to connect. Return code {rc}")

client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect

client.tls_set(
    ca_certs=CA_PATH,
    certfile=CERT_PATH,
    keyfile=KEY_PATH,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

client.connect(ENDPOINT, PORT)
client.loop_start()

print(f"🚀 Connecting to AWS IoT Core and publishing to '{TOPIC}'...")

# ✋ המתן לחיבור
while not is_connected:
    print("⏳ Waiting for connection...")
    time.sleep(1)

try:
    while True:
        payload = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "temp": round(random.uniform(22.0, 34.5), 2),
            "hum": round(random.uniform(30.0, 60.0), 2)
        }
        result = client.publish(TOPIC, json.dumps(payload))
        status = result[0]
        if status == 0:
            print("📤 Sent:", payload)
        else:
            print(f"⚠️ Failed to send message: {status}")
        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 Publisher stopped by user")
    client.loop_stop()
    client.disconnect()
