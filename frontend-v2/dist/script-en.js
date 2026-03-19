function bootstrapTracking() {
  const initTracking = () => window.PinnacleTracking?.init?.();
  if (window.PinnacleTracking) {
    initTracking();
    return;
  }

  const existingTrackingScript = document.querySelector("script[data-pinnacle-tracking='true']");
  if (existingTrackingScript) {
    existingTrackingScript.addEventListener("load", initTracking, { once: true });
    return;
  }

  const trackingScript = document.createElement("script");
  trackingScript.src = new URL("./js/tracking.js", document.currentScript?.src || window.location.href).href;
  trackingScript.async = true;
  trackingScript.dataset.pinnacleTracking = "true";
  trackingScript.addEventListener("load", initTracking, { once: true });
  document.head.appendChild(trackingScript);
}

bootstrapTracking();

const reveals = document.querySelectorAll(".reveal");
const menuButton = document.querySelector(".menu-button");
const siteNav = document.querySelector(".site-nav");
const navLinks = document.querySelectorAll(".site-nav a");
const approachPhases = document.querySelectorAll(".approach-phase");
const approachDetailTitle = document.querySelector("#approach-detail-title");
const approachDetailIntro = document.querySelector("#approach-detail-intro");
const approachDetailFocus = document.querySelector("#approach-detail-focus");
const approachDetailImpact = document.querySelector("#approach-detail-impact");
const approachDetailImpactBlock = document.querySelector(".approach-detail__block--impact");
const contextCarouselTrack = document.querySelector("#context-carousel-track");
const contextCarouselViewport = document.querySelector("#context-carousel-viewport");
const scrollTopButton = document.querySelector(".scroll-top-button");
const heroSlides = document.querySelectorAll(".hero-slide");
const isCoarsePointer = window.matchMedia("(pointer: coarse)").matches;
let contextAutoplayInterval = null;
let contextAutoplayResumeTimeout = null;
let contextAutoplayReleaseTimeout = null;
let contextAllCards = [];
let contextRealCards = [];
let contextLoopSpan = 0;
let isContextAutoScrolling = false;
let heroSlideIndex = 0;

const approachContent = {
  diagnostic: {
    title: "Diagnosis",
    intro:
      "Clarify the fragilities of the current model, objectify priorities and establish a shared decision base before moving forward with the rest of the trajectory.",
    focus: [
      "Reading operational, organizational and systems breakpoints",
      "Prioritizing the issues that are truly structural",
      "Aligning stakeholders around a shared decision base",
    ],
    impact: [
      "A clearer view of the starting situation",
      "More fact-based trade-offs",
      "A trajectory launched on stronger foundations",
    ],
  },
  design: {
    title: "Design",
    intro:
      "Design a credible target by linking organization, flows, systems and business requirements without producing a theoretical model disconnected from the field.",
    focus: [
      "Consistency between strategic ambition and execution reality",
      "Definition of an operable target model",
      "Translation of structural choices into concrete scenarios",
    ],
    impact: [
      "A stronger, more shareable target",
      "A clear framework for prioritizing investments",
      "Better continuity between vision and deployment",
    ],
  },
  transformation: {
    title: "Transformation",
    intro:
      "Steer critical workstreams, sequence decisions and secure progress so the target becomes a trajectory that is genuinely under control.",
    focus: [
      "Coordination of business, operational and digital workstreams",
      "Sequencing dependencies and critical milestones",
      "Quality of trade-offs during execution",
    ],
    impact: [
      "A clearer rollout for teams",
      "Less friction between project and operations",
      "A more reliable transformation over time",
    ],
  },
  stabilisation: {
    title: "Stabilization",
    intro:
      "Support frontline adoption, resolve friction points and consolidate new practices so the transformation holds in day-to-day execution.",
    focus: [
      "Operational ownership of new standards",
      "Rapid resolution of post-deployment irritants",
      "Consolidation of execution and management routines",
    ],
    impact: [
      "Faster team adoption",
      "Reduced post-launch instability",
      "A more durable model across sites",
    ],
  },
  performance: {
    title: "Performance",
    intro:
      "Install sustainable management discipline to make performance readable, actionable and connected both to management decisions and frontline realities.",
    focus: [
      "Definition of indicators that are truly useful for action",
      "Organization of coherent performance reviews",
      "Articulation among frontline, management and governance",
    ],
    impact: [
      "A more reliable reading of results",
      "Better-oriented improvement priorities",
      "Performance managed as a lasting system",
    ],
  },
};

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.18 }
);

reveals.forEach((node) => observer.observe(node));

if (menuButton && siteNav) {
  menuButton.addEventListener("click", () => {
    const isOpen = siteNav.classList.toggle("is-open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });
}

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    if (siteNav && siteNav.classList.contains("is-open")) {
      siteNav.classList.remove("is-open");
      menuButton?.setAttribute("aria-expanded", "false");
    }
  });
});

function renderList(container, items) {
  if (!container) return;
  container.innerHTML = items.map((item) => `<li>${item}</li>`).join("");
}

function refreshContextCardCollections() {
  if (!contextCarouselTrack) {
    contextAllCards = [];
    contextRealCards = [];
    return;
  }

  contextAllCards = Array.from(contextCarouselTrack.querySelectorAll(".context-card"));
  contextRealCards = contextAllCards.filter((card) => card.dataset.clone !== "true");
  recalculateContextLoopSpan();
}

function animateImpactList() {
  if (!approachDetailImpactBlock) return;

  approachDetailImpactBlock.classList.remove("is-animating");
  void approachDetailImpactBlock.offsetWidth;
  approachDetailImpactBlock.classList.add("is-animating");
}

function setupContextCarouselLoop() {
  if (!contextCarouselTrack || !contextCarouselViewport) return;
  if (contextCarouselTrack.dataset.loopReady === "true") {
    refreshContextCardCollections();
    return;
  }

  const originalCards = Array.from(contextCarouselTrack.querySelectorAll(".context-card"));
  if (originalCards.length < 2) {
    refreshContextCardCollections();
    return;
  }

  const cloneCount = originalCards.length;
  const headClones = originalCards.slice(-cloneCount).map((card) => {
    const clone = card.cloneNode(true);
    clone.dataset.clone = "true";
    return clone;
  });

  const tailClones = originalCards.slice(0, cloneCount).map((card) => {
    const clone = card.cloneNode(true);
    clone.dataset.clone = "true";
    return clone;
  });

  headClones.reverse().forEach((clone) => {
    contextCarouselTrack.insertBefore(clone, contextCarouselTrack.firstChild);
  });

  tailClones.forEach((clone) => {
    contextCarouselTrack.appendChild(clone);
  });

  contextCarouselTrack.dataset.loopReady = "true";
  refreshContextCardCollections();
}

function updateContextGlide() {
  if (!contextCarouselViewport || !contextAllCards.length) return;

  const viewportRect = contextCarouselViewport.getBoundingClientRect();
  const viewportCenter = viewportRect.left + viewportRect.width / 2;
  const maxDistance = Math.max(viewportRect.width / 2, 1);

  let nearestCard = null;
  let nearestDistance = Number.POSITIVE_INFINITY;

  contextAllCards.forEach((card) => {
    const rect = card.getBoundingClientRect();
    const cardCenter = rect.left + rect.width / 2;
    const distance = Math.abs(viewportCenter - cardCenter);
    const normalized = Math.min(distance / maxDistance, 1);
    const scale = 0.92 + (1 - normalized) * 0.08;
    const opacity = 0.52 + (1 - normalized) * 0.48;
    const blur = normalized * 2.4;

    card.style.transform = `scale(${scale})`;
    card.style.opacity = opacity.toFixed(3);
    card.style.filter = `blur(${blur.toFixed(2)}px)`;

    if (distance < nearestDistance) {
      nearestDistance = distance;
      nearestCard = card;
    }
  });

  contextAllCards.forEach((card) => {
    card.classList.toggle("is-focused", card === nearestCard);
  });
}

function getActiveContextIndex() {
  if (!contextCarouselViewport || !contextRealCards.length) return 0;

  const viewportRect = contextCarouselViewport.getBoundingClientRect();
  const viewportCenter = viewportRect.left + viewportRect.width / 2;
  let nearestIndex = 0;
  let nearestDistance = Number.POSITIVE_INFINITY;

  contextRealCards.forEach((card, index) => {
    const rect = card.getBoundingClientRect();
    const cardCenter = rect.left + rect.width / 2;
    const distance = Math.abs(viewportCenter - cardCenter);

    if (distance < nearestDistance) {
      nearestDistance = distance;
      nearestIndex = index;
    }
  });

  return nearestIndex;
}

function scrollToContextIndex(index) {
  if (!contextCarouselViewport || !contextRealCards.length) return;
  const safeIndex = (index + contextRealCards.length) % contextRealCards.length;
  const targetCard = contextRealCards[safeIndex];

  isContextAutoScrolling = true;

  contextCarouselViewport.scrollTo({
    left: targetCard.offsetLeft,
    behavior: "smooth",
  });

  if (contextAutoplayReleaseTimeout) {
    window.clearTimeout(contextAutoplayReleaseTimeout);
  }

  contextAutoplayReleaseTimeout = window.setTimeout(() => {
    isContextAutoScrolling = false;
    normalizeContextCarouselLoop();
    updateContextGlide();
  }, 900);
}

function stopContextAutoplay() {
  if (contextAutoplayInterval) {
    window.clearInterval(contextAutoplayInterval);
    contextAutoplayInterval = null;
  }

  if (contextAutoplayResumeTimeout) {
    window.clearTimeout(contextAutoplayResumeTimeout);
    contextAutoplayResumeTimeout = null;
  }
}

function startContextAutoplay() {
  if (!contextCarouselViewport || !contextRealCards.length || !isCoarsePointer || contextAutoplayInterval) return;

  contextAutoplayInterval = window.setInterval(() => {
    const currentIndex = getActiveContextIndex();
    scrollToContextIndex(currentIndex + 1);
  }, 2000);
}

function scheduleContextAutoplayResume() {
  if (!isCoarsePointer) return;

  stopContextAutoplay();

  if (contextAutoplayResumeTimeout) {
    window.clearTimeout(contextAutoplayResumeTimeout);
  }

  contextAutoplayResumeTimeout = window.setTimeout(() => {
    startContextAutoplay();
  }, 3000);
}

function recalculateContextLoopSpan() {
  if (contextRealCards.length < 2) {
    contextLoopSpan = 0;
    return;
  }

  const firstReal = contextRealCards[0];
  const lastReal = contextRealCards[contextRealCards.length - 1];
  contextLoopSpan = lastReal.offsetLeft + lastReal.offsetWidth - firstReal.offsetLeft;
}

function normalizeContextCarouselLoop() {
  if (!contextCarouselViewport || !contextRealCards.length || !contextLoopSpan) return;

  const realCount = contextRealCards.length;
  const firstTailClone = contextAllCards[realCount * 2];
  const firstReal = contextRealCards[0];
  if (!firstTailClone) return;

  const currentLeft = contextCarouselViewport.scrollLeft;
  const threshold = firstReal.offsetWidth * 0.6;
  const loopStart = firstReal.offsetLeft;
  const loopEndStart = firstTailClone.offsetLeft;
  const maxScrollLeft = contextCarouselViewport.scrollWidth - contextCarouselViewport.clientWidth;
  const nearNativeRightEdge = currentLeft >= maxScrollLeft - threshold;
  const nearLoopLeftEdge = currentLeft < loopStart - threshold;
  const nearLoopRightEdge = currentLeft >= loopEndStart - threshold;

  if (nearLoopLeftEdge || nearLoopRightEdge || nearNativeRightEdge) {
    const offsetWithinLoop = ((currentLeft - loopStart) % contextLoopSpan + contextLoopSpan) % contextLoopSpan;
    contextCarouselViewport.scrollLeft = loopStart + offsetWithinLoop;
  }
}

function setActiveApproachPhase(key) {
  const content = approachContent[key];
  if (!content) return;

  approachPhases.forEach((phase) => {
    const isActive = phase.dataset.phase === key;
    phase.classList.toggle("is-active", isActive);
    phase.setAttribute("aria-pressed", String(isActive));
  });

  if (approachDetailTitle) approachDetailTitle.textContent = content.title;
  if (approachDetailIntro) approachDetailIntro.textContent = content.intro;
  renderList(approachDetailFocus, content.focus);
  renderList(approachDetailImpact, content.impact);
  animateImpactList();
}

approachPhases.forEach((phase) => {
  phase.addEventListener("click", () => {
    setActiveApproachPhase(phase.dataset.phase);
  });

  phase.addEventListener("mouseenter", () => {
    if (window.innerWidth > 900) {
      setActiveApproachPhase(phase.dataset.phase);
    }
  });
});

setActiveApproachPhase("diagnostic");
setupContextCarouselLoop();
recalculateContextLoopSpan();

if (contextCarouselViewport && contextRealCards.length) {
  contextCarouselViewport.scrollLeft = contextRealCards[0].offsetLeft;
}

updateContextGlide();

contextCarouselViewport?.addEventListener(
  "scroll",
  () => {
    updateContextGlide();
    normalizeContextCarouselLoop();

    if (!isContextAutoScrolling) {
      scheduleContextAutoplayResume();
    }
  },
  { passive: true }
);
contextCarouselViewport?.addEventListener("touchstart", stopContextAutoplay, { passive: true });
contextCarouselViewport?.addEventListener("touchend", scheduleContextAutoplayResume, { passive: true });
contextCarouselViewport?.addEventListener("pointerdown", stopContextAutoplay);
contextCarouselViewport?.addEventListener("pointerup", scheduleContextAutoplayResume);
contextCarouselViewport?.addEventListener("mouseenter", stopContextAutoplay);
contextCarouselViewport?.addEventListener("mouseleave", scheduleContextAutoplayResume);
window.addEventListener("resize", () => {
  refreshContextCardCollections();
  normalizeContextCarouselLoop();
  updateContextGlide();
  scheduleContextAutoplayResume();
});
startContextAutoplay();

function updateScrollTopButton() {
  if (!scrollTopButton) return;
  const shouldShow = window.scrollY > 520;
  scrollTopButton.classList.toggle("is-visible", shouldShow);
}

function setActiveHeroSlide(index) {
  if (!heroSlides.length) return;
  heroSlideIndex = (index + heroSlides.length) % heroSlides.length;
  heroSlides.forEach((slide, slideIndex) => {
    slide.classList.toggle("is-active", slideIndex === heroSlideIndex);
  });
}

scrollTopButton?.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

window.addEventListener("scroll", updateScrollTopButton, { passive: true });
updateScrollTopButton();

if (heroSlides.length > 1) {
  window.setInterval(() => {
    setActiveHeroSlide(heroSlideIndex + 1);
  }, 2000);
}

