from asaase_sense.ingestion.client import get_client
from asaase_sense.ingestion.countries import get_countries, filter_african_countries


def get_locations(country_code: str) -> list[dict]:

    with get_client() as client:
        response = client.get(
            "/locations", params={"iso": country_code, "limit": 1000, "page": 1}
        )

        response.raise_for_status()

        data = response.json()

    return data["results"]


def get_african_locations() -> list[dict]:

    countries = get_countries()

    african_countries = filter_african_countries(countries)

    all_locations = []

    for country in african_countries:
        locations = get_locations(country["code"])
        all_locations.extend(locations)

    return all_locations
