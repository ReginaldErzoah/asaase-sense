from asaase_sense.ingestion.client import get_client

def get_locations(country_code: str) -> list[dict]:

    with get_client() as client:
        response = client.get("/locations",params={"limit": 1000, "page": 1})

        response.raise_for_status()

        data = response.json()

    return data["results"]