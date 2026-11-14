from asaase_sense.ingestion.client import get_client


def test_openaq_connection():
    with get_client() as client:
        response = client.get(
            "/countries",
            params={"limit": 1},
        )

        assert response.status_code == 200

        data = response.json()

        assert "results" in data
        assert len(data["results"]) == 1

        print("OpenAQ connection successful!")


if __name__ == "__main__":
    test_openaq_connection()
