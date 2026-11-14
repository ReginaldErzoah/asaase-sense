
from asaase_sense.ingestion.client import get_client
from asaase_sense.ingestion.locations import get_african_locations


def get_sensors(location_id: int) -> list[dict]:

    sensors = []
    page = 1

    with get_client() as client:

        while True:
            response = client.get(f"/locations/{location_id}/sensors",params={"limit": 1000,"page": page})

            response.raise_for_status()

            data = response.json()

            results = data["results"]

            if not results:
                break

            sensors.extend(results)

            if len(sensors) >= data["meta"]["found"]:
                break

            page += 1

    return sensors


def get_african_sensors() -> list[dict]:

    locations = get_african_locations()

    all_sensors = []

    for location in locations:
        sensors = get_sensors(location["id"])

        all_sensors.extend(sensors)

    return all_sensors
