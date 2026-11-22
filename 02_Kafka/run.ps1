$ErrorActionPreference = 'Continue
Set-Location (Join-Path $PSScriptRoot '..')
docker compose --profile kafka up -d
if ($LASTEXITCODE -ne 0) { throw 'Kafka startup failed' }
$ready = $false
for ($i=0; $i -lt 40; $i++) {
  docker compose exec -T kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) { $ready = $true; break }
  Start-Sleep -Seconds 3
}
if (-not $ready) { throw 'Kafka did not become ready. Run docker compose logs kafka.' }
docker compose exec -T kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic traffic-sensors --partitions 1 --replication-factor 1
if ($LASTEXITCODE -ne 0) { throw 'Topic creation failed' }
Write-Host 'Ready. In two terminals run the consumer and then the producer as described in README.md.'
