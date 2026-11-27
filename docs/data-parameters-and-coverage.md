# Data Parameters and Geographic Coverage

## 1. Purpose

This document describes the environmental parameters represented in the sensor metadata currently collected by Asaase Sense and the geographic coverage available through the OpenAQ API.

It is intended to make two things clear:

1. What kinds of environmental measurements the sensors in the current extraction are configured to provide.
2. How much of Africa is represented in the OpenAQ data currently accessible to Asaase Sense.

This document describes the sensor metadata ingestion stage. It does not mean that historical measurement observations for these parameters have already been collected.

## 2. Current data collection status

Asaase Sense currently retrieves country, monitoring-location, and sensor metadata from OpenAQ API v3.

The current sensor extraction is parameter-agnostic: it collects sensor records returned for the selected African locations rather than filtering the sensor inventory to PM2.5 alone.

The `data/raw/sensors.jsonl` file contains sensor metadata. Each record describes a sensor and includes information such as:

- Sensor identifier and name.
- Parameter identifier, internal name, units, and display name.
- First and last measurement timestamps reported in the sensor metadata.
- Coverage summaries, where supplied by OpenAQ.
- Latest-value and summary metadata, where supplied by OpenAQ.

These fields describe the sensor and its reported history. They are not a substitute for the individual timestamped observations that will eventually be collected from the measurements endpoint.

Current implementation status: countries, locations, and sensors are being ingested and stored as raw JSONL records. Historical measurement ingestion and measurement-level validation are future stages.

## 3. Parameters observed in the current sensor sample

The sensor records inspected so far include the following parameter names:

| OpenAQ parameter name | Parameter | What it measures | Environmental significance |
|---|---|---|---|
| `pm25` | PM2.5 — fine particulate matter | Airborne particles with aerodynamic diameters generally 2.5 micrometres or smaller | Fine particles can penetrate deep into the respiratory system. PM2.5 is an important indicator for assessing exposure to particle pollution. |
| `pm10` | PM10 — particulate matter | Airborne particles with aerodynamic diameters generally 10 micrometres or smaller | PM10 captures inhalable particles, including dust and other coarse particles, and is useful for understanding particle pollution. |
| `pm1` | PM1 — very fine particulate matter | Particles with diameters around 1 micrometre or smaller | Provides a finer particle-size measure than PM2.5. It can help characterize the smaller fraction of airborne particulate pollution where monitoring data is available. |
| `no2` | Nitrogen dioxide | Concentration of nitrogen dioxide gas in ambient air | NO2 is associated with fuel combustion, especially road traffic and industrial activity. It is an important gaseous air pollutant for air-quality assessment. |
| `temperature` | Ambient temperature | Air temperature reported by a sensor | Temperature is not an air pollutant. It is a supporting environmental variable that can help describe atmospheric conditions and provide context for interpreting environmental observations. |

**Important inventory qualification:** this is the parameter list observed in the sensor records and examples inspected so far. It should not be treated as a verified, exhaustive list of every distinct parameter in the complete `sensors.jsonl` file. The complete inventory should be regenerated from the `parameter.name` values in that file when the file is available for inspection.

### 3.1 Units of measurement

The unit is provided in each sensor's nested `parameter.units` field. Asaase Sense should preserve the source unit rather than assume that every sensor reports in the same unit.

For example:

- Particulate-matter concentrations are commonly expressed in micrograms per cubic metre (`µg/m³`).
- Gaseous pollutant concentrations may be expressed in units such as `µg/m³`, parts per billion (`ppb`), or parts per million (`ppm`), depending on the source.
- Temperature may be reported in degrees Celsius (`°C`).

The actual unit stored on each sensor record is authoritative for that sensor. Unit standardization should happen in a later processing stage, with explicit conversion rules and retained source values.

## 4. Why these parameters matter

### 4.1 Particulate matter: PM1, PM2.5, and PM10

Particulate matter is a mixture of solid particles and liquid droplets suspended in air. The PM labels distinguish particle-size fractions.

- **PM1** describes the smallest particle fraction in this current inventory.
- **PM2.5** describes fine particles with aerodynamic diameters generally no greater than 2.5 µm.
- **PM10** describes inhalable particles with aerodynamic diameters generally no greater than 10 µm.

These measurements help characterize particle pollution. Particle size matters because it influences how particles enter and travel through the respiratory system. The three measures should not be treated as interchangeable.

### 4.2 Nitrogen dioxide: NO2

Nitrogen dioxide is a gaseous air pollutant commonly associated with combustion, including emissions from road transport and industrial processes. Monitoring NO2 can help characterize pollution associated with these activities.

### 4.3 Temperature

Temperature is a meteorological measurement rather than a pollutant concentration. It can provide useful context when examining environmental conditions alongside air-quality measurements. It should be classified separately from pollutant parameters in downstream datasets and analyses.

## 5. Geographic coverage of OpenAQ in Africa

Asaase Sense uses an African country-code reference list to identify African countries represented in OpenAQ's country catalogue. It then retrieves monitoring locations for the African countries returned by the API and retrieves sensors associated with those locations.

OpenAQ coverage is not equivalent to complete African monitoring coverage. The API exposes data that OpenAQ has discovered, received, and made publicly available. A country or location missing from the API response should therefore be described as not represented in the retrieved OpenAQ catalogue, not as a place with no air-quality monitoring.

### 5.1 Recorded extraction snapshot

The following figures are from a previous Asaase Sense extraction run:

| Coverage measure | Recorded result |
|---|---:|
| African countries represented in the OpenAQ country catalogue | 35 |
| Monitoring locations retrieved for those countries | 860 |
| Sensor records retrieved | 3,440 |
| Locations with unsuccessful sensor retrieval | 17 |
| Locations with successful sensor retrieval | 843 (approximately 98.0% of the 860 locations) |

These figures describe that extraction run only. They are not guaranteed to represent the current live OpenAQ catalogue or the current contents of the raw files. OpenAQ data availability can change over time, and a failed location request means that sensor retrieval could not be completed for that location during the run.

The country names and country-by-country location counts are not reproduced here because a verified country-level extraction summary was not available when this document was prepared. They should be generated from the corresponding raw country and location records rather than inferred from the total.

### 5.2 What the coverage figures do and do not mean

The figures above mean that, during the recorded run:

- OpenAQ listed 35 African countries in its country catalogue.
- Asaase Sense retrieved 860 monitoring-location records associated with those countries.
- Sensor retrieval succeeded for 843 locations and failed for 17 locations.
- The extraction returned 3,440 sensor records.

They do *not** mean that:

- Only 35 African countries have air-quality monitoring stations.
- The 860 locations represent every monitoring station in those countries.
- Every sensor is active or currently reporting.
- Every sensor has a complete historical record.
- Every parameter is available in every country or at every location.
- The 3,440 sensor records represent 3,440 unique monitoring locations.

A country absent from OpenAQ's country catalogue is not proof that the country has no monitoring network. It means that the catalogue queried by Asaase Sense did not list a country record for it at the time of extraction.

## 6. OpenAQ coverage and source limitations

Asaase Sense depends on the data OpenAQ makes available through its API. Consequently, the platform inherits several source-coverage limitations:

1. **Incomplete geographic representation:** OpenAQ does not claim to contain every air-quality monitoring dataset or station worldwide.
2. **Uneven country coverage:** the number of represented locations and sensors can differ substantially between countries.
3. **Uneven parameter availability:** a location may have sensors for some parameters but not others.
4. **Incomplete or interrupted records:** a sensor's reported first and last timestamps do not establish that every time interval between them contains an observation.
5. **Upstream request failures:** API errors can prevent Asaase Sense from retrieving sensor metadata for a location during a particular run.
6. **Changing coverage:** the set of countries, locations, sensors, and available observations can change as OpenAQ's source catalogue changes.

For these reasons, Asaase Sense should report its coverage transparently and retain extraction dates, successful and failed request counts, and source identifiers as the ingestion process develops.

## 7. How parameter selection will work

The sensor inventory should remain broad. Asaase Sense should preserve all sensor metadata returned for the selected African locations, regardless of parameter.

Parameter selection should happen later, when the measurement-ingestion process chooses which sensors to request observations from.

For example, a measurement-ingestion run could select sensors using the parameter name:

```python
selected_sensors = [
    sensor
    for sensor in all_sensors
    if sensor.get("parameter", {}).get("name") == "pm25"
]
```

The selection can later be expanded to multiple parameters without changing the purpose of the raw sensor inventory:

```python
selected_parameters = {"pm25", "pm10", "no2"}

selected_sensors = [
    sensor
    for sensor in all_sensors
    if sensor.get("parameter", {}).get("name") in selected_parameters
]
```

These examples illustrate the intended selection approach. They do not indicate that historical measurement ingestion has already been implemented.

## 8. Recommended coverage reporting

As the project develops, each extraction run should produce a small coverage summary containing:

- Extraction timestamp.
- Number of African countries listed by OpenAQ.
- Number of countries successfully queried.
- Number of locations retrieved.
- Number of locations with successful sensor retrieval.
- Number of locations with failed sensor retrieval.
- Total sensor records retrieved.
- Distinct parameter names and units found in the sensor records.
- Counts of sensors by country and parameter, where the metadata supports this grouping.

This will allow Asaase Sense to describe its actual source coverage at a particular point in time instead of relying on static figures in documentation.

## 9. References

### OpenAQ documentation

- [OpenAQ API — About the API](https://docs.openaq.org/about/about)
- [OpenAQ API — Countries resource](https://docs.openaq.org/resources/countries)
- [OpenAQ API — Locations resource](https://docs.openaq.org/resources/locations)
- [OpenAQ API — Parameters resource](https://docs.openaq.org/resources/parameters)

### Environmental and health references

- [World Health Organization — Ambient (outdoor) air pollution and health](https://www.who.int/news-room/fact-sheets/detail/ambient-%28outdoor%29-air-quality-and-health)
- [United States Environmental Protection Agency — Particulate Matter (PM) Basics](https://www.epa.gov/pm-pollution/particulate-matter-pm-basics)

---

## 10. Documentation maintenance

Update this document when:

- A new extraction reveals additional parameter names.
- The distinct parameter inventory or units change.
- A new coverage run produces updated country, location, or sensor counts.
- The ingestion scope changes beyond the current African OpenAQ source.

Always distinguish between **parameters represented in sensor metadata**, **parameters selected for measurement ingestion**, and **parameters for which historical observations have actually been collected**.