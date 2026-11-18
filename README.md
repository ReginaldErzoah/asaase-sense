**Project:** Asaase Sense  
**Category:** Environmental Data Intelligence Platform  
**Initial Data Source:** OpenAQ API v3  
**Status:** Under active development

---

Environmental data exists, but turning it into reliable, usable information is difficult.

For air quality specifically, data can be:

- Distributed across different monitoring locations and data providers.
- Inconsistent in structure, timestamps, and measurement units.
- Incomplete, with gaps in historical observations.
- Difficult to compare across locations and countries.
- Difficult to trust without systematic data-quality checks.

**Asaase Sense** aims to address this by building a reliable environmental data platform that collects, standardizes, validates, and organizes environmental observations.

The initial focus is air quality across Africa, using [OpenAQ](https://openaq.org/) as our first data source.


## Project Objectives

Asaase Sense aims to:

- Collect environmental observations from accessible data sources.
- Build a structured and reliable repository of environmental data.
- Standardize measurements, timestamps, and units.
- Identify missing, invalid, duplicate, and inconsistent records.
- Preserve historical observations for analysis.
- Make trusted environmental data accessible to applications, researchers, and decision-makers.

## Current Development

The initial development stage focuses on building the data ingestion foundation.

Currently implemented:

- OpenAQ API v3 integration.
- Retrieval of countries represented in OpenAQ.
- Identification of African countries using ISO country codes.
- Retrieval of monitoring locations across selected countries.
- Retrieval of sensors associated with monitoring locations.
- API pagination and retry handling.
- Raw data storage using JSON Lines (JSONL).
- Tracking and targeted recovery of failed sensor requests.

The project is currently collecting reference data about countries, locations, and sensors. Historical measurement ingestion and subsequent data-processing stages are still under development.

**Data coverage note:** Asaase Sense uses data made available through OpenAQ. It does not claim to represent every air-quality monitoring station or data provider across Africa.

## Planned Architecture

The intended data flow is:

```text
OpenAQ API
     |
     v
Data Ingestion
     |
     v
Raw Data Storage
     |
     v
Data Processing & Validation
     |
     v
Structured Database
     |
     v
Asaase Sense API
     |
     v
Dashboards & Other Applications
```

The architecture will evolve as the project develops. The current implementation is focused on ingestion and raw data storage.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming language | Python |
| Data source | OpenAQ API v3 |
| HTTP requests | HTTPX |
| Data handling | Pandas |
| Environment management | uv |
| Raw storage | JSON Lines (JSONL) |
| Version control | Git and GitHub |

Additional technologies for orchestration, databases, data validation, testing, and deployment will be introduced as the project progresses.

## Project Documentation

For 

- [Project Overview](docs/project-overview.md)
- [System Architecture](docs/architecture.md)
- [Data Ingestion](docs/data-ingestion.md)
- [Error Handling and Recovery](docs/error-handling.md)
- [Data Storage](docs/data-storage.md)

## Project Vision

The long-term vision is to develop Asaase Sense into a dependanble environment data infrastructure platform that makes environmental observations easier to access, understand, validate, and use.

Beyond collecting data, the goal is to establish a reliable data foundation that supports environmental analysis, monitoring, research, and informed decision-making.