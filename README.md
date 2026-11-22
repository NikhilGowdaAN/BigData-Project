# Big Data Assignment 2: practical projects

Generate the current primary charts with `python generate_all_graphs.py`. Each activity writes PNG and SVG files to its `graphs` directory; missing Kafka or Flink runtime data is skipped. MongoDB charts use the JSON dataset and do not connect to the database. Each activity has a `REPORT.md`, `architecture.mmd`, and `SCREENSHOTS.md`. Run `python -m unittest discover -s tests -v` for validation. See [VERIFICATION.md](VERIFICATION.md) for the evidence and limitations.

Kafka charts can be regenerated with `python 02_Kafka/graphs.py` from the recorded `02_Kafka/outputs/traffic_events.csv`. To capture a new run, start Kafka as described below, then run the consumer with a fresh group and an output file, for example `python 02_Kafka/consumer.py --group fresh-demo --max-messages 30 --output 02_Kafka/outputs/new_events.csv`, and run the producer in another terminal. Generate its charts using `python 02_Kafka/graphs.py --input 02_Kafka/outputs/new_events.csv`. The consumer appends to existing files; choose a new path to keep captures separate.

Five independent demonstrations for Windows. Data and alerts are synthetic; they do not represent real sales, patients, traffic, infrastructure usage, or clinical guidance. See REPORT_CONTENT.md for explanatory notes, not a final report. See VERIFICATION.md for what was actually tested.

## Setup

Install Python 3.11 (64-bit), Docker Desktop with Linux containers, and MongoDB Community Server plus mongosh; Compass is a GUI, not the database server or the shell. Start Docker Desktop and the MongoDB server when needed. Ensure ports 10000, 9092 and 8081 are free. PowerShell commands below assume the current directory is this project root. Images and Maven dependencies require internet on first use. If PowerShell blocks scripts, run `Set-ExecutionPolicy -Scope Process Bypass` for that window.

```powershell
cd D:\BigData
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

If Python launcher is unavailable, use an installed Python 3.11 executable in place of `py -3.11`. Start only one Docker service group at a time. After each exercise use `docker compose --profile hive down`, `docker compose --profile kafka down`, or `docker compose --profile flink down` respectively; this removes the Compose containers and their ephemeral data. Do not run `down` while another exercise is running. No MongoDB Docker container is used.

## 1. Hive: supermarket sales

```powershell
.\01_Hive\run.ps1
docker compose --profile hive down
```

The script starts HiveServer2, waits up to five minutes, creates a local Derby-backed database and reloads the CSV into a managed table. The queries show total revenue, product units/revenue, branch revenue and branch-product demand. Revenue is quantity ï¿½ unit price. The query recreates the assignment table; rerunning replaces its data. Read the branch-product results alongside stock and supplier lead times before deciding reorder quantities; sales volume alone does not measure current stock or profit. Expected format: `TOTAL_REVENUE | <amount>`, then tables with product/branch, units, revenue. Initial image download and startup may take several minutes. Inspect `docker compose logs hive` if readiness fails.

## 2. Kafka: traffic sensors

```powershell
.\02_Kafka\run.ps1
# Terminal A (activate .venv):
python .\02_Kafka\consumer.py --group demo1
# Terminal B (activate .venv):
python .\02_Kafka\producer.py --count 30 --interval 1
# Stop consumer with Ctrl+C, then:
docker compose --profile kafka down
```

The single broker uses KRaft, with no ZooKeeper. The producer sends seeded synthetic measurements with current UTC timestamps. Each consumer line is JSON containing the event and `congestion_alert`; the demonstration rule is speed < 25 km/h AND at least 30 vehicles. An alert is an illustrative classification, not real traffic advice. Each group resumes committed offsets; use a new `--group` to replay retained messages. The group stops after 30 messages with `--max-messages 30`. Kafka data is ephemeral on teardown. If connection fails, check Docker logs and port 9092; wait for the run script to finish first.

## 3. Flink: synthetic patient vitals

```powershell
.\03_Flink\run.ps1
docker compose logs flink-taskmanager
# Web UI: http://localhost:8081
docker compose --profile flink down
```

The script builds the Java 11 DataStream job with a pinned Maven container, starts Flink 1.19.1, and submits the finite stream. Alternatively after building and starting, `python .\03_Flink\patient_stream.py` submits it. The stream emits 60 seeded samples over approximately six seconds, with one-second event-time spacing. It prints alerts for heart rate >120 or temperature >=38ï¿½C and 10-second tumbling event-time averages per patient. Expected task-manager log lines start `ALERT` and `SUMMARY patient=P1 window=[...,...)`. Out-of-order tolerance is one second; a finite source closes the final windows. Thresholds and data are demonstrations only, not medical advice. No real patient data is used. Maven's first build requires dependency downloads. The web UI shows job state and logs; inspect job/task-manager logs on failure.

## 4. MongoDB: catalog

Start the existing MongoDB server (Compass alone does not start it), then:

```powershell
.\04_MongoDB\run.ps1
# For a different deployment:
.\04_MongoDB\run.ps1 -MongoUri 'mongodb://localhost:27017'
```

The script requires mongosh on PATH. It resets only the `products` collection in the dedicated `big_data_assignment_catalog` database on every run; do not use that collection for other data. It imports 24 products, creates unique SKU and category/price indexes, reads electronics, inserts and updates a demo item, deletes it and prints a query plan. Expected markers include `COUNT AFTER IMPORT: 24`, `UPDATE`, `DELETE`, and `INDEXES`. In Compass connect to the same URI, then open `big_data_assignment_catalog.products`. For authenticated installations supply an appropriate URI without embedding credentials in screenshots. An index may or may not be chosen by the optimizer depending on collection size and server version.

## 5. Cloud analytics: simulated logs

```powershell
.\05_Cloud_Analytics\run.ps1
```

Open `05_Cloud_Analytics/output/hourly.svg` and `statuses.svg` in a browser; `summary.json` contains the calculated metrics. The sample has 480 requests, spread evenly across 24 UTC hours, so all hours tie for peak. Errors include both 4xx and 5xx. Input and output paths can be changed with `python .\05_Cloud_Analytics\analysis.py --input <CSV> --output <directory>`. This is local analysis of synthetic data, not an actual cloud deployment or bill. Architecture and clearly illustrative cost arithmetic are in REPORT_CONTENT.md.

## Troubleshooting and output

Python scripts return nonzero on execution errors. Docker port conflicts require freeing the port or changing the Compose mapping and client endpoint consistently. Docker resources are isolated Compose services; inspect `docker compose ps -a` and service logs when needed. MongoDB authentication and availability depend on the user's installation. The checked-in source data is deterministic; generated graphs, build artifacts and virtual environments are ignored. The scripts and example formats are demonstrations, not claims of verified runs.
