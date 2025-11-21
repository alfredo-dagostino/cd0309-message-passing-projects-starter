import logging
import os
import json
from kafka import KafkaConsumer
from app import create_app, db
from app.udaconnect.models import Location
from geoalchemy2.functions import ST_Point

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-processor")

KAFKA_SERVER = os.environ.get('KAFKA_SERVER', 'kafka:9092')
TOPIC_NAME = os.environ.get('KAFKA_TOPIC', 'location_topic')

def process_message(message):
    logger.info(f"Processing message: {message}")
    try:
        data = json.loads(message.value.decode('utf-8'))
        
        # Basic validation (could use Marshmallow schema here too)
        if not all(k in data for k in ("person_id", "creation_time", "latitude", "longitude")):
            logger.warning(f"Invalid message format: {data}")
            return

        new_location = Location()
        new_location.person_id = data["person_id"]
        new_location.creation_time = data["creation_time"]
        new_location.coordinate = ST_Point(data["latitude"], data["longitude"])
        
        db.session.add(new_location)
        db.session.commit()
        logger.info("Location saved to database")
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        db.session.rollback()

def main():
    app = create_app()
    app.app_context().push()
    
    logger.info("Starting Location Processor...")
    
    # Retry logic or wait for Kafka could be added here
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_SERVER,
        group_id='location_processor_group'
    )

    for message in consumer:
        process_message(message)

if __name__ == "__main__":
    main()
