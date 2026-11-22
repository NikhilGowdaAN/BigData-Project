import argparse, json, csv
from pathlib import Path
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from common import TOPIC, classify, decode

def main():
    p = argparse.ArgumentParser(); p.add_argument('--bootstrap', default='localhost:9092'); p.add_argument('--group', default='traffic-demo'); p.add_argument('--max-messages', type=int, default=0); p.add_argument('--output', type=Path, help='Append broker-consumed events to CSV'); args = p.parse_args()
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=args.bootstrap, group_id=args.group, auto_offset_reset='earliest', enable_auto_commit=True, api_version_auto_timeout_ms=10000)
    print('Listening for traffic events (Ctrl+C to stop)...', flush=True)
    try:
        for msg in consumer:
            try:
                event = decode(msg.value); alert = classify(event)
                if args.output:
                    args.output.parent.mkdir(parents=True, exist_ok=True)
                    exists = args.output.exists() and args.output.stat().st_size > 0
                    with args.output.open('a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=['sensor_id', 'timestamp', 'speed_kmh', 'vehicles', 'congestion_alert'])
                        if not exists: writer.writeheader()
                        writer.writerow({**{k: event[k] for k in ('sensor_id', 'timestamp', 'speed_kmh', 'vehicles')}, 'congestion_alert': alert})
                print(json.dumps({'event': event, 'congestion_alert': alert}), flush=True)
            except (ValueError, TypeError, KeyError) as exc: print(f'Skipping malformed event: {exc}', flush=True)
            if args.max_messages and msg.offset >= 0:
                args.max_messages -= 1
                if args.max_messages == 0: break
    finally: consumer.close()
if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: print('Stopped.')
    except (KafkaError, OSError) as exc: raise SystemExit(f'Kafka consumer failed: {exc}')
