from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-ingestion")

KAFKA_SERVER = os.environ.get('KAFKA_SERVER', 'kafka:9092')
TOPIC_NAME = os.environ.get('KAFKA_TOPIC', 'location_topic')

# Retry logic for Kafka connection could be added here, but for simplicity we assume Kafka is up.
# In a real scenario, we might want to wait for Kafka.
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    logger.error(f"Failed to connect to Kafka: {e}")
    producer = None

@app.route('/api/locations', methods=['POST'])
def ingest_location():
    if not producer:
        return jsonify({"error": "Kafka unavailable"}), 500
        
    data = request.get_json()
    logger.info(f"Received location data: {data}")
    producer.send(TOPIC_NAME, data)
    return jsonify({"status": "Location received"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
