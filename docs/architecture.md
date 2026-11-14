# System Architecture

## Overview

The current Asaase Sense workflow collects reference data from the OpenAQ API and saves the returned records as raw JSONL files.

```text
OpenAQ API v3
     |
     v
Python ingestion pipeline
     |
     +--> Countries
     |
     +--> Locations
     |
     +--> Sensors
     |
     v
data/raw/ (JSONL files)
```

## Main parts

### 1. OpenAQ API

OpenAQ is the external data source. Asaase Sense uses API v3 to retrieve information that OpenAQ makes available.

The API key is supplied through an environment variable. It should not be committed to Git.

### 2. Python ingestion code

The ingestion code sends requests to OpenAQ, handles pagination, and collects the returned records.

The current extraction order is:

1. Retrieve countries.
2. Select countries using an African ISO country-code list.
3. Retrieve locations for those countries.
4. Retrieve sensors for each location.

### 3. Raw data files

The current pipeline saves API records as JSON Lines files under `data/raw/`.

Raw records are preserved before later transformation so that the original API responses can be inspected and processed again.

## Future architecture

The longer-term direction is:

```text
OpenAQ API
    |
    v
Data ingestion
    |
    v
Raw data storage
    |
    v
Processing and data quality checks
    |
    v
Structured database
    |
    v
Asaase Sense API
    |
    v
Dashboards and other applications
```

This is the intended direction, not a description of fully implemented functionality. Measurement ingestion, processing, database storage, and the Asaase Sense API are future stages.

## Important design point

The OpenAQ API is the external source. A future Asaase Sense API will be a separate service that provides access to data stored and managed by Asaase Sense. A dashboard should eventually use the Asaase Sense API rather than make every request directly to OpenAQ.
