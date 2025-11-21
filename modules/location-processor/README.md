# Location Processor Service

This service consumes location data from a Kafka topic and persists it to the PostgreSQL database.

## Functionality

- Connects to the Kafka topic specified by `KAFKA_TOPIC`.
- Consumes messages containing location data.
- Validates and saves the data to the `location` table in the database.

## Configuration

- `KAFKA_SERVER`: Address of the Kafka bootstrap server (default: `kafka:9092`).
- `KAFKA_TOPIC`: Name of the Kafka topic to consume from (default: `location_topic`).
- `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`: Database connection details.
