
import time

import httpx

from asaase_sense.ingestion.client import get_client
from asaase_sense.ingestion.locations import get_african_locations


REQUEST_DELAY = 1.1
PAGE_LIMIT = 1000


def get_sensors(
    client: httpx.Client,
    location_id: int,
) -> list[dict]:

    sensors = []
    page = 1

    while True:

        time.sleep(REQUEST_DELAY)

        response = client.get(
            f"/locations/{location_id}/sensors",
            params={
                "limit": PAGE_LIMIT,
                "page": page,
            },
        )

        response.raise_for_status()

        data = response.json()
        results = data["results"]

        if not results:
            break

        sensors.extend(results)

        found = data["meta"]["found"]

        if len(sensors) >= found:
            break

        page += 1

    return sensors


def get_african_sensors() -> list[dict]:

    locations = get_african_locations()

    pm25_sensors = []
    failed_locations = []

    total_locations = len(locations)

    with get_client() as client:

        for index, location in enumerate(locations, start=1):

            location_id = location["id"]

            print(
                f"[{index}/{total_locations}] "
                f"Processing location {location_id}..."
            )

            try:

                sensors = get_sensors(
                    client=client,
                    location_id=location_id,
                )

                location_pm25 = [
                    sensor
                    for sensor in sensors
                    if sensor.get("parameter", {}).get("name") == "pm25"
                ]

                pm25_sensors.extend(location_pm25)

                print(
                    f"    Found {len(location_pm25)} PM2.5 sensors."
                )

            except httpx.HTTPError as error:

                failed_locations.append(
                    {
                        "location_id": location_id,
                        "error": str(error),
                    }
                )

                print(
                    f"    Failed to retrieve sensors: {error}"
                )

    print("\nSENSOR EXTRACTION SUMMARY")
    print("-------------------------")
    print(f"Locations processed: {total_locations}")
    print(f"PM2.5 sensors found: {len(pm25_sensors)}")
    print(f"Failed locations: {len(failed_locations)}")

    if failed_locations:
        print("\nFailed location IDs:")

        for failure in failed_locations:
            print(f"    {failure['location_id']}")

    return pm25_sensors
