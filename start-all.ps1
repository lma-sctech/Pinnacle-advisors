# Script PowerShell pour lancer backend + frontend simultanément
Write-Host "🚀 Démarrage COMPLET Pinnacle Advisors (Backend + Frontend)..." -ForegroundColor Cyan
Write-Host ""

# Lancer le backend dans une nouvelle fenêtre PowerShell
Write-Host "📦 Lancement Backend Django..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\start-backend.ps1"

# Attendre 3 secondes pour laisser le backend démarrer
Start-Sleep -Seconds 3

# Lancer le frontend dans une nouvelle fenêtre PowerShell
Write-Host "🎨 Lancement Frontend Next.js..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\start-frontend.ps1"

Write-Host ""
Write-Host "✅ Backend démarré sur http://localhost:8000" -ForegroundColor Green
Write-Host "✅ Frontend démarré sur http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Ouvre ton navigateur sur http://localhost:3000" -ForegroundColor Cyan
Write-Host "⚠️  Ferme les fenêtres PowerShell pour arrêter les serveurs" -ForegroundColor Yellow
