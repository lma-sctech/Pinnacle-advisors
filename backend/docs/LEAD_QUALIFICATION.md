# Système de Qualification Automatique des Leads

## Vue d'ensemble

Le système CRM de Pinnacle intègre un **algorithme de qualification automatique** des leads basé sur plusieurs critères pondérés. Chaque lead reçoit un **score de 0 à 100** et une **qualification** (Hot/Warm/Cold) calculée automatiquement lors de sa création.

## Objectif

Permettre une priorisation intelligente des leads pour optimiser le temps commercial et améliorer le taux de conversion en identifiant automatiquement les prospects à fort potentiel.

---

## Critères de Qualification

### 1. Taille de l'Entreprise (Max 30 points)

La taille de l'entreprise est un indicateur de capacité budgétaire et de complexité des projets supply chain.

| Taille | Employés | Points | Rationale |
|--------|----------|--------|-----------|
| **Grande Entreprise (GE)** | > 5000 | 30 | Budgets importants, projets d'envergure |
| **ETI** | 200-5000 | 25 | Forte capacité d'investissement |
| **PME** | 50-200 | 15 | Budgets moyens, bonne capacité |
| **TPE** | < 50 | 5 | Budgets limités |
| **Inconnu** | - | 0 | Pas d'information |

### 2. Budget Mentionné (Max 30 points)

L'indication d'un budget démontre un projet concret et une intention sérieuse.

| Situation | Points | Détails |
|-----------|--------|---------|
| **Budget mentionné** | 20 | Le prospect a indiqué avoir un budget |
| **Budget ≥ 100 000 €** | +10 | Projet d'envergure (total: 30 points) |
| **Budget ≥ 50 000 €** | +5 | Projet moyen (total: 25 points) |
| **Pas de budget** | 0 | Aucun budget indiqué |

### 3. Urgence du Besoin (Max 15 points)

Détection de mots-clés d'urgence dans le message initial.

**Mots-clés détectés :**
- "urgent"
- "rapidement"
- "immédiat"
- "besoin urgent"
- "au plus vite"

**Attribution :** 15 points si au moins un mot-clé est présent

**Rationale :** Un besoin urgent indique un projet en cours avec une décision rapide.

### 4. Type de Besoin Stratégique (Max 15 points)

Certains types de besoins sont plus stratégiques et génèrent des projets plus importants.

**Besoins stratégiques :**
- Transformation digitale
- Optimisation supply chain
- Stratégie logistique

**Attribution :** 15 points si le besoin correspond à une catégorie stratégique

**Rationale :** Ces projets sont généralement transversaux, à fort impact et bien budgétés.

### 5. Qualité du Message (Max 10 points)

La longueur et le niveau de détail du message initial reflètent le sérieux du prospect.

| Longueur du message | Points | Interprétation |
|-------------------|--------|----------------|
| > 50 mots | 10 | Message détaillé, contexte fourni |
| 20-50 mots | 5 | Message moyen |
| < 20 mots | 0 | Message trop court, peu d'info |

### 6. Complétude des Informations (Max 10 points)

La fourniture d'informations complètes démontre un engagement sérieux.

| Informations fournies | Points |
|----------------------|--------|
| **Téléphone + Entreprise + Poste** | 10 |
| **2 sur 3** | 5 |
| **Moins de 2** | 0 |

---

## Attribution de la Qualification

Une fois le score total calculé (max 100 points), la qualification est attribuée :

| Score | Qualification | Signification | Action recommandée |
|-------|---------------|---------------|-------------------|
| **70-100** | 🔥 **Hot** | Priorité haute | Contact sous 24h, assignation immédiate |
| **40-69** | ☀️ **Warm** | Priorité moyenne | Contact sous 48-72h, qualification approfondie |
| **0-39** | ❄️ **Cold** | Priorité basse | Contact sous 1 semaine, nurturing |

---

## Exemples Pratiques

### Exemple 1 : Lead HOT (Score 85)

**Contexte :**
- Entreprise : Grande distribution (8000 employés) → **30 points**
- Budget : 150 000€ mentionné → **30 points**
- Message : "Besoin urgent d'optimiser notre supply chain..." (75 mots) → **15 + 15 + 10 points**
- Informations : Téléphone + Email + Poste fournis → **10 points**

**Total : 85 points → 🔥 HOT**

**Action :** Assignation immédiate à un senior, appel sous 4h, proposition sous 48h.

---

### Exemple 2 : Lead WARM (Score 55)

**Contexte :**
- Entreprise : PME logistique (150 employés) → **15 points**
- Budget : Non mentionné → **0 points**
- Message : "Je souhaite discuter d'une transformation digitale de nos processus" (45 mots) → **15 + 10 points**
- Informations : Téléphone + Entreprise fournis → **5 points**

**Total : 45 points → ☀️ WARM**

**Action :** Contact sous 48h, qualification téléphonique, envoi documentation.

---

### Exemple 3 : Lead COLD (Score 25)

**Contexte :**
- Entreprise : TPE (20 employés) → **5 points**
- Budget : Non mentionné → **0 points**
- Message : "Demande d'information" (3 mots) → **0 points**
- Informations : Email uniquement → **0 points**

**Total : 5 points → ❄️ COLD**

**Action :** Envoi automatique de documentation, nurturing par email, suivi à J+7.

---

## Avantages du Système

### 1. Gain de Temps Commercial
- Priorisation automatique des leads à fort potentiel
- Réduction du temps passé sur les leads non qualifiés
- Focus sur les opportunités réelles

### 2. Amélioration du Taux de Conversion
- Meilleure réactivité sur les leads hot
- Personnalisation de l'approche selon la qualification
- Réduction du cycle de vente

### 3. Objectivité
- Élimination des biais subjectifs
- Critères uniformes pour tous les leads
- Traçabilité et auditabilité

### 4. Optimisation Continue
- Analyse des patterns de conversion par qualification
- Ajustement des pondérations basé sur les résultats
- Amélioration continue de l'algorithme

---

## Configuration et Personnalisation

Le système de qualification est défini dans le modèle `Lead` :

**Fichier :** `backend/apps/crm/models.py`
**Méthode :** `Lead.auto_qualify()`

### Modifier les Pondérations

Pour ajuster les critères de qualification, modifier les valeurs dans la méthode `auto_qualify()` :

```python
def auto_qualify(self):
    score = 0

    # Modifier les points par taille d'entreprise
    size_scores = {
        'ge': 35,    # Au lieu de 30
        'eti': 28,   # Au lieu de 25
        'pme': 18,   # Au lieu de 15
        'tpe': 8,    # Au lieu de 5
    }
    score += size_scores.get(self.company_size, 0)

    # ... reste du code
```

### Modifier les Seuils de Qualification

Pour changer les seuils Hot/Warm/Cold :

```python
# Dans la méthode auto_qualify()
self.qualification = 'hot' if score >= 75 else ('warm' if score >= 45 else 'cold')
# Seuils modifiables : 75 et 45
```

---

## Suivi et Analytics

### Métriques à Suivre

1. **Distribution des qualifications**
   - % de leads Hot/Warm/Cold
   - Évolution dans le temps

2. **Taux de conversion par qualification**
   - Hot → Client : Objectif > 40%
   - Warm → Client : Objectif > 20%
   - Cold → Client : Objectif > 5%

3. **Temps de conversion**
   - Délai moyen par qualification
   - Identification des outliers

4. **Pertinence de la qualification**
   - Taux de leads Hot convertis
   - Taux de leads Cold qui surprennent

### Dashboard CRM

Accéder aux statistiques dans le Django Admin :
- **URL :** `/admin/crm/lead/`
- **Section :** Vue de liste avec statistiques globales
- **Filtres :** Par qualification, statut, date, source

---

## Bonnes Pratiques

### Pour les Commerciaux

1. **Leads Hot** : Contacter dans les 4h, maximum 24h
2. **Leads Warm** : Qualifier par téléphone sous 48h
3. **Leads Cold** : Nurturing automatisé, qualification progressive
4. **Révision manuelle** : Possibilité d'ajuster la qualification manuellement

### Pour les Managers

1. **Monitoring** : Vérifier quotidiennement les leads Hot non assignés
2. **Distribution** : Assigner les Hot leads aux seniors
3. **Formation** : Former les juniors sur les Warm/Cold
4. **Analyse** : Review mensuelle des conversions par qualification

---

## Améliorations Futures

### Court terme
- Intégration du scoring avec l'historique de navigation du site
- Prise en compte de la source du lead (LinkedIn = +5 points)
- Détection d'entreprises target (liste prédéfinie)

### Moyen terme
- Machine Learning pour ajuster automatiquement les pondérations
- Prédiction du délai de conversion
- Scoring dynamique basé sur les interactions

### Long terme
- Intégration avec enrichissement de données (Clearbit, Hunter.io)
- Scoring prédictif basé sur l'IA
- Recommandations d'actions personnalisées

---

## Support et Questions

Pour toute question sur le système de qualification :

1. **Documentation technique** : `backend/apps/crm/models.py`
2. **Configuration** : Variables dans `settings.py`
3. **Analytics** : Dashboard Django Admin

---

*Document créé le : 27/10/2025*
*Dernière mise à jour : 27/10/2025*
*Version : 1.0*
