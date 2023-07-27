Write-Host "$(.\venv\Scripts\python -m pip --version)" -ForegroundColor Green

Write-Host "[1] Installing libs..." -ForegroundColor Yellow
.\venv\Scripts\python -m pip install -r .\requirements.txt | Out-Null

Write-Host "[2] Doing migrations..." -ForegroundColor Yellow 
.\venv\Scripts\python .\manage.py migrate | Out-Null

Write-Host "[3] Starting server on http://127.0.0.1:8000/" -ForegroundColor Yellow
.\venv\Scripts\python .\manage.py runserver | Out-Null 