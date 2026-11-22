$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
docker compose --profile flink-build run --rm flink-build
if ($LASTEXITCODE -ne 0) { throw 'Flink Maven build failed' }
docker compose --profile flink up -d
if ($LASTEXITCODE -ne 0) { throw 'Flink startup failed' }
$ready = $false
for ($i=0; $i -lt 40; $i++) {
 try { $null = Invoke-WebRequest -UseBasicParsing http://localhost:8081/overview -TimeoutSec 2; $ready = $true; break } catch { Start-Sleep -Seconds 3 }
}
if (-not $ready) { throw 'Flink did not become ready. Run docker compose logs flink-jobmanager.' }
docker compose exec -T flink-jobmanager flink run -c assignment.PatientStream /workspace/target/patient-stream-1.0.jar
if ($LASTEXITCODE -ne 0) { throw 'Flink job failed' }
Write-Host 'Output is in task manager logs: docker compose logs flink-taskmanager'
