# Verification record

Checks performed in the creation environment on 2026-11-22:

- `docker compose config --quiet` succeeded. The Docker client warned that its user configuration was inaccessible.
- PowerShell parsed all five run scripts without syntax errors.
- An independent Node.js data check counted 120 sales rows and calculated total revenue 49,951; 24 catalog products with 24 distinct SKUs; and 480 log rows, 29 HTTP errors, and 20 requests in each UTC hour.

Not executed here: Python unit tests or programs (the available `python` is an inaccessible Windows Store alias); Docker containers, Hive queries, Kafka producer/consumer, Maven build, or Flink job (the Docker engine was unavailable); MongoDB operations (mongosh was not on PATH, and no server connection was verified). These integrations and their output formats remain unverified, not demonstrated successes. Install/start the prerequisites and run the commands in README.md to validate them on your machine.
