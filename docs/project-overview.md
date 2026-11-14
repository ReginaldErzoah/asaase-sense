# Project Overview

## What is Asaase Sense?

**Asaase Sense** is an Environmental Data Intelligence Platform. Its initial focus is air-quality monitoring data available through the OpenAQ API.

The project aims to collect, organize, validate, and make environmental data easier to use for analysis and other applications.

"Asaase" means "Earth" in Akan.

## The problem

Environmental observations are collected by monitoring locations and sensors. Before these observations can be used confidently, data needs to be gathered from its sources and organized in a consistent way.

Working directly with an external API every time someone needs data can also make it harder to manage historical records, handle interruptions, and provide a dependable supply of data.

Asaase Sense is being developed to build that data foundation.

## What the project aims to do

- Collect air-quality monitoring information exposed by OpenAQ.
- Organize information about countries, monitoring locations, and sensors.
- Collect and preserve measurement observations.
- Check data quality and handle problems in incoming data.
- Make organized data available for analysis and other applications.

## Current scope

The first stage focuses on reference data:

- Countries represented in OpenAQ.
- Monitoring locations associated with those countries.
- Sensors associated with those locations.

The project currently saves these records as raw JSONL files.

The project does **not** claim to represent every air-quality monitoring station in Africa. Its coverage depends on the data OpenAQ ingests and makes available through its API.

## Current development status

Implemented:

- OpenAQ API v3 client.
- Retrieval of country records and selection of African countries.
- Retrieval of locations by country.
- Retrieval of sensors by location.
- Pagination for location and sensor requests.
- Retry handling for selected temporary API failures.
- Incremental sensor-file writing and tracking of failed sensor requests.

Still to be developed:

- Historical measurement ingestion.
- More complete data validation and standardization.
- Database storage.
- A user-facing API and other data consumers.
- Scheduled orchestration, monitoring, and deployment.

## Why this project matters

Asaase Sense is also a practical learning project for Data Engineering and DataOps. It provides an opportunity to work with a real external data source and address practical engineering concerns such as pagination, API limits, retries, persistence, and recovery from failures.
