# Kafka screenshot checklist

1. Run `docker compose ps` after starting Kafka; capture the broker status.
2. Capture topic listing with `docker compose exec -T kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list`.
3. Capture a producer terminal running `python 02_Kafka/producer.py --count 30`.
4. Capture a separate consumer terminal running `python 02_Kafka/consumer.py --group screenshot-demo --output 02_Kafka/outputs/screenshot_events.csv`, including a genuine alert. Captions should identify synthetic sensor readings and the Boolean rule. Use Ctrl+C to stop the consumer.
