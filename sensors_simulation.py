import time
import random
import json
from datetime import datetime
import paho.mqtt.client as mqtt

# יצירת לקוח MQTT
client = mqtt.Client()
client.connect("localhost", 1883)

# שליחת נתונים כל 5 שניות
while True:
    # יצירת נתוני טמפ' ולחות רנדומליים
    temp = round(random.uniform(20.0, 30.0), 2)
    hum = round(random.uniform(30.0, 60.0), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # יצירת הודעה בפורמט JSON מתאים
    payload = {
        "timestamp": timestamp,
        "temp": temp,
        "hum": hum
    }

    # המרה למחרוזת JSON ושליחה ל־MQTT
    message = json.dumps(payload)
    client.publish("sensors/environment", message)
    print("📤 Sent:", message)

    time.sleep(5)
