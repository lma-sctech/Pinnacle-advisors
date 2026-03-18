# Deployment Root Cause

## Executive Summary

The public homepage is still serving an **older deployed revision** that contains the legacy modal architecture.

The repository working tree on this machine has the post-modal refactor, but `HEAD` and `origin/main` are still on commit `ca78159`, which still contains:

- homepage modal containers
- modal close buttons
- modal section headings
- modal JavaScript
- modal CSS

So the production mismatch is **not** caused by hidden runtime injection in the current local source.

It is caused by the fact that the **live site is aligned with the old tracked revision**, while the cleaned refactor exists only in the local modified workspace and has not yet become the deployed source of truth.

## What Was Investigated

### Local deployment-related repository state

Checked:

- git branch status
- tracked commit history for homepage files
- presence of deployment scripts or hosting config
- current working tree diffs

Findings:

- current branch: `main`
- tracked remote: `origin`
- `HEAD` and `origin/main` both point to `ca78159`
- no deployment config was found in the repository
- no build script or hosting manifest was found
- no alternate published output folder exists in the repo

This strongly suggests the site is deployed either:

- manually from the `frontend/` folder, or
- from an external host configuration not committed in this repository

## Actual Deployment Source Path

Based on the public URLs and asset paths, the actual published source is the content of:

- `frontend/index.html`
- `frontend/index-en.html`
- `frontend/script.js`
- `frontend/script-en.js`
- `frontend/styles.css`
- `frontend/img/*`
- `frontend/logo-pinnacle.png`

published at the site root:

- `/`
- `/index-en.html`
- `/script.js`
- `/script-en.js`
- `/styles.css`
- `/img/...`

## Actual Published Files

The live homepage at `https://www.pinnacle-advisors.tech/` is serving a version equivalent to the tracked old homepage source, including:

- modal containers
- repeated `Fermer`
- empty modal headings
- modal section shells for expertise and perspective

Observed in live output:

- `Enjeux traités`
- `Ce que nous faisons`
- `Résultats recherchés`
- `Contextes typiques`
- `Forces motrices 2026–2036`
- `Implications`
- `Recommandations 2026–2036`
- `Grille de pilotage stratégique`

## Mismatch Found

### Local working tree

Current local source removes modal markup from:

- `frontend/index.html`
- `frontend/index-en.html`

and removes modal logic from:

- `frontend/script.js`
- `frontend/script-en.js`
- `frontend/styles.css`

### Tracked Git revision

`HEAD` and `origin/main` still point to `ca78159`, which still contains:

- modal homepage cards using `data-expertise` / `data-insight`
- modal DOM blocks at the end of the homepage
- modal CSS blocks
- modal JavaScript open/close logic

### Live public site

The live homepage output matches the old modal-bearing tracked revision, not the cleaned local workspace.

## Exact Reason Legacy Modal Residue Is Still Live

The modal cleanup has been done **locally in uncommitted / unpushed changes**, but the public site is still serving the older tracked revision.

Evidence:

- `git branch -vv` shows:
  - `main ca78159 [origin/main] Add hero slideshow and image metadata updates`
- `git status --short` shows the cleaned homepage files are still modified locally:
  - `frontend/index.html`
  - `frontend/index-en.html`
  - `frontend/script.js`
  - `frontend/script-en.js`
  - `frontend/styles.css`
- the live homepage output still contains the exact old modal blocks found in commit `ca78159`

So the root cause is:

- **the deployed source is still the old tracked revision**

not:

- JS injecting modal residue from the cleaned source
- hidden duplicate markup in the current local homepage source
- stale modal code still present in the cleaned local files

## Why This Is Not a Pure CDN Cache Issue

A CDN cache alone is unlikely to explain the full mismatch because the live HTML still exposes the exact old modal block structure that exists in the old tracked revision.

That indicates the server is still serving the old homepage artifact itself, not just a partially cached asset.

Cache invalidation may still help after redeploy, but cache is not the primary root cause.

## Exact Fix Required

### Required first

Publish the cleaned local workspace version of these files:

- `frontend/index.html`
- `frontend/index-en.html`
- `frontend/script.js`
- `frontend/script-en.js`
- `frontend/styles.css`
- `frontend/pages/fr/*`
- `frontend/pages/en/*`
- `frontend/js/page-enhancements.js`

### Operationally

One of these must happen:

1. Commit and push the cleaned refactor to the branch/environment that the host actually deploys from.
2. Or manually upload the cleaned `frontend/` contents to the production document root.

### After publish

- invalidate CDN cache if applicable
- hard refresh browser cache
- verify the public homepage source no longer contains modal containers

## Is A Fresh Deploy Alone Enough?

### Yes, if:

- the fresh deploy uses the **current cleaned local files**
- and overwrites the currently published root files

### No, if:

- the deploy is run from the current tracked remote revision (`origin/main`) without first pushing the cleanup

In that case, a “fresh deploy” would simply redeploy the old modal version again.

## Is Host-Side Cleanup Required?

For the modal residue itself, **host-side cleanup is probably not required** if the deploy properly overwrites:

- `/index.html`
- `/index-en.html`
- `/script.js`
- `/script-en.js`
- `/styles.css`

Why:

- the residue comes from old homepage HTML still being served
- not from orphaned auxiliary files alone

Host-side cleanup may still be useful if the hosting workflow does not overwrite old files reliably, but based on the evidence, the blocking issue is the stale deployed revision, not a hidden extra file on the server.

## Deployment Process Visibility Limits

I could not inspect a committed deployment script or hosting config because none exists in this repository.

That means the exact host mechanism is not versioned here. What can be established with confidence is:

- what the public site is serving
- what `origin/main` contains
- what the current local workspace contains
- and where the mismatch sits

## Final Conclusion

The real root cause is:

- **production is serving the old modal-bearing tracked revision (`ca78159` / `origin/main`)**
- while the cleaned SEO refactor exists only in the local modified workspace

So the required fix is:

- deploy the cleaned local `frontend/` tree, not the currently tracked old revision

Fresh deploy status:

- **Fresh deploy is enough only if it deploys the cleaned local files**
- **Fresh deploy is not enough if it redeploys current `origin/main` unchanged**
