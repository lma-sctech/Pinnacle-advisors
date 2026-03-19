# frontend-v2

Nouvelle base de travail pour sortir de la maintenance manuelle du dossier `frontend/`.

Objectif:

- mutualiser le header, le footer, le GTM et le shell HTML
- séparer le contenu éditorial des templates
- générer un site statique final sans framework frontend
- garder la compatibilité SEO, tracking et bilingue FR/EN

## Structure

```text
frontend-v2/
  build.py
  REFACTOR_PLAN.md
  src/
    content/
    data/
    partials/
    templates/
```

## Principe

- `src/templates/` contient les layouts HTML
- `src/partials/` contient les blocs réutilisables
- `src/content/` contiendra les contenus FR/EN par famille de page
- `src/data/` contiendra la navigation, les mappings FR/EN et les métadonnées SEO
- `build.py` deviendra le générateur statique vers un dossier de sortie

## Décision technique

Le modèle retenu est un build statique léger en Python, sans React/Vue/Next/Astro.

Cela permet:

- des pages HTML finales indexables
- une vraie notion de `base.html`
- des partials communs
- une réduction forte de la duplication

## Statut

Cette v2 est pour l’instant un squelette d’architecture et un plan de migration.
Le dossier `frontend/` reste la base actuelle du site en attendant la migration progressive.
