# SEO Migration Plan

## 1. Audit Summary
- Homepage sections confirmed: `#top`, `#about`, `#expertises`, `#approach`, `#insights`, `#contact`
- Expertise triggers found: `strategie`, `operations`, `digital`, `data`
- Insight triggers found: `network-redesign`, `warehouse-performance`, `digital-transformation`
- Perspective trigger found: `.perspective-trigger`

## 2. Modal Content Sources In `script.js`
- `frontend/script.js:56` `const expertiseContent = { ... }`
- `frontend/script.js:191` `const insightContent = { ... }`
- `frontend/script.js:244` `const perspectiveContent = { ... }`
- `frontend/script.js:372` `const approachContent = { ... }`
- English mirror sources: `frontend/script-en.js:56`, `:191`, `:244`, `:372`

## 3. Page Mapping
- `/pages/fr/strategie-supply-chain.html` <-> `/pages/en/supply-chain-strategy.html`
- `/pages/fr/operations-logistiques.html` <-> `/pages/en/logistics-operations.html`
- `/pages/fr/transformation-digitale.html` <-> `/pages/en/digital-transformation.html`
- `/pages/fr/data-pilotage-performance.html` <-> `/pages/en/data-performance-steering.html`
- `/pages/fr/pourquoi-redesigner-les-reseaux-logistiques.html` <-> `/pages/en/why-logistics-networks-must-be-redesigned-before-being-optimized.html`
- `/pages/fr/performance-entrepot-volumes-acceleration.html` <-> `/pages/en/what-strong-warehouse-operations-share-when-volumes-accelerate.html`
- `/pages/fr/projet-systeme-levier-execution-logistique.html` <-> `/pages/en/how-to-turn-a-system-project-into-a-real-logistics-execution-lever.html`
- `/pages/fr/perspective-cabinet-performance-supply-chain-robuste.html` <-> `/pages/en/firm-perspective-building-more-robust-supply-chain-performance.html`

## 4. Updated File Structure
- `frontend/index.html`
- `frontend/index-en.html`
- `frontend/styles.css`
- `frontend/script.js`
- `frontend/script-en.js`
- `frontend/js/page-enhancements.js`
- `frontend/pages/fr/...`
- `frontend/pages/en/...`

## 5. Homepage Changes Required
- Keep the one-page anchor navigation.
- Add real crawlable links in every expertise, insight and perspective card.
- Keep modals as progressive enhancement on the homepage only.
- Ignore modal opening when the visitor clicks an actual anchor.

## 6. SEO Tags To Add On Every Page
- Unique `<title>`
- Unique `<meta name="description">`
- `<link rel="canonical">`
- `<link rel="alternate" hreflang="fr">`
- `<link rel="alternate" hreflang="en">`
- `<link rel="alternate" hreflang="x-default" href="/index.html">`
- One clear `<h1>`
- Semantic `<h2>` / `<h3>` hierarchy
- Internal links back to homepage sections and related pages

## 7. Risks And Technical Constraints
- No server-side include or build step exists, so header/footer duplication remains a maintenance constraint.
- Root-relative canonicals and `hreflang` tags assume the deployed site root is the current `frontend/` directory.
- Homepage modals still depend on JavaScript, but no critical SEO content is locked inside them anymore.
- Structured data and sitemap generation remain useful next-step enhancements.
