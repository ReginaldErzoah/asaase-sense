
import time
from datetime import datetime, timezone

import httpx

from asaase_sense.ingestion.countries import (
    get_countries,
    filter_african_countries,
)
from asaase_sense.ingestion.locations import get_locations
from asaase_sense.ingestion.sensors import get_sensors
from asaase_sense.ingestion.raw import (
    save_jsonl,
    append_jsonl,
    read_jsonl,
)


SENSORS_FILE = "sensors.jsonl"
FAILED_LOCATIONS_FILE = "failed_locations.jsonl"


def ingest_countries() -> list[dict]:
    """Retrieve and save OpenAQ country records."""

    print("\nRetrieving countries...")

    countries = get_countries()
    save_jsonl(countries, "countries.jsonl")

    african_countries = filter_african_countries(countries)
    save_jsonl(african_countries, "african_countries.jsonl")

    print(f"Total countries retrieved: {len(countries)}")
    print(f"African countries identified: {len(african_countries)}")

    return african_countries


def ingest_locations(
    african_countries: list[dict],
) -> tuple[list[dict], list[str]]:
    """Retrieve and save locations across African countries."""

    print("\nRetrieving African locations...")

    all_locations = []
    failed_countries = []

    for country in african_countries:
        country_code = country["code"]

        print(f"\nRetrieving locations for {country_code}...")

        try:
            locations = get_locations(country_code)

        except httpx.HTTPError as error:
            print(
                f"WARNING: Failed to retrieve locations for "
                f"{country_code}: {error}"
            )
            failed_countries.append(country_code)
            continue

        all_locations.extend(locations)
        print(f"Locations retrieved: {len(locations)}")

    save_jsonl(all_locations, "locations.jsonl")

    print(f"\nTotal locations retrieved: {len(all_locations)}")

    if failed_countries:
        print(f"Countries with failed requests: {failed_countries}")

    return all_locations, failed_countries


def get_sensors_with_retry(
    location_id: int,
    max_retries: int = 3,
) -> list[dict]:
    """Retrieve sensors and retry temporary API failures."""

    for attempt in range(max_retries + 1):

        try:
            return get_sensors(location_id)

        except httpx.HTTPStatusError as error:

            status_code = error.response.status_code

            retryable = (
                status_code == 429
                or 500 <= status_code < 600
            )

            if not retryable or attempt == max_retries:
                raise

            retry_after = error.response.headers.get("Retry-After")

            try:
                delay = (
                    float(retry_after)
                    if retry_after
                    else 5 * (2 ** attempt)
                )
            except ValueError:
                delay = 5 * (2 ** attempt)

        except httpx.RequestError:

            if attempt == max_retries:
                raise

            delay = 5 * (2 ** attempt)

        print(
            f"Temporary failure for location {location_id}. "
            f"Retrying in {delay:.1f} seconds "
            f"(attempt {attempt + 1}/{max_retries})..."
        )

        time.sleep(delay)

    return []


def get_existing_sensor_ids() -> set[int]:
    """Return sensor IDs already stored in the raw sensor file."""

    existing_sensors = read_jsonl(SENSORS_FILE)

    return {
        sensor["id"]
        for sensor in existing_sensors
        if "id" in sensor
    }


def save_new_sensors(
    sensors: list[dict],
    existing_sensor_ids: set[int],
) -> int:
    """Save only sensor records that are not already stored."""

    new_sensors = [
        sensor
        for sensor in sensors
        if sensor["id"] not in existing_sensor_ids
    ]

    if not new_sensors:
        return 0

    append_jsonl(new_sensors, SENSORS_FILE)

    existing_sensor_ids.update(
        sensor["id"]
        for sensor in new_sensors
    )

    return len(new_sensors)


def ingest_sensors(
    locations: list[dict],
) -> tuple[int, list[int]]:
    """Retrieve sensors and persist progress incrementally."""

    print("\nRetrieving sensors...")

    existing_sensor_ids = get_existing_sensor_ids()

    # Load previously outstanding failures.
    failed_records = {
        record["location_id"]: record
        for record in read_jsonl(FAILED_LOCATIONS_FILE)
    }

    new_sensor_count = 0

    for index, location in enumerate(locations, start=1):

        location_id = location["id"]

        print(
            f"\nProcessing location {index}/{len(locations)}: "
            f"{location_id}"
        )

        try:
            sensors = get_sensors_with_retry(location_id)

        except httpx.HTTPError as error:

            print(
                f"WARNING: Could not retrieve sensors for "
                f"location {location_id}: {error}"
            )

            failed_records[location_id] = {
                "location_id": location_id,
                "error": str(error),
                "failed_at": datetime.now(timezone.utc).isoformat(),
            }

            # Persist failure immediately.
            save_jsonl(
                list(failed_records.values()),
                FAILED_LOCATIONS_FILE,
            )

            continue

        saved_count = save_new_sensors(
            sensors,
            existing_sensor_ids,
        )

        new_sensor_count += saved_count

        # A successful request means this location is no longer
        # an outstanding failure.
        failed_records.pop(location_id, None)

        print(
            f"Location {location_id}: "
            f"{len(sensors)} sensors retrieved, "
            f"{saved_count} new sensors saved"
        )

    # Save the remaining outstanding failures.
    save_jsonl(
        list(failed_records.values()),
        FAILED_LOCATIONS_FILE,
    )

    total_stored = len(existing_sensor_ids)
    failed_locations = list(failed_records.keys())

    print(f"\nNew sensors saved: {new_sensor_count}")
    print(f"Total sensors stored: {total_stored}")

    if failed_locations:
        print(f"Locations with failed sensor requests: {len(failed_locations)}")
        print(f"Failed location IDs: {failed_locations}")

    return total_stored, failed_locations


def recover_failed_locations() -> None:
    """Retry only locations with previously failed sensor requests."""

    print("\nStarting failed-location recovery...")

    failed_records = {
        record["location_id"]: record
        for record in read_jsonl(FAILED_LOCATIONS_FILE)
    }

    if not failed_records:
        print("No failed locations to recover.")
        return

    existing_sensor_ids = get_existing_sensor_ids()

    new_sensor_count = 0

    print(f"Locations awaiting recovery: {len(failed_records)}")

    for location_id in list(failed_records):

        print(f"\nRetrying location {location_id}...")

        try:
            sensors = get_sensors_with_retry(location_id)

        except httpx.HTTPError as error:

            print(
                f"WARNING: Recovery failed for location "
                f"{location_id}: {error}"
            )

            failed_records[location_id]["error"] = str(error)
            failed_records[location_id]["last_attempt_at"] = (
                datetime.now(timezone.utc).isoformat()
            )

        else:

            saved_count = save_new_sensors(
                sensors,
                existing_sensor_ids,
            )

            new_sensor_count += saved_count

            print(
                f"Location {location_id}: "
                f"{len(sensors)} sensors retrieved, "
                f"{saved_count} new sensors saved"
            )

            # Remove successfully recovered location.
            failed_records.pop(location_id)

        # Persist the current recovery status.
        save_jsonl(
            list(failed_records.values()),
            FAILED_LOCATIONS_FILE,
        )

    print("\n" + "=" * 50)
    print("FAILED-LOCATION RECOVERY COMPLETED")
    print("=" * 50)

    print(f"New sensors recovered: {new_sensor_count}")
    print(f"Remaining failed locations: {len(failed_records)}")

    if failed_records:
        print(f"Remaining IDs: {list(failed_records.keys())}")
    else:
        print("All previously failed locations recovered!")


def run_pipeline():
    """Execute the Asaase Sense reference data ingestion pipeline."""

    print("=" * 50)
    print("ASAASE SENSE - DATA INGESTION PIPELINE")
    print("=" * 50)

    try:
        african_countries = ingest_countries()

    except httpx.HTTPError as error:
        print(f"\nCOUNTRY INGESTION FAILED: {error}")
        print("Pipeline stopped because country data could not be retrieved.")
        return

    locations, failed_countries = ingest_locations(african_countries)

    print("\nWaiting 60 seconds for the API rate limit to reset...")
    time.sleep(60)

    total_sensors, failed_locations = ingest_sensors(locations)

    print("\n" + "=" * 50)

    if failed_countries or failed_locations:
        print("INGESTION COMPLETED WITH WARNINGS")
    else:
        print("INGESTION COMPLETED SUCCESSFULLY")

    print("=" * 50)

    print(f"African countries: {len(african_countries)}")
    print(f"Locations retrieved: {len(locations)}")
    print(f"Total sensors stored: {total_sensors}")

    print(f"Countries with failed requests: {len(failed_countries)}")
    print(f"Locations with failed requests: {len(failed_locations)}")

    print("\nRaw data saved in data/raw/")


if __name__ == "__main__":
    run_pipeline()