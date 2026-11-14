from asaase_sense.ingestion.client import get_client


def get_countries() -> list[dict]:

    with get_client() as client:
        response = client.get("/countries", params={"limit": 1000, "page": 1})

        response.raise_for_status()

        data = response.json()

    return data["results"]


AFRICAN_COUNTRY_CODES = {
    "DZ",
    "AO",
    "BJ",
    "BW",
    "BF",
    "BI",
    "CV",
    "CM",
    "CF",
    "TD",
    "KM",
    "CG",
    "CD",
    "CI",
    "DJ",
    "EG",
    "GQ",
    "ER",
    "SZ",
    "ET",
    "GA",
    "GM",
    "GH",
    "GN",
    "GW",
    "KE",
    "LS",
    "LR",
    "LY",
    "MG",
    "MW",
    "ML",
    "MR",
    "MU",
    "MA",
    "MZ",
    "NA",
    "NE",
    "NG",
    "RW",
    "ST",
    "SN",
    "SC",
    "SL",
    "SO",
    "ZA",
    "SS",
    "SD",
    "TZ",
    "TG",
    "TN",
    "UG",
    "ZM",
    "ZW",
}


def filter_african_countries(countries: list[dict]) -> list[dict]:
    """Filter OpenAQ country records to African countries."""

    return [
        country for country in countries if country["code"] in AFRICAN_COUNTRY_CODES
    ]
