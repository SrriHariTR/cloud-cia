import logging
import json
import os

import azure.functions as func
from azure.data.tables import TableServiceClient

app = func.FunctionApp()


# =========================================================
# 1. IoT Hub → Event Hub → Process Telemetry
# =========================================================

@app.event_hub_message_trigger(
    arg_name="event",
    event_hub_name="iothub-ehub-smart-cold-56230012-7b5c5daa6f",
    connection="IOTHUB_CONNECTION",
    consumer_group="$Default"
)
def ProcessColdChainTelemetry(event: func.EventHubEvent):

    try:
        message = event.get_body().decode("utf-8")
        data = json.loads(message)

        device_id = data.get("device_id")
        timestamp = data.get("timestamp")
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        door_status = data.get("door_status")

        # Determine alert
        alerts = []

        if temperature < 2:
            alerts.append("TEMPERATURE_LOW")

        if temperature > 8:
            alerts.append("TEMPERATURE_HIGH")

        if door_status == "OPEN":
            alerts.append("DOOR_OPEN")

        alert = ",".join(alerts) if alerts else "NONE"

        logging.info("===================================")
        logging.info("Cold Chain Telemetry")
        logging.info("===================================")
        logging.info(f"Device ID    : {device_id}")
        logging.info(f"Temperature  : {temperature} °C")
        logging.info(f"Humidity     : {humidity} %")
        logging.info(f"Location     : {latitude}, {longitude}")
        logging.info(f"Door Status  : {door_status}")
        logging.info(f"Alert        : {alert}")

        # Connect to Table Storage
        connection_string = os.environ["TABLE_STORAGE_CONNECTION"]

        table_service = TableServiceClient.from_connection_string(
            connection_string
        )

        table_client = table_service.get_table_client(
            table_name="ColdChainTelemetry"
        )

        # Create table if necessary
        try:
            table_client.create_table()
        except Exception:
            pass

        # Create unique RowKey
        row_key = timestamp.replace(":", "").replace(".", "").replace("+", "")

        entity = {
            "PartitionKey": device_id,
            "RowKey": row_key,
            "device_id": device_id,
            "timestamp": timestamp,
            "temperature": temperature,
            "humidity": humidity,
            "latitude": latitude,
            "longitude": longitude,
            "door_status": door_status,
            "alert": alert
        }

        table_client.upsert_entity(entity)

        logging.info("Telemetry stored successfully.")
        logging.info("===================================")

    except Exception as e:
        logging.error(f"Error processing telemetry: {e}")


# =========================================================
# 2. HTTP API → Dashboard
# =========================================================

@app.route(
    route="telemetry",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def GetTelemetry(req: func.HttpRequest) -> func.HttpResponse:

    try:
        connection_string = os.environ["TABLE_STORAGE_CONNECTION"]

        table_service = TableServiceClient.from_connection_string(
            connection_string
        )

        table_client = table_service.get_table_client(
            table_name="ColdChainTelemetry"
        )

        telemetry = []

        entities = table_client.list_entities()

        for entity in entities:
            telemetry.append({
                "device_id": entity.get("device_id"),
                "timestamp": entity.get("timestamp"),
                "temperature": entity.get("temperature"),
                "humidity": entity.get("humidity"),
                "latitude": entity.get("latitude"),
                "longitude": entity.get("longitude"),
                "door_status": entity.get("door_status"),
                "alert": entity.get("alert")
            })

        # Latest records first
        telemetry.sort(
            key=lambda x: x["timestamp"] or "",
            reverse=True
        )

        return func.HttpResponse(
            json.dumps(telemetry),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:

        logging.error(f"Error reading telemetry: {e}")

        return func.HttpResponse(
            json.dumps({
                "error": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )