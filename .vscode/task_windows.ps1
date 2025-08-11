if (-not (Test-Path .venv)) {
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    } else {
    .venv\Scripts\Activate.ps1
}

clear
beet watch
