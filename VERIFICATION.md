# Verification record

## Visualization update

- PASS: Hive graph script ran with Python 3.12 and checked all supplied product and branch totals and total revenue against the CSV. Four PNG and four SVG files were generated. The transcript contains the command but no Hive result tables, so it does not independently verify the supplied Hive results.
- PASS: Cloud graph script generated four PNG and four SVG files from 480 CSV log rows, including 29 errors.
- PASS: MongoDB graph script generated four PNG and four SVG files from 24 JSON products. No database was contacted.
- PASS: Kafka 3.9.0 KRaft broker accepted 60 synthetic producer events; a consumer read them and saved the CSV. The chart script validated the rule and generated four PNG and SVG files, with 8 alerts.
- NOT TESTED / NOT IMPLEMENTED: Flink graph generation, runtime capture, and reports. No claims of their execution are made.

Checks performed in the creation environment on 2026-11-22:

- `docker compose config --quiet` succeeded. The Docker client warned that its user configuration was inaccessible.
- PowerShell parsed all five run scripts without syntax errors.
- An independent Node.js data check counted 120 sales rows and calculated total revenue 49,951; 24 catalog products with 24 distinct SKUs; and 480 log rows, 29 HTTP errors, and 20 requests in each UTC hour.

Not executed here: Python unit tests or programs (the available `python` is an inaccessible Windows Store alias); Docker containers, Hive queries, Kafka producer/consumer, Maven build, or Flink job (the Docker engine was unavailable); MongoDB operations (mongosh was not on PATH, and no server connection was verified). These integrations and their output formats remain unverified, not demonstrated successes. Install/start the prerequisites and run the commands in README.md to validate them on your machine.
