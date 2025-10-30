# Script PowerShell pour lancer le frontend Next.js
Write-Host "🚀 Démarrage Frontend Next.js Pinnacle Advisors..." -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\frontend"

# Lancer le serveur Next.js
Write-Host "🌐 Lancement du serveur Next.js sur http://localhost:3000" -ForegroundColor Green
npm run dev
