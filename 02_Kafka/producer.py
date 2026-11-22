import argparse, json, random, time
from datetime import datetime, timezone
from kafka import KafkaProducer
from kafka.errors import KafkaError
from common import TOPIC

def main():
    p = argparse.ArgumentParser(); p.add_argument('--count', type=int, default=30); p.add_argument('--interval', type=float, default=1); p.add_argument('--bootstrap', default='localhost:9092'); args = p.parse_args()
    if args.count < 1 or args.interval < 0: p.error('count must be positive and interval nonnegative')
    rng = random.Random(42)
    producer = KafkaProducer(bootstrap_servers=args.bootstrap, value_serializer=lambda x: json.dumps(x).encode(), request_timeout_ms=10000, api_version_auto_timeout_ms=10000)
    try:
        for i in range(args.count):
            event = {'sensor_id': f'S{i%3+1}', 'timestamp': datetime.now(timezone.utc).isoformat(), 'speed_kmh': rng.randint(10, 75), 'vehicles': rng.randint(10, 60)}
            producer.send(TOPIC, event).get(timeout=15); print(json.dumps(event), flush=True); time.sleep(args.interval)
    finally: producer.close()
if __name__ == '__main__':
    try: main()
    except (KafkaError, OSError) as exc: raise SystemExit(f'Kafka producer failed: {exc}')
