$ErrorActionPreference = 'Continue'
Set-Location (Join-Path $PSScriptRoot '..')
docker compose --profile hive up -d
if ($LASTEXITCODE -ne 0) { throw 'Hive startup failed' }
Write-Host 'Waiting up to 5 minutes for HiveServer2...'
$ready = $false
for ($i=0; $i -lt 60; $i++) {
  docker compose exec -T hive beeline -u 'jdbc:hive2://localhost:10000/default' -n hive -e 'SELECT 1' 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) { $ready = $true; break }
  Start-Sleep -Seconds 5
}
if (-not $ready) { throw 'Hive did not become ready. Run docker compose logs hive.' }
docker compose exec -T hive beeline --showHeader=true --outputformat=table -u 'jdbc:hive2://localhost:10000/default' -n hive -f /workspace/queries.hql
if ($LASTEXITCODE -ne 0) { throw 'Hive query failed' }
