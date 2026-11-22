# 1. Activity Name

Apache Kafka: Smart City Traffic Monitoring. Synthetic sensor events travel through a real Kafka broker before classification and analysis.

# 2. Problem Definition

Traffic operators need timely indications of potentially congested junctions. Periodic manual summaries can obscure individual low-speed, high-volume observations. This demonstration streams synthetic readings and flags a simple two-condition rule.

# 3. Objectives

1. Run a Kafka broker in KRaft mode.
2. Publish JSON readings to a topic.
3. Consume events using a consumer group.
4. Detect illustrative congestion conditions.
5. Capture consumed records for inspection.
6. Compare sensor readings and alert counts.

# 4. Technology Study

Kafka is a distributed event-streaming platform. Producers publish records to topics, which are divided into ordered partitions. Brokers store and serve records; consumer groups coordinate reading and track offsets. KRaft uses Kafka's controller quorum rather than ZooKeeper. This exercise uses a single broker and one partition, so it demonstrates the basic flow rather than fault-tolerant scaling. Streaming is useful for continuous sensor ingestion and operator notifications.

# 5. Architecture and Working

See [architecture.mmd](architecture.mmd). The seeded Python producer sends JSON to the `traffic-sensors` topic. The consumer receives broker records, flags speed below 25 km/h with at least 30 vehicles, prints results, and optionally appends the received data to CSV. The plot scripts analyze that CSV.

# 6. Implementation and Procedure

Docker Compose pins Apache Kafka 3.9.0. Python 3.12 uses kafka-python 2.0.6. Start the broker using `.\02_Kafka\run.ps1`, run the consumer with a new group and `--output`, then run the producer. The captured experiment used 60 events with a 0.1-second delay. See the root README for commands. Generate enhanced plots with `python 02_Kafka/advanced_graphs.py`.

# 7. Code, Queries and Configurations

The rule in [common.py](common.py) is `speed_kmh < 25 and vehicles >= 30`. [producer.py](producer.py) uses a fixed seed and UTC timestamps. [consumer.py](consumer.py) reads the broker topic, emits a Boolean classification and can append a CSV. The Compose file configures a single KRaft broker, one controller and advertised localhost port 9092.

# 8. Outputs, Graphs and Images

The actual consumer capture is [traffic_events.csv](outputs/traffic_events.csv), and its grouped summary is [sensor_summary.csv](outputs/sensor_summary.csv). The capture contains 60 readings and 8 alerts. These are synthetic events genuinely passed through Kafka, not measurements from city infrastructure.

1. [Figure 2.1: sensor speeds and alert markers](graphs/fig_2_1_sensor_time.png). The horizontal line is the speed component; volume is also required for an alert.
2. [Figure 2.2: alerts per sensor](graphs/fig_2_2_alerts_by_sensor.png). Counts compare alert frequency in this short run.
3. [Figure 2.3: reported vehicle-count sums and mean speeds](graphs/fig_2_3_volume_speed.png). Sums are sums of readings, not necessarily unique vehicles.
4. [Figure 2.4: alert classification](graphs/fig_2_4_event_status.png). This compares the 8 alerts with 52 non-alert events.

Capture actual console and broker status images as listed in [SCREENSHOTS.md](SCREENSHOTS.md); existing console output was not saved as a separate transcript.

# 9. Analysis and Interpretation

Each sensor produced 20 events. S1 recorded a vehicle-count sum of 757 and mean speed of 46.05 km/h, S2 678 and 37.80 km/h, and S3 674 and 46.25 km/h. Alert counts were 3, 3 and 2 respectively. The run is brief and synthetic, so these comparisons do not establish a causal traffic relationship or real-world demand.

# 10. Limitations

Single-broker operation is not fault tolerant. Values are randomly generated, not measured traffic. The alert condition is a demonstration rather than a calibrated congestion model. No consumer latency, lag or processing performance was measured; the capture is only a few seconds long.

# 11. Conclusion

The experiment demonstrates real Kafka transport, consumer-side rule evaluation and reproducible analysis of 60 synthetic events. Its eight alerts illustrate the workflow, not a production traffic service.
