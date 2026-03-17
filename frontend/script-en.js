const reveals = document.querySelectorAll(".reveal");
const menuButton = document.querySelector(".menu-button");
const siteNav = document.querySelector(".site-nav");
const navLinks = document.querySelectorAll(".site-nav a");
const expertiseTriggers = document.querySelectorAll(".expertise-trigger");
const expertiseModal = document.querySelector(".expertise-modal");
const expertiseModalClose = document.querySelector(".expertise-modal__close");
const expertiseModalLabel = document.querySelector("#expertise-modal-label");
const expertiseModalTitle = document.querySelector("#expertise-modal-title");
const expertiseModalIntro = document.querySelector("#expertise-modal-intro");
const expertiseModalIssues = document.querySelector("#expertise-modal-issues");
const expertiseModalActions = document.querySelector("#expertise-modal-actions");
const expertiseModalOutcomes = document.querySelector("#expertise-modal-outcomes");
const expertiseModalContexts = document.querySelector("#expertise-modal-contexts");
const insightTriggers = document.querySelectorAll(".insight-trigger");
const insightModal = document.querySelector("#insight-modal");
const insightModalClose = document.querySelector(".insight-modal__close");
const insightModalLabel = document.querySelector("#insight-modal-label");
const insightModalTitle = document.querySelector("#insight-modal-title");
const insightModalSubtitle = document.querySelector("#insight-modal-subtitle");
const insightModalBody = document.querySelector("#insight-modal-body");
const perspectiveTrigger = document.querySelector(".perspective-trigger");
const perspectiveModal = document.querySelector("#perspective-modal");
const perspectiveModalClose = document.querySelector(".perspective-modal__close");
const perspectiveModalLabel = document.querySelector("#perspective-modal-label");
const perspectiveModalTitle = document.querySelector("#perspective-modal-title");
const perspectiveModalSubtitle = document.querySelector("#perspective-modal-subtitle");
const perspectiveModalSummary = document.querySelector("#perspective-modal-summary");
const perspectiveModalForces = document.querySelector("#perspective-modal-forces");
const perspectiveModalImplications = document.querySelector("#perspective-modal-implications");
const perspectiveModalRecommendations = document.querySelector("#perspective-modal-recommendations");
const perspectiveTable = document.querySelector("#perspective-table");
const perspectiveModalConclusion = document.querySelector("#perspective-modal-conclusion");
const approachPhases = document.querySelectorAll(".approach-phase");
const approachDetailTitle = document.querySelector("#approach-detail-title");
const approachDetailIntro = document.querySelector("#approach-detail-intro");
const approachDetailFocus = document.querySelector("#approach-detail-focus");
const approachDetailImpact = document.querySelector("#approach-detail-impact");
const approachDetailImpactBlock = document.querySelector(".approach-detail__block--impact");
const contextCarouselTrack = document.querySelector("#context-carousel-track");
const contextCarouselViewport = document.querySelector("#context-carousel-viewport");
const isCoarsePointer = window.matchMedia("(pointer: coarse)").matches;
let contextAutoplayInterval = null;
let contextAutoplayResumeTimeout = null;
let contextAutoplayReleaseTimeout = null;
let contextAllCards = [];
let contextRealCards = [];
let contextLoopSpan = 0;
let isContextAutoScrolling = false;

const expertiseContent = {
  strategie: {
    label: "Supply chain strategy",
    title: "Rethink supply chain architectures to support growth, resilience and service quality.",
    intro:
      "We support leadership teams that need to evolve a supply chain model that has become insufficient in the face of growth, increasing flow complexity or simultaneous pressure on costs, capacity and service. Our role is to clarify structural trade-offs, define a coherent target and build a transformation path aligned with business priorities.",
    issues: [
      "A logistics network no longer suited to actual volumes or markets",
      "A service model insufficiently aligned with customer expectations",
      "Limited visibility on cost, service and resilience trade-offs",
      "Progressive saturation of logistics capacity",
      "Difficulty linking strategic vision with operational reality",
    ],
    actions: [
      "End-to-end supply chain diagnosis",
      "Analysis of physical and information flows",
      "Assessment of vulnerabilities in the current model",
      "Design of current-state and target-state operating models",
      "Development of logistics master plans",
      "Decision support on transformation priorities",
    ],
    outcomes: [
      "A stronger and more readable model",
      "Better-structured network and capacity decisions",
      "A shared view of the target operating model",
      "Stronger alignment between strategy, service and execution",
    ],
    contexts: [
      "Rapidly growing supply chains",
      "Logistics network reorganization",
      "Distribution model evolution",
      "Need to rebalance service, cost and resilience",
    ],
  },
  operations: {
    label: "Logistics operations",
    title: "Upgrade frontline operations toward execution standards that are more reliable, more stable and more productive.",
    intro:
      "We intervene when day-to-day logistics performance becomes too unstable to sustainably support a company's ambitions. In these situations, difficulties rarely come from one issue alone, but from a set of operational fragilities: organization, flows, practices, management and execution discipline.",
    issues: [
      "Insufficient or highly variable productivity",
      "Recurring execution errors",
      "Poor inventory reliability",
      "Warehouse capacity pressure",
      "Inconsistent performance across sites",
      "Weakly structured frontline management",
    ],
    actions: [
      "Diagnosis of logistics operations",
      "Warehouse activity organization",
      "Optimization of physical flows and layouts",
      "Structuring of management rules and operating standards",
      "Improvement of picking, control and shipping practices",
      "Implementation of frontline management routines",
    ],
    outcomes: [
      "More stable execution",
      "Stronger control of daily performance",
      "Fewer errors and operational irritants",
      "A more scalable organization in multi-site environments",
    ],
    contexts: [
      "Warehouses ramping up",
      "Capacity-constrained operations",
      "Need to stabilize execution before or after a scale change",
      "Standardization of practices across several sites",
    ],
  },
  digital: {
    label: "Digital transformation",
    title: "Align systems with operations to secure deployments and accelerate adoption.",
    intro:
      "Logistics digital projects rarely fail for purely technical reasons. More often, they fail because business requirements were poorly framed, project execution was weakly governed, or the deployed system never truly integrates with frontline practices. We help organizations turn systems projects into concrete execution levers.",
    issues: [
      "Insufficient framing of business requirements",
      "Gap between the selected solution and operational reality",
      "Governance that is too weak or too fragmented",
      "Difficulty securing testing, deployment and adoption",
      "Digital transformation disconnected from frontline issues",
    ],
    actions: [
      "Framing of business requirements",
      "Structuring of functional requirements",
      "Support in selecting WMS, TMS, OMS or DMS solutions",
      "Preparation of testing and deployment phases",
      "Coordination between business teams, IT, integrators and partners",
      "Support for change management",
    ],
    outcomes: [
      "A better-structured, better-arbitrated project",
      "A more secure rollout",
      "Faster frontline adoption",
      "A stronger systems contribution to logistics performance",
    ],
    contexts: [
      "WMS or TMS deployment or redesign",
      "High-criticality business systems projects",
      "Multi-stakeholder digital transformations",
      "Organizations needing to reconnect systems projects and execution",
    ],
  },
  data: {
    label: "Data & performance steering",
    title: "Give organizations a more reliable view of their performance and the levers they can act on.",
    intro:
      "In many organizations, supply chain data exists, but it does not help enough with decision-making. Indicators are scattered, reporting is not actionable enough and performance gaps are observed without always being tied to a clear management logic. We help companies structure management systems that are more useful, more readable and closer to action.",
    issues: [
      "Too many KPIs or KPIs with limited relevance",
      "Reporting disconnected from operational decisions",
      "Limited visibility on performance gaps",
      "Difficulty connecting frontline, management and governance",
      "Weak ability to prioritize improvement levers",
    ],
    actions: [
      "Definition of genuinely actionable supply chain KPIs",
      "Structuring of performance dashboards",
      "Analysis of gaps and root causes",
      "Implementation of performance review routines",
      "Linking frontline management and governance",
    ],
    outcomes: [
      "A clearer reading of performance",
      "Faster, more fact-based trade-offs",
      "Better prioritization of actions",
      "More coherent management from the floor to decision bodies",
    ],
    contexts: [
      "Organizations seeking more mature management discipline",
      "Need to strengthen multi-site performance visibility",
      "Transformations requiring a stronger decision base",
      "Supply chain leadership teams structuring their management rituals",
    ],
  },
};

const insightContent = {
  "network-redesign": {
    label: "Supply chain resilience",
    title: "Why logistics networks must be redesigned before they are simply optimized",
    subtitle:
      "A strategic reading of the trade-offs between service, cost, flexibility and network resilience.",
    quoteIndex: 5,
    paragraphs: [
      "For a long time, the logistics challenge was mainly about optimizing what already existed: reducing kilometers, improving load factors, compressing transport costs or increasing warehouse productivity. That logic is still useful, but it quickly reaches its limits when the network itself is no longer aligned with market reality.",
      "Today, many companies still operate schemes designed for a context that no longer exists: more volatile demand, stronger pressure on lead times, logistics inflation, fragmented flows, higher customer expectations and greater exposure to disruptions and geopolitical uncertainty. In that context, optimizing the wrong network often means making an outdated structure more efficient.",
      "The real issue is no longer just the local performance of a site, warehouse or transport plan. It lies in the overall coherence of the network: where to stock, where to produce, how to serve, with what degree of centralization, what redundancy, what shock absorption capacity and at what total cost.",
      "That is where logistics redesign comes in. To redesign means making lucid choices across four major tensions: service, to deliver a real customer promise rather than a theoretical one; cost, looked at globally rather than in silos; flexibility, to absorb changes in volumes, channels and markets; and resilience, to prevent an overly stretched network from becoming fragile at the slightest incident.",
      "A network optimized too aggressively for cost can become rigid. A network built only for service can become economically unsustainable. A very flexible but poorly structured network can generate complexity and inefficiency. A resilient but oversized network can undermine competitiveness.",
      "The strategic question is therefore not: how can we perform better with the current network? The real question is: is the current network still the right one?",
      "Before looking for marginal gains, companies need to verify that their logistics architecture matches their commercial ambitions, operational constraints and real risks. Optimization only improves what already exists. Redesign makes it possible to reset the structural choices themselves.",
      "In practice, companies that take this step seriously are not just trying to become more efficient. They are trying to build a network that is competitive, agile and resilient at the same time. In an unstable environment, that capacity for trade-off is often what creates durable advantage.",
    ],
  },
  "warehouse-performance": {
    label: "Warehouse performance",
    title: "What the strongest operations have in common when volumes accelerate",
    subtitle:
      "Execution, management and reliability standards that allow organizations to perform under pressure.",
    quoteIndex: null,
    paragraphs: [
      "When volumes rise quickly, most organizations do not break because of the volume itself, but because their operational foundations are not built to absorb variability.",
      "The strongest operations are not the ones that improvise well under pressure. They are the ones that have already structured execution, management and reliability standards capable of absorbing acceleration without losing control.",
      "1. Non-negotiable execution standards. Resilient organizations rely on stable, documented and industrialized processes: clear operating methods for receiving, picking, shipping and exception management; reduced human variability through standardization; a process-first logic rather than dependence on heroes. When volumes increase, there is no room left for interpretation. Repeatability becomes a performance lever.",
      "2. Real-time, decision-oriented management. Strong operations are not managed through next-day reporting. They rely on continuously monitored operational KPIs, short and frequent management checkpoints, and the ability to make rapid trade-offs on flow prioritization, resource allocation or replanning. Under pressure, speed of decision becomes as critical as quality of execution.",
      "3. Controlled capacity management. High-performing organizations know exactly where their bottlenecks are, how far they can ramp up before breaking, and which levers they can activate: overtime, temporary labor, flow reconfiguration or partial outsourcing. They do not suffer through ramp-up. They anticipate it. Capacity is managed, not discovered.",
      "4. Strong discipline on quality and reliability.\nWhen volumes accelerate, errors cost more and spread faster. Strong operations maintain quality controls embedded in the process, reliable flow traceability and structured anomaly management, not permanent firefighting. They understand that reliability is a performance multiplier, not a cost.",
      "5. An organization built to absorb pressure. The best operations do not depend on a few key profiles: roles and responsibilities are clear, backups are identified and teams continuously build capability. They avoid the classic trap of performance depending on a handful of critical individuals. Resilience is systemic, not individual.",
    ],
  },
  "digital-transformation": {
    label: "Digital transformation",
    title: "How to turn a systems project into a real lever for logistics execution",
    subtitle:
      "A more demanding approach to aligning business needs, deployment and frontline adoption.",
    quoteIndex: null,
    paragraphs: [
      "Most digital projects in supply chain fail on one crucial point: they deliver a system, but they do not truly transform execution.",
      "A WMS, TMS or ERP does not create performance on its own. Without strong alignment with operations, it quickly becomes a tool that is bypassed, underused or, worse, an additional source of rigidity.",
      "The real challenge is therefore not technical deployment. It is the ability to make the system an accelerator of frontline performance.",
      "1. Start from real flows, not features. Successful projects begin with a fine reading of operations: flow variability, physical constraints such as docks, storage or labor, and recurring friction points. The goal is not to implement a software vendor standard. It is to translate operational reality into a coherent systems logic. A misaligned system forces teams to adapt permanently. A good system structures and simplifies execution.",
      "2. Design for execution, not for compliance. Too many projects are designed to tick functional boxes. The best ones are designed to answer a simple question: does this make frontline work smoother, faster and more reliable? That means interfaces adapted to real usage, simple workflows without unnecessary complexity and maximum reduction of useless actions. A high-performing system is one that teams use naturally, without excessive cognitive effort.",
      "3. Embed management from the design stage.\nA successful digital project does not stop at executing flows. It must also make them manageable: real-time visibility on operations, indicators directly usable by managers and decision support built into prioritization, alerts and trade-offs. Without management capability, a system executes. With it, it shapes performance.",
      "4. Treat adoption as a central issue. Adoption is not a final phase. It is a structural lever of the project. The strongest organizations involve frontline teams from the design stage, test in real conditions rather than only in project environments and train with an operational logic, not only a functional one. An adopted system transforms execution. An imposed system generates workarounds.",
      "5. Align organization, process and system. A digital project cannot correct a weak organization. If roles are unclear, processes are unstable or rules are inconsistent, the system will only crystallize dysfunctions. Effective digital transformation relies on an inseparable trio: clear processes, a structured organization and an aligned system.",
    ],
  },
};

const perspectiveContent = {
  label: "Firm perspective",
  title: "Making supply chain performance more resilient in a context of sustained instability",
  subtitle:
    "A 2026-2036 firm view on how to design an operating model able to arbitrate quickly, reconfigure without degrading service, and treat resilience as a performance capability.",
  summary: [
    "Between 2026 and 2036, supply chain performance will no longer be won through marginal optimization of a stable network, but through the ability to maintain a credible service level in an environment where cost shocks, compliance constraints and the reconfiguration of international flows become recurrent.",
    "Resilience ceases to be a defensive logic. It becomes a matter of operating model design: choosing, sizing and governing the trade-offs between cost, service, flexibility and resilience, then industrializing decision-making to arbitrate quickly when reality diverges from plan.",
  ],
  forces: [
    {
      title: "Cost volatility and supply shocks",
      body:
        "Supply chain budgets are increasingly exposed to rapid and significant deviations, requiring a shift from pure cost compression to active volatility management.",
    },
    {
      title: "Geo-economic fragmentation",
      body:
        "Corridor stability, access to critical technologies and footprint choices are becoming structural constraints, sometimes with high adjustment costs.",
    },
    {
      title: "ESG pressure and operating compliance",
      body:
        "Traceability, reporting and due-diligence obligations are no longer confined to reporting. They now shape planning, data models and supplier governance.",
    },
    {
      title: "Critical dependencies on inputs and components",
      body:
        "The concentration of certain production stages, the energy transition and technological rivalry are turning input security into a matter of industrial competitiveness.",
    },
    {
      title: "Technological acceleration",
      body:
        "Value is shifting toward visibility, simulation and augmented decision-making. Traceability, interoperability and data are becoming management assets as much as compliance assets.",
    },
  ],
  implications: [
    "The first implication is moving beyond a cost-versus-service logic and toward explicit management of trade-offs among cost, service, flexibility and resilience, with a stable decision framework shared by top management and operations.",
    "The second implication is designing the operating model as a reconfigurable system rather than a set of parameters optimized once a year. Network, inventory, allocation rules and contracts must all accommodate durable gaps between plan and reality.",
    "The third implication is that resilience depends as much on data governance and partner governance as on tools. Interfaces, multi-tier visibility and exchange quality become model choices, not project details.",
  ],
  recommendations: [
    {
      title: "Build adaptive networks",
      body:
        "Move from a friction-minimized architecture to an options-driven architecture, with segmented service promises, alternative routes and known switching points.",
    },
    {
      title: "Manage through total value",
      body:
        "Formalize a value equation that combines cost-to-serve, service level, risk exposure and carbon trajectory to move beyond siloed trade-offs.",
    },
    {
      title: "Deploy decision-grade visibility",
      body:
        "Build actionable traceability focused on alerts, impacts and decisions instead of accumulating dashboards with no operational translation.",
    },
    {
      title: "Industrialize decision-making",
      body:
        "Reduce decision latency and outcome variability through scenarios, risk budgets, prewritten arbitration rules and action-oriented management rituals.",
    },
    {
      title: "Govern partner interfaces",
      body:
        "Design the supply chain as a contractual, data-driven and regulated ecosystem in which data quality and SLA alignment are governed as tightly as service itself.",
    },
  ],
  table: [
    {
      title: "Cost volatility and supply shocks",
      impact:
        "Supply chain budgets are more exposed to rapid deviations, creating the need to protect margin while maintaining service.",
      action:
        "Move from a cost-reduction logic to a volatility-management logic with cost-to-serve scenarios by segment.",
      kpi:
        "Cost-to-serve variance vs budget, logistics cost of poor quality, contribution of exceptions to total cost.",
    },
    {
      title: "Geopolitical fragmentation",
      impact:
        "Corridors are redefined, restriction risks increase and footprint adjustments become more frequent and more costly.",
      action:
        "Map critical multi-tier dependencies and formalize alternative corridors and switching rules.",
      kpi:
        "Time-to-recover by product family, share of spend covered by tier-2/tier-3 mapping, supplier switch lead time.",
    },
    {
      title: "ESG pressure and operating compliance",
      impact:
        "Data and due-diligence requirements become embedded in execution, creating cost, legal and reputational exposure.",
      action:
        "Build a supply chain ESG data architecture integrated with procurement and planning.",
      kpi:
        "Emissions data coverage rate, compliant supplier rate, due-diligence incidents and closure time.",
    },
    {
      title: "Critical dependencies on materials and components",
      impact:
        "Concentration and tension on strategic inputs increase pressure on transformation capacity and diversification.",
      action:
        "Define a secure-by-design strategy with strategic stocks, dual sourcing, substitution options and long-term agreements.",
      kpi:
        "Supplier concentration index, critical stock coverage, internal dependency threshold compliance.",
    },
    {
      title: "Technological acceleration and traceability",
      impact:
        "The focus shifts from tools to decision systems, making interoperability and traceability competitive advantages.",
      action:
        "Deploy decision-grade visibility based on identifiers, data quality and automatable arbitration rules.",
      kpi:
        "Detection and decision latency, rate of actionable alerts, ETA/ETD accuracy, workflow adoption.",
    },
    {
      title: "Interface governance",
      impact:
        "Performance increasingly depends on data sharing, coordination and aligned incentives across actors.",
      action:
        "Create cross-functional and cross-partner governance around data, SLAs, responsibilities and escalations.",
      kpi:
        "Partner data quality, intercompany SLA compliance, dispute rate, availability of critical flows.",
    },
  ],
  conclusion:
    "By the 2026-2036 horizon, the best supply chain will not be the one that most finely optimizes a fixed network, but the one that turns instability into a manageable constraint by designing an operating model able to arbitrate quickly and reconfigure without degrading the customer promise.",
};

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

function renderInsightParagraphs(container, paragraphs, quoteIndex = null) {
  if (!container) return;
  container.innerHTML = paragraphs
    .map((paragraph, index) => {
      const sectionMatch = paragraph.match(/^(\d\.\s[^\n.]+\.)\s*([\s\S]+)$/);

      if (quoteIndex !== null && index === quoteIndex) {
        return `
          <div class="insight-modal__quote">
            <p>${paragraph}</p>
          </div>
          <div class="insight-modal__divider" aria-hidden="true"></div>
        `;
      }

      if (sectionMatch) {
        const [, title, body] = sectionMatch;
        return `
          <section class="insight-modal__section">
            <h3>${title}</h3>
            <p>${body}</p>
          </section>
        `;
      }

      const extraClass = index === 0 ? " insight-modal__paragraph--lead" : "";
      return `
        <article class="insight-modal__paragraph${extraClass}">
          <p>${paragraph}</p>
        </article>
      `;
    })
    .join("");
}

function renderParagraphs(container, paragraphs) {
  if (!container) return;
  container.innerHTML = paragraphs.map((paragraph) => `<p>${paragraph}</p>`).join("");
}

function renderPerspectiveForces(container, items) {
  if (!container) return;
  container.innerHTML = items
    .map(
      (item) => `
        <article class="perspective-force">
          <h3>${item.title}</h3>
          <p>${item.body}</p>
        </article>
      `
    )
    .join("");
}

function renderPerspectiveRecommendations(container, items) {
  if (!container) return;
  container.innerHTML = items
    .map(
      (item) => `
        <article class="perspective-reco">
          <h3>${item.title}</h3>
          <p>${item.body}</p>
        </article>
      `
    )
    .join("");
}

function renderPerspectiveTable(container, items) {
  if (!container) return;
  container.innerHTML = items
    .map(
      (item) => `
        <article class="perspective-table__row">
          <h3>${item.title}</h3>
          <div class="perspective-table__meta">
            <div class="perspective-table__pill">
              <strong>Impact 2026–2036</strong>
              <span>${item.impact}</span>
            </div>
            <div class="perspective-table__pill">
              <strong>Priority action</strong>
              <span>${item.action}</span>
            </div>
            <div class="perspective-table__pill">
              <strong>Tracking KPI</strong>
              <span>${item.kpi}</span>
            </div>
          </div>
        </article>
      `
    )
    .join("");
}

function animateImpactList() {
  if (!approachDetailImpactBlock) return;

  approachDetailImpactBlock.classList.remove("is-animating");
  void approachDetailImpactBlock.offsetWidth;
  approachDetailImpactBlock.classList.add("is-animating");

  window.setTimeout(() => {
    approachDetailImpactBlock.classList.remove("is-animating");
  }, 1200);
}

function refreshContextCardCollections() {
  contextAllCards = contextCarouselTrack
    ? Array.from(contextCarouselTrack.querySelectorAll(".context-card"))
    : [];
  contextRealCards = contextCarouselTrack
    ? Array.from(contextCarouselTrack.querySelectorAll(".context-card:not([data-clone='true'])"))
    : [];
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

function openExpertiseModal(key) {
  if (!expertiseModal) return;
  const content = expertiseContent[key];
  if (!content) return;

  expertiseModalLabel.textContent = content.label;
  expertiseModalTitle.textContent = content.title;
  expertiseModalIntro.textContent = content.intro;
  renderList(expertiseModalIssues, content.issues);
  renderList(expertiseModalActions, content.actions);
  renderList(expertiseModalOutcomes, content.outcomes);
  renderList(expertiseModalContexts, content.contexts);

  expertiseModal.classList.add("is-open");
  expertiseModal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeExpertiseModal() {
  if (!expertiseModal) return;
  expertiseModal.classList.remove("is-open");
  expertiseModal.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

function openInsightModal(key) {
  if (!insightModal) return;
  const content = insightContent[key];
  if (!content) return;

  if (insightModalLabel) insightModalLabel.textContent = content.label;
  if (insightModalTitle) insightModalTitle.textContent = content.title;
  if (insightModalSubtitle) insightModalSubtitle.textContent = content.subtitle;
  renderInsightParagraphs(insightModalBody, content.paragraphs, content.quoteIndex ?? null);

  insightModal.classList.add("is-open");
  insightModal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeInsightModal() {
  if (!insightModal) return;
  insightModal.classList.remove("is-open");
  insightModal.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

function openPerspectiveModal() {
  if (!perspectiveModal) return;

  if (perspectiveModalLabel) perspectiveModalLabel.textContent = perspectiveContent.label;
  if (perspectiveModalTitle) perspectiveModalTitle.textContent = perspectiveContent.title;
  if (perspectiveModalSubtitle) perspectiveModalSubtitle.textContent = perspectiveContent.subtitle;
  renderParagraphs(perspectiveModalSummary, perspectiveContent.summary);
  renderPerspectiveForces(perspectiveModalForces, perspectiveContent.forces);
  renderParagraphs(perspectiveModalImplications, perspectiveContent.implications);
  renderPerspectiveRecommendations(perspectiveModalRecommendations, perspectiveContent.recommendations);
  renderPerspectiveTable(perspectiveTable, perspectiveContent.table);
  if (perspectiveModalConclusion) {
    perspectiveModalConclusion.innerHTML = `<p>${perspectiveContent.conclusion}</p>`;
  }

  perspectiveModal.classList.add("is-open");
  perspectiveModal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closePerspectiveModal() {
  if (!perspectiveModal) return;
  perspectiveModal.classList.remove("is-open");
  perspectiveModal.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

expertiseTriggers.forEach((trigger) => {
  trigger.addEventListener("click", () => {
    openExpertiseModal(trigger.dataset.expertise);
  });

  trigger.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openExpertiseModal(trigger.dataset.expertise);
    }
  });
});

insightTriggers.forEach((trigger) => {
  trigger.addEventListener("click", () => {
    openInsightModal(trigger.dataset.insight);
  });

  trigger.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openInsightModal(trigger.dataset.insight);
    }
  });
});

perspectiveTrigger?.addEventListener("click", openPerspectiveModal);
perspectiveTrigger?.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    openPerspectiveModal();
  }
});

document.querySelectorAll("[data-close-modal='true']").forEach((node) => {
  node.addEventListener("click", closeExpertiseModal);
});

document.querySelectorAll("[data-close-insight-modal='true']").forEach((node) => {
  node.addEventListener("click", closeInsightModal);
});

document.querySelectorAll("[data-close-perspective-modal='true']").forEach((node) => {
  node.addEventListener("click", closePerspectiveModal);
});

expertiseModalClose?.addEventListener("click", closeExpertiseModal);
insightModalClose?.addEventListener("click", closeInsightModal);
perspectiveModalClose?.addEventListener("click", closePerspectiveModal);

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeExpertiseModal();
    closeInsightModal();
    closePerspectiveModal();
  }
});

