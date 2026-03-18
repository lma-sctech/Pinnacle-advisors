# Tracking Implementation Report

## Files Modified

- `frontend/js/tracking.js`
- `frontend/script.js`
- `frontend/script-en.js`
- `frontend/js/page-enhancements.js`

## Event Model Implemented

### `card_click`

Tracked for:

- homepage expertise cards
- homepage insight cards
- homepage perspective feature block
- related internal cards on standalone pages

Parameters:

- `card_family`
- `card_name`
- `page_language`
- `source_page`
- `destination_url`

### `contact_click`

Tracked for:

- `mailto:` links
- `tel:` links

Parameters:

- `contact_type`
- `cta_label`
- `page_language`
- `source_page`
- `destination_value`

### `cta_click`

Tracked for:

- header CTA
- hero buttons
- page CTA buttons
- back-to-home links
- CTA buttons in standalone pages

Parameters:

- `cta_name`
- `cta_label`
- `cta_location`
- `page_language`
- `source_page`
- `destination_url`

### `language_switch`

Tracked for:

- all FR / EN language switch links on homepage and internal pages

Parameters:

- `from_language`
- `to_language`
- `source_page`
- `destination_url`

### `navigation_click`

Tracked for:

- brand / logo click
- header navigation links
- footer navigation links
- breadcrumb links
- homepage anchor menu links
- internal-page links back to homepage anchors

Parameters:

- `nav_location`
- `nav_label`
- `nav_target_type`
- `page_language`
- `source_page`
- `destination_url`

### `outbound_click`

Generic helper implemented for:

- external links
- file download links matching common office / archive extensions

Parameters:

- `link_url`
- `link_domain`
- `link_text`
- `page_language`
- `source_page`

### `content_engagement_30s`

Parameters:

- `page_language`
- `source_page`
- `page_type`

### `content_engagement_60s`

Parameters:

- `page_language`
- `source_page`
- `page_type`

### `scroll_depth`

Thresholds implemented:

- `25`
- `50`
- `75`
- `90`

Parameters:

- `scroll_percent`
- `page_language`
- `source_page`
- `page_type`

## Shared Tracking Layer

Implemented in:

- `frontend/js/tracking.js`

Responsibilities:

- initialize and safely use `window.dataLayer`
- normalize page language
- infer page type
- classify cards, CTAs and navigation links
- prevent duplicate scroll threshold firing
- prevent duplicate timed engagement firing
- attach delegated click tracking without modifying UX

## Selectors / Elements Tracked

Homepage FR + EN:

- `.brand`
- `.header-cta`
- `.language-switcher a`
- `.site-nav a`
- `.footer-links a`
- `.button`
- `.editorial-card.expertise-trigger`
- `.insight-card`
- `.insight-hero.perspective-trigger`
- `a[href^="mailto:"]`
- `a[href^="tel:"]`

Internal pages FR + EN:

- `.brand`
- `.header-cta`
- `.language-switcher a`
- `.site-nav a`
- `.footer-links a`
- `.breadcrumb a`
- `.back-link`
- `.text-link`
- `.ghost-button`
- `.related-card`
- `a[href^="mailto:"]`
- `a[href^="tel:"]`

## New Data Attributes Added

None.

The tracking layer was implemented with delegated listeners and metadata inference from:

- `href`
- visible text
- existing classes
- DOM position

## Timed Engagement Logic

- Uses cumulative visible time, not naive elapsed time.
- Milestones at `30s` and `60s`.
- Each milestone fires once per page load.
- No milestone fires while the page is hidden.
- If the page becomes hidden before a milestone, timing pauses and resumes only when visible again.

## Scroll Threshold Logic

- Tracks `25`, `50`, `75`, `90` percent scroll depth.
- Each threshold fires once per page load.
- Uses document scrollable height and current scroll position.

## Validation Performed

- `node --check frontend/js/tracking.js`
- `node --check frontend/script.js`
- `node --check frontend/script-en.js`
- `node --check frontend/js/page-enhancements.js`

Additional checks:

- confirmed homepage and internal pages all load an existing runtime script that now bootstraps the shared tracking helper
- confirmed FR and EN key interaction points are covered by selectors in the implemented tracking logic

## Known Limitations

- Contact-section anchor CTAs such as `#contact` are tracked as `cta_click`, while `contact_click` is reserved for `mailto:` and `tel:` interactions because its parameter model expects `email | phone`.
- `outbound_click` is currently generic and future-ready; the current site has little or no external-link volume beyond standard contact links.
- Navigation links inside the same shared header structure are classified as `mobile_menu` only when the mobile menu is open on small screens; otherwise they are tracked as `header`.
