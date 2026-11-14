
import time

import httpx

from asaase_sense.ingestion.countries import (
    get_countries,
    filter_african_countries,
)
from asaase_sense.ingestion.locations import get_locations
from asaase_sense.ingestion.sensors import get_sensors
from asaase_sense.ingestion.raw import save_jsonl


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

            # Retry rate-limit and server errors only.
            retryable = (
                status_code == 429
                or 500 <= status_code < 600
            )

            if not retryable or attempt == max_retries:
                raise

            # Use Retry-After when OpenAQ provides it.
            retry_after = error.response.headers.get("Retry-After")

            try:
                delay = float(retry_after) if retry_after else 5 * (2 ** attempt)
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


def ingest_sensors(
    locations: list[dict],
) -> tuple[list[dict], list[int]]:
    """Retrieve and save sensors across African locations."""

    print("\nRetrieving sensors...")

    all_sensors = []
    failed_locations = []

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

            failed_locations.append(location_id)
            continue

        all_sensors.extend(sensors)

        print(
            f"Location {location_id}: "
            f"{len(sensors)} sensors retrieved"
        )

    # Save all successfully retrieved sensor records.
    save_jsonl(all_sensors, "sensors.jsonl")

    print(f"\nTotal sensors retrieved: {len(all_sensors)}")

    if failed_locations:
        print(f"Locations with failed sensor requests: {len(failed_locations)}")
        print(f"Failed location IDs: {failed_locations}")

    return all_sensors, failed_locations


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

    sensors, failed_locations = ingest_sensors(locations)

    print("\n" + "=" * 50)

    if failed_countries or failed_locations:
        print("INGESTION COMPLETED WITH WARNINGS")
    else:
        print("INGESTION COMPLETED SUCCESSFULLY")

    print("=" * 50)

    print(f"African countries: {len(african_countries)}")
    print(f"Locations retrieved: {len(locations)}")
    print(f"Sensors retrieved: {len(sensors)}")

    print(f"Countries with failed requests: {len(failed_countries)}")
    print(f"Locations with failed requests: {len(failed_locations)}")

    print("\nRaw data saved in data/raw/")


if __name__ == "__main__":
    run_pipeline()
