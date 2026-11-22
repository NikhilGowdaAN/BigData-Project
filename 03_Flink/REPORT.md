# 1. Activity Name

Apache Flink: Real-time Synthetic Patient Vital-Sign Monitoring.

# 2. Problem Definition

A monitoring demonstration needs to process a continuous sequence of observations, flag specified conditions and summarize recent readings by patient. Processing each event as it arrives and grouping event-time windows illustrates this workflow; the measurements are fictional and do not support diagnosis.

# 3. Objectives

1. Generate reproducible fictional vital readings.
2. Execute the stream in Apache Flink.
3. Assign event timestamps and watermarks.
4. Detect illustrative thresholds.
5. Compute per-patient time-window means.
6. Reconcile captured readings, alerts and summaries.

# 4. Technology Study

Flink executes dataflow graphs of stream operators. A JobManager coordinates work and a TaskManager runs operator subtasks. Sources emit events; keyed windows maintain window contents until event-time progress permits output. Watermarks describe event-time progress. This application applies a one-second bounded-out-of-orderness strategy and ten-second tumbling event-time windows. Stream processing is appropriate for continuously arriving sensor observations; the single-worker local Docker demonstration does not establish production scalability.

# 5. Architecture and Working

See [architecture.mmd](architecture.mmd). A finite source emits 60 synthetic records; timestamps are assigned, the stream branches into a print sink, threshold filter, and patient-keyed window operator. Window summaries and alerts are printed to the task-manager log. The plotting script validates that log before drawing figures.

# 6. Implementation and Procedure

The Java 11 job in [PatientStream.java](src/main/java/assignment/PatientStream.java) uses Flink 1.19.1, a fixed seed, three fictional IDs and fixed 2025 event times. Run `.\03_Flink\run.ps1` with Docker Desktop; it builds with Maven, starts the cluster and submits the job. Save the task-manager log, then run `python 03_Flink/graphs.py`. Capture one complete job per log. No SpO₂ sensor is implemented.

# 7. Code, Queries and Configurations

The demonstration filter is `heartRate > 120 || temperature >= 38.0`. The window uses `keyBy(v -> v.patient).window(TumblingEventTimeWindows.of(Time.seconds(10)))`; a process function outputs count, mean heart rate and mean temperature. The Compose configuration runs one JobManager and one TaskManager with one task slot.

# 8. Outputs, Graphs and Images

The actual job completed successfully; [flink_run.log](outputs/flink_run.log) contains the reading, alert and summary lines. [readings.csv](outputs/readings.csv) and [window_summary.csv](outputs/window_summary.csv) are extracted from that log.

1. [Figure 3.1: heart rate and temperature](graphs/01_vital_signs_over_time.png) compares fictional patients with educational thresholds.
2. [Figure 3.2: alerts per patient](graphs/02_threshold_alerts.png) counts readings meeting either condition.
3. [Figure 3.3: ten-second window means](graphs/03_window_aggregations.png) displays Flink's mean heart rate by patient.
4. [Figure 3.4: normal and flagged readings](graphs/04_reading_classification.png) compares classifications.

See [SCREENSHOTS.md](SCREENSHOTS.md) for actual capture instructions; no screenshots were fabricated.

# 9. Analysis and Interpretation

The run produced 60 readings and 34 alert records (56.7% of readings), with 18 patient-window summaries. The graph script checks each alert against the rule and each summary count and rounded mean against its window readings. The event-time span is synthetic and does not imply an observed clinical period.

# 10. Limitations

Thresholds and values are educational only and are not clinically validated. No oxygen saturation, patient history, real devices, late-event experiments, latency or production fault tolerance are measured. Printing to logs is a demonstration sink; repeated runs must be separated to avoid duplicate capture.

# 11. Conclusion

The real Flink runtime processed and summarized a finite synthetic stream. Reconciled alerts and event-time means demonstrate the processing pipeline without making medical claims.
