# Data Storage

## Where raw data is stored

The current ingestion pipeline writes raw records to:

```text
data/raw/
```

It uses the JSON Lines format, commonly called JSONL.

## What is JSONL?

JSONL stores one JSON object on each line. For example:

```json
{"id": 1, "name": "Example record"}
{"id": 2, "name": "Another record"}
```

Each line can be read as an individual record. This makes JSONL convenient for storing API responses and processing records in batches.

## Current files

| File | Contents |
|---|---|
| `countries.jsonl` | Country records retrieved from OpenAQ |
| `african_countries.jsonl` | Retrieved countries selected by the African country-code list |
| `locations.jsonl` | Location records retrieved for the selected countries |
| `sensors.jsonl` | Sensor records retrieved for locations |
| `failed_locations.jsonl` | Locations whose sensor requests remain unsuccessful |

Some files are snapshots that are replaced when the corresponding extraction runs. Sensor records are appended incrementally, and existing sensor IDs are checked to avoid adding the same sensor twice. The failed-location file is updated as recovery progresses.

## Why preserve raw data?

Keeping source records gives the project a reference copy of what the API returned. It allows later processing rules to be changed without having to rely only on previously transformed data.

## Data protection

- Do not commit `.env` or API keys.
- Do not commit large raw data files unless there is a clear reason to publish them.
- Keep generated data separate from source code.
- Check the source's terms, licensing, and attribution requirements before redistributing data.

## Future storage

JSONL files are useful for the initial ingestion stage. A later stage of Asaase Sense is expected to process and validate the records and store structured data in a database. That database stage has not yet been implemented.
