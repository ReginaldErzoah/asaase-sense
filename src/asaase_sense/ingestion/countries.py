from asaase_sense.ingestion.client import get_client

def get_countries() -> list[dict]:

    with get_client() as client:
        response = client.get("/countries", params={"limit": 1000, "page": 1})

        response.raise_for_status()

        data = response.json()

    return data["results"]