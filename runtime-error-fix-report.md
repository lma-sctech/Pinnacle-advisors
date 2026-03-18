# Runtime Error Fix Report

## Root Cause

The homepage scripts referenced helper functions that no longer existed in the file:

- `animateImpactList()`
- `refreshContextCardCollections()`

Observed blocking error:

- `Uncaught ReferenceError: animateImpactList is not defined`

Why it happened:

- `setActiveApproachPhase()` still called `animateImpactList()`
- the context carousel setup still called `refreshContextCardCollections()`
- both helpers had been removed or lost in an earlier cleanup/refactor pass

## Files Modified

- `frontend/script.js`
- `frontend/script-en.js`

## Exact Fix Applied

### Restored `refreshContextCardCollections()`

Added a helper that:

- refreshes `contextAllCards`
- refreshes `contextRealCards`
- excludes cloned carousel cards from the real-card collection
- recalculates loop span safely

### Restored `animateImpactList()`

Added a helper that:

- safely exits if the impact block is absent
- removes the `is-animating` class
- forces a reflow
- re-applies `is-animating`

This matches the existing CSS animation hook:

- `.approach-detail__block--impact.is-animating`

### Stabilized resize behavior

Updated the resize handler to call:

- `refreshContextCardCollections()`

instead of only:

- `recalculateContextLoopSpan()`

This keeps the context-card collections in sync after layout changes.

## Behavior Preserved Or Changed

Preserved:

- approach phase switching still updates title, intro, focus list and impact list
- impact block animation can run again without throwing
- context carousel looping logic still works with refreshed card collections
- no visual UX was intentionally changed

Changed:

- missing helper calls are now resolved instead of crashing script execution

## Validation

- `animateImpactList()` reference now resolves in both homepage scripts
- `refreshContextCardCollections()` reference now resolves in both homepage scripts
- no missing-function reference remains for these helpers in:
  - `frontend/script.js`
  - `frontend/script-en.js`
- syntax validation should be run after this fix before deploy

## Remaining Risks

- Browser-level runtime validation was not executed here, so a final live smoke test is still recommended on:
  - homepage initial load
  - approach-phase click / hover changes
  - context carousel interaction
  - tracking initialization after homepage load

- The FR homepage script still contains mojibake text in some string literals, but that issue is separate from this runtime fix and does not affect the missing-function error directly.
