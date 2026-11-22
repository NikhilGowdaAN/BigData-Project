# Flink screenshot checklist

1. Start the job using `.\03_Flink\run.ps1`; capture the submission and successful completion in the terminal (caption: Flink job execution).
2. Open http://localhost:8081 while the cluster is running; capture the completed job and operator graph (caption: Flink dashboard).
3. Run `docker compose logs flink-taskmanager`; capture genuine READING, ALERT and SUMMARY lines (caption: synthetic readings and window output).
4. Open the figures in `03_Flink/graphs` and capture them if the assignment requires screenshots.

To regenerate charts from a fresh single run, save task-manager output as UTF-8 at `03_Flink/outputs/flink_run.log`, after preserving the existing log. Use a fresh task-manager container so the capture contains only one job, then run `python 03_Flink/graphs.py`. The script rejects duplicate or incomplete runs.
