
from asaase_sense.ingestion.client import get_client
from asaase_sense.ingestion.sensors import get_african_sensors


def get_measurements(sensor_id: int) -> list[dict]:

    measurements = []
    page = 1
    limit = 1000

    with get_client() as client:

        while True:
            response = client.get(f"/sensors/{sensor_id}/measurements",params={"limit": limit,"page": page})

            response.raise_for_status()

            data = response.json()

            results = data["results"]

            if not results:
                break

            measurements.extend(results)

            if len(results) < limit:
                break

            page += 1

    return measurements


def get_african_measurements() -> list[dict]:

    sensors = get_african_sensors()

    all_measurements = []

    for sensor in sensors:
        measurements = get_measurements(sensor["id"])

        all_measurements.extend(measurements)

    return all_measurements
