import json
import random
import time
import json
import random
import time
import os
from datetime import datetime, timezone
from azure.iot.device import IoTHubDeviceClient, Message

# ==========================================
# AZURE CONFIGURATION
# ==========================================
CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
DEVICE_ID = "COLDCHAIN_001"


# ==========================================
# INITIAL GPS LOCATION
# ==========================================

latitude = 13.0827
longitude = 80.2707


# ==========================================
# INITIAL SENSOR VALUES
# ==========================================

temperature = 5.0
humidity = 60.0
door_status = "CLOSED"


# ==========================================
# CONNECT TO AZURE IOT HUB
# ==========================================

client = IoTHubDeviceClient.create_from_connection_string(
    CONNECTION_STRING
)

client.connect()

print("Connected to Azure IoT Hub")
print("Device:", DEVICE_ID)
print()


# ==========================================
# SIMULATE SENSORS
# ==========================================

try:

    while True:

        # Temperature
        temperature += random.uniform(-0.3, 0.3)

        # Humidity
        humidity += random.uniform(-1.0, 1.0)

        # GPS movement
        latitude += random.uniform(-0.0005, 0.0005)
        longitude += random.uniform(-0.0005, 0.0005)

        # Door status
        if random.random() < 0.05:
            door_status = "OPEN"
        else:
            door_status = "CLOSED"

        # Keep values realistic
        temperature = max(0, min(12, temperature))
        humidity = max(30, min(90, humidity))


        # ==========================================
        # CREATE TELEMETRY
        # ==========================================

        data = {
            "device_id": DEVICE_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "latitude": round(latitude, 6),
            "longitude": round(longitude, 6),
            "door_status": door_status
        }


        # Convert to JSON
        payload = json.dumps(data)


        # ==========================================
        # SEND MESSAGE
        # ==========================================

        message = Message(payload)

        message.content_type = "application/json"
        message.content_encoding = "utf-8"

        client.send_message(message)


        # ==========================================
        # DISPLAY
        # ==========================================

        print("Telemetry sent:")
        print(payload)
        print("-" * 60)


        # Wait 5 seconds
        time.sleep(5)


except KeyboardInterrupt:

    print("\nStopping simulator...")


finally:

    client.shutdown()

    print("Disconnected from Azure IoT Hub")