# Script PowerShell pour lancer le backend Django
Write-Host "🚀 Démarrage Backend Django Pinnacle Advisors..." -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\backend"

# Activer l'environnement virtuel
& ".\venv\Scripts\Activate.ps1"

# Lancer le serveur Django
Write-Host "✅ Environnement virtuel activé" -ForegroundColor Green
Write-Host "🌐 Lancement du serveur Django sur http://localhost:8000" -ForegroundColor Green
python manage.py runserver
