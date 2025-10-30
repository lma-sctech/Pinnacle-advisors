#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de population de la base de données Pinnacle Supply Chain
Génère du contenu professionnel et réaliste pour le site web et le CRM
"""

import os
import sys
import django
from decimal import Decimal

# Fix encoding pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.website.models import (
    HeroSection, Service, AboutSection, TeamMember,
    FAQCategory, FAQ, ContactInfo
)
from apps.crm.models import Lead, Pipeline


def clear_data():
    """Nettoie les données existantes"""
    print("🗑️  Nettoyage des données existantes...")
    HeroSection.objects.all().delete()
    Service.objects.all().delete()
    AboutSection.objects.all().delete()
    TeamMember.objects.all().delete()
    FAQ.objects.all().delete()
    FAQCategory.objects.all().delete()
    ContactInfo.objects.all().delete()
    Lead.objects.all().delete()
    Pipeline.objects.all().delete()
    print("✅ Données nettoyées\n")


def create_hero():
    """Crée la section hero"""
    print("🎯 Création Hero Section...")
    hero = HeroSection.objects.create(
        title="Transformez votre Supply Chain en Avantage Compétitif",
        subtitle="Cabinet de conseil expert en optimisation logistique et transformation digitale. Nous accompagnons les entreprises dans la modernisation de leur chaîne d'approvisionnement pour une performance durable.",
        cta_text="Diagnostiquer ma Supply Chain",
        cta_link="#contact",
        is_active=True
    )
    print(f"✅ Hero créé: {hero.title}\n")
    return hero


def create_services():
    """Crée les services supply chain"""
    print("📦 Création des Services...")

    services_data = [
        {
            'title': 'Stratégie Supply Chain',
            'description': """Élaborez une stratégie supply chain alignée sur vos objectifs business.
            Nous analysons votre écosystème logistique, identifions les leviers de performance et concevons
            une feuille de route pragmatique intégrant innovation technologique et excellence opérationnelle.
            Notre approche combine diagnostic approfondi, benchmark sectoriel et modélisation de scénarios
            pour maximiser votre retour sur investissement.""",
            'icon': 'chart-bar',
            'order': 1
        },
        {
            'title': 'Optimisation des Flux Logistiques',
            'description': """Fluidifiez vos opérations et réduisez vos coûts jusqu'à 30%.
            Nous cartographions vos flux physiques et informationnels, identifions les goulots d'étranglement
            et déployons des solutions d'optimisation : réorganisation d'entrepôts, mutualisation transport,
            cross-docking, SMED. Nos experts terrain garantissent une mise en œuvre réussie avec mesure d'impact.""",
            'icon': 'truck',
            'order': 2
        },
        {
            'title': 'Transformation Digitale',
            'description': """Accélérez votre digitalisation avec les technologies Industry 4.0.
            WMS, TMS, OMS, IoT, IA prédictive, blockchain... Nous vous accompagnons du cahier des charges
            au déploiement en passant par le choix des solutions. Notre méthode agile garantit un ROI rapide
            et une adoption utilisateur optimale. Experts SAP, Oracle, Manhattan, Blue Yonder.""",
            'icon': 'cpu-chip',
            'order': 3
        },
        {
            'title': 'Gestion des Stocks & S&OP',
            'description': """Optimisez votre trésorerie en réduisant vos stocks de 20-40%.
            Nous implémentons des processus S&OP performants, des modèles de prévision avancés (IA/ML)
            et des stratégies de réapprovisionnement adaptées : Kanban, VMI, Drop-shipping.
            Réduction des ruptures, amélioration du taux de service, libération de cash.""",
            'icon': 'archive-box',
            'order': 4
        },
        {
            'title': 'Achats & Sourcing Stratégique',
            'description': """Structurez une fonction achats créatrice de valeur.
            Nous professionnalisons vos pratiques : segmentation fournisseurs, TCO, e-procurement,
            négociation stratégique, gestion des risques supply. Audits fournisseurs internationaux,
            nearshoring, dual sourcing. Économies moyennes constatées : 12-18% sur les postes optimisés.""",
            'icon': 'shopping-cart',
            'order': 5
        },
        {
            'title': 'Supply Chain Durable (ESG)',
            'description': """Construisez une supply chain responsable et conforme aux enjeux ESG.
            Bilan carbone scope 3, éco-conception packaging, reverse logistics, économie circulaire.
            Nous vous aidons à réduire votre empreinte environnementale tout en optimisant vos coûts.
            Reporting CSRD, certifications ISO 14001, stratégie net-zero.""",
            'icon': 'leaf',
            'order': 6
        },
        {
            'title': 'Excellence Opérationnelle',
            'description': """Déployez les meilleures pratiques Lean & Six Sigma dans vos opérations.
            5S, VSM, DMAIC, Kaizen, TPM... Nos Black Belts certifiés forment vos équipes et pilotent
            des chantiers d'amélioration continue. Gains typiques : +25% productivité, -40% défauts,
            +30% satisfaction client. Culture de la performance ancrée durablement.""",
            'icon': 'cog',
            'order': 7
        },
        {
            'title': 'Formation & Change Management',
            'description': """Développez les compétences de vos équipes supply chain.
            Catalogues sur-mesure : fondamentaux logistique, S&OP, transport, douanes, Incoterms,
            Excel avancé, Power BI. Accompagnement au changement lors de transformations :
            conduite projet, communication, pilotage de la montée en compétences. Formats présentiels,
            e-learning, blended.""",
            'icon': 'academic-cap',
            'order': 8
        },
    ]

    services = []
    for data in services_data:
        service = Service.objects.create(**data)
        services.append(service)
        print(f"  ✓ {service.title}")

    print(f"✅ {len(services)} services créés\n")
    return services


def create_about():
    """Crée la section À propos"""
    print("ℹ️  Création About Section...")

    about = AboutSection.objects.create(
        title="Excellence Supply Chain depuis 2008",
        description="""Pinnacle Supply Chain est un cabinet de conseil français spécialisé dans l'optimisation
        et la transformation des chaînes d'approvisionnement. Fondé en 2008 par d'anciens directeurs supply chain
        de groupes internationaux, nous combinons expertise métier pointue et pragmatisme opérationnel.""",

        mission_statement="""Notre mission est d'aider les entreprises industrielles et de distribution à
        transformer leur supply chain en véritable avantage compétitif. Nous croyons qu'une supply chain
        performante n'est pas qu'une question de coûts, mais un levier stratégique de croissance,
        d'agilité et de durabilité.""",

        vision_statement="""Devenir le partenaire de référence des ETI et grandes entreprises françaises
        pour leurs enjeux supply chain, reconnu pour l'excellence de nos livrables, notre transfert de
        compétences et notre capacité à générer des résultats mesurables rapidement.""",

        values="""Expertise métier : Seuls des experts supply chain avec 15+ ans d'expérience terrain
Pragmatisme : Solutions actionnables, pas de PowerPoint théoriques
Mesure d'impact : Chaque mission génère des KPIs mesurables
Transfert de compétences : Vos équipes autonomes à la fin de la mission
Confidentialité & Éthique : Engagement absolu sur la protection de vos données""",

        years_experience=17,
        clients_count=240,
        projects_count=520,
        is_active=True
    )

    print(f"✅ About créé: {about.title}")
    print(f"   📊 {about.years_experience} ans | {about.clients_count} clients | {about.projects_count} projets\n")
    return about


def create_team():
    """Crée les membres de l'équipe"""
    print("👥 Création Team Members...")

    team_data = [
        {
            'name': 'Jean-Philippe Moreau',
            'position': 'Associé Fondateur & Directeur Supply Chain',
            'bio': """25 ans d'expérience supply chain dont 12 ans comme DSC de groupes industriels internationaux
            (automobile, aéronautique). Expert en transformation supply chain, stratégie S&OP et excellence opérationnelle.
            Diplômé ESSEC et certifié CPIM (APICS). A dirigé des transformations supply chain générant +50M€ d'économies.
            Intervenant régulier à HEC et Kedge sur les enjeux supply chain.""",
            'linkedin_url': 'https://linkedin.com/in/jpmoreau-supply',
            'email': 'jp.moreau@pinnacle-advisors.tech',
            'order': 1
        },
        {
            'name': 'Sophie Bertrand',
            'position': 'Associée & Experte Transformation Digitale',
            'bio': """20 ans d'expérience en conseil IT et supply chain digitale. Spécialiste des projets WMS, TMS,
            OMS et intelligence artificielle appliquée à la prévision. Ex-Manager chez Accenture Supply Chain Practice.
            A piloté +40 déploiements de solutions supply chain (SAP, Manhattan, Blue Yonder). Diplômée CentraleSupélec
            et MBA INSEAD. Experte reconnue en IA prédictive pour la supply chain.""",
            'linkedin_url': 'https://linkedin.com/in/sophie-bertrand-sc',
            'email': 'sophie.bertrand@pinnacle-advisors.tech',
            'order': 2
        },
        {
            'name': 'Marc Lefebvre',
            'position': 'Senior Manager - Transport & Distribution',
            'bio': """18 ans dans le transport et la logistique. Ex-Directeur Transport Europe d'un distributeur retail
            (1200 magasins). Expert en optimisation de schémas de transport, massification, négociation transporteurs,
            douanes et Incoterms. A généré 8M€ d'économies annuelles via la refonte d'un schéma logistique paneuropéen.
            Diplômé CNAM en Logistique Internationale.""",
            'linkedin_url': 'https://linkedin.com/in/marclefebvre-transport',
            'email': 'marc.lefebvre@pinnacle-advisors.tech',
            'order': 3
        },
        {
            'name': 'Amélie Dubois',
            'position': 'Manager - Achats & Sourcing',
            'bio': """15 ans en achats et sourcing stratégique. Ex-Directrice Achats Indirects d'un groupe industriel CAC40.
            Spécialiste de la négociation complexe, du sourcing international (Asie, Europe de l'Est) et de la gestion
            des risques supply. Certifiée CPSM (ISM) et Black Belt Lean Six Sigma. A dirigé des audits fournisseurs dans
            12 pays et généré 22M€ d'économies sur 3 ans.""",
            'linkedin_url': 'https://linkedin.com/in/amelie-dubois-achats',
            'email': 'amelie.dubois@pinnacle-advisors.tech',
            'order': 4
        },
        {
            'name': 'Thomas Renault',
            'position': 'Manager - Excellence Opérationnelle & Lean',
            'bio': """12 ans en amélioration continue et excellence opérationnelle. Black Belt Lean Six Sigma certifié,
            formateur agréé. Ex-Responsable Amélioration Continue chez Renault (usine Flins). Expert en VSM, 5S, SMED,
            TPM et déploiement de programmes Lean à grande échelle. A formé +300 Green Belts et piloté +80 chantiers
            Kaizen avec ROI moyen de 180k€ par chantier.""",
            'linkedin_url': 'https://linkedin.com/in/thomas-renault-lean',
            'email': 'thomas.renault@pinnacle-advisors.tech',
            'order': 5
        },
        {
            'name': 'Claire Martin',
            'position': 'Consultante Senior - Supply Chain Durable',
            'bio': """10 ans en supply chain responsable et reporting ESG. Spécialiste du bilan carbone scope 3,
            économie circulaire, reverse logistics et conformité CSRD. Ex-Responsable Développement Durable Supply Chain
            chez L'Oréal. Diplômée AgroParisTech et Master DD (HEC). A piloté la certification ISO 14001 de 8 sites
            logistiques et réduit de 35% les émissions CO2 transport.""",
            'linkedin_url': 'https://linkedin.com/in/claire-martin-esg',
            'email': 'claire.martin@pinnacle-advisors.tech',
            'order': 6
        },
    ]

    members = []
    for data in team_data:
        member = TeamMember.objects.create(**data)
        members.append(member)
        print(f"  ✓ {member.name} - {member.position}")

    print(f"✅ {len(members)} membres créés\n")
    return members


def create_faq():
    """Crée les catégories FAQ et questions"""
    print("❓ Création FAQ Categories & Questions...")

    # Catégories
    categories_data = [
        {
            'name': 'Nos Services & Méthodologie',
            'description': 'Questions sur notre offre de conseil et notre approche',
            'order': 1
        },
        {
            'name': 'Tarifs & Modalités',
            'description': 'Informations sur nos tarifs, durée de missions et ROI',
            'order': 2
        },
        {
            'name': 'Expertise Sectorielle',
            'description': 'Nos domaines d\'expertise par secteur d\'activité',
            'order': 3
        },
        {
            'name': 'Transformation Digitale',
            'description': 'Questions sur les technologies et outils supply chain',
            'order': 4
        },
        {
            'name': 'Déroulement des Missions',
            'description': 'Comment se passe une mission de conseil chez Pinnacle',
            'order': 5
        },
    ]

    categories = {}
    for data in categories_data:
        cat = FAQCategory.objects.create(**data)
        categories[cat.name] = cat
        print(f"  📁 {cat.name}")

    # Questions détaillées
    faq_data = [
        # Nos Services & Méthodologie
        {
            'category': categories['Nos Services & Méthodologie'],
            'question': 'Quelle est votre approche méthodologique pour un projet supply chain ?',
            'answer': """Notre méthodologie s'articule en 5 phases éprouvées :

1. **Diagnostic & Cadrage (2-3 semaines)** : Audit terrain, analyse de données, cartographie des flux, benchmark. Nous identifions les quick wins et les chantiers structurants.

2. **Conception de la solution (3-4 semaines)** : Co-construction avec vos équipes des scénarios d'optimisation, modélisation économique, business case détaillé, feuille de route.

3. **Pilotage du déploiement (variable)** : Conduite du changement, formation des équipes, mise en œuvre opérationnelle, suivi des indicateurs.

4. **Mesure d'impact (ongoing)** : Dashboard KPIs, pilotage de la performance, ajustements, capitalisation.

5. **Transfert de compétences** : Documentation, formation avancée, autonomisation de vos équipes.

Notre approche est résolument pragmatique : 80% terrain, 20% PowerPoint. Chaque recommandation est testée, chiffrée et actio pitch.""",
            'order': 1,
            'is_published': True
        },
        {
            'category': categories['Nos Services & Méthodologie'],
            'question': 'Quelle est la différence entre un audit supply chain et un diagnostic ?',
            'answer': """**Audit supply chain** : Évaluation complète et normée de vos processus selon un référentiel (SCOR, ISO, best practices). Livrable : rapport d'audit avec scoring de maturité, écarts identifiés, plan de mise en conformité. Durée typique : 4-6 semaines. Idéal pour un état des lieux exhaustif ou une préparation certification.

**Diagnostic rapide** : Analyse ciblée sur une problématique spécifique (coûts transport, taux de service, stocks...). Approche terrain intensive avec mesures sur 1-2 semaines. Livrable : top 10 quick wins actionnables immédiatement + 3-5 chantiers structurants. ROI visible sous 3 mois.

Nous recommandons généralement le diagnostic pour démarrer : résultats rapides, implication forte des équipes, momentum créé. L'audit vient souvent ensuite pour industrialiser.""",
            'order': 2,
            'is_published': True
        },
        {
            'category': categories['Nos Services & Méthodologie'],
            'question': 'Travaillez-vous uniquement avec de grandes entreprises ?',
            'answer': """Non, notre clientèle est variée. Nous intervenons auprès de :

- **Grandes entreprises (>5000 pers.)** : 40% de nos missions. Transformations d'envergure, déploiements internationaux, programmes pluriannuels.

- **ETI (200-5000 pers.)** : 45% de nos missions. Notre sweet spot. Structuration de la supply chain, professionnalisation, préparation à la croissance.

- **PME (50-200 pers.)** : 15% de nos missions. Diagnostics ciblés, accompagnement à la digitalisation, formation des équipes.

Notre approche s'adapte à chaque contexte : nous dimensionnons nos équipes et notre méthodologie selon la taille de votre organisation. Une PME n'a pas besoin de la même "machinerie" qu'un groupe du CAC40.

Le critère clé n'est pas la taille mais **l'ambition** : voulez-vous faire de votre supply chain un avantage compétitif ?""",
            'order': 3,
            'is_published': True
        },
        {
            'category': categories['Nos Services & Méthodologie'],
            'question': 'Proposez-vous de l\'assistance à maîtrise d\'ouvrage (AMO) ?',
            'answer': """Absolument. L'AMO représente 30% de notre activité. Nous accompagnons nos clients dans :

**AMO Sélection d'outils** : Cahier des charges, RFP, démos, grille d'évaluation, négociation contractuelle. Nos experts connaissent le marché (WMS, TMS, OMS, S&OP...) et sont indépendants des éditeurs.

**AMO Déploiement** : Validation des specs, recette, conduite du changement, formation, go-live. Nous garantissons que le projet reste aligné sur vos objectifs business (pas de feature creep).

**AMO Post-déploiement** : Optimisation paramétrages, montée en compétences équipes, hypersoin.

Nos clients apprécient notre **neutralité** (aucun partenariat éditeur) et notre **expertise terrain** : nous savons ce qui marche vraiment vs. ce qui est joli dans les brochures. Taux de succès projets avec AMO Pinnacle : 94% (vs. 60% moyenne marché selon Gartner).""",
            'order': 4,
            'is_published': True
        },

        # Tarifs & Modalités
        {
            'category': categories['Tarifs & Modalités'],
            'question': 'Quels sont vos tarifs journaliers ?',
            'answer': """Nos tarifs dépendent du niveau d'expertise et du format d'intervention :

**Consultant Senior** : 1 200 - 1 500 € HT/jour
**Manager** : 1 500 - 1 800 € HT/jour
**Senior Manager / Expert** : 1 800 - 2 200 € HT/jour
**Associé / Directeur** : 2 200 - 2 800 € HT/jour

**Forfaits mission** : Nous privilégions les approches forfaitaires pour sécuriser votre budget. Exemples :
- Diagnostic supply chain (3 semaines) : 25-35k€ HT
- Optimisation schéma logistique (8 semaines) : 70-95k€ HT
- Sélection + déploiement WMS (6 mois) : 180-250k€ HT

**Formats alternatifs** :
- Direction Supply Chain à temps partagé : 3-5j/mois, forfait mensuel
- Abonnement conseil (retainer) : X jours/an, tarif dégressif
- Success fee : rémunération indexée sur les gains générés

Notre promesse : ROI minimum de 5:1 sur 18 mois (5€ de gains pour 1€ investi).""",
            'order': 1,
            'is_published': True
        },
        {
            'category': categories['Tarifs & Modalités'],
            'question': 'Quelle est la durée moyenne d\'une mission ?',
            'answer': """La durée varie selon le type de mission :

**Diagnostics rapides** : 2-4 semaines
Livrable : top quick wins + roadmap

**Missions d'optimisation** : 2-4 mois
Conception + pilotage déploiement d'une solution (refonte schéma transport, réorganisation entrepôt, mise en place S&OP...)

**Transformations structurantes** : 6-18 mois
Programmes complexes (digitalisation, refonte globale supply chain, déploiement international...)

**Accompagnement continu** : 12-36 mois
DSC temps partagé, pilotage de la performance, amélioration continue

Notre approche favorise les **résultats rapides** : nous ciblons des gains mesurables dès les 3 premiers mois (quick wins) tout en construisant les fondations de transformations durables.

Format type recommandé pour démarrer : **Diagnostic 3 semaines + Mission d'optimisation 3 mois**. Cela permet de valider la collaboration et générer un premier ROI avant d'engager un programme plus long.""",
            'order': 2,
            'is_published': True
        },
        {
            'category': categories['Tarifs & Modalités'],
            'question': 'Proposez-vous des success fees ou rémunération à la performance ?',
            'answer': """Oui, nous proposons plusieurs modèles incluant une part variable :

**Modèle Hybride (recommandé)** :
- Part fixe : 60-70% du budget (couvre nos coûts d'intervention)
- Part variable : 30-40% indexée sur les gains mesurés
Exemple : mission 100k€ = 65k€ fixe + 35k€ si objectifs atteints

**Success Fee pure** :
- Honoraires réduits pendant la mission (coûts directs uniquement)
- Bonus significatif si objectifs dépassés (% des économies générées)
- Période de mesure : 12-18 mois post-mission
Exemple : 40k€ pendant mission + 15% des économies année 1 + 10% année 2

**Conditions** :
- KPIs définis contractuellement (réduction coûts, amélioration taux de service, réduction stocks...)
- Méthode de mesure validée (baseline, attribution des gains)
- Gouvernance de suivi (comité trimestriel)

Ce modèle aligne totalement nos intérêts. Nous le réservons aux missions avec ROI mesurable rapidement (optimisation coûts, stocks...). 70% de nos clients choisissent cette approche.""",
            'order': 3,
            'is_published': True
        },

        # Expertise Sectorielle
        {
            'category': categories['Expertise Sectorielle'],
            'question': 'Dans quels secteurs avez-vous le plus d\'expérience ?',
            'answer': """Nos expertises sectorielles se concentrent sur 6 verticales :

**1. Industrie & Manufacturing (35% activité)**
Automobile, aéronautique, biens d'équipement, chimie. Expertise : Lean manufacturing, supply chain intégrée, DDMRP, planification avancée.

**2. Retail & Distribution (25%)**
Grande distribution, e-commerce, omnicanal. Expertise : DRP, prévision IA, réseaux logistiques multicanaux, reverse logistics.

**3. Biens de Consommation - FMCG (15%)**
Agroalimentaire, cosmétiques, produits d'entretien. Expertise : S&OP, co-packing, traçabilité, gestion DLC/DLUO.

**4. Pharma & Santé (10%)**
Laboratoires, dispositifs médicaux, pharmacies. Expertise : GDP, sérialization, cold chain, gestion des recalls.

**5. High-Tech & Electronics (10%)**
Composants, équipements IT, telecom. Expertise : allocation, gestion obsolescence, supply chain agile.

**6. Luxe & Mode (5%)**
Maroquinerie, prêt-à-porter, joaillerie. Expertise : supply chain responsable, traçabilité, seasonal planning.

Nous intervenons aussi ponctuellement en énergie, logistique 3PL et secteur public.""",
            'order': 1,
            'is_published': True
        },
        {
            'category': categories['Expertise Sectorielle'],
            'question': 'Avez-vous de l\'expérience à l\'international ?',
            'answer': """Oui, 60% de nos missions comportent une dimension internationale :

**Europe** : 80% de nos projets internationaux
Déploiements multipalier (France, Allemagne, Benelux, Espagne, Italie, Europe de l'Est). Expertise réglementaire (douanes, Incoterms, fiscalité).

**Asie** : 15%
Sourcing Chine/Vietnam/Inde, audits fournisseurs, optimisation supply chain Asia-Europe. Nous avons des partenaires locaux à Shanghai, Mumbai, Hanoï.

**Afrique** : 3%
Principalement Maghreb et Afrique de l'Ouest. Mise en place de schémas logistiques dans des contextes complexes.

**Amériques** : 2%
Quelques missions US et LATAM pour clients français s'internationalisant.

**Formats d'intervention** :
- Diagnostic global multi-pays (2-3 mois)
- Pilotage déploiement harmonisé de solutions (6-12 mois)
- Optimisation réseau international (footprint, hubs, flux)
- Accompagnement implantation nouveaux marchés

Notre équipe est multilingue (FR/EN/ES/DE/IT) et habituée aux contextes multiculturels.""",
            'order': 2,
            'is_published': True
        },

        # Transformation Digitale
        {
            'category': categories['Transformation Digitale'],
            'question': 'Quelles solutions WMS/TMS recommandez-vous ?',
            'answer': """Nous sommes **agnostiques** (aucun partenariat éditeur) et recommandons selon votre contexte :

**WMS - Leaders du marché** :
- **Manhattan (SCALE, Active)** : Le Rolls. Multi-sites, retail/industrie. Budget : 500k€-2M€
- **Blue Yonder (ex-JDA)** : Forte en prévision + WMS. Budget : 400k€-1,5M€
- **SAP EWM** : Intégré SAP. Pour clients SAP existants. Budget : 300k€-1M€
- **Generix (WMS)** : Solide, bon rapport qualité/prix. Budget : 150-400k€
- **Reflex (Hardis)** : PME/ETI françaises. Pragmatique. Budget : 80-250k€

**TMS - Transport Management** :
- **Acteos, BluJay, E2open** : Solutions enterprise
- **Shippeo** : Excellent en visibility temps réel
- **Generix TMS, Log'in TMS** : Bonnes solutions françaises

**Notre process de sélection** :
1. Cadrage besoins (grille 150 critères)
2. Longlist → Shortlist (4-5 éditeurs)
3. Ateliers + démos scénarisées
4. POC sur vos données réelles
5. Évaluation TCO 5 ans + négociation

Durée : 8-12 semaines. Nous vous faisons gagner 6-18 mois et économiser 20-40% vs. achat direct.""",
            'order': 1,
            'is_published': True
        },
        {
            'category': categories['Transformation Digitale'],
            'question': 'L\'intelligence artificielle peut-elle vraiment améliorer la prévision de la demande ?',
            'answer': """Oui, mais avec des nuances importantes :

**Gains typiques IA vs. méthodes classiques** :
- Réduction erreur de prévision (MAPE) : -15% à -40%
- Réduction ruptures : -20% à -35%
- Réduction stock : -10% à -25%
- ROI : 3:1 à 8:1 sur 24 mois

**Conditions de succès** :
1. **Données suffisantes** : Min. 24 mois d'historique, granulaire (SKU x site x jour/semaine)
2. **Data quality** : Nettoyage indispensable (outliers, promos, ruptures historiques)
3. **Enrichissement** : Prix concurrents, météo, événements, tendances Google
4. **Processus S&OP** : L'IA aide les humains, ne les remplace pas

**Technologies que nous déployons** :
- **Prévision statistique avancée** : ARIMA, modèles exponentiels
- **Machine Learning** : Random Forest, XGBoost, réseaux neuronaux (LSTM)
- **Solutions packagées** : Blue Yonder Luminate, o9 Solutions, Anaplan (avec modules IA)

**Notre recommandation** : Commencer par un **POC 8 semaines** sur une catégorie produits. Budget : 25-40k€. Si MAPE améliore de >10%, déploiement progressif. Sinon, on optimise d'abord les fondamentaux (données, processus).""",
            'order': 2,
            'is_published': True
        },
        {
            'category': categories['Transformation Digitale'],
            'question': 'Faut-il investir dans la blockchain pour ma supply chain ?',
            'answer': """**Réponse courte : probablement pas encore, sauf cas spécifiques.**

**Cas d'usage pertinents** (10% des entreprises) :
- **Traçabilité exigeante** : Pharma (lutte anti-contrefaçon), luxe, agroalimentaire bio/premium
- **Supply chains multi-acteurs complexes** : Nombreux intermédiaires, besoin de confiance décentralisée
- **Conformité réglementaire stricte** : Provenance, certifications (ex: minerais de conflit)

**Solutions matures** :
- IBM Food Trust (agroalimentaire) - Carrefour, Walmart
- TradeLens (Maersk + IBM) - conteneurs maritimes
- VeChain (luxe, pharma) - LVMH, BMW

**Pourquoi attendre pour la majorité ?** :
- Technologies encore émergentes, standardisation en cours
- ROI difficile à justifier vs. solutions classiques (ERP, track & trace)
- Coûts élevés (infra, change management)
- Nécessite l'adhésion de TOUS les acteurs de la chaîne

**Notre recommandation** :
1. D'abord : maîtriser les basiques (ERP, WMS, traçabilité classique)
2. Puis : évaluer blockchain si contrainte réglementaire forte OU différenciation client
3. Commencer par **POC 3 mois** (budget 30-60k€) avant déploiement

Nous restons en veille active et conseillons 2-3 clients/an sur des POC blockchain.""",
            'order': 3,
            'is_published': True
        },

        # Déroulement des Missions
        {
            'category': categories['Déroulement des Missions'],
            'question': 'Comment se passe la première prise de contact ?',
            'answer': """Notre processus de démarrage est conçu pour être **rapide et non engageant** :

**1. Premier contact (J0)** :
Échange téléphonique ou visio 30min avec un Associé. Compréhension de votre contexte et enjeux. Qualification mutuelle (fit expertise, timing, budget).

**2. Cadrage approfondi (J+7)** :
Réunion 2h sur site (ou visio). Visite terrain si pertinent (entrepôt, usine). Rencontre équipes clés. Accès à quelques données (coûts, KPIs).

**3. Proposition commerciale (J+14)** :
Livrable : diagnostic express (5-10 slides) + proposition d'intervention (objectifs, méthodologie, équipe, planning, budget). Présentation 1h + Q&A.

**4. Décision & contractualisation (J+21 à J+30)** :
Validation commerciale. Signature contrat + accord de confidentialité. Kickoff dans les 2 semaines.

**Engagement avant mission** : ZÉRO €
Les phases 1-2-3 sont offertes (investissement commercial de notre part). Vous ne payez que si vous décidez de lancer la mission.

**Délai moyen de la prise de contact au démarrage mission : 4-6 semaines.**

Prêt à démarrer ? Contactez-nous via le formulaire ou directement : contact@pinnacle-advisors.tech / +33 1 85 74 32 10""",
            'order': 1,
            'is_published': True
        },
        {
            'category': categories['Déroulement des Missions'],
            'question': 'Quelle est l\'implication attendue de nos équipes pendant la mission ?',
            'answer': """Nous sommes convaincus que **le succès d'une mission repose sur la co-construction**. Voici l'implication typique :

**Direction / Sponsor (5-10% temps)** :
- Comité de pilotage mensuel (2h)
- Validation des orientations stratégiques
- Déblocage des ressources

**Chef de projet interne (30-50% temps)** :
- Coordinateur quotidien avec Pinnacle
- Collecte de données, organisation ateliers
- Relai communication interne

**Équipes opérationnelles (10-20% temps)** :
- Participation ateliers (2-3 sessions de 3h par phase)
- Interviews, observations terrain
- Tests et validation des solutions

**Équipes IT/Data (10-15% temps si projet digitalisé)** :
- Extraction de données
- Support technique déploiement outils

**Nos engagements** :
- Minimiser la charge sur vos équipes (on fait, vous validez)
- Formations intégrées (montée en compétences en faisant)
- Planning adapté à vos contraintes (on évite les périodes de pics)

**Facteur clé de succès** : Avoir un **chef de projet interne dédié à temps partiel** (même 2j/semaine). Cela accélère x2 la mission et améliore l'appropriation.""",
            'order': 2,
            'is_published': True
        },
        {
            'category': categories['Déroulement des Missions'],
            'question': 'Que se passe-t-il après la fin de la mission ? Assurez-vous un suivi ?',
            'answer': """Nous ne vous lâchons pas après le livrable final. Notre **engagement post-mission** :

**Garantie 6 mois** (incluse) :
- Hotline email/tel (réponse <48h)
- 2 comités de suivi (M+3 et M+6) pour mesurer les résultats
- Ajustements mineurs des livrables si besoin
- Accès à notre base documentaire et outils

**Support étendu** (optionnel) :
- **Forfait suivi** : 2-4 jours/trimestre pour pilotage de la performance (tarif : -40% vs. TJM normal)
- **Hotline premium** : Support email/tel illimité (forfait mensuel 800-1500€)
- **Amélioration continue** : Chantiers Kaizen trimestriels (format 2j sur site)

**Formation continue** :
- Invitations à nos webinars supply chain (4-6/an)
- Accès à notre veille réglementaire et technologique
- Événements clients annuels (benchmark, REX)

**Mesure d'impact** :
Nous committons contractuellement sur un suivi des KPIs définis. Tableau de bord partagé pour tracker les gains réalisés vs. objectifs. Transparence totale.

**Statistique** : 75% de nos clients font appel à nous pour une 2ème mission dans les 18 mois. Taux de recommandation NPS : 68 (excellent dans le conseil).""",
            'order': 3,
            'is_published': True
        },

        # Questions bonus
        {
            'category': categories['Nos Services & Méthodologie'],
            'question': 'Quelle est votre valeur ajoutée par rapport à un grand cabinet de conseil ?',
            'answer': """Excellente question. Voici nos différences clés :

**1. Expertise métier pure supply chain**
Nos consultants ont 15+ ans d'expérience OPÉRATIONNELLE (ils ont été DSC, directeurs transport, demand planners...). Pas de junior fraîchement diplômé qui apprend sur votre dossier. Chez les Big4, 60% de l'équipe = juniors. Chez nous : 100% seniors.

**2. Pragmatisme terrain**
On passe 80% du temps sur le terrain (entrepôt, usine, transports) et 20% en salle de réunion. Nos recommandations sont actionnables, testées, chiffrées. Pas de slides théoriques.

**3. Tarifs optimisés**
TJM : 1200-2200€ (vs. 1800-3500€ chez Big4). Pourquoi ? Structure légère (pas de pyramide), pas de frais généraux pharaoniques. Vous payez l'expertise, pas les bureaux Champs-Élysées.

**4. Engagement sur les résultats**
On propose des success fees (rémunération sur les gains). Les Big4 facturent le temps passé, point. Nous alignons nos intérêts avec les vôtres.

**5. Transfert de compétences réel**
Vos équipes sont autonomes à la fin. On forme en faisant. Pas de dépendance au conseil.

**Quand choisir un grand cabinet ?**
- Projets très politiques (besoin du "logo" McKinsey/BCG pour convaincre)
- Missions >10M€ nécessitant 20+ consultants simultanés
- Votre DSI impose Big4 pour IT (SAP...)

**Quand choisir Pinnacle ?**
- Vous voulez des RÉSULTATS, pas des PowerPoints
- Budget contrôlé avec ROI garanti
- Transformation réelle avec adoption équipes""",
            'order': 10,
            'is_published': True
        },
        {
            'category': categories['Expertise Sectorielle'],
            'question': 'Accompagnez-vous les e-commerçants et acteurs digitaux ?',
            'answer': """Absolument ! Le e-commerce représente 20% de notre activité (croissance rapide).

**Nos expertises e-commerce** :

**1. Fulfillment & Opérations**
- Optimisation picking/packing (réduction -30% temps)
- Choix 3PL vs. entrepôt propre (modélisation économique)
- Multi-entrepôts pour réduire délais livraison
- Gestion pics activité (Black Friday, soldes)

**2. Promesse client & Livraison**
- Click & collect, drive, livraison express
- Stratégie last-mile (partenaires, véhicules, circuits)
- Reverse logistics optimisée (retours = 20-30% en mode/beauté)
- Customer experience livraison

**3. Omnicanal**
- Ship from store, endless aisle
- Orchestration stock physique/digital
- OMS (Order Management System) : sélection + déploiement

**4. Prévision & Allocation**
- Prévision e-commerce (volatilité forte, saisonnalité)
- Allocation multi-canal optimisée
- Gestion promotions flash

**Clients e-commerce** : Pure players (100% digital), Retailers omnicanaux (Fnac, Leroy Merlin...), Marketplaces.

**Format d'intervention apprécié** : Diagnostic 3 semaines (15-25k€) identifiant 5-10 quick wins + roadmap 12 mois. ROI moyen : réduction coûts fulfillment de 18%, amélioration NPS livraison de +12 points.""",
            'order': 5,
            'is_published': True
        },
        {
            'category': categories['Transformation Digitale'],
            'question': 'Aidez-vous au choix et déploiement d\'un système S&OP / IBP ?',
            'answer': """Oui, c'est un de nos domaines d'excellence. 25% de nos missions incluent un volet S&OP/IBP.

**Notre approche S&OP** se décline en 3 niveaux :

**Niveau 1 : Processus & Organisation (70% du succès)**
Avant toute techno, nous structurons le processus S&OP :
- Définition cycle mensuel (5 étapes classiques)
- Rôles & responsabilités (demand review, supply review, pre-S&OP, exec S&OP)
- KPIs de pilotage (MAPE, bias, service level, stock rotation)
- Gouvernance & rituels

**Niveau 2 : Solutions Technologiques**
Sélection parmi les leaders :
- **o9 Solutions** : Nouvelle génération, IA intégrée, UX moderne (clients : PepsiCo, Unilever)
- **Blue Yonder Luminate** : Suite complète demand/supply planning (clients : Nestlé, Carrefour)
- **Anaplan** : Flexible, forte en modélisation financière
- **SAP IBP** : Intégré SAP, pour clients SAP
- **Kinaxis RapidResponse** : Réactivité, scénarios what-if

**Niveau 3 : Déploiement & Adoption**
- Paramétrage solution (6-12 mois)
- Formation des planificateurs (demand planners, supply planners)
- Conduite du changement (crucial !)
- Amélioration continue post-go-live

**Durée mission typique** : 9-15 mois (cadrage → déploiement → stabilisation)
**Budget** : 120-350k€ selon périmètre et solution

**ROI typique** : Réduction stocks 15-25%, amélioration taux de service 8-15 points, réduction obsolescence 30-50%.""",
            'order': 4,
            'is_published': True
        },
    ]

    faqs = []
    for data in faq_data:
        faq = FAQ.objects.create(**data)
        faqs.append(faq)

    print(f"✅ {len(categories)} catégories et {len(faqs)} questions créées\n")
    return categories, faqs


def create_contact_info():
    """Crée les informations de contact"""
    print("📞 Création Contact Info...")

    contact = ContactInfo.objects.create(
        company_name='Pinnacle Supply Chain',
        email='contact@pinnacle-advisors.tech',
        phone='+33185743210',
        address='42 Avenue de la Grande Armée',
        city='Paris',
        country='France',
        linkedin_url='https://linkedin.com/company/pinnacle-supply-chain',
        twitter_url='https://twitter.com/pinnacle_sc',
        working_hours='Lun-Ven: 9h00-18h30',
        is_active=True
    )

    print(f"✅ Contact créé: {contact.company_name} - {contact.email}\n")
    return contact


def create_pipelines():
    """Crée les pipelines CRM"""
    print("🎯 Création Pipelines CRM...")

    pipelines_data = [
        {
            'name': 'Pipeline Commercial Principal',
            'description': 'Pipeline de vente pour les missions de conseil',
            'order': 1,
            'color': '#3B82F6'
        },
        {
            'name': 'Pipeline Projets Transformation',
            'description': 'Projets de transformation supply chain (>6 mois)',
            'order': 2,
            'color': '#10B981'
        },
        {
            'name': 'Pipeline Formations & AMO',
            'description': 'Missions de formation et assistance à maîtrise d\'ouvrage',
            'order': 3,
            'color': '#F59E0B'
        },
    ]

    pipelines = []
    for data in pipelines_data:
        pipeline = Pipeline.objects.create(**data)
        pipelines.append(pipeline)
        print(f"  ✓ {pipeline.name}")

    print(f"✅ {len(pipelines)} pipelines créés\n")
    return pipelines


def create_leads(pipelines):
    """Crée des leads d'exemple"""
    print("🔥 Création Leads CRM...")

    # Pipeline principal pour tous les leads
    main_pipeline = pipelines[0]

    leads_data = [
        # LEADS HOT (3-4)
        {
            'name': 'Marie Dupont',
            'email': 'marie.dupont@carrefour.fr',
            'phone': '+33612345678',
            'company': 'Carrefour France',
            'company_size': 'ge',
            'position': 'Directrice Supply Chain',
            'need_type': 'Optimisation globale supply chain',
            'message': """Bonjour, nous souhaitons optimiser notre supply chain omnicanale de manière urgente.
            Notre objectif est de réduire nos coûts logistiques de 15% tout en améliorant notre taux de service.
            Nous avons un budget de 250k€ pour cette transformation et souhaitons démarrer rapidement,
            idéalement d'ici 6 semaines. Nous recherchons un cabinet avec une forte expertise retail et
            digital pour nous accompagner sur un diagnostic puis un déploiement.""",
            'budget_mentioned': True,
            'estimated_budget': Decimal('250000.00'),
            'source': 'linkedin',
            'pipeline': main_pipeline,
            'status': 'qualified',
            'expected_revenue': Decimal('180000.00'),
        },
        {
            'name': 'Thomas Bernard',
            'email': 'thomas.bernard@renault.com',
            'phone': '+33623456789',
            'company': 'Renault Group',
            'company_size': 'ge',
            'position': 'VP Supply Chain Operations',
            'need_type': 'Transformation digitale',
            'message': """Nous lançons un programme de transformation digitale de notre supply chain avec
            déploiement d'un nouveau WMS sur 8 sites européens. Budget projet confirmé de 400k€ pour l'AMO.
            Besoin d'un accompagnement immédiat sur le cahier des charges et la sélection de solution.
            Le comité de direction attend une présentation dans 3 semaines. Pouvez-vous intervenir rapidement ?""",
            'budget_mentioned': True,
            'estimated_budget': Decimal('400000.00'),
            'source': 'referral',
            'pipeline': pipelines[1],  # Pipeline Transformation
            'status': 'proposal',
            'expected_revenue': Decimal('350000.00'),
        },
        {
            'name': 'Sophie Leroy',
            'email': 'sleroy@loreal.com',
            'phone': '+33634567890',
            'company': 'L\'Oréal',
            'company_size': 'ge',
            'position': 'Head of Supply Chain Sustainability',
            'need_type': 'Supply chain durable (ESG)',
            'message': """Urgent : nous devons mettre en conformité notre reporting CSRD d'ici fin Q2.
            Besoin d'un bilan carbone scope 3 complet et d'une stratégie de réduction des émissions supply chain.
            Budget de 180k€ alloué. Nous recherchons une expertise pointue en ESG supply chain et une méthodologie
            éprouvée. Disponibilité pour un kick-off la semaine prochaine ?""",
            'budget_mentioned': True,
            'estimated_budget': Decimal('180000.00'),
            'source': 'website',
            'pipeline': main_pipeline,
            'status': 'contacted',
            'expected_revenue': Decimal('160000.00'),
        },
        {
            'name': 'Laurent Petit',
            'email': 'lpetit@decathlon.com',
            'phone': '+33645678901',
            'company': 'Decathlon',
            'company_size': 'ge',
            'position': 'Directeur Logistique Europe',
            'need_type': 'Optimisation schéma logistique',
            'message': """Nous voulons optimiser notre schéma de distribution européen (15 entrepôts)
            pour réduire nos coûts de transport. Transformation stratégique avec budget > 150k€.
            Besoin d'une modélisation complète et d'un accompagnement sur le déploiement. Timeline :
            démarrage dans 1 mois maximum.""",
            'budget_mentioned': True,
            'estimated_budget': Decimal('170000.00'),
            'source': 'event',
            'pipeline': main_pipeline,
            'status': 'new',
            'expected_revenue': Decimal('150000.00'),
        },

        # LEADS WARM (4-5)
        {
            'name': 'Isabelle Martin',
            'email': 'i.martin@sanofi.com',
            'phone': '+33656789012',
            'company': 'Sanofi',
            'company_size': 'ge',
            'position': 'Supply Chain Manager',
            'need_type': 'Audit supply chain',
            'message': """Nous envisageons un audit complet de notre supply chain pharma pour identifier
            les axes d'amélioration. Notre direction étudie plusieurs cabinets. Pourriez-vous nous présenter
            votre méthodologie et vos références secteur pharma ? Budget en cours de validation mais enveloppe
            prévisionnelle autour de 60-80k€.""",
            'budget_mentioned': False,
            'estimated_budget': Decimal('70000.00'),
            'source': 'linkedin',
            'pipeline': main_pipeline,
            'status': 'new',
            'expected_revenue': Decimal('65000.00'),
        },
        {
            'name': 'Pierre Dubois',
            'email': 'pdubois@auchan.fr',
            'phone': '+33667890123',
            'company': 'Auchan Retail France',
            'company_size': 'ge',
            'position': 'Chef de Projet Supply Chain',
            'need_type': 'Formation équipes',
            'message': """Nous souhaitons former nos 25 planificateurs demand/supply aux meilleures pratiques S&OP.
            Pouvez-vous nous proposer un programme de formation sur-mesure ? Idéalement sur 6 mois avec mix
            présentiel et e-learning. Budget formation annuel disponible.""",
            'budget_mentioned': False,
            'source': 'website',
            'pipeline': pipelines[2],  # Pipeline Formations
            'status': 'contacted',
            'expected_revenue': Decimal('45000.00'),
        },
        {
            'name': 'Nathalie Rousseau',
            'email': 'nrousseau@lvmh.com',
            'phone': '',
            'company': 'LVMH',
            'company_size': 'ge',
            'position': 'Supply Chain Director Luxury Division',
            'need_type': 'Traçabilité et blockchain',
            'message': """Intéressés par vos services autour de la traçabilité supply chain pour le secteur luxe.
            Nous explorons les solutions blockchain pour garantir l'authenticité de nos produits. Souhaitons
            échanger sur vos retours d'expérience et méthodologie.""",
            'budget_mentioned': False,
            'source': 'referral',
            'pipeline': main_pipeline,
            'status': 'new',
            'expected_revenue': Decimal('80000.00'),
        },
        {
            'name': 'François Moreau',
            'email': 'fmoreau@schneider-electric.com',
            'phone': '+33689012345',
            'company': 'Schneider Electric',
            'company_size': 'ge',
            'position': 'Supply Planning Manager',
            'need_type': 'Prévision de la demande (IA)',
            'message': """Nous cherchons à améliorer notre forecast accuracy qui est aujourd'hui à 65% (MAPE).
            Intéressés par les solutions IA/ML que vous mentionnez. Pourriez-vous nous présenter vos
            success stories et envisager un POC sur une de nos business units ?""",
            'budget_mentioned': False,
            'company': 'Schneider Electric',
            'source': 'website',
            'pipeline': main_pipeline,
            'status': 'new',
            'expected_revenue': Decimal('55000.00'),
        },
        {
            'name': 'Céline Garnier',
            'email': 'cgarnier@danone.com',
            'phone': '+33690123456',
            'company': 'Danone',
            'company_size': 'ge',
            'position': 'Head of Logistics EMEA',
            'need_type': 'Optimisation transport',
            'message': """Bonjour, nous voulons optimiser nos coûts de transport qui ont augmenté de 22%
            depuis 2 ans. Recherchons expertise en négociation transporteurs et optimisation de tournées.
            Pouvez-vous partager des cas clients similaires (FMCG) et votre approche ?""",
            'budget_mentioned': False,
            'source': 'linkedin',
            'pipeline': main_pipeline,
            'status': 'contacted',
            'expected_revenue': Decimal('50000.00'),
        },

        # LEADS COLD (3-4)
        {
            'name': 'Marc Lefevre',
            'email': 'mlefevre@pme-logistique.fr',
            'phone': '',
            'company': 'PME Logistique',
            'company_size': 'pme',
            'position': 'Gérant',
            'need_type': 'Conseil général',
            'message': """Bonjour, je cherche des infos sur l'optimisation logistique. Merci.""",
            'budget_mentioned': False,
            'source': 'website',
            'pipeline': main_pipeline,
            'status': 'new',
        },
        {
            'name': 'Julie Lemoine',
            'email': 'jlemoine@startup-ecommerce.com',
            'phone': '+33601234567',
            'company': 'Startup E-commerce',
            'company_size': 'tpe',
            'position': 'CEO',
            'need_type': 'Autre',
            'message': """Salut, on est une jeune startup e-commerce. On aimerait discuter supply chain
            mais on n'a pas encore de budget. Vous faites du pro-bono ?""",
            'budget_mentioned': False,
            'source': 'other',
            'pipeline': main_pipeline,
            'status': 'new',
        },
        {
            'name': 'Robert Blanc',
            'email': 'rblanc@entreprise-inconnue.fr',
            'phone': '',
            'company': '',
            'company_size': 'unknown',
            'position': '',
            'need_type': 'Autre',
            'message': """Pouvez-vous m'envoyer vos tarifs et plaquette commerciale ?""",
            'budget_mentioned': False,
            'source': 'website',
            'pipeline': main_pipeline,
            'status': 'new',
        },
        {
            'name': 'Valérie Fontaine',
            'email': 'vfontaine@eti-industrie.com',
            'phone': '+33623456780',
            'company': 'ETI Industrie Plastique',
            'company_size': 'eti',
            'position': 'Assistante Direction',
            'need_type': 'Formation',
            'message': """Bonjour, mon directeur m'a demandé de me renseigner sur des formations supply chain.
            Vous organisez des sessions inter-entreprises ?""",
            'budget_mentioned': False,
            'source': 'phone',
            'pipeline': pipelines[2],
            'status': 'new',
        },
    ]

    leads = []
    for data in leads_data:
        lead = Lead.objects.create(**data)
        # La qualification automatique se fera via auto_qualify() dans le save()
        leads.append(lead)
        qual_emoji = '🔥' if lead.qualification == 'hot' else ('☀️' if lead.qualification == 'warm' else '❄️')
        print(f"  {qual_emoji} {lead.name} - {lead.company} (Score: {lead.score}, {lead.get_qualification_display()})")

    print(f"✅ {len(leads)} leads créés\n")

    # Statistiques
    hot = len([l for l in leads if l.qualification == 'hot'])
    warm = len([l for l in leads if l.qualification == 'warm'])
    cold = len([l for l in leads if l.qualification == 'cold'])
    print(f"   📊 Répartition: {hot} Hot | {warm} Warm | {cold} Cold\n")

    return leads


def main():
    """Fonction principale"""
    print("="*70)
    print("🚀 POPULATION BASE DE DONNÉES PINNACLE SUPPLY CHAIN")
    print("="*70)
    print()

    # Nettoyage
    clear_data()

    # Création du contenu
    hero = create_hero()
    services = create_services()
    about = create_about()
    team = create_team()
    categories, faqs = create_faq()
    contact = create_contact_info()
    pipelines = create_pipelines()
    leads = create_leads(pipelines)

    # Résumé
    print("="*70)
    print("✅ POPULATION TERMINÉE AVEC SUCCÈS!")
    print("="*70)
    print()
    print("📊 RÉSUMÉ DES DONNÉES CRÉÉES:")
    print(f"   • Hero Sections: 1")
    print(f"   • Services: {len(services)}")
    print(f"   • About Sections: 1")
    print(f"   • Team Members: {len(team)}")
    print(f"   • FAQ Categories: {len(categories)}")
    print(f"   • FAQ Questions: {len(faqs)}")
    print(f"   • Contact Info: 1")
    print(f"   • Pipelines CRM: {len(pipelines)}")
    print(f"   • Leads CRM: {len(leads)}")
    print()
    print("🎯 PROCHAINES ÉTAPES:")
    print("   1. Accédez à l'admin Django: http://localhost:8000/admin/")
    print("   2. Vérifiez les données créées")
    print("   3. Testez les endpoints API:")
    print("      - GET /api/website/hero/active/")
    print("      - GET /api/website/services/")
    print("      - GET /api/website/faq-categories/")
    print()
    print("💡 NOTE: Les images (photos équipe, hero, etc.) devront être")
    print("   ajoutées manuellement via l'admin Django ou via upload.")
    print()
    print("="*70)


if __name__ == '__main__':
    main()
