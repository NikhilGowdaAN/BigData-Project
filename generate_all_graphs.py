from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent
scripts=['01_Hive/advanced_graphs.py','02_Kafka/advanced_graphs.py','03_Flink/graphs.py','05_Cloud_Analytics/advanced_graphs.py','04_MongoDB/graphs.py']
inputs={'02_Kafka/advanced_graphs.py':'02_Kafka/outputs/traffic_events.csv','03_Flink/graphs.py':'03_Flink/outputs/flink_run.log'}
failed=[]
for script in scripts:
    if script in inputs and not (ROOT/inputs[script]).exists(): print(f'SKIP {script}: missing {inputs[script]}',flush=True);continue
    print(f'Running {script}',flush=True)
    if subprocess.call([sys.executable,str(ROOT/script)],cwd=ROOT):failed.append(script)
if failed: raise SystemExit('Failed: '+', '.join(failed))
