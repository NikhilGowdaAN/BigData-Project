# Report preparation notes (not a final assignment report)

## Hive
The 120-row synthetic CSV records transaction lines. Hive stores a delimited managed table and aggregates quantity ï¿½ unit price for revenue. Use product revenue and branch-product unit rankings to identify candidates for restocking, but combine them with stock on hand, lead time, seasonality and margins; no stock-on-hand data is present, so exact reorder quantities cannot be inferred. Sales are not profits.

## Kafka
The producer sends JSON to one KRaft broker; the consumer reads a topic and applies a two-condition congestion rule. Event timestamps are real run times while measurements come from a fixed random seed. One partition gives a simple ordered demonstration; offsets are tracked per consumer group. A single broker is not fault tolerant.

## Flink
A finite synthetic source assigns one-second event times. One-second bounded out-of-order watermarks drive 10-second tumbling windows keyed by patient ID; alerts and per-window averages are emitted separately. The fixed generated timestamps make the windows reproducible. Values and thresholds are illustrative and must not be used in clinical decisions. Flink runs the Java DataStream job inside Docker; Python is only an optional submission wrapper.

## MongoDB
Documents hold SKU, product name, category, price, stock, tags and active status. A unique SKU index enforces uniqueness and a compound category/price index supports category filtering with ordered prices. A relational alternative might split products and tags into tables joined by keys, use SQL and declared schemas, and enforce constraints through relational definitions. MongoDB's document model can embed arrays and allows flexible fields, although validation and transactions are also available; neither model is universally better.

## Cloud analytics
The local program counts HTTP 4xx/5xx errors, requests by UTC hour and path, and mean latency. The synthetic data has equal hourly volume, so the peak is a 24-way tie. Graphs are local SVG files. A proposed production architecture: application/load-balancer logs ? managed streaming ingestion ? object storage (raw, partitioned by date) ? scheduled ETL/query engine ? dashboard and monitoring alerts, with IAM, encryption, retention and access controls. This is a proposal; no cloud services are provisioned.

Illustrative monthly calculation in USD, not a vendor quote or measured bill: assume 100 GB ingested at $0.05/GB ($5), 100 GB-month stored at $0.02/GB-month ($2), and 20 GB scanned at $0.005/GB ($0.10), totaling **$7.10/month** before compute, requests, egress, taxes, monitoring and support. Rates are hypothetical, not current provider pricing. Actual costs depend on region, service, volume, retention and pricing; check a provider's current calculator before deployment.
