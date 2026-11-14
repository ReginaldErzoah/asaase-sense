# Data Ingestion

## What is data ingestion?

Data ingestion is the process of collecting data from a source and bringing it into a system where it can be stored and used.

In Asaase Sense, the initial source is the OpenAQ API v3.

## Current extraction process

The pipeline retrieves three types of reference data.

### 1. Countries

The pipeline requests the countries represented in OpenAQ. It then selects records whose country codes appear in the project's African country-code list.

The result is a list of African countries represented in the source data, not a guarantee that every African country has monitoring data available.

### 2. Locations

A location represents a place where monitoring takes place.

The pipeline requests locations using each country's ISO alpha-2 code. It follows the API's pagination information to retrieve additional pages when needed.

### 3. Sensors

A sensor is associated with a monitoring location and measures a parameter, such as PM2.5 or nitrogen dioxide.

The pipeline retrieves sensors for each location. It processes locations one at a time rather than requesting all sensors in one API call.

## Pagination

An API may return only part of a large result set in one response. Pagination allows the pipeline to request the remaining pages.

The current code requests up to 1,000 records per page and advances through pages until it reaches the end of the results.

## Request frequency and retries

The sensor retrieval code includes a delay between requests. The pipeline also retries selected temporary failures, including HTTP 429 responses and server-side 5xx responses.

Retries do not guarantee that a request will eventually succeed. A location can still fail after all configured attempts.

## Current limitations

- The current extraction stage collects countries, locations, and sensors; it does not yet collect historical measurements.
- Sensor retrieval can take time because requests are made for individual locations.
- Some API requests may fail even after retries.
- A successful request returning no sensors is different from a failed request.

## Next ingestion improvements

Future improvements include stronger checkpointing, more complete retry handling, measurement extraction using bounded date windows, and automated monitoring of ingestion results.
