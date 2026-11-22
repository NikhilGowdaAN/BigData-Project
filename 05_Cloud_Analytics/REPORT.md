# 1. Activity Name

Cloud Big Data Analytics: Simulated Server Log Analysis.

# 2. Problem Definition

Online services generate logs that operators need to summarize for failures, usage and latency. This exercise uses local synthetic CSV analysis to demonstrate the metrics and proposes a cloud architecture for larger workloads; no cloud service was deployed.

# 3. Objectives

1. Parse the server-log dataset.
2. Count status codes and HTTP errors.
3. Compare request volume by UTC hour.
4. Rank endpoint activity.
5. Visualize error patterns.
6. Describe a scalable cloud design and transparent illustrative cost.

# 4. Technology Study

Cloud analytics commonly separates ingestion, durable object storage, processing and querying. Managed services can scale independently and reduce infrastructure administration, while access control, partitioning and retention govern data use and cost. Here pandas aggregates a local CSV and Matplotlib generates plots; the proposed cloud components are not part of the executed workflow.

# 5. Architecture and Working

See [architecture.mmd](architecture.mmd): the actual flow is synthetic CSV to local Python to summaries and graphs. The separate proposed flow is application logs to managed ingestion, object storage, managed ETL/query and dashboard. Object storage can partition by date, while query engines scan only relevant partitions.

# 6. Implementation and Procedure

The existing CSV contains 480 timestamped requests on one synthetic day, including method, path, HTTP status, response time and bytes. Run `python 05_Cloud_Analytics/analysis.py` for the JSON summary and `python 05_Cloud_Analytics/advanced_graphs.py` for the enhanced figures. No cloud credentials or resources are required.

# 7. Code, Queries and Configurations

[analysis.py](analysis.py) counts status codes, hours and paths and calculates mean response time. [advanced_graphs.py](advanced_graphs.py) validates fields, groups hourly timestamps, and saves 300-DPI PNG and SVG plots. An error is a status of 400 or above.

# 8. Outputs, Graphs and Images

Source: [server_logs.csv](server_logs.csv). The generated [status table](outputs/status_summary.csv) and [endpoint table](outputs/endpoint_summary.csv) contain the counts.

1. [Figure 5.1: status distribution](graphs/fig_5_1_status.png) distinguishes 200, 404 and 500.
2. [Figure 5.2: hourly requests](graphs/fig_5_2_hourly.png) shows every hour tied at 20.
3. [Figure 5.3: endpoints](graphs/fig_5_3_endpoints.png) shows all four paths tied at 120.
4. [Figure 5.4: error patterns](graphs/fig_5_4_errors.png) compares errors over time and by code.

The evidence is a generated dataset and local execution, not cloud telemetry. See [SCREENSHOTS.md](SCREENSHOTS.md).

# 9. Analysis and Interpretation

There are 451 successful 200 responses, 16 client 404 responses and 13 server 500 responses. The error rate is 29/480 = 6.04%; mean response time is 273.375 ms. Each of the four paths has 120 requests and every hour has 20; the data has no unique peak. These regular patterns reflect its generator rather than observed user demand.

Illustrative monthly estimate, not a provider quote: 100 GB ingested at $0.05/GB = $5; 100 GB-month stored at $0.02/GB-month = $2; 20 GB queried at $0.005/GB = $0.10; assumed request operations cost $0 for this simplified example, totaling $7.10 before real request, compute, transfer, monitoring and tax charges. Rates are hypothetical and require replacement with current provider and region pricing.

# 10. Limitations

The sample is small, synthetic and evenly distributed. Local execution does not validate cloud scaling, availability, ingestion costs or production latency. Error status alone cannot establish cause.

# 11. Conclusion

Local analysis demonstrates reproducible service metrics and highlights the synthetic data's tied traffic patterns. A cloud implementation remains a proposal with hypothetical costs.
