# Pinnacle Advisors - Frontend Next.js

Site web one-page moderne pour Pinnacle Advisors, cabinet de conseil expert en supply chain.

## 🚀 Technologies

- **Next.js 15+** - Framework React avec App Router
- **TypeScript** - Typage statique
- **Tailwind CSS** - Styling utility-first
- **Framer Motion** - Animations fluides
- **React Query** - Data fetching et cache
- **Axios** - Client HTTP
- **React Hook Form + Zod** - Formulaires avec validation
- **Heroicons** - Icônes

## 📦 Installation

```bash
npm install
```

## 🛠️ Développement

```bash
npm run dev
```

Le site sera accessible sur [http://localhost:3000](http://localhost:3000)

**Important:** Le backend Django doit tourner sur `http://localhost:8000` pour l'API.

## 🏗️ Structure du Projet

```
frontend/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Layout principal
│   ├── page.tsx             # Page d'accueil
│   ├── providers.tsx        # React Query Provider
│   └── globals.css          # Styles globaux
├── components/
│   ├── ui/                  # Composants UI réutilisables
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   ├── layout/              # Composants de layout
│   │   ├── Navbar.tsx
│   │   └── Footer.tsx
│   └── sections/            # Sections de la page
│       ├── Hero.tsx
│       ├── Services.tsx
│       ├── About.tsx
│       ├── Team.tsx
│       ├── FAQ.tsx
│       └── Contact.tsx
├── lib/
│   ├── api.ts               # Client API Axios
│   ├── analytics.ts         # SDK Analytics
│   └── utils.ts             # Utilitaires
└── types/
    └── index.ts             # Types TypeScript
```

## 🎨 Palette de Couleurs

- **Primary Blue**: `#3B82F6` - Couleur principale
- **Success Green**: `#10B981` - Actions positives
- **Danger Red**: `#EF4444` - Erreurs, Hot Leads
- **Warning Orange**: `#F59E0B` - Warm Leads

## 📡 API Endpoints Consommés

### Website
- `GET /api/website/hero/active/` - Hero section
- `GET /api/website/services/` - Liste des services
- `GET /api/website/about/active/` - Section À propos
- `GET /api/website/team/` - Équipe
- `GET /api/website/faq-categories/` - FAQ
- `GET /api/website/contact-info/active/` - Infos contact
- `POST /api/website/contact/` - Soumission formulaire

### Analytics (Tracking)
- `POST /api/analytics/track/session/` - Tracking session
- `POST /api/analytics/track/pageview/` - Tracking page vue
- `POST /api/analytics/track/event/` - Tracking événement
- `POST /api/analytics/track/heatmap/` - Tracking clics (heatmap)

## ✨ Fonctionnalités

### 🎯 Section Hero
- Animation d'entrée Framer Motion
- Stats animées (17+ ans, 240+ clients, 520+ projets)
- CTA principal vers formulaire contact
- Scroll down indicator animé

### 📦 Section Services
- Grid responsive (1-2-3 colonnes)
- 8 services supply chain détaillés
- Cards avec hover effet
- Expand/collapse pour voir descriptions complètes
- Icônes Heroicons

### ℹ️ Section About
- Stats counter animés (au scroll)
- Mission et Vision
- 5 valeurs clés avec icônes
- Design gradient bleu/vert

### 👥 Section Team
- 6 profils d'experts
- Cards avec photo + bio
- Hover overlay avec liens LinkedIn/Email
- Avatars générés si pas de photo

### ❓ Section FAQ
- 18 questions réparties en 5 catégories
- Accordion animé (Framer Motion)
- Barre de recherche en temps réel
- Réponses détaillées (400-800 mots)

### 📧 Section Contact
- Formulaire validé (React Hook Form + Zod)
- Champs: Nom, Email, Téléphone, Entreprise, Type besoin, Message
- Feedback success/error
- Infos contact (email, téléphone, adresse)
- Soumission asynchrone vers API Django

## 📊 Analytics & Tracking

Le site intègre un **SDK Analytics complet** qui track automatiquement:

- ✅ **Sessions utilisateur** (device, browser, OS, UTM params)
- ✅ **Page views** (temps passé, scroll depth)
- ✅ **Événements** (clics CTA, navigation, formulaires)
- ✅ **Heatmap** (coordonnées clics pour visualisation)

**Données envoyées au backend Django** pour analyse dans le God View Dashboard.

## 🔧 Configuration

### Variables d'environnement

Créer `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Tailwind Config

Couleurs personnalisées dans `tailwind.config.ts`:
- Palette Pinnacle (bleu/vert)
- Animations custom (fade-in, slide-up, scale-in)
- Gradients

## 🚀 Build & Production

```bash
# Build de production
npm run build

# Démarrer en mode production
npm start

# Lint
npm run lint
```

## 📱 Responsive Design

Le site est **100% responsive**:
- **Mobile** (< 768px): 1 colonne, menu hamburger
- **Tablet** (768px - 1024px): 2 colonnes
- **Desktop** (> 1024px): 3 colonnes, layout complet

## 🎭 Animations

Toutes les sections utilisent **Framer Motion** pour:
- Animations au scroll (viewport detection)
- Transitions fluides entre états
- Hover effects sur cards
- Loading states

## 🔒 Validation Formulaire

Le formulaire contact utilise **Zod Schema**:
- Nom: min 2 caractères
- Email: format valide
- Message: min 20 caractères
- Téléphone: optionnel
- Sélection type de besoin (dropdown)

## 🌐 SEO

- Metadata Next.js dans `layout.tsx`
- Balises OpenGraph
- Sitemap auto-généré (Next.js)
- Structure sémantique HTML5

## 🐛 Debugging

Le SDK Analytics log dans la console:
- `✅ Analytics initialized with session: <id>`
- Erreurs API en cas d'échec

## 📦 Dépendances Principales

```json
{
  "next": "^15.1.6",
  "react": "^19.0.0",
  "typescript": "^5.7.3",
  "tailwindcss": "^3.4.17",
  "framer-motion": "^11.15.0",
  "@tanstack/react-query": "^5.62.13",
  "axios": "^1.7.9",
  "react-hook-form": "^7.54.2",
  "zod": "^3.24.1"
}
```

## 👨‍💻 Développement

### Ajouter une nouvelle section

1. Créer `components/sections/NewSection.tsx`
2. Utiliser Framer Motion pour animations
3. Fetcher data avec React Query si besoin
4. Ajouter dans `components/sections/index.ts`
5. Importer dans `app/page.tsx`

### Ajouter un nouveau type

1. Définir interface dans `types/index.ts`
2. Aligner avec modèles Django backend
3. Ajouter fonction fetch dans `lib/api.ts`
4. Créer queryKey si besoin

## 🎯 Prochaines Étapes (Optionnel)

- [ ] Ajouter tests E2E (Playwright)
- [ ] Optimiser images (Next/Image)
- [ ] Ajouter blog section
- [ ] Multilingue (FR/EN)
- [ ] Dark mode toggle

## 📝 Notes

- Le site est **one-page** avec scroll smooth entre sections
- Tous les liens utilisent `#section-id` pour navigation interne
- Analytics initialisé automatiquement au mount
- React Query cache les données API (5min staleTime)

---

**Développé avec ❤️ pour Pinnacle Advisors**
