# Smart Office Environment Monitor 🌡️💨

This project simulates a smart office environment monitoring system using virtual sensors for temperature and humidity. It utilizes AWS IoT Core for MQTT communication, Lambda for processing, DynamoDB for storage, and a Flask web server to visualize live sensor data.

## 📁 Project Structure


---

## 🚀 How to Start the Program

### 1. 🔒 Set Up AWS IoT Certificates
Ensure you have the following certificates in the `certs/` folder:
- `AmazonRootCA1.pem`
- `YourDevice.cert.pem`
- `YourDevice.private.key`

Make sure the names in `mqtt_publisher.py` and `mqtt_listener.py` match your files.

---

### 2. 📡 Start the MQTT Listener (Subscriber)

In one terminal, run:
```bash
python mqtt_listener.py
3. 🌐 Start the Flask Dashboard

python app.py
4. 🌡️ Start the Sensor Publisher

python mqtt_publisher.py

✅ Output Example
📤 Sent: {"timestamp": "2025-06-16 14:45:21", "temp": 28.5, "hum": 44.2}
📤 Sent: {"timestamp": "2025-06-16 14:45:26", "temp": 29.1, "hum": 40.9}

📊 Optional: Offline Temperature Plot
python plot_temperature.py

📎 Related AWS Services

AWS IoT Core
AWS Lambda
Amazon DynamoDB
Amazon CloudWatch


🧠 Authors

Alaa Bargita – 322566027
ayman Omer – 20807212


