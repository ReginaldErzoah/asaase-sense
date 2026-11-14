# Asaase Sense Documentation

Welcome to the documentation for **Asaase Sense**, an Environmental Data Intelligence Platform focused initially on air-quality monitoring data available through OpenAQ.

These documents explain the project, how its current ingestion pipeline works, and how raw data is stored.

## Documentation

1. [Project overview](project-overview.md) — what the project is and the problem it addresses.
2. [Architecture](architecture.md) — how data moves through the system.
3. [Data ingestion](data-ingestion.md) — how countries, locations, and sensors are collected.
4. [Error handling and recovery](error-handling.md) — how the pipeline responds to API failures.
5. [Data storage](data-storage.md) — how raw API records are saved.

## Project status

The current implementation retrieves reference data from OpenAQ: countries, locations, and sensors. It saves raw records as JSON Lines (JSONL) files.

Measurement-history ingestion, database storage, API delivery, orchestration, and monitoring are future development areas. They should not be considered implemented yet.

## Keeping the documentation accurate

Update these documents when the implementation changes. Clearly distinguish between features that exist today and ideas planned for later.
