# Location Ingestion Service

This service is responsible for receiving location data via HTTP POST requests and publishing them to a Kafka topic.

## API Endpoints

### POST /api/locations

Accepts a JSON payload containing location data.

**Payload:**
```json
{
    "person_id": 1,
    "latitude": "37.7749",
    "longitude": "-122.4194",
    "creation_time": "2020-01-01T12:00:00"
}
```

**Response:**
- 201 Created: Location received and queued.
- 500 Internal Server Error: If Kafka is unavailable.

## Configuration

- `KAFKA_SERVER`: Address of the Kafka bootstrap server (default: `kafka:9092`).
- `KAFKA_TOPIC`: Name of the Kafka topic to publish to (default: `location_topic`).
