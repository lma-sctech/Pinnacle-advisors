# Deployment Parity Check

## Scope Checked

- `frontend/index.html`
- `frontend/index-en.html`
- `frontend/script.js`
- `frontend/script-en.js`
- `frontend/styles.css`
- `frontend/js/page-enhancements.js`
- `frontend/pages/fr/*.html`
- `frontend/pages/en/*.html`

## Summary

The active source code in this repository is clean with respect to the legacy modal architecture.

No modal containers, modal titles, modal close buttons, modal placeholders, modal-specific selectors or modal-opening functions remain in the active homepage source or active shared assets.

This means the most likely explanation for modal residue still appearing in the live homepage output is **deployment mismatch**, not active source code.

## What Was Checked

### Homepage source markup

Checked:

- `frontend/index.html`
- `frontend/index-en.html`

Confirmed absent:

- `#expertise-modal`
- `#insight-modal`
- `#perspective-modal`
- `data-close-modal`
- modal close buttons
- hidden modal panels
- orphan modal headings
- empty modal wrapper sections

### Homepage scripts

Checked:

- `frontend/script.js`
- `frontend/script-en.js`

Confirmed absent:

- `openExpertiseModal`
- `openInsightModal`
- `openPerspectiveModal`
- modal render helpers tied to removed modal DOM
- JS-based modal injection logic

### Shared assets

Checked:

- `frontend/styles.css`
- `frontend/js/page-enhancements.js`

Confirmed absent:

- modal CSS blocks
- modal-only selectors
- runtime JS that injects modal nodes into the DOM

### Repository structure

Confirmed:

- there is no duplicate `index.html` or `index-en.html` outside `frontend/`
- there is no build output folder generating alternative homepage HTML
- there is no service worker registration or cache-manifest logic in the checked source

## Root Cause Assessment

Based on the current repository state, the live modal residue is **not** caused by:

- duplicated modal markup still present in active homepage source
- homepage JavaScript injecting leftover modal nodes
- CSS/HTML mismatch creating phantom modal panels
- a local build artifact generated from another HTML source inside this repo

Most likely cause:

- **undeployed code**, or
- **stale published files / CDN cache / browser cache**

Why this is the most likely cause:

- the active homepage source files are already clean
- no build system or service worker was found that could recreate old modal markup at runtime
- no second homepage source exists in the repository
- no modal strings remain in the active homepage and shared asset scope

## Cleanup Performed

No modal-related source cleanup was required in the active homepage files because the source is already clean.

The deployment-parity check did confirm that the active source already excludes:

- modal containers
- modal titles
- modal close buttons
- modal placeholders
- modal injection functions
- modal-specific CSS

## Homepage Card Verification

Confirmed all homepage cards still link directly to standalone pages with real crawlable anchors.

French homepage:

- `./pages/fr/strategie-supply-chain.html`
- `./pages/fr/operations-logistiques.html`
- `./pages/fr/transformation-digitale.html`
- `./pages/fr/data-pilotage-performance.html`
- `./pages/fr/pourquoi-redesigner-les-reseaux-logistiques.html`
- `./pages/fr/performance-entrepot-volumes-acceleration.html`
- `./pages/fr/projet-systeme-levier-execution-logistique.html`
- `./pages/fr/perspective-cabinet-performance-supply-chain-robuste.html`

English homepage:

- `./pages/en/supply-chain-strategy.html`
- `./pages/en/logistics-operations.html`
- `./pages/en/digital-transformation.html`
- `./pages/en/data-performance-steering.html`
- `./pages/en/why-logistics-networks-must-be-redesigned-before-being-optimized.html`
- `./pages/en/what-strong-warehouse-operations-share-when-volumes-accelerate.html`
- `./pages/en/how-to-turn-a-system-project-into-a-real-logistics-execution-lever.html`
- `./pages/en/firm-perspective-building-more-robust-supply-chain-performance.html`

## Source vs Live Output Status

### Source code

Current source code is aligned with the intended post-modal architecture.

### Live output

If the live homepage still renders modal residue, the live deployment is not yet aligned with the current source state.

## What Was Removed

Nothing further had to be removed in this pass from the active source, because the modal layer had already been removed from the checked files.

## What Still Needs Deployment

If the live site still shows modal residue, deploy the current contents of:

- `frontend/index.html`
- `frontend/index-en.html`
- `frontend/script.js`
- `frontend/script-en.js`
- `frontend/styles.css`

Recommended deployment follow-up:

- invalidate CDN cache if one is in use
- hard-refresh browser cache
- verify the production host is serving `frontend/index.html` and `frontend/index-en.html` from the current revision
- verify the published scripts are the current `script.js` and `script-en.js`, not older cached copies

## Final Conclusion

Source code and intended local output are aligned.

If the live homepage still shows modal residue, the issue is most consistently explained by **undeployed or stale published assets**, not by remaining modal code in the current repository source.
