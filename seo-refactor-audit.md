# SEO Refactor Audit

## Scope

Files audited first:

- `frontend/index.html`
- `frontend/index-en.html`
- `frontend/script.js`
- `frontend/styles.css`

Additional observation:

- `frontend/script-en.js` exists and mirrors the localized modal content structure used by the EN homepage.

## 1. Current Architecture Snapshot

The site is a bilingual static website with:

- a French one-page homepage in `frontend/index.html`
- an English one-page homepage in `frontend/index-en.html`
- anchored navigation for homepage sections
- card-based expertise and insight blocks
- modal containers still present in both homepages
- JavaScript-driven modal population logic in `frontend/script.js` and `frontend/script-en.js`
- shared styling in `frontend/styles.css`

Homepage sections confirmed:

- `#top`
- `#about`
- `#expertises`
- `#approach`
- `#insights`
- `#contact`

Important current-state note:

- The cards now carry `data-url` and navigate to standalone pages on click.
- The modal DOM and modal content sources still exist in the codebase.
- This means the site is currently in a hybrid state: standalone pages exist, but the legacy modal architecture is still present.

## 2. Card Triggers And Modal Triggers

### French homepage triggers

Source: `frontend/index.html`

#### Expertise card triggers

- `frontend/index.html:122`
  - `data-expertise="strategie"`
  - `data-url="./pages/fr/strategie-supply-chain.html"`
- `frontend/index.html:138`
  - `data-expertise="operations"`
  - `data-url="./pages/fr/operations-logistiques.html"`
- `frontend/index.html:154`
  - `data-expertise="digital"`
  - `data-url="./pages/fr/transformation-digitale.html"`
- `frontend/index.html:170`
  - `data-expertise="data"`
  - `data-url="./pages/fr/data-pilotage-performance.html"`

#### Insight / perspective triggers

- `frontend/index.html:382`
  - `.perspective-trigger`
  - `data-url="./pages/fr/perspective-cabinet-performance-supply-chain-robuste.html"`
- `frontend/index.html:399`
  - `data-insight="network-redesign"`
  - `data-url="./pages/fr/pourquoi-redesigner-les-reseaux-logistiques.html"`
- `frontend/index.html:412`
  - `data-insight="warehouse-performance"`
  - `data-url="./pages/fr/performance-entrepot-volumes-acceleration.html"`
- `frontend/index.html:425`
  - `data-insight="digital-transformation"`
  - `data-url="./pages/fr/projet-systeme-levier-execution-logistique.html"`

### English homepage triggers

Source: `frontend/index-en.html`

#### Expertise card triggers

- `frontend/index-en.html:121`
  - `data-expertise="strategie"`
  - `data-url="./pages/en/supply-chain-strategy.html"`
- `frontend/index-en.html:137`
  - `data-expertise="operations"`
  - `data-url="./pages/en/logistics-operations.html"`
- `frontend/index-en.html:153`
  - `data-expertise="digital"`
  - `data-url="./pages/en/digital-transformation.html"`
- `frontend/index-en.html:169`
  - `data-expertise="data"`
  - `data-url="./pages/en/data-performance-steering.html"`

#### Insight / perspective triggers

- `frontend/index-en.html:381`
  - `.perspective-trigger`
  - `data-url="./pages/en/firm-perspective-building-more-robust-supply-chain-performance.html"`
- `frontend/index-en.html:398`
  - `data-insight="network-redesign"`
  - `data-url="./pages/en/why-logistics-networks-must-be-redesigned-before-being-optimized.html"`
- `frontend/index-en.html:411`
  - `data-insight="warehouse-performance"`
  - `data-url="./pages/en/what-strong-warehouse-operations-share-when-volumes-accelerate.html"`
- `frontend/index-en.html:424`
  - `data-insight="digital-transformation"`
  - `data-url="./pages/en/how-to-turn-a-system-project-into-a-real-logistics-execution-lever.html"`

### Modal containers present in both homepages

French modal container lines:

- `frontend/index.html:494` `#expertise-modal`
- `frontend/index.html:532` `#insight-modal`
- `frontend/index.html:552` `#perspective-modal`

English modal container lines:

- `frontend/index-en.html:493` `#expertise-modal`
- `frontend/index-en.html:531` `#insight-modal`
- `frontend/index-en.html:551` `#perspective-modal`

## 3. Exact Content Sources For Each Modal

### Expertise modal

Primary FR content source:

- `frontend/script.js:56`
  - `const expertiseContent = { ... }`

Population logic:

- `frontend/script.js:845` `function openExpertiseModal(key)`
- `frontend/script.js:853` `renderList(expertiseModalIssues, content.issues)`
- `frontend/script.js:854` `renderList(expertiseModalActions, content.actions)`
- `frontend/script.js:855` `renderList(expertiseModalOutcomes, content.outcomes)`
- `frontend/script.js:856` `renderList(expertiseModalContexts, content.contexts)`

Target DOM slots in homepage:

- `frontend/index.html:504` `#expertise-modal-label`
- `frontend/index.html:505` `#expertise-modal-title`
- `frontend/index.html:506` `#expertise-modal-intro`
- `frontend/index.html:511` `#expertise-modal-issues`
- `frontend/index.html:516` `#expertise-modal-actions`
- `frontend/index.html:521` `#expertise-modal-outcomes`
- `frontend/index.html:526` `#expertise-modal-contexts`

Localized EN mirror:

- `frontend/script-en.js:56`
- `frontend/script-en.js:845`

### Insight modal

Primary FR content source:

- `frontend/script.js:191`
  - `const insightContent = { ... }`

Population logic:

- `frontend/script.js:878` `function openInsightModal(key)`
- `frontend/script.js:886` `renderInsightParagraphs(insightModalBody, content.paragraphs, content.quoteIndex ?? null)`

Target DOM slots in homepage:

- `frontend/index.html:542` `#insight-modal-label`
- `frontend/index.html:543` `#insight-modal-title`
- `frontend/index.html:544` `#insight-modal-subtitle`
- `frontend/index.html:547` `#insight-modal-body`

Localized EN mirror:

- `frontend/script-en.js:191`
- `frontend/script-en.js:878`

### Perspective modal

Primary FR content source:

- `frontend/script.js:244`
  - `const perspectiveContent = { ... }`

Population logic:

- `frontend/script.js:908` `function openPerspectiveModal()`
- `frontend/script.js:915` `renderPerspectiveForces(perspectiveModalForces, perspectiveContent.forces)`
- `frontend/script.js:917` `renderPerspectiveRecommendations(perspectiveModalRecommendations, perspectiveContent.recommendations)`
- `frontend/script.js:918` `renderPerspectiveTable(perspectiveTable, perspectiveContent.table)`
- `frontend/script.js:914` and `frontend/script.js:916`
  - summary / implications paragraphs are rendered from `perspectiveContent.summary` and `perspectiveContent.implications`

Target DOM slots in homepage:

- `frontend/index.html:562` `#perspective-modal-label`
- `frontend/index.html:563` `#perspective-modal-title`
- `frontend/index.html:564` `#perspective-modal-subtitle`
- `frontend/index.html:571` `#perspective-modal-forces`
- `frontend/index.html:578` `#perspective-modal-implications`
- `frontend/index.html:585` `#perspective-modal-recommendations`
- `frontend/index.html:592` `#perspective-table`
- `frontend/index.html:596` `#perspective-modal-conclusion`

Localized EN mirror:

- `frontend/script-en.js:244`
- `frontend/script-en.js:908`

## 4. Complete FR / EN Content Mapping Table

| Type | Trigger key | FR label/title family | EN label/title family | Recommended FR slug | Recommended EN slug |
| --- | --- | --- | --- | --- | --- |
| Expertise | `strategie` | Stratégie supply chain | Supply chain strategy | `strategie-supply-chain` | `supply-chain-strategy` |
| Expertise | `operations` | Opérations logistiques | Logistics operations | `operations-logistiques` | `logistics-operations` |
| Expertise | `digital` | Transformation digitale | Digital transformation | `transformation-digitale` | `digital-transformation` |
| Expertise | `data` | Data & pilotage | Data & performance steering | `data-pilotage-performance` | `data-performance-steering` |
| Insight | `network-redesign` | Résilience supply chain | Supply chain resilience | `pourquoi-redesigner-les-reseaux-logistiques` | `why-logistics-networks-must-be-redesigned-before-being-optimized` |
| Insight | `warehouse-performance` | Performance entrepôt | Warehouse performance | `performance-entrepot-volumes-acceleration` | `what-strong-warehouse-operations-share-when-volumes-accelerate` |
| Insight | `digital-transformation` | Transformation digitale | Digital transformation | `projet-systeme-levier-execution-logistique` | `how-to-turn-a-system-project-into-a-real-logistics-execution-lever` |
| Perspective | `.perspective-trigger` | Perspective du cabinet | Firm perspective | `perspective-cabinet-performance-supply-chain-robuste` | `firm-perspective-building-more-robust-supply-chain-performance` |

## 5. Which Blocks Should Become Standalone SEO Pages

These are the priority blocks that deserve fully indexable pages because their content payloads are already structured and semantically rich enough to support dedicated URLs:

### Must become standalone pages

- 4 expertise cards
  - strategy
  - operations
  - digital
  - data / performance steering
- 3 insight cards
  - network redesign
  - warehouse performance under volume acceleration
  - systems project as logistics execution lever
- 1 long-form perspective page
  - cabinet / firm perspective on robust supply chain performance

### Why these blocks are strongest SEO candidates

- They already have unique titles and differentiated content payloads.
- Their content is too deep to remain trapped in modal-only rendering.
- They map naturally to category-intent and editorial-intent search behavior.
- They can strengthen internal linking from the homepage without breaking the one-page brand UX.

## 6. Shared Layout Parts That Can Be Reused

### Header

- FR: `frontend/index.html:25`
- EN: `frontend/index-en.html:25`
- Reusable elements:
  - logo / brand block
  - mobile menu button
  - main nav anchors
  - CTA button
  - language switcher

### Footer

- FR: `frontend/index.html:475`
- EN: `frontend/index-en.html:474`
- Reusable elements:
  - footer logo
  - positioning sentence
  - footer links
  - copyright

### Language switcher

- FR mobile: `frontend/index.html:42`
- FR desktop: `frontend/index.html:50`
- EN mobile: `frontend/index-en.html:42`
- EN desktop: `frontend/index-en.html:50`
- Shared styling hooks in CSS:
  - `frontend/styles.css:144` `.language-switcher`
  - `frontend/styles.css:150` `.language-switcher-mobile`

### Contact CTA block

- FR contact section wrapper: `frontend/index.html:442`
- EN contact section wrapper: `frontend/index-en.html:441`
- Shared structural value:
  - section label
  - transformation conversation CTA
  - email / phone / address / hours panel
- Shared layout styling:
  - `frontend/styles.css:205` `.contact-layout`
  - `frontend/styles.css:905` `.contact-layout`

## 7. Styling Hooks Relevant To Refactor

Key reusable CSS hooks:

- `frontend/styles.css:58` `.site-header`
- `frontend/styles.css:547` `.expertise-trigger`
- `frontend/styles.css:433` `.insight-trigger`
- `frontend/styles.css:859` `.perspective-trigger`
- `frontend/styles.css:934` `.expertise-modal`
- `frontend/styles.css:1072` `.insight-modal`
- `frontend/styles.css:1233` `.perspective-modal`
- `frontend/styles.css:928` `.site-footer`

Current standalone-page styling also already exists in the stylesheet:

- `frontend/styles.css:1853` `.page-main`
- page hero / breadcrumb / page-grid / page-section / steering-grid related rules below that point

This confirms the stylesheet is already prepared for shared standalone-page layouts.

## 8. Migration Logic Recommendation

### Recommended migration direction

1. Keep `index.html` and `index-en.html` as premium one-page brand landing pages.
2. Treat homepage cards as discovery and navigation surfaces.
3. Move all modal-grade content into crawlable HTML pages with one clear `h1`, unique title, unique meta description, and semantic section hierarchy.
4. Preserve card interaction as direct navigation, not as JS-only disclosure.
5. Retain modal code only if there is a deliberate UX reason to keep previews.
6. If modals are no longer part of the intended UX, remove the legacy modal layer after confirming no dependency remains.

### Recommended page families

- Expertise pages:
  - context / challenges
  - what we address
  - what we do
  - expected outcomes
  - typical contexts
  - CTA
- Insight pages:
  - introduction
  - problem framing
  - strategic analysis
  - operational implications
  - conclusion / CTA
- Perspective page:
  - introduction
  - driving forces 2026-2036
  - implications
  - recommendations
  - strategic steering grid
  - conclusion

## 9. Key Audit Takeaways

- The legacy modal architecture is still fully present in the markup, CSS, and JavaScript.
- The content sources for expertise, insight, and perspective are clearly isolated in structured JS objects.
- The trigger keys are stable and map cleanly across FR and EN.
- The homepage already contains the shared layout pieces needed for reuse on standalone pages.
- The strongest SEO migration path is to formalize each modal content block as a dedicated page and then remove or deprecate the modal layer once the standalone architecture is complete.
