from asaase_sense.ingestion.client import get_client
from asaase_sense.ingestion.countries import get_countries, filter_african_countries


def get_locations(country_code: str) -> list[dict]:

    locations = []
    page = 1

    with get_client() as client:
        while True:
            response = client.get("/locations",params={"iso": country_code,"limit": 1000,"page": page})

            response.raise_for_status()

            data = response.json()

            results = data["results"]

            if not results:
                break

            locations.extend(results)

            if len(locations) >= data["meta"]["found"]:
                break

            page += 1

    return locations


def get_african_locations() -> list[dict]:

    countries = get_countries()

    african_countries = filter_african_countries(countries)

    all_locations = []

    for country in african_countries:
        locations = get_locations(country["code"])
        all_locations.extend(locations)

    return all_locations
