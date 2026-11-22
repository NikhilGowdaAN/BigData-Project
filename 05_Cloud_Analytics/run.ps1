$ErrorActionPreference = 'Stop'
& python (Join-Path $PSScriptRoot 'analysis.py')
if ($LASTEXITCODE -ne 0) { throw 'Cloud analysis failed; check Python and input data.' }
