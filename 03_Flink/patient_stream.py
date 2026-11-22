"""Submit the Java DataStream job already built by run.ps1; no PyFlink install needed."""
import subprocess, sys
cmd = ['docker', 'compose', 'exec', '-T', 'flink-jobmanager', 'flink', 'run', '-c', 'assignment.PatientStream', '/workspace/target/patient-stream-1.0.jar']
try:
    sys.exit(subprocess.call(cmd, cwd=__import__('pathlib').Path(__file__).resolve().parent.parent))
except FileNotFoundError:
    sys.exit('Docker CLI not found. Install and start Docker Desktop.')
