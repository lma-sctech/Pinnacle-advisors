(function () {
  const GLOBAL_KEY = "__pinnacleTrackingInitialized";
  const SCROLL_THRESHOLDS = [25, 50, 75, 90];
  const ENGAGEMENT_MILESTONES = [30, 60];
  const FILE_EXTENSION_PATTERN = /\.(pdf|docx?|xlsx?|csv|zip|pptx?)$/i;
  const EXPERTISE_SLUGS = new Set([
    "strategie-supply-chain",
    "operations-logistiques",
    "transformation-digitale",
    "data-pilotage-performance",
    "supply-chain-strategy",
    "logistics-operations",
    "digital-transformation",
    "data-performance-steering",
  ]);
  const INSIGHT_SLUGS = new Set([
    "pourquoi-redesigner-les-reseaux-logistiques",
    "performance-entrepot-volumes-acceleration",
    "projet-systeme-levier-execution-logistique",
    "why-logistics-networks-must-be-redesigned-before-being-optimized",
    "what-strong-warehouse-operations-share-when-volumes-accelerate",
    "how-to-turn-a-system-project-into-a-real-logistics-execution-lever",
  ]);
  const PERSPECTIVE_SLUGS = new Set([
    "perspective-cabinet-performance-supply-chain-robuste",
    "firm-perspective-building-more-robust-supply-chain-performance",
  ]);

  function ensureDataLayer() {
    window.dataLayer = window.dataLayer || [];
    return window.dataLayer;
  }

  function pushTrackingEvent(eventName, params) {
    ensureDataLayer().push({
      event: eventName,
      ...params,
    });
  }

  function getPageLanguage() {
    const lang = (document.documentElement.lang || "").toLowerCase();
    if (lang.startsWith("fr")) return "fr";
    if (lang.startsWith("en")) return "en";
    return window.location.pathname.includes("/fr/") ? "fr" : "en";
  }

  function getSourcePage() {
    const path = window.location.pathname || "/";
    return `${path}${window.location.search || ""}`;
  }

  function normalizeText(value) {
    return (value || "").replace(/\s+/g, " ").trim();
  }

  function slugify(value) {
    return normalizeText(value)
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
  }

  function getPathSlug(pathname) {
    const segments = pathname.split("/").filter(Boolean);
    const lastSegment = segments[segments.length - 1] || "";
    return lastSegment.replace(/\.html?$/i, "");
  }

  function inferPageType(pathname = window.location.pathname) {
    const lowerPath = pathname.toLowerCase();
    const slug = getPathSlug(lowerPath);

    if (
      lowerPath === "/" ||
      lowerPath.endsWith("/index.html") ||
      lowerPath.endsWith("/index-en.html") ||
      lowerPath === "/index.html" ||
      lowerPath === "/index-en.html"
    ) {
      return "home";
    }

    if (PERSPECTIVE_SLUGS.has(slug)) return "perspective";
    if (EXPERTISE_SLUGS.has(slug)) return "expertise";
    if (INSIGHT_SLUGS.has(slug)) return "insight";
    return "generic";
  }

  function parseUrl(href) {
    try {
      const url = new URL(href, window.location.href);
      const isExternal = url.origin !== window.location.origin;
      return {
        url,
        isExternal,
        normalized: isExternal ? url.href : `${url.pathname}${url.search}${url.hash}`,
      };
    } catch (error) {
      return null;
    }
  }

  function getLinkLabel(link) {
    return normalizeText(
      link.dataset.trackLabel ||
        link.getAttribute("aria-label") ||
        link.textContent ||
        link.title ||
        ""
    );
  }

  function getCardFamily(link, parsedUrl) {
    if (
      link.matches(".editorial-card.expertise-trigger") ||
      link.matches("[data-track-family='expertise']")
    ) {
      return "expertise";
    }

    if (
      link.matches(".insight-card, .insight-trigger") ||
      link.matches("[data-track-family='insight']")
    ) {
      return "insight";
    }

    if (
      link.matches(".insight-hero, .perspective-trigger") ||
      link.matches("[data-track-family='perspective']")
    ) {
      return "perspective";
    }

    if (link.matches(".context-card, [data-track-family='context']")) {
      return "context";
    }

    const destinationType = parsedUrl ? inferPageType(parsedUrl.url.pathname) : "generic";
    if (destinationType === "expertise") return "expertise";
    if (destinationType === "insight") return "insight";
    if (destinationType === "perspective") return "perspective";
    return "context";
  }

  function shouldTrackCard(link) {
    return (
      link.matches(".editorial-card[href]") ||
      link.matches(".insight-card[href]") ||
      link.matches(".insight-hero[href]") ||
      link.matches(".related-card[href]")
    );
  }

  function getNavLocation(link) {
    if (link.closest(".language-switcher-mobile")) return "mobile_menu";
    if (link.closest("footer.site-footer")) return "footer";

    const inHeader = !!link.closest(".site-header");
    const mobileMenuOpen =
      inHeader &&
      window.innerWidth <= 900 &&
      document.querySelector(".menu-button")?.getAttribute("aria-expanded") === "true";

    if (mobileMenuOpen && link.closest(".site-nav")) return "mobile_menu";
    if (inHeader) return "header";
    return "header";
  }

  function getNavTargetType(parsedUrl) {
    if (!parsedUrl) return "internal_page";
    const { url } = parsedUrl;
    const currentPath = window.location.pathname;

    if (url.hash && url.pathname === currentPath) return "anchor";

    if (
      url.hash &&
      (url.pathname.endsWith("/index.html") ||
        url.pathname.endsWith("/index-en.html") ||
        url.pathname === "/index.html" ||
        url.pathname === "/index-en.html" ||
        url.pathname === "/")
    ) {
      return "homepage_anchor";
    }

    return "internal_page";
  }

  function getCtaLocation(link) {
    if (link.closest(".site-header")) return "header";
    if (link.closest("footer.site-footer")) return "footer";
    if (link.closest("#contact, .contact-layout, .page-meta")) return "contact_section";
    if (link.closest(".hero, .page-hero")) return "hero";
    return "page_body";
  }

  function shouldTrackCta(link) {
    return (
      link.matches(".header-cta") ||
      link.matches(".button") ||
      link.matches(".text-link") ||
      link.matches(".ghost-button") ||
      link.matches(".back-link")
    );
  }

  function pushCardClick(link, parsedUrl) {
    pushTrackingEvent("card_click", {
      card_family: getCardFamily(link, parsedUrl),
      card_name: link.dataset.trackName || getPathSlug(parsedUrl?.url.pathname || "") || slugify(getLinkLabel(link)),
      page_language: getPageLanguage(),
      source_page: getSourcePage(),
      destination_url: parsedUrl?.normalized || link.getAttribute("href") || "",
    });
  }

  function pushContactClick(link, parsedUrl) {
    const href = link.getAttribute("href") || "";
    const contactType = href.startsWith("mailto:") ? "email" : "phone";
    const destinationValue = href.replace(/^mailto:|^tel:/i, "");

    pushTrackingEvent("contact_click", {
      contact_type: contactType,
      cta_label: getLinkLabel(link),
      page_language: getPageLanguage(),
      source_page: getSourcePage(),
      destination_value: destinationValue,
    });
  }

  function pushCtaClick(link, parsedUrl) {
    pushTrackingEvent("cta_click", {
      cta_name: link.dataset.trackName || slugify(getLinkLabel(link)) || getPathSlug(parsedUrl?.url.pathname || ""),
      cta_label: getLinkLabel(link),
      cta_location: link.dataset.trackLocation || getCtaLocation(link),
      page_language: getPageLanguage(),
      source_page: getSourcePage(),
      destination_url: parsedUrl?.normalized || link.getAttribute("href") || "",
    });
  }

  function pushLanguageSwitch(link, parsedUrl) {
    const toLanguage = link.textContent.trim().toLowerCase() === "fr" ? "fr" : "en";
    pushTrackingEvent("language_switch", {
      from_language: getPageLanguage(),
      to_language: toLanguage,
      source_page: getSourcePage(),
      destination_url: parsedUrl?.normalized || link.getAttribute("href") || "",
    });
  }

  function pushNavigationClick(link, parsedUrl) {
    let navLabel = getLinkLabel(link);
    if (link.classList.contains("brand")) {
      navLabel = "brand_logo";
    }

    pushTrackingEvent("navigation_click", {
      nav_location: link.dataset.navLocation || getNavLocation(link),
      nav_label: navLabel,
      nav_target_type: getNavTargetType(parsedUrl),
      page_language: getPageLanguage(),
      source_page: getSourcePage(),
      destination_url: parsedUrl?.normalized || link.getAttribute("href") || "",
    });
  }

  function pushOutboundClick(link, parsedUrl) {
    if (!parsedUrl) return;
    pushTrackingEvent("outbound_click", {
      link_url: parsedUrl.normalized,
      link_domain: parsedUrl.url.hostname,
      link_text: getLinkLabel(link),
      page_language: getPageLanguage(),
      source_page: getSourcePage(),
    });
  }

  function handleLinkClick(event) {
    const link = event.target.closest("a[href]");
    if (!link) return;

    const parsedUrl = parseUrl(link.getAttribute("href"));
    const href = link.getAttribute("href") || "";

    if (link.closest(".language-switcher")) {
      pushLanguageSwitch(link, parsedUrl);
      return;
    }

    if (link.classList.contains("brand")) {
      pushNavigationClick(link, parsedUrl);
      return;
    }

    if (shouldTrackCard(link)) {
      pushCardClick(link, parsedUrl);
    }

    if (href.startsWith("mailto:") || href.startsWith("tel:")) {
      pushContactClick(link, parsedUrl);
    }

    if (shouldTrackCta(link)) {
      pushCtaClick(link, parsedUrl);
    }

    if (
      link.closest(".site-nav") ||
      link.closest("footer.site-footer .footer-links") ||
      link.closest(".breadcrumb")
    ) {
      pushNavigationClick(link, parsedUrl);
    }

    if (
      parsedUrl &&
      (parsedUrl.isExternal || FILE_EXTENSION_PATTERN.test(parsedUrl.url.pathname))
    ) {
      pushOutboundClick(link, parsedUrl);
    }
  }

  function setupScrollTracking() {
    const firedThresholds = new Set();

    function handleScroll() {
      const scrollableHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      if (scrollableHeight <= 0) return;

      const currentPercent = Math.min(
        100,
        Math.round((window.scrollY / scrollableHeight) * 100)
      );

      SCROLL_THRESHOLDS.forEach((threshold) => {
        if (currentPercent >= threshold && !firedThresholds.has(threshold)) {
          firedThresholds.add(threshold);
          pushTrackingEvent("scroll_depth", {
            scroll_percent: threshold,
            page_language: getPageLanguage(),
            source_page: getSourcePage(),
            page_type: inferPageType(),
          });
        }
      });
    }

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();
  }

  function setupEngagementTracking() {
    const firedMilestones = new Set();
    let accumulatedVisibleMs = 0;
    let visibleStartedAt = document.visibilityState === "visible" ? Date.now() : null;
    let milestoneTimeout = null;

    function clearMilestoneTimeout() {
      if (milestoneTimeout) {
        window.clearTimeout(milestoneTimeout);
        milestoneTimeout = null;
      }
    }

    function getNextMilestoneSeconds() {
      return ENGAGEMENT_MILESTONES.find(
        (seconds) => !firedMilestones.has(seconds)
      );
    }

    function scheduleNextMilestone() {
      clearMilestoneTimeout();

      if (document.visibilityState !== "visible") return;

      const nextMilestone = getNextMilestoneSeconds();
      if (!nextMilestone) return;

      const remainingMs = nextMilestone * 1000 - accumulatedVisibleMs;
      if (remainingMs <= 0) {
        fireMilestone(nextMilestone);
        scheduleNextMilestone();
        return;
      }

      milestoneTimeout = window.setTimeout(() => {
        accumulatedVisibleMs = nextMilestone * 1000;
        fireMilestone(nextMilestone);
        visibleStartedAt = Date.now();
        scheduleNextMilestone();
      }, remainingMs);
    }

    function fireMilestone(seconds) {
      if (firedMilestones.has(seconds)) return;
      firedMilestones.add(seconds);
      pushTrackingEvent(`content_engagement_${seconds}s`, {
        page_language: getPageLanguage(),
        source_page: getSourcePage(),
        page_type: inferPageType(),
      });
    }

    function updateAccumulatedVisibleTime() {
      if (visibleStartedAt !== null) {
        accumulatedVisibleMs += Date.now() - visibleStartedAt;
        visibleStartedAt = null;
      }
    }

    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "hidden") {
        updateAccumulatedVisibleTime();
        clearMilestoneTimeout();
        return;
      }

      visibleStartedAt = Date.now();
      scheduleNextMilestone();
    });

    window.addEventListener("beforeunload", updateAccumulatedVisibleTime);
    scheduleNextMilestone();
  }

  function init() {
    if (window[GLOBAL_KEY]) return;
    window[GLOBAL_KEY] = true;

    ensureDataLayer();
    document.addEventListener("click", handleLinkClick, true);
    setupScrollTracking();
    setupEngagementTracking();
  }

  window.PinnacleTracking = {
    init,
    pushTrackingEvent,
    inferPageType,
    getPageLanguage,
  };
})();
