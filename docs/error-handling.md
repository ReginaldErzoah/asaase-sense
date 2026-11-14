# Error Handling and Recovery

## Why error handling matters

External APIs can be temporarily unavailable, respond slowly, limit request rates, or return server errors.

A reliable ingestion pipeline should handle these problems without losing track of what succeeded and what failed.

## Errors handled by the current pipeline

The sensor retrieval process retries selected temporary errors:

- **HTTP 429:** the API is rate-limiting requests.
- **HTTP 5xx:** the server encountered an error.
- **Request errors:** the client could not complete the request, for example because of a connection problem.

The retry logic waits between attempts. When the configured attempts are exhausted, the location is recorded as failed and the pipeline continues with the next location.

## Failed-location tracking

Failed sensor requests are stored in:

```text
data/raw/failed_locations.jsonl
```

Each record includes the location ID, an error message, and the time of failure.

Keeping this information means failed work is visible after the pipeline has finished. It can be investigated and retried later.

## Targeted recovery

The recovery function reads the failed-location file and retries only the locations listed there.

Run it from the project root with:

```bash
uv run python -c "from asaase_sense.ingestion.pipeline import recover_failed_locations; recover_failed_locations()"
```

If a location is retrieved successfully, its sensors are saved and the location is removed from the outstanding failure file. If it fails again, its failure record remains.

A recovery attempt may fail again. This does not necessarily mean the ingestion code is incorrect; the upstream service may still be unavailable for that request.

## Important distinction

A location with zero sensors returned successfully is not a failed location. A failed location is one for which the pipeline could not complete the sensor request.

## Current limitations

The failure file supports targeted retries, but it is not yet a complete job-checkpoint system. More robust checkpointing, structured run history, and monitoring are future improvements.
