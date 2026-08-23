# 🌡️ Smart Cold Chain Monitoring System

An IoT-based **Smart Cold Chain Monitoring System** for real-time monitoring of temperature-sensitive goods during transportation and storage.

The system collects **temperature, humidity, door status, and GPS location** data from a simulated cold-chain device, sends the telemetry to **Azure IoT Hub**, processes the data in the cloud, and displays the latest information on a web dashboard.

---

## 🚀 Features

- 🌡️ Real-time temperature monitoring
- 💧 Humidity monitoring
- 🚪 Door status monitoring
- 📍 GPS location tracking
- ☁️ Microsoft Azure IoT Hub integration
- 📊 Real-time web dashboard
- 🚨 Temperature anomaly alerts
- 📡 Continuous IoT telemetry
- 🔐 Environment-based secret management
- 📦 Device-based telemetry identification

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │   Cold Chain Device     │
                    │                         │
                    │  Temperature            │
                    │  Humidity               │
                    │  Door Status            │
                    │  GPS Location           │
                    └────────────┬────────────┘
                                 │
                                 │ Telemetry
                                 ▼
                    ┌─────────────────────────┐
                    │     Azure IoT Hub       │
                    │                         │
                    │   COLDCHAIN_001         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Azure Functions      │
                    │                         │
                    │  Data Processing        │
                    │  Alert Detection        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Web Dashboard       │
                    │                         │
                    │ Temperature             │
                    │ Humidity                │
                    │ Door Status             │
                    │ GPS Location            │
                    │ Alerts                  │
                    └─────────────────────────┘
```

# Smart Cold Chain Monitoring System 🚚❄️

A cloud-connected IoT monitoring platform designed for cold-chain logistics, providing real-time visibility of environmental conditions, door status, and shipment location. The system continuously processes sensor telemetry via Azure cloud services to identify abnormal conditions early and ensure the safety of temperature-sensitive cargo.

---

## 🛠️ Technology Stack

* **IoT & Simulation:** Python, Azure IoT Device SDK (`azure-iot-device`), Simulated JSON Telemetry
* **Cloud & Processing:** Microsoft Azure IoT Hub, Azure Functions, Azure Event Hub-compatible endpoints, Azure Storage
* **Frontend:** React.js, JavaScript, HTML5, CSS3, Vite

---

## 📁 Project Structure

```text
smart-cold-chain/
│
├── backend/
│   ├── function_app.py
│   ├── requirements.txt
│   └── simulator/
│       └── sensor_simulator.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

## 📡 IoT Device & Telemetry
The platform uses a simulated IoT device (COLDCHAIN_001) that continuously publishes JSON telemetry payloads to Azure IoT Hub.

Telemetry Payload Schema

```text
{
  "device_id": "COLDCHAIN_001",
  "timestamp": "2026-08-23T10:30:00+00:00",
  "temperature": 5.42,
  "humidity": 63.21,
  "latitude": 13.0827,
  "longitude": 80.2707,
  "door_status": "CLOSED"
}
```

## Monitored Sensor Attributes
Temperature: Dynamic range between 0.0°C and 12.0°C.

Humidity: Dynamic range between 30% and 90%.

Door Status: Binary status (OPEN or CLOSED).

GPS Location: Dynamic latitude and longitude updating to simulate continuous transit.

## 🔄 System Architecture & Data Flow
```text
┌──────────────────┐      ┌───────────────┐      ┌─────────────────┐
│ Sensor Simulator ├────► │ Azure IoT Hub ├────► │ Azure Functions │
└──────────────────┘      └───────────────┘      └────────┬────────┘
                                                          │ Validate & Detect
                                                          ▼
┌──────────────────┐                             ┌─────────────────┐
│  Web Dashboard   │ ◄───────────────────────────┤  Alert System   │
└──────────────────┘     Real-Time Monitoring    └─────────────────┘

```

Telemetry Generation: sensor_simulator.py simulates sensor state variations.

Ingestion: Telemetry is transmitted over MQTT/HTTPS to Azure IoT Hub.

Processing & Validation: Azure Functions ingests the Event Hub-compatible stream to validate values against configured thresholds.

Alert Generation: Flags anomalies (TEMPERATURE_HIGH, HUMIDITY_LOW, DOOR_OPEN).

Visualization: Dashboard surfaces telemetry metrics, GPS location, and active alerts.

## 🚨 Alert System
The system evaluates incoming data frames and raises automated flags for out-of-bound conditions:

TEMPERATURE_HIGH / TEMPERATURE_LOW

HUMIDITY_HIGH / HUMIDITY_LOW

DOOR_OPEN

## 🔐 Security & Best Practices
Never hardcode credentials or IoT Hub connection strings in source files. Always use environment variables.

Local Environment Setup
Windows PowerShell:

PowerShell
$env:IOTHUB_DEVICE_CONNECTION_STRING="HostName=...;DeviceId=COLDCHAIN_001;SharedAccessKey=..."
Linux / macOS:

Bash
export IOTHUB_DEVICE_CONNECTION_STRING="HostName=...;DeviceId=COLDCHAIN_001;SharedAccessKey=..."
Mandatory .gitignore Configuration
Ensure your .gitignore includes the following entries:

Code snippet
# Environment variables
.env
.env.*
!.env.example

# Python cache & environments
__pycache__/
*.pyc
*.pyo
venv/
.venv/

# Node dependencies & builds
node_modules/
dist/
build/

## 📦 Getting Started
1. Backend & Simulator Setup
Navigate to the backend directory and set up your Python environment:

```text
Bash
cd backend
pip install -r requirements.txt
```
Set your environment variable (as shown in the Security section) and execute the simulator:

```text
Bash
python simulator/sensor_simulator.py
```
Expected Console Output:

```text
Plaintext
Connected to Azure IoT Hub
Device: COLDCHAIN_001
```

Telemetry sent:
```text
{
    "device_id": "COLDCHAIN_001",
    "timestamp": "2026-08-23T10:30:00+00:00",
    "temperature": 5.42,
    "humidity": 63.21,
    "latitude": 13.0827,
    "longitude": 80.2707,
    "door_status": "CLOSED"
}
```
------------------------------------------------------------
2. Frontend Setup
Navigate to the frontend directory, install dependencies, and start the development server:

```text
Bash
cd frontend
npm install
npm run dev
```

🖥️ Dashboard Interface
```text
Plaintext
┌──────────────────────────────────────────────┐
│         SMART COLD CHAIN DASHBOARD           │
├──────────────────────────────────────────────┤
│                                              │
│  🌡 Temperature       8.49 °C                │
│                                              │
│  💧 Humidity          64.44 %                │
│                                              │
│  🚪 Door              CLOSED                 │
│                                              │
│  🚨 Alert             TEMPERATURE_HIGH       │
│                                              │
│  📍 Location                                 │
│     Latitude          13.079111              │
│     Longitude         80.272223              │
│                                              │
└──────────────────────────────────────────────┘
```

## 🎯 Targeted Use Cases
💊 Pharmaceuticals & Vaccines: Temperature-controlled medical storage.

🥛 Dairy & Food Logistics: Preservation of perishable food supplies.

🚚 Fleet Management: Continuous environmental and geographical tracking in transit.

🔮 Future Enhancements
[ ] Live Map Integration: Render interactive real-time vehicle routes using Leaflet or Azure Maps.

[ ] Predictive Analytics: ML-based anomaly detection for predicting potential temperature spikes before they occur.

[ ] Multi-Device Support: Expand telemetry management to support fleet-wide multi-vehicle monitoring.

[ ] Automated Notifications: SMS and Email dispatch via Azure Communication Services / SendGrid upon critical alerts.
