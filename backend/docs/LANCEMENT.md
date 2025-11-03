# 🚀 Guide de Lancement - Pinnacle Advisors

## 🔧 Configuration Initiale (Une seule fois)

### 1. Autoriser l'exécution de scripts PowerShell

Ouvre un terminal PowerShell dans VS Code et exécute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Confirme avec `Y` si demandé.

**✅ Cette commande est à faire UNE SEULE FOIS!**

---

## 🎯 Méthodes de Lancement

### Méthode 1: Scripts PowerShell (⭐ Recommandé)

#### Lancer TOUT (Backend + Frontend)
```powershell
.\start-all.ps1
```
Ouvre 2 fenêtres PowerShell automatiquement.

#### Lancer Backend seul
```powershell
.\start-backend.ps1
```

#### Lancer Frontend seul
```powershell
.\start-frontend.ps1
```

---

### Méthode 2: VS Code Tasks (Intégré à l'éditeur)

1. Appuie sur `Ctrl + Shift + P`
2. Tape: `Tasks: Run Task`
3. Choisis:
   - `🔥 Start ALL (Backend + Frontend)` - Lance les 2
   - `🚀 Start Backend Django` - Backend seul
   - `🎨 Start Frontend Next.js` - Frontend seul

---

### Méthode 3: Commandes Manuelles (Terminal VS Code)

#### Backend Django
```powershell
cd backend
.\venv\Scripts\python.exe manage.py runserver
```

#### Frontend Next.js
```powershell
cd frontend
npm run dev
```

---

## 🌐 URLs d'accès

Une fois lancé:

- **Frontend:** http://localhost:3000 (Site web)
- **Backend API:** http://localhost:8000/api/
- **Django Admin:** http://localhost:8000/admin/

---

## 🛑 Arrêter les serveurs

- **Via scripts:** Ferme les fenêtres PowerShell
- **Via VS Code Tasks:** Clic sur la poubelle 🗑️ dans le panneau terminal
- **Manuellement:** `Ctrl + C` dans le terminal

---

## 🐛 Problèmes Courants

### ❌ "L'exécution de scripts est désactivée"
**Solution:** Exécute la commande de configuration initiale ci-dessus.

### ❌ "npm: command not found"
**Solution:** Vérifie que Node.js est installé: `node -v`

### ❌ "Port 8000 déjà utilisé"
**Solution:**
```powershell
# Trouver le processus
netstat -ano | findstr :8000
# Tuer le processus (remplace <PID> par le numéro trouvé)
taskkill /PID <PID> /F
```

### ❌ "Module 'django' introuvable"
**Solution:** Réinstalle les dépendances
```powershell
cd backend
.\venv\Scripts\pip.exe install -r requirements.txt
```

---

## 💡 Astuces

### Debug Django dans VS Code
1. Appuie sur `F5`
2. Choisis `🐍 Django: Debug`
3. Place des breakpoints dans ton code

### Recharger automatiquement
- **Django:** Recharge automatiquement ✅
- **Next.js:** Hot reload activé ✅

### Voir les logs
Les logs s'affichent directement dans les terminaux VS Code.

---

## 📊 Workflow Recommandé

1. Ouvre VS Code dans le dossier `D:\DEV\Pinnacle-website`
2. Lance: `.\start-all.ps1`
3. Attends 5-10 secondes que les serveurs démarrent
4. Ouvre ton navigateur sur http://localhost:3000
5. Code et sauvegarde - les changements sont appliqués automatiquement
6. Ferme les fenêtres PowerShell quand tu as fini

---

**Enjoy coding! 🎉**
