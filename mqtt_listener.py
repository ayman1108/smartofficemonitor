import paho.mqtt.client as mqtt
import json
from collections import deque

# יצירת תור (Buffer) עם מקסימום 300 רשומות אחרונות
data_buffer = deque(maxlen=300)

# פונקציה שמופעלת בעת קבלת הודעה ב-MQTT
def on_message(client, userdata, msg):
    try:
        # פירוק ה-Payload מההודעה
        payload = json.loads(msg.payload.decode())

        # שליפת שדות מה-JSON
        timestamp = payload.get("timestamp")
        temp = payload.get("temp")
        hum = payload.get("hum")

        # בדיקה אם כל השדות קיימים
        if timestamp and temp is not None and hum is not None:
            # הוספת הנתונים לתור
            data_point = {
                "timestamp": timestamp,
                "temperature": temp,
                "humidity": hum
            }
            data_buffer.append(data_point)

            # ✅ בדיקות חריגות
            if temp > 30:
                print(f"🚨 High Temperature Alert: {temp}°C at {timestamp}")
            if hum < 35:
                print(f"💧 Low Humidity Alert: {hum}% at {timestamp}")

            # הדפסת נתונים שהתקבלו
            print("✅ Received:", data_point)
        else:
            print("⚠️ Missing fields in payload:", payload)

    except Exception as e:
        print("❌ Failed to parse message:", e)

# פונקציה שמפעילה את הלקוח MQTT ומחזירה את התור
def start_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883)  # כתובת ה-broker (לוקאלי)
    client.subscribe("sensors/environment")  # שם ה-Topic
    client.loop_start()
    print("🚀 MQTT Listener started and subscribed to 'sensors/environment'")
    return client, data_buffer
