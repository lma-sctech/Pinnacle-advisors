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
let activeModalType = null;
let ignoreNextModalPopstate = false;

const expertiseContent = {
  strategie: {
    label: "Stratégie supply chain",
    title: "Repenser les architectures supply chain pour soutenir la croissance, la résilience et la qualité de service.",
    intro:
      "Nous accompagnons les directions qui doivent faire évoluer un modèle supply chain devenu insuffisant face à la croissance, à la complexification des flux ou à la pression simultanée sur les coûts, les capacités et le service. Notre intervention consiste à clarifier les arbitrages structurants, définir une cible cohérente et construire une trajectoire de transformation alignée avec les priorités business.",
    issues: [
      "Réseau logistique devenu inadapté à la réalité des volumes ou des marchés",
      "Modèle de service insuffisamment aligné avec les attentes clients",
      "Manque de lisibilité sur les arbitrages coût, service et résilience",
      "Saturation progressive des capacités logistiques",
      "Difficulté à relier vision stratégique et réalité opérationnelle",
    ],
    actions: [
      "Diagnostic global supply chain",
      "Analyse des flux physiques et informationnels",
      "Évaluation des vulnérabilités du modèle existant",
      "Conception de modèles cibles AS-IS et TO-BE",
      "Élaboration de schémas directeurs logistiques",
      "Aide à la décision sur les priorités de transformation",
    ],
    outcomes: [
      "Un modèle plus robuste et plus lisible",
      "Des décisions mieux structurées sur le réseau et les capacités",
      "Une vision partagée de la cible opérationnelle",
      "Un meilleur alignement entre stratégie, service et exécution",
    ],
    contexts: [
      "Supply chain en croissance rapide",
      "Réorganisation de réseau logistique",
      "Évolution du modèle de distribution",
      "Besoin de rééquilibrer service, coûts et résilience",
    ],
  },
  operations: {
    label: "Opérations logistiques",
    title: "Faire évoluer les opérations terrain vers des standards d'exécution plus fiables, plus stables et plus productifs.",
    intro:
      "Nous intervenons lorsque la performance logistique quotidienne devient trop instable pour soutenir durablement les ambitions de l'entreprise. Dans ces contextes, les difficultés ne viennent pas d'un seul sujet, mais d'un ensemble de fragilités opérationnelles : organisation, flux, pratiques, pilotage et discipline d'exécution.",
    issues: [
      "Productivité insuffisante ou très variable",
      "Erreurs d'exécution récurrentes",
      "Fiabilité des stocks trop faible",
      "Tension sur les capacités entrepôt",
      "Hétérogénéité de fonctionnement entre sites",
      "Pilotage terrain peu structuré",
    ],
    actions: [
      "Diagnostic des opérations logistiques",
      "Organisation des activités entrepôt",
      "Optimisation des flux physiques et des layouts",
      "Structuration des règles de gestion et des standards",
      "Amélioration des pratiques de préparation, contrôle et expédition",
      "Mise en place de routines de pilotage terrain",
    ],
    outcomes: [
      "Une exécution plus stable",
      "Une meilleure maîtrise de la performance quotidienne",
      "Une réduction des erreurs et des irritants opérationnels",
      "Une organisation plus scalable en environnement multi-sites",
    ],
    contexts: [
      "Entrepôts en montée en charge",
      "Opérations sous tension capacitaire",
      "Besoin de fiabiliser l'exécution avant ou après un changement d'échelle",
      "Harmonisation de pratiques sur plusieurs sites",
    ],
  },
  digital: {
    label: "Transformation digitale",
    title: "Aligner les systèmes avec les opérations pour sécuriser les déploiements et accélérer l'adoption.",
    intro:
      "Les projets digitaux logistiques échouent rarement pour des raisons purement techniques. Ils échouent le plus souvent parce que le besoin métier est mal cadré, que l'exécution projet est mal gouvernée, ou que le système déployé ne s'intègre pas réellement aux pratiques terrain. Nous aidons les organisations à transformer des projets systèmes en leviers d'exécution concrets.",
    issues: [
      "Cadrage insuffisant des besoins métier",
      "Écart entre solution choisie et réalité opérationnelle",
      "Gouvernance projet trop faible ou trop fragmentée",
      "Difficulté à sécuriser tests, déploiement et adoption",
      "Transformation digitale déconnectée des enjeux terrain",
    ],
    actions: [
      "Cadrage des besoins métier",
      "Structuration des exigences fonctionnelles",
      "Accompagnement au choix de solutions WMS, TMS, OMS ou DMS",
      "Préparation des phases de test et de déploiement",
      "Coordination entre équipes métier, SI, intégrateurs et partenaires",
      "Accompagnement de la conduite du changement",
    ],
    outcomes: [
      "Un projet mieux structuré et mieux arbitré",
      "Un déploiement plus sécurisé",
      "Une adoption terrain plus rapide",
      "Une meilleure contribution des systèmes à la performance logistique",
    ],
    contexts: [
      "Déploiement ou refonte de WMS ou TMS",
      "Projets SI à forte criticité métier",
      "Transformation digitale multi-acteurs",
      "Organisations ayant besoin de reconnecter projet système et exécution",
    ],
  },
  data: {
    label: "Data & pilotage",
    title: "Donner aux organisations une lecture plus fiable de leur performance et de leurs leviers d'action.",
    intro:
      "Dans de nombreuses organisations, la donnée supply chain existe, mais elle n'aide pas suffisamment à décider. Les indicateurs sont dispersés, le reporting est peu actionnable et les écarts sont constatés sans toujours être reliés à une logique d'arbitrage ou de pilotage. Nous aidons les entreprises à structurer un pilotage plus utile, plus lisible et plus proche de l'action.",
    issues: [
      "KPI trop nombreux ou peu pertinents",
      "Reporting peu relié aux décisions opérationnelles",
      "Manque de visibilité sur les écarts de performance",
      "Difficulté à relier terrain, management et gouvernance",
      "Faible capacité à prioriser les leviers d'amélioration",
    ],
    actions: [
      "Définition de KPI supply chain réellement actionnables",
      "Structuration de tableaux de bord de pilotage",
      "Analyse des écarts et des causes",
      "Mise en place de routines de revue de performance",
      "Articulation entre pilotage terrain, management et gouvernance",
    ],
    outcomes: [
      "Une lecture plus claire de la performance",
      "Des arbitrages plus rapides et plus factuels",
      "Une meilleure priorisation des actions",
      "Un pilotage plus cohérent du terrain jusqu'aux instances de décision",
    ],
    contexts: [
      "Organisations en recherche de pilotage plus mature",
      "Besoin de fiabiliser la lecture de performance multi-sites",
      "Transformations nécessitant une base de décision plus solide",
      "Directions supply chain souhaitant mieux structurer leurs rituels de pilotage",
    ],
  },
};

const insightContent = {
  "network-redesign": {
    label: "Résilience supply chain",
    title: "Pourquoi les réseaux logistiques doivent être redesignés avant d'être simplement optimisés",
    subtitle:
      "Une lecture stratégique des arbitrages entre service, coût, flexibilité et robustesse du réseau.",
    quoteIndex: 5,
    paragraphs: [
      "Pendant longtemps, l'enjeu logistique consistait surtout à optimiser l'existant : réduire les kilomètres, améliorer le taux de remplissage, compresser les coûts de transport ou augmenter la productivité entrepôt. Cette logique reste utile, mais elle atteint vite ses limites lorsque le réseau lui-même n'est plus aligné avec la réalité du marché.",
      "Aujourd'hui, beaucoup d'entreprises opèrent encore sur des schémas conçus pour un contexte qui n'existe plus : demande plus volatile, pression accrue sur les délais, inflation logistique, fragmentation des flux, exigences clients plus élevées, exposition plus forte aux ruptures et aux aléas géopolitiques. Dans ce cadre, optimiser un mauvais réseau revient souvent à rendre plus efficace une structure devenue inadaptée.",
      "Le vrai sujet n'est donc plus seulement la performance locale d'un site, d'un entrepôt ou d'un plan de transport. Il est dans la cohérence globale du réseau : où stocker, où produire, comment servir, avec quel niveau de centralisation, quelle redondance, quelle capacité d'absorption des chocs, et à quel coût total.",
      "C'est là qu'intervient le redesign logistique. Redesigner, c'est arbitrer de façon lucide entre quatre tensions majeures : le service, pour garantir la promesse client réelle, pas théorique ; le coût, en raisonnant en coût global et non en silos ; la flexibilité, pour absorber les variations de volumes, de canaux et de marchés ; la robustesse, pour éviter qu'un réseau trop tendu devienne fragile au moindre incident.",
      "Un réseau trop optimisé sur le coût peut devenir rigide. Un réseau construit uniquement pour le service peut devenir économiquement insoutenable. Un réseau très flexible mais mal structuré peut générer de la complexité et de l'inefficacité. Un réseau robuste mais surdimensionné peut dégrader la compétitivité.",
      "La question stratégique n'est donc pas : comment faire mieux avec le réseau actuel ? La vraie question est : le réseau actuel est-il encore le bon ?",
      "Avant de chercher des gains marginaux, il faut vérifier que l'architecture logistique est adaptée aux ambitions commerciales, aux contraintes opérationnelles et aux risques réels. Car une optimisation n'améliore que ce qui existe déjà. Un redesign, lui, permet de reposer les bons choix structurels.",
      "En pratique, les entreprises qui prennent cette étape au sérieux ne cherchent pas seulement à être plus efficientes. Elles cherchent à bâtir un réseau capable d'être à la fois compétitif, agile et résilient. Et dans un environnement instable, c'est souvent cette capacité d'arbitrage qui crée l'avantage durable.",
    ],
  },
  "warehouse-performance": {
    label: "Performance entrepôt",
    title: "Ce que les opérations les plus solides ont en commun quand les volumes accélèrent",
    subtitle:
      "Des standards d'exécution, de pilotage et de fiabilité qui permettent de tenir sous pression.",
    quoteIndex: null,
    paragraphs: [
      "Quand les volumes augmentent rapidement, la plupart des organisations ne cassent pas à cause du volume lui-même, mais parce que leurs fondations opérationnelles ne sont pas dimensionnées pour encaisser la variabilité.",
      "Les opérations les plus solides ne sont pas celles qui improvisent bien sous pression. Ce sont celles qui ont déjà structuré des standards d'exécution, de pilotage et de fiabilité capables d'absorber l'accélération sans perte de contrôle.",
      "1. Des standards d'exécution non négociables. Les organisations robustes reposent sur des processus stables, documentés et industrialisés : modes opératoires clairs pour la réception, le picking, l'expédition et la gestion des exceptions ; réduction de la variabilité humaine par la standardisation ; logique process first, pas héros terrain. Quand les volumes montent, il n'y a plus de place pour l'interprétation. La répétabilité devient un levier de performance.",
      "2. Un pilotage en temps réel orienté décision. Les opérations solides ne pilotent pas avec des reportings en J+1. Elles fonctionnent avec des KPI opérationnels suivis en continu, des points de pilotage courts et fréquents, et une capacité à arbitrer rapidement sur la priorisation des flux, l'allocation des ressources ou la replanification. Sous pression, la vitesse de décision devient aussi critique que la qualité d'exécution.",
      "3. Une gestion maîtrisée de la capacité. Les organisations performantes savent précisément où sont leurs goulots d'étranglement, jusqu'où elles peuvent monter en charge avant rupture, et quels leviers activer : heures supplémentaires, intérim, reconfiguration des flux ou externalisation partielle. Elles ne subissent pas la montée en charge. Elles l'anticipent. La capacité est pilotée, pas découverte.",
      "4. Une discipline forte sur la qualité et la fiabilité.\nQuand les volumes accélèrent, les erreurs coûtent plus cher et se propagent plus vite. Les opérations solides maintiennent des contrôles qualité intégrés au process, une traçabilité fiable des flux et une gestion structurée des anomalies, pas du firefighting permanent. Elles comprennent que la fiabilité est un multiplicateur de performance, pas un coût.",
      "5. Une organisation conçue pour encaisser la pression. Les meilleures opérations ne reposent pas sur quelques profils clés : rôles et responsabilités clairs, backups identifiés, montée en compétence continue des équipes. Elles évitent le piège classique d'une performance dépendante de quelques individus critiques. La robustesse est systémique, pas individuelle.",
    ],
  },
  "digital-transformation": {
    label: "Transformation digitale",
    title: "Comment faire d'un projet système un vrai levier d'exécution logistique",
    subtitle:
      "Une approche plus exigeante de l'alignement entre besoins métier, déploiement et adoption terrain.",
    quoteIndex: null,
    paragraphs: [
      "La plupart des projets digitaux en supply chain échouent sur un point clé : ils livrent un système, mais ne transforment pas réellement l'exécution.",
      "Un WMS, un TMS ou un ERP ne crée pas de performance par lui-même. Sans alignement fort avec les opérations, il devient rapidement un outil contourné, sous-utilisé, ou pire, un facteur de rigidité supplémentaire.",
      "Le véritable enjeu n'est donc pas le déploiement technique. C'est la capacité à faire du système un accélérateur de performance terrain.",
      "1. Partir des flux réels, pas des fonctionnalités. Les projets qui réussissent commencent par une lecture fine des opérations : variabilité des flux, contraintes physiques comme les quais, le stockage ou les ressources, et points de friction récurrents. L'objectif n'est pas d'implémenter un standard éditeur. C'est de traduire la réalité opérationnelle en logique système cohérente. Un système mal aligné oblige les équipes à s'adapter en permanence. Un bon système structure et simplifie l'exécution.",
      "2. Concevoir pour l'exécution, pas pour la conformité. Trop de projets sont pensés pour cocher des cases fonctionnelles. Les meilleurs sont conçus pour répondre à une question simple : est-ce que cela rend le travail terrain plus fluide, plus rapide et plus fiable ? Cela implique des écrans adaptés aux usages réels, des parcours simples sans surcomplexité, et une réduction maximale des actions inutiles. Un système performant est un système que les équipes utilisent naturellement, sans effort cognitif excessif.",
      "3. Intégrer le pilotage dès la conception.\nUn projet digital réussi ne se limite pas à exécuter des flux. Il doit aussi permettre de les piloter efficacement : visibilité en temps réel sur les opérations, indicateurs directement exploitables par les managers, aide à la décision intégrée pour la priorisation, les alertes et les arbitrages. Sans pilotage, le système exécute. Avec pilotage, il oriente la performance.",
      "4. Traiter l'adoption comme un enjeu central. L'adoption n'est pas une phase finale. C'est un levier structurant du projet. Les organisations les plus performantes impliquent le terrain dès la conception, testent en conditions réelles et non uniquement en environnement projet, et forment avec une logique opérationnelle, pas seulement fonctionnelle. Un système adopté transforme l'exécution. Un système imposé génère des contournements.",
      "5. Aligner organisation, process et système. Un projet digital ne peut pas corriger une organisation défaillante. Si les rôles sont flous, les processus instables ou les règles incohérentes, le système ne fera que cristalliser les dysfonctionnements. La transformation digitale efficace repose sur un triptyque indissociable : processus clairs, organisation structurée, système aligné.",
    ],
  },
};

const perspectiveContent = {
  label: "Perspective du cabinet",
  title: "Rendre la performance supply chain plus robuste dans un contexte d'instabilité durable",
  subtitle:
    "Une lecture cabinet 2026–2036 sur la manière de concevoir un modèle opérationnel capable d'arbitrer vite, de se reconfigurer sans dégrader le service, et de traiter la résilience comme une capacité de performance.",
  summary: [
    "Entre 2026 et 2036, la performance supply chain ne se gagnera plus par l'optimisation marginale d'un réseau stable, mais par la capacité à tenir un niveau de service crédible dans un environnement où les chocs de coûts, les contraintes de conformité et la reconfiguration des flux internationaux deviennent récurrents.",
    "La résilience cesse d'être une logique défensive. Elle devient un sujet de conception du modèle opérationnel : choisir, dimensionner et gouverner les compromis entre coût, service, flexibilité et robustesse, puis industrialiser la décision pour arbitrer vite lorsque la réalité diverge du plan.",
  ],
  forces: [
    {
      title: "Volatilité des coûts et chocs d'offre",
      body:
        "Les budgets supply chain sont plus exposés à des écarts rapides et significatifs, ce qui impose de passer d'une logique de compression des coûts à une logique de gestion de la volatilité.",
    },
    {
      title: "Fragmentation géoéconomique",
      body:
        "La stabilité des corridors, l'accès aux technologies critiques et les choix d'implantation deviennent des contraintes de structure, avec des coûts d'ajustement parfois élevés.",
    },
    {
      title: "Pression ESG et conformité opératoire",
      body:
        "Les obligations de traçabilité, de reporting et de diligence ne relèvent plus du seul reporting. Elles s'invitent dans la planification, les données et la gouvernance fournisseurs.",
    },
    {
      title: "Dépendances critiques sur intrants et composants",
      body:
        "La concentration de certaines étapes, la transition énergétique et la bataille technologique requalifient la sécurisation d'intrants comme un sujet de compétitivité industrielle.",
    },
    {
      title: "Accélération technologique",
      body:
        "La valeur se déplace vers la visibilité, la simulation et la décision augmentée. Traçabilité, interopérabilité et données deviennent des actifs de pilotage autant que de conformité.",
    },
  ],
  implications: [
    "La première implication est de sortir d'un pilotage coût vs service pour passer à une gestion explicite des arbitrages coût, service, flexibilité et robustesse, avec un cadre de décision stable partagé par le top management et les opérations.",
    "La deuxième implication est de concevoir le modèle opérationnel comme un dispositif reconfigurable, et non comme une suite de paramètres optimisés une fois par an. Réseau, stocks, règles d'allocation et contrats doivent intégrer des écarts durables entre plan et réel.",
    "La troisième implication est que la résilience dépend autant de la gouvernance de la donnée et des partenaires que de l'outil. Les interfaces, la visibilité multi-tiers et la qualité des échanges deviennent des choix de modèle, pas des détails de projet.",
  ],
  recommendations: [
    {
      title: "Construire des réseaux adaptatifs",
      body:
        "Passer d'une architecture friction-minimisée à une architecture options-driven, avec segmentation des promesses de service, circuits alternatifs et points de bascule connus.",
    },
    {
      title: "Piloter en Total Value",
      body:
        "Formaliser une équation de valeur combinant coût-to-serve, niveau de service, exposition au risque et trajectoire carbone, afin de sortir des arbitrages en silos.",
    },
    {
      title: "Déployer une visibilité décisionnelle",
      body:
        "Construire une traçabilité exploitable orientée alertes, impacts et décisions, plutôt qu'accumuler des tableaux de bord sans traduction opérationnelle.",
    },
    {
      title: "Industrialiser la décision",
      body:
        "Réduire la latence de décision et la variabilité de résultat avec des scénarios, des budgets de risque, des règles d'arbitrage pré-écrites et des rituels de pilotage orientés action.",
    },
    {
      title: "Gouverner les interfaces partenaires",
      body:
        "Designer la supply chain comme un écosystème contractuel, data-driven et régulé, où la qualité de la donnée et l'alignement des SLA sont contractualisés comme le service.",
    },
  ],
  table: [
    {
      title: "Volatilité des coûts et chocs d'offre",
      impact:
        "Budgets supply chain plus exposés à des écarts rapides, nécessité de protéger la marge tout en tenant le service.",
      action:
        "Passer d'une logique réduction des coûts à une logique gestion de volatilité avec des scénarios de cost-to-serve par segments.",
      kpi:
        "Variance cost-to-serve vs budget, coût de non-qualité logistique, contribution des exceptions au coût total.",
    },
    {
      title: "Fragmentation géopolitique",
      impact:
        "Redéfinition de corridors, risques de restrictions, coûts d'ajustement et reconfiguration des implantations.",
      action:
        "Cartographier les dépendances critiques multi-tiers et contractualiser corridors alternatifs et switch rules.",
      kpi:
        "Time-to-recover par famille produit, part du spend couverte par mapping T2/T3, délai de bascule fournisseur.",
    },
    {
      title: "Pression ESG et conformité opératoire",
      impact:
        "Exigences de données et de diligence intégrées à l'exécution, avec coûts et risques juridiques ou réputationnels.",
      action:
        "Construire une architecture de données ESG supply chain intégrée aux achats et à la planification.",
      kpi:
        "Taux de couverture des données émissions, taux de fournisseurs conformes, incidents de diligence et temps de clôture.",
    },
    {
      title: "Dépendances critiques matières et composants",
      impact:
        "Concentration et tension sur intrants stratégiques, pression sur la capacité de transformation et la diversification.",
      action:
        "Définir une stratégie secure-by-design avec stocks stratégiques, dual sourcing, substitution et accords long terme.",
      kpi:
        "Indice de concentration fournisseurs, couverture de stocks critiques, respect du seuil de dépendance interne.",
    },
    {
      title: "Accélération technologique et traçabilité",
      impact:
        "Passage de l'outil au système de décision, interopérabilité et traçabilité deviennent des avantages compétitifs.",
      action:
        "Déployer une visibilité décisionnelle appuyée sur identifiants, data quality et règles d'arbitrage automatisables.",
      kpi:
        "Latence de détection et de décision, taux d'alertes actionnables, précision ETA/ETD, adoption des workflows.",
    },
    {
      title: "Gouvernance des interfaces",
      impact:
        "La performance dépend du partage de données, de la coordination et des incitations entre acteurs.",
      action:
        "Créer une gouvernance inter-fonctions et inter-partenaires sur données, SLA, responsabilités et escalades.",
      kpi:
        "Qualité des données partenaires, respect des SLA inter-entreprises, taux de litiges, disponibilité des flux critiques.",
    },
  ],
  conclusion:
    "À l'horizon 2026–2036, la meilleure supply chain ne sera pas celle qui optimise le plus finement un réseau figé, mais celle qui transforme l'instabilité en contrainte gérable en concevant un modèle opérationnel capable d'arbitrer vite et de se reconfigurer sans dégrader la promesse client.",
};

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
              <strong>Action prioritaire</strong>
              <span>${item.action}</span>
            </div>
            <div class="perspective-table__pill">
              <strong>KPI de suivi</strong>
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

  activeModalType = "expertise";
  window.history.pushState({ pinnacleModal: "expertise" }, "", window.location.href);
  expertiseModal.classList.add("is-open");
  expertiseModal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeExpertiseModal() {
  if (!expertiseModal) return;
  if (activeModalType === "expertise" && window.history.state?.pinnacleModal === "expertise") {
    ignoreNextModalPopstate = true;
    window.history.back();
    return;
  }
  expertiseModal.classList.remove("is-open");
  expertiseModal.setAttribute("aria-hidden", "true");
  activeModalType = null;
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

  activeModalType = "insight";
  window.history.pushState({ pinnacleModal: "insight" }, "", window.location.href);
  insightModal.classList.add("is-open");
  insightModal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeInsightModal() {
  if (!insightModal) return;
  if (activeModalType === "insight" && window.history.state?.pinnacleModal === "insight") {
    ignoreNextModalPopstate = true;
    window.history.back();
    return;
  }
  insightModal.classList.remove("is-open");
  insightModal.setAttribute("aria-hidden", "true");
  activeModalType = null;
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

  activeModalType = "perspective";
  window.history.pushState({ pinnacleModal: "perspective" }, "", window.location.href);
  perspectiveModal.classList.add("is-open");
  perspectiveModal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closePerspectiveModal() {
  if (!perspectiveModal) return;
  if (activeModalType === "perspective" && window.history.state?.pinnacleModal === "perspective") {
    ignoreNextModalPopstate = true;
    window.history.back();
    return;
  }
  perspectiveModal.classList.remove("is-open");
  perspectiveModal.setAttribute("aria-hidden", "true");
  activeModalType = null;
  document.body.style.overflow = "";
}

function forceCloseAllModals() {
  expertiseModal?.classList.remove("is-open");
  expertiseModal?.setAttribute("aria-hidden", "true");
  insightModal?.classList.remove("is-open");
  insightModal?.setAttribute("aria-hidden", "true");
  perspectiveModal?.classList.remove("is-open");
  perspectiveModal?.setAttribute("aria-hidden", "true");
  activeModalType = null;
  document.body.style.overflow = "";
}

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

window.addEventListener("popstate", () => {
  if (ignoreNextModalPopstate) {
    ignoreNextModalPopstate = false;
    forceCloseAllModals();
    return;
  }

  if (activeModalType) {
    forceCloseAllModals();
  }
});

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

