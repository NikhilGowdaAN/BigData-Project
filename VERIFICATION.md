# Verification record

## Current validation (2026-11-22)

- PASS: `generate_all_graphs.py` regenerated all twenty primary PNGs and their SVG counterparts from the named sources.
- PASS: Eleven automated unit tests passed, including nonempty graph files, report headings, source counts, Kafka rule consistency and Flink log record counts.
- PASS: Flink 1.19.1 Maven build and Docker job completed. Task-manager output contains 60 readings, 34 alert lines and 18 summaries. The plotting script reconciles alert records and window counts and means against the captured readings.
- PASS: Kafka broker execution previously captured 60 consumed synthetic events and 8 alerts. No independent producer or consumer transcript was saved.
- DATASET ONLY: Hive charts reconcile to 600 units and 49,951 revenue in the CSV and to the figures supplied by the user. The available transcript contains no result tables; independent historical Hive output verification is not possible from it.
- DATASET ONLY: Cloud and MongoDB charts use the synthetic CSV and JSON respectively. Cloud deployment and billing are proposals; MongoDB CRUD was intentionally not executed.
- NOT TESTED: MongoDB live CRUD and query plan. Screenshots have not been captured.

## Visualization update

- PASS: Hive graph script ran with Python 3.12 and checked all supplied product and branch totals and total revenue against the CSV. Four PNG and four SVG files were generated. The transcript contains the command but no Hive result tables, so it does not independently verify the supplied Hive results.
- PASS: Cloud graph script generated four PNG and four SVG files from 480 CSV log rows, including 29 errors.
- PASS: MongoDB graph script generated four PNG and four SVG files from 24 JSON products. No database was contacted.
- PASS: Kafka 3.9.0 KRaft broker accepted 60 synthetic producer events; a consumer read them and saved the CSV. The chart script validated the rule and generated four PNG and SVG files, with 8 alerts.
- Historical note: at the time of the earlier visualization update, Flink graph generation and runtime capture had not yet been completed; see current validation above.

Checks performed in the creation environment on 2026-11-22:

- `docker compose config --quiet` succeeded. The Docker client warned that its user configuration was inaccessible.
- PowerShell parsed all five run scripts without syntax errors.
- An independent Node.js data check counted 120 sales rows and calculated total revenue 49,951; 24 catalog products with 24 distinct SKUs; and 480 log rows, 29 HTTP errors, and 20 requests in each UTC hour.

Not executed here: Python unit tests or programs (the available `python` is an inaccessible Windows Store alias); Docker containers, Hive queries, Kafka producer/consumer, Maven build, or Flink job (the Docker engine was unavailable); MongoDB operations (mongosh was not on PATH, and no server connection was verified). These integrations and their output formats remain unverified, not demonstrated successes. Install/start the prerequisites and run the commands in README.md to validate them on your machine.
