# dataLayer Events Audit

## Scope Scanned

- `frontend/index.html`
- `frontend/index-en.html`
- `frontend/script.js`
- `frontend/script-en.js`
- `frontend/js/*`
- `frontend/pages/fr/*.html`
- `frontend/pages/en/*.html`

## Summary

All tracking events are implemented through a shared helper in:

- `frontend/js/tracking.js`

There are no inline `dataLayer.push(...)` calls in HTML files.
There are no direct `window.dataLayer.push(...)` calls outside the shared helper.

The shared wrapper is:

- `pushTrackingEvent(eventName, params)`

Implementation:

```js
function pushTrackingEvent(eventName, params) {
  ensureDataLayer().push({
    event: eventName,
    ...params,
  });
}
```

This guarantees every pushed event contains an `event` key, which is mandatory for GTM.

## Unique Event Names

- `card_click`
- `contact_click`
- `cta_click`
- `language_switch`
- `navigation_click`
- `outbound_click`
- `content_engagement_30s`
- `content_engagement_60s`
- `scroll_depth`

## Event Breakdown

### Card Interactions

----------------------------------------
Event name: `card_click`

Example payload:

```js
{
  event: "card_click",
  card_family: "expertise",
  card_name: "strategie-supply-chain",
  page_language: "fr",
  source_page: "/index.html",
  destination_url: "/pages/fr/strategie-supply-chain.html"
}
```

Full object pushed:

```js
{
  event: "card_click",
  card_family: getCardFamily(link, parsedUrl),
  card_name: link.dataset.trackName || getPathSlug(parsedUrl?.url.pathname || "") || slugify(getLinkLabel(link)),
  page_language: getPageLanguage(),
  source_page: getSourcePage(),
  destination_url: parsedUrl?.normalized || link.getAttribute("href") || ""
}
```

Parameters:

- `card_family`
- `card_name`
- `page_language`
- `source_page`
- `destination_url`

Triggered on:

- homepage expertise cards
- homepage insight cards
- homepage perspective feature block
- related internal cards on standalone pages

Trigger logic:

- delegated click listener on `a[href]`
- filtered by:
  - `.editorial-card[href]`
  - `.insight-card[href]`
  - `.insight-hero[href]`
  - `.related-card[href]`

Files:

- `frontend/js/tracking.js`
- markup source examples:
  - `frontend/index.html`
  - `frontend/index-en.html`
  - `frontend/pages/fr/*.html`
  - `frontend/pages/en/*.html`
----------------------------------------

### Contact Interactions

----------------------------------------
Event name: `contact_click`

Example payload:

```js
{
  event: "contact_click",
  contact_type: "email",
  cta_label: "Nous écrire",
  page_language: "fr",
  source_page: "/index.html",
  destination_value: "contact@pinnacle-advisors.tech"
}
```

Full object pushed:

```js
{
  event: "contact_click",
  contact_type: contactType,
  cta_label: getLinkLabel(link),
  page_language: getPageLanguage(),
  source_page: getSourcePage(),
  destination_value: destinationValue
}
```

Parameters:

- `contact_type`
- `cta_label`
- `page_language`
- `source_page`
- `destination_value`

Triggered on:

- all `mailto:` links
- all `tel:` links

Trigger logic:

- delegated click listener on `a[href]`
- filtered by:
  - `href.startsWith("mailto:")`
  - `href.startsWith("tel:")`

Files:

- `frontend/js/tracking.js`
- markup source examples:
  - homepage contact CTAs in `frontend/index.html`
  - homepage contact CTAs in `frontend/index-en.html`
  - internal page contact/sidebar links in `frontend/pages/fr/*.html`
  - internal page contact/sidebar links in `frontend/pages/en/*.html`
----------------------------------------

### CTA Interactions

----------------------------------------
Event name: `cta_click`

Example payload:

```js
{
  event: "cta_click",
  cta_name: "echanger-avec-nous",
  cta_label: "Échanger avec nous",
  cta_location: "hero",
  page_language: "fr",
  source_page: "/index.html",
  destination_url: "/index.html#contact"
}
```

Full object pushed:

```js
{
  event: "cta_click",
  cta_name: link.dataset.trackName || slugify(getLinkLabel(link)) || getPathSlug(parsedUrl?.url.pathname || ""),
  cta_label: getLinkLabel(link),
  cta_location: link.dataset.trackLocation || getCtaLocation(link),
  page_language: getPageLanguage(),
  source_page: getSourcePage(),
  destination_url: parsedUrl?.normalized || link.getAttribute("href") || ""
}
```

Parameters:

- `cta_name`
- `cta_label`
- `cta_location`
- `page_language`
- `source_page`
- `destination_url`

Triggered on:

- `.header-cta`
- `.button`
- `.text-link`
- `.ghost-button`
- `.back-link`

Trigger logic:

- delegated click listener on `a[href]`
- location inferred from DOM:
  - `header`
  - `footer`
  - `contact_section`
  - `hero`
  - `page_body`

Files:

- `frontend/js/tracking.js`
- markup source examples:
  - hero buttons on `frontend/index.html`
  - hero buttons on `frontend/index-en.html`
  - header CTA on all pages
  - internal page CTAs in `frontend/pages/fr/*.html`
  - internal page CTAs in `frontend/pages/en/*.html`
----------------------------------------

### Language Switch

----------------------------------------
Event name: `language_switch`

Example payload:

```js
{
  event: "language_switch",
  from_language: "fr",
  to_language: "en",
  source_page: "/index.html",
  destination_url: "/index-en.html"
}
```

Full object pushed:

```js
{
  event: "language_switch",
  from_language: getPageLanguage(),
  to_language: toLanguage,
  source_page: getSourcePage(),
  destination_url: parsedUrl?.normalized || link.getAttribute("href") || ""
}
```

Parameters:

- `from_language`
- `to_language`
- `source_page`
- `destination_url`

Triggered on:

- all language switch links inside `.language-switcher`

Trigger logic:

- delegated click listener on `a[href]`
- first matching rule:
  - `link.closest(".language-switcher")`

Files:

- `frontend/js/tracking.js`
- markup source examples:
  - `frontend/index.html`
  - `frontend/index-en.html`
  - `frontend/pages/fr/*.html`
  - `frontend/pages/en/*.html`
----------------------------------------

### Navigation

----------------------------------------
Event name: `navigation_click`

Example payload:

```js
{
  event: "navigation_click",
  nav_location: "header",
  nav_label: "À propos",
  nav_target_type: "anchor",
  page_language: "fr",
  source_page: "/index.html",
  destination_url: "/index.html#about"
}
```

Full object pushed:

```js
{
  event: "navigation_click",
  nav_location: link.dataset.navLocation || getNavLocation(link),
  nav_label: navLabel,
  nav_target_type: getNavTargetType(parsedUrl),
  page_language: getPageLanguage(),
  source_page: getSourcePage(),
  destination_url: parsedUrl?.normalized || link.getAttribute("href") || ""
}
```

Parameters:

- `nav_location`
- `nav_label`
- `nav_target_type`
- `page_language`
- `source_page`
- `destination_url`

Triggered on:

- `.brand`
- links inside `.site-nav`
- links inside `footer.site-footer .footer-links`
- links inside `.breadcrumb`

Trigger logic:

- delegated click listener on `a[href]`
- `.brand` is handled separately and immediately
- other nav clicks are inferred from DOM position

Possible values:

- `nav_location`
  - `header`
  - `footer`
  - `mobile_menu`
- `nav_target_type`
  - `anchor`
  - `homepage_anchor`
  - `internal_page`

Files:

- `frontend/js/tracking.js`
- markup source examples:
  - `frontend/index.html`
  - `frontend/index-en.html`
  - `frontend/pages/fr/*.html`
  - `frontend/pages/en/*.html`
----------------------------------------

### Other

----------------------------------------
Event name: `outbound_click`

Example payload:

```js
{
  event: "outbound_click",
  link_url: "https://external-domain.example/path",
  link_domain: "external-domain.example",
  link_text: "Example",
  page_language: "en",
  source_page: "/pages/en/supply-chain-strategy.html"
}
```

Full object pushed:

```js
{
  event: "outbound_click",
  link_url: parsedUrl.normalized,
  link_domain: parsedUrl.url.hostname,
  link_text: getLinkLabel(link),
  page_language: getPageLanguage(),
  source_page: getSourcePage()
}
```

Parameters:

- `link_url`
- `link_domain`
- `link_text`
- `page_language`
- `source_page`

Triggered on:

- external links
- file download links matching:
  - `pdf`
  - `doc`
  - `docx`
  - `xls`
  - `xlsx`
  - `csv`
  - `zip`
  - `ppt`
  - `pptx`

Current repository status:

- helper exists and is active
- no significant external-link inventory was found in the scanned markup besides contact links

Files:

- `frontend/js/tracking.js`
----------------------------------------

### Scroll / Engagement

----------------------------------------
Event name: `scroll_depth`

Example payload:

```js
{
  event: "scroll_depth",
  scroll_percent: 50,
  page_language: "fr",
  source_page: "/pages/fr/strategie-supply-chain.html",
  page_type: "expertise"
}
```

Full object pushed:

```js
{
  event: "scroll_depth",
  scroll_percent: threshold,
  page_language: getPageLanguage(),
  source_page: getSourcePage(),
  page_type: inferPageType()
}
```

Parameters:

- `scroll_percent`
- `page_language`
- `source_page`
- `page_type`

Trigger:

- window scroll reaching thresholds:
  - `25`
  - `50`
  - `75`
  - `90`

Rules:

- each threshold fires once per page load

Files:

- `frontend/js/tracking.js`
----------------------------------------

----------------------------------------
Event name: `content_engagement_30s`

Example payload:

```js
{
  event: "content_engagement_30s",
  page_language: "en",
  source_page: "/index-en.html",
  page_type: "home"
}
```

Full object pushed:

```js
{
  event: "content_engagement_30s",
  page_language: getPageLanguage(),
  source_page: getSourcePage(),
  page_type: inferPageType()
}
```

Parameters:

- `page_language`
- `source_page`
- `page_type`

Trigger:

- user accumulates 30 seconds of visible time on page

Rules:

- fires once per page load
- pauses while page is hidden

Files:

- `frontend/js/tracking.js`
----------------------------------------

----------------------------------------
Event name: `content_engagement_60s`

Example payload:

```js
{
  event: "content_engagement_60s",
  page_language: "fr",
  source_page: "/pages/fr/perspective-cabinet-performance-supply-chain-robuste.html",
  page_type: "perspective"
}
```

Full object pushed:

```js
{
  event: "content_engagement_60s",
  page_language: getPageLanguage(),
  source_page: getSourcePage(),
  page_type: inferPageType()
}
```

Parameters:

- `page_language`
- `source_page`
- `page_type`

Trigger:

- user accumulates 60 seconds of visible time on page

Rules:

- fires once per page load
- pauses while page is hidden

Files:

- `frontend/js/tracking.js`
----------------------------------------

## Mapping Table

| Event name | Parameters | Trigger | Files |
| --- | --- | --- | --- |
| `card_click` | `card_family`, `card_name`, `page_language`, `source_page`, `destination_url` | Click on expertise cards, insight cards, perspective block, related cards | `frontend/js/tracking.js`, markup in homepages and internal pages |
| `contact_click` | `contact_type`, `cta_label`, `page_language`, `source_page`, `destination_value` | Click on `mailto:` and `tel:` links | `frontend/js/tracking.js`, markup in homepages and internal pages |
| `cta_click` | `cta_name`, `cta_label`, `cta_location`, `page_language`, `source_page`, `destination_url` | Click on main CTAs, back links, page CTA buttons | `frontend/js/tracking.js`, markup in homepages and internal pages |
| `language_switch` | `from_language`, `to_language`, `source_page`, `destination_url` | Click on FR / EN switch links | `frontend/js/tracking.js`, homepages and internal pages |
| `navigation_click` | `nav_location`, `nav_label`, `nav_target_type`, `page_language`, `source_page`, `destination_url` | Click on brand, header nav, footer nav, breadcrumb links | `frontend/js/tracking.js`, homepages and internal pages |
| `outbound_click` | `link_url`, `link_domain`, `link_text`, `page_language`, `source_page` | Click on external or file links | `frontend/js/tracking.js` |
| `scroll_depth` | `scroll_percent`, `page_language`, `source_page`, `page_type` | Reaching 25/50/75/90% page scroll | `frontend/js/tracking.js` |
| `content_engagement_30s` | `page_language`, `source_page`, `page_type` | 30 seconds visible-time milestone | `frontend/js/tracking.js` |
| `content_engagement_60s` | `page_language`, `source_page`, `page_type` | 60 seconds visible-time milestone | `frontend/js/tracking.js` |

## Bootstrap / Where Tracking Is Loaded

Tracking is bootstrapped by:

- `frontend/script.js`
- `frontend/script-en.js`
- `frontend/js/page-enhancements.js`

These files dynamically load:

- `frontend/js/tracking.js`

Homepage coverage:

- `frontend/index.html` loads `./script.js`
- `frontend/index-en.html` loads `./script-en.js`

Internal page coverage:

- all standalone pages load `../../js/page-enhancements.js`

## Duplicates / Naming Audit

### Mandatory `event` key

Status:

- OK

Every tracked payload is sent through `pushTrackingEvent()`, which injects:

- `event: eventName`

### Duplicate event names

Status:

- No duplicate naming variants found for the same concept.

### Inconsistent naming

Status:

- No event-name inconsistency found.

Minor modeling note:

- `contact_click` is reserved for `mailto:` and `tel:` interactions only.
- Contact-section anchor links such as `#contact` are intentionally tracked as `cta_click` or `navigation_click`, not `contact_click`.

## Recommendations

### Missing events

- No obvious critical business event is missing relative to the currently implemented model.

### Potential improvements

- Add explicit `data-track-name` attributes on a few strategic CTAs if GTM stakeholders want guaranteed stable naming independent of visible text changes.
- Add explicit `data-track-family="context"` on any future clickable context cards if those cards become links later.
- If GTM needs richer form-lead tracking later, add dedicated events such as `form_start` and `form_submit` when a real form exists.

### Data quality notes

- `card_name` is inferred from destination slug or link label, which is robust for the current site structure.
- `page_type` is inferred from URL slug sets in `frontend/js/tracking.js`; if new page families are added later, this helper should be updated.
- `outbound_click` is implemented generically but may fire rarely on the current site because the link inventory is mostly internal plus contact links.
