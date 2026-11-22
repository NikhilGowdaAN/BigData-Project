param([string]$MongoUri = 'mongodb://localhost:27017')
$ErrorActionPreference = 'Stop'
if (-not (Get-Command mongosh -ErrorAction SilentlyContinue)) { throw 'mongosh not found. Install MongoDB Shell and add it to PATH.' }
mongosh $MongoUri --file (Join-Path $PSScriptRoot 'operations.js')
if ($LASTEXITCODE -ne 0) { throw 'MongoDB operations failed. Check URI, credentials and server.' }
