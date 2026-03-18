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
    title: "Diagnostic",
    intro:
      "Clarifier les fragilités du modèle existant, objectiver les priorités et établir une base de décision partagée avant d'engager la suite de la trajectoire.",
    focus: [
      "La lecture des points de rupture opérationnels, organisationnels et systèmes",
      "La hiérarchisation des enjeux réellement structurants",
      "L'alignement des parties prenantes sur une base de décision commune",
    ],
    impact: [
      "Une vision plus lisible de la situation de départ",
      "Des arbitrages plus factuels",
      "Une trajectoire engagée sur des fondations solides",
    ],
  },
  design: {
    title: "Design",
    intro:
      "Concevoir une cible crédible en reliant organisation, flux, systèmes et exigences business, sans produire un modèle théorique déconnecté du terrain.",
    focus: [
      "La cohérence entre ambition stratégique et réalité d'exécution",
      "La définition d'un modèle cible opérable",
      "La traduction des choix structurants en scénarios concrets",
    ],
    impact: [
      "Une cible plus robuste et plus partageable",
      "Un cadre clair pour prioriser les investissements",
      "Une meilleure continuité entre vision et déploiement",
    ],
  },
  transformation: {
    title: "Transformation",
    intro:
      "Piloter les chantiers critiques, séquencer les décisions et sécuriser l'avancement pour transformer la cible en trajectoire réellement maîtrisée.",
    focus: [
      "La coordination des chantiers métier, opérationnels et digitaux",
      "Le séquencement des dépendances et des jalons critiques",
      "La qualité des arbitrages pendant l'exécution",
    ],
    impact: [
      "Un déploiement plus lisible pour les équipes",
      "Moins de friction entre projet et exploitation",
      "Une transformation plus fiable dans la durée",
    ],
  },
  stabilisation: {
    title: "Stabilisation",
    intro:
      "Accompagner l'adoption terrain, traiter les points de friction et consolider les nouvelles pratiques pour que la transformation tienne dans l'exécution quotidienne.",
    focus: [
      "L'appropriation opérationnelle des nouveaux standards",
      "La résolution rapide des irritants post-déploiement",
      "La consolidation des routines d'exécution et de management",
    ],
    impact: [
      "Une adoption plus rapide par les équipes",
      "Une baisse des instabilités post-lancement",
      "Un modèle plus durable à l'échelle des sites",
    ],
  },
  performance: {
    title: "Performance",
    intro:
      "Installer un pilotage durable pour rendre la performance lisible, actionnable et reliée aux décisions de management comme aux réalités terrain.",
    focus: [
      "La définition d'indicateurs véritablement utiles à l'action",
      "L'organisation de revues de performance cohérentes",
      "L'articulation entre terrain, management et gouvernance",
    ],
    impact: [
      "Une lecture plus fiable des résultats",
      "Des priorités d'amélioration mieux orientées",
      "Une performance pilotée comme un système durable",
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

  const cloneCount = Math.min(2, originalCards.length);
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

  const firstReal = contextRealCards[0];
  const lastReal = contextRealCards[contextRealCards.length - 1];
  const currentLeft = contextCarouselViewport.scrollLeft;
  const threshold = firstReal.offsetWidth * 0.6;

  if (currentLeft < firstReal.offsetLeft - threshold) {
    contextCarouselViewport.scrollLeft = currentLeft + contextLoopSpan;
  } else if (currentLeft > lastReal.offsetLeft + threshold) {
    contextCarouselViewport.scrollLeft = currentLeft - contextLoopSpan;
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
  const initialIndex = contextRealCards.length > 2 ? 1 : 0;
  contextCarouselViewport.scrollLeft = contextRealCards[initialIndex].offsetLeft;
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
  recalculateContextLoopSpan();
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

