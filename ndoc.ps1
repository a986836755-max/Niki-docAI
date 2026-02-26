$env:PYTHONPATH = Join-Path $PSScriptRoot "src"
& py -m ndoc @args
