# 📇 CARTE DE VISITE DIGITALE - Documentation

**Date:** 29 Octobre 2025
**Statut:** ✅ COMPLÉTÉ

---

## 🎯 Vue d'ensemble

Nouvelle fonctionnalité de **carte de visite digitale** accessible via QR code, avec design glassmorphism et gestion complète via Django Admin.

### Fonctionnalités

✅ **Backend Django**
- Modèle `BusinessCard` complet avec 20+ champs
- API REST avec 5 endpoints
- Django Admin personnalisé avec aperçus, badges, QR code
- Génération automatique de fichiers vCard (.vcf)
- Tracking des vues et scans QR

✅ **Frontend Next.js**
- Page `/card` avec design glassmorphism
- Responsive mobile-first
- Animations Framer Motion
- 4 boutons d'action (Email, Tél, LinkedIn, vCard)
- Bouton retour en haut à gauche
- Tracking automatique des visites

---

## 📁 Fichiers Créés/Modifiés

### Backend Django

**Modèles:**
- `backend/apps/website/models.py` - Ajout du modèle `BusinessCard`
- `backend/apps/website/migrations/0003_businesscard.py` - Migration

**Serializers:**
- `backend/apps/website/serializers.py` - Ajout de `BusinessCardSerializer` et `BusinessCardPublicSerializer`

**Views:**
- `backend/apps/website/views.py` - Ajout de `BusinessCardViewSet` avec actions custom

**URLs:**
- `backend/apps/website/urls.py` - Enregistrement du router `business-card`

**Admin:**
- `backend/apps/website/admin.py` - Ajout de `BusinessCardAdmin` avec QR code, aperçus, actions

**Scripts:**
- `backend/create_sample_business_card.py` - Script de création de carte de démo

### Frontend Next.js

**Types:**
- `frontend/types/index.ts` - Ajout de l'interface `BusinessCard`

**API Client:**
- `frontend/lib/api.ts` - Ajout de 4 méthodes pour BusinessCard

**Pages:**
- `frontend/app/card/page.tsx` - Page carte de visite avec glassmorphism (320 lignes)

---

## 🚀 Utilisation

### 1. Accès Django Admin

```
http://localhost:8000/admin/website/businesscard/
```

**Créer/Modifier une carte:**
1. Cliquez sur "Ajouter carte de visite digitale"
2. Remplissez les informations (nom, poste, tagline, bio)
3. Uploadez une photo de profil (format carré recommandé)
4. Ajoutez logo entreprise (optionnel)
5. Configurez les contacts (email, téléphone, LinkedIn)
6. Personnalisez les couleurs (accent, dégradés)
7. Cochez "Actif" (une seule carte peut être active)
8. Sauvegardez

**Récupérer le QR Code:**
- Après sauvegarde, scrollez vers le bas dans l'admin
- Section "Liens Utiles" → "QR Code"
- Cliquez sur "Télécharger QR Code"
- Utilisez ce QR code dans votre signature email

### 2. Accès Frontend

**URL de la carte:**
```
http://localhost:3000/card
```

**URL avec tracking QR:**
```
http://localhost:3000/card?source=qr
```

### 3. Créer une Carte de Démo

```bash
cd backend
python create_sample_business_card.py
```

Puis ajoutez une photo via l'admin Django.

---

## 🎨 Design Glassmorphism

La carte utilise un effet de verre dépoli moderne avec:
- Fond dégradé personnalisable
- Carte semi-transparente avec backdrop-blur
- Bordures blanches translucides
- Animations Framer Motion
- Elements flottants animés en arrière-plan

**Personnalisation des couleurs:**
- `accent_color` - Couleur du bouton principal
- `background_gradient_start` - Début du dégradé de fond
- `background_gradient_end` - Fin du dégradé de fond

---

## 🔌 Endpoints API

### 1. GET `/api/website/business-card/active/`
Retourne la carte de visite active

**Réponse:**
```json
{
  "id": 2,
  "full_name": "Jean Dupont",
  "job_title": "Directeur Supply Chain",
  "tagline": "Expert en optimisation...",
  "bio": "Plus de 15 ans d'expérience...",
  "photo": "/media/business_card/photo.jpg",
  "email": "jean.dupont@example.com",
  "phone": "+33612345678",
  "company_name": "Pinnacle Advisors",
  "company_logo": "/media/business_card/logos/logo.png",
  "website_url": "http://localhost:3000",
  "linkedin_url": "https://linkedin.com/in/...",
  "accent_color": "#3B82F6",
  "background_gradient_start": "#3B82F6",
  "background_gradient_end": "#10B981"
}
```

### 2. POST `/api/website/business-card/{id}/increment_views/`
Incrémente le compteur de vues

### 3. POST `/api/website/business-card/{id}/increment_qr_scans/`
Incrémente le compteur de scans QR

### 4. GET `/api/website/business-card/{id}/vcard/`
Télécharge le fichier vCard (.vcf)

**Format vCard:**
```
BEGIN:VCARD
VERSION:3.0
FN:Jean Dupont
N:Dupont;Jean;;;
TITLE:Directeur Supply Chain
ORG:Pinnacle Advisors
EMAIL;TYPE=INTERNET,WORK:jean.dupont@example.com
TEL;TYPE=WORK,VOICE:+33612345678
URL:http://localhost:3000
URL;TYPE=LinkedIn:https://linkedin.com/in/...
NOTE:Expert en optimisation...
END:VCARD
```

---

## 📊 Tracking & Analytics

**Métriques trackées:**
- `views_count` - Nombre de visites de la carte
- `qr_scans_count` - Nombre de scans du QR code (via URL param `?source=qr`)

**Affichage dans l'admin:**
- Liste: colonnes `views_count` et `qr_scans_count`
- Détail: section "Statistiques & Paramètres"
- Action bulk: "Réinitialiser les statistiques"

---

## 🎯 Cas d'Usage

### Signature Email avec QR Code

1. Créez votre carte dans l'admin
2. Téléchargez le QR code
3. Ajoutez le QR code dans votre signature email:
   ```html
   <img src="qr_code.png" width="100" alt="Ma carte de visite" />
   <p style="font-size: 10px;">Scannez pour ma carte de visite</p>
   ```
4. Les personnes scannent et accèdent à `/card?source=qr`
5. Ils peuvent télécharger votre contact (.vcf) en 1 clic

### Événements & Networking

- Imprimez le QR code sur des flyers/badges
- Partagez l'URL directe `/card` sur LinkedIn
- Ajoutez en bio Instagram/Twitter
- Intégrez dans présentations PowerPoint

### Avantages vs Carte Papier

✅ Toujours à jour (modifiable via admin)
✅ Écologique (pas d'impression)
✅ Tracking des consultations
✅ Enregistrement contact en 1 clic
✅ Liens directs (email, téléphone, LinkedIn)
✅ Design moderne et professionnel
✅ Accessible partout (smartphone)

---

## 🔧 Actions Admin Personnalisées

**Liste des cartes:**
- Badge "ACTIVE" vert / "INACTIVE" gris
- Colonnes: nom, poste, entreprise, statut, vues, scans QR

**Actions bulk:**
1. **Activer cette carte** - Active une carte (désactive les autres)
2. **Désactiver les cartes** - Désactive les cartes sélectionnées
3. **Réinitialiser les statistiques** - Remet à 0 les compteurs

**Détail d'une carte:**
- **Aperçu Photo** - Preview circulaire de la photo
- **Aperçu Logo** - Preview du logo entreprise
- **Prévisualisation** - Bouton bleu "Voir la Carte de Visite"
- **QR Code** - Section avec QR code généré et bouton téléchargement

**Fieldsets organisés:**
1. Informations Personnelles
2. Contact
3. Entreprise
4. Réseaux Sociaux (collapsible)
5. Personnalisation Design (collapsible)
6. Statistiques & Paramètres (collapsible)
7. Liens Utiles (collapsible)

---

## 🎨 Personnalisation Design

### Couleurs par Défaut

```python
accent_color = "#3B82F6"  # Bleu Pinnacle
background_gradient_start = "#3B82F6"  # Bleu
background_gradient_end = "#10B981"  # Vert
```

### Palette Suggérée

**Professionnel Bleu/Vert (défaut):**
- Accent: `#3B82F6`
- Dégradé: `#3B82F6` → `#10B981`

**Élégant Violet/Rose:**
- Accent: `#8B5CF6`
- Dégradé: `#8B5CF6` → `#EC4899`

**Corporate Bleu Foncé:**
- Accent: `#1E40AF`
- Dégradé: `#1E40AF` → `#3B82F6`

**Tech Orange/Rouge:**
- Accent: `#F59E0B`
- Dégradé: `#F59E0B` → `#EF4444`

---

## 🐛 Dépannage

### La carte n'apparaît pas

**Problème:** Page blanche ou erreur 404

**Solutions:**
1. Vérifiez qu'une carte est active:
   ```bash
   python manage.py shell
   >>> from apps.website.models import BusinessCard
   >>> BusinessCard.objects.filter(is_active=True).count()
   ```
2. Créez une carte de démo:
   ```bash
   python create_sample_business_card.py
   ```
3. Ajoutez une photo via l'admin (obligatoire)

### Erreur "Photo field required"

**Problème:** La photo est un champ obligatoire

**Solution:**
1. Accédez à l'admin: `http://localhost:8000/admin/website/businesscard/`
2. Éditez votre carte
3. Uploadez une photo (format carré JPG/PNG, max 2MB)

### Le QR code ne fonctionne pas

**Problème:** Le QR code ne redirige pas vers la bonne URL

**Solution:**
1. Modifiez l'URL dans l'admin (`qr_code_url` method)
2. Ligne 238 de `backend/apps/website/admin.py`:
   ```python
   card_url = f'https://votre-domaine.com/card'  # Changez localhost
   ```
3. Régénérez le QR code

### Le bouton vCard ne télécharge pas

**Problème:** Clic sur "Enregistrer le contact" ne fait rien

**Solution:**
1. Vérifiez l'endpoint API:
   ```bash
   curl http://localhost:8000/api/website/business-card/2/vcard/
   ```
2. Vérifiez la console navigateur pour les erreurs CORS

---

## 📈 Évolutions Futures Possibles

**Phase 1 - Améliorations:**
- [ ] Upload photo/logo directement depuis le frontend
- [ ] Mode édition en live preview
- [ ] Thèmes prédéfinis (5-6 designs)
- [ ] Export PDF de la carte

**Phase 2 - Multi-cartes:**
- [ ] Plusieurs cartes par utilisateur
- [ ] URL personnalisée: `/card/jean-dupont`
- [ ] Carte d'équipe: `/team/nom-prenom`

**Phase 3 - Analytics Avancés:**
- [ ] Dashboard analytics dédié aux cartes
- [ ] Graphique vues/scans par jour
- [ ] Géolocalisation des scans (ville/pays)
- [ ] Heure de consultation

**Phase 4 - Intégrations:**
- [ ] Bouton "Ajouter à Contacts" Apple/Android natif
- [ ] Partage sur réseaux sociaux (LinkedIn, Twitter)
- [ ] Génération QR code avec logo au centre
- [ ] Widget embed pour sites tiers

**Phase 5 - Fonctionnalités Pro:**
- [ ] Lien Calendly pour prise de RDV direct
- [ ] Vidéo de présentation (30 sec)
- [ ] Portfolio / Réalisations
- [ ] Témoignages clients

---

## ✅ Checklist Mise en Production

Avant de déployer en production:

**Backend:**
- [ ] Modifier l'URL du QR code dans `admin.py` (ligne 238)
- [ ] Configurer les médias sur AWS S3 ou CDN
- [ ] Vérifier les permissions API (actuellement AllowAny)
- [ ] Ajouter rate limiting sur les endpoints increment

**Frontend:**
- [ ] Modifier l'URL dans le QR code généré
- [ ] Optimiser les images (Next.js Image)
- [ ] Tester sur mobile (iOS Safari, Android Chrome)
- [ ] Valider les animations (performance)

**Contenu:**
- [ ] Créer la vraie carte avec vraie photo
- [ ] Remplir tous les champs (bio, tagline, etc.)
- [ ] Tester le téléchargement vCard
- [ ] Imprimer et tester le QR code

**Testing:**
- [ ] Tester sur différents appareils
- [ ] Valider le tracking vues/scans
- [ ] Tester les 4 boutons d'action
- [ ] Vérifier le responsive design

---

## 📞 Support

Pour toute question ou problème:
1. Consultez cette documentation
2. Vérifiez les logs Django: `python manage.py runserver`
3. Vérifiez la console navigateur (F12)
4. Testez l'API manuellement avec curl

---

**Développé pour Pinnacle Advisors**
**Date:** 29 Octobre 2025
**Version:** 1.0
