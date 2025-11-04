# 🚀 Plan d'Optimisation SEO - Pinnacle Advisors

**Date de création**: 4 novembre 2025
**État actuel**: 45/100
**Objectif**: 90+/100
**Site en production**: https://pinnacle-advisors.tech

---

## 📊 État Actuel du Projet

### ✅ Déploiement Complet (Phase 10 - TERMINÉE)
- **Backend Django**: https://api.pinnacle-advisors.tech (Render.com)
- **Frontend Next.js**: https://pinnacle-advisors.tech (Vercel)
- **DNS**: Configuré sur Namecheap
- **CORS**: Configuré et fonctionnel
- **SSL**: Certificats actifs (HTTPS)

### 📈 Progression SEO
```
┌─────────────────────────────────────────────────────────┐
│              SEO OPTIMIZATION PROGRESS                  │
├─────────────────────────────────────────────────────────┤
│ Phase 1: Fondations Critiques        [█████] 5/5 (100%)│
│ Phase 2: Métadonnées Avancées        [ ] 0/4   (0%)    │
│ Phase 3: Performance & Images        [ ] 0/5   (0%)    │
│ Phase 4: Structured Data             [ ] 0/5   (0%)    │
├─────────────────────────────────────────────────────────┤
│ TOTAL PROGRESS:                      [██] 5/19  (26%)  │
│ SEO SCORE ESTIMATE:                      62/100        │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 PHASE 1: Fondations Critiques ✅ COMPLÈTE

**Durée estimée**: 1-2 jours
**Priorité**: P0 - CRITIQUE
**Impact SEO**: +17 points (45 → 62)

Ces éléments sont **OBLIGATOIRES** pour que Google indexe correctement le site.

### 1.1 Créer robots.txt ✅

**Fichier**: `frontend/app/robots.ts`

**Code à implémenter**:
```typescript
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/card/*', '/api/*'], // Exclure cartes visite et API
      },
    ],
    sitemap: 'https://pinnacle-advisors.tech/sitemap.xml',
  }
}
```

**Validation**:
- [x] Fichier créé
- [ ] Accessible sur https://pinnacle-advisors.tech/robots.txt (après déploiement)
- [ ] Google Search Console vérifie le fichier (après déploiement)

---

### 1.2 Générer sitemap.xml ✅

**Fichier**: `frontend/app/sitemap.ts`

**Code à implémenter**:
```typescript
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://pinnacle-advisors.tech'

  // Pages statiques
  const staticPages = [
    '',
    '/about',
    '/services',
    '/team',
    '/faq',
    '/contact',
  ]

  return staticPages.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: route === '' ? 'weekly' : 'monthly',
    priority: route === '' ? 1.0 : 0.8,
  }))
}
```

**Validation**:
- [x] Fichier créé
- [ ] Accessible sur https://pinnacle-advisors.tech/sitemap.xml (après déploiement)
- [x] Page unique listée (architecture one-page scroll: /)
- [ ] Soumis à Google Search Console (après déploiement)

---

### 1.3 Ajouter viewport meta tag ✅

**Fichier**: `frontend/app/layout.tsx`

**Modification à apporter**:
```typescript
// Ajouter dans la fonction generateMetadata ou metadata export
export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
}
```

**Validation**:
- [x] Tag ajouté (viewport export ajouté à layout.tsx)
- [ ] Visible dans le source HTML: `<meta name="viewport" content="...">` (après déploiement)
- [ ] Test mobile Google: https://search.google.com/test/mobile-friendly (après déploiement)

---

### 1.4 Ajouter canonical URLs ✅

**Fichier**: `frontend/app/layout.tsx`

**Modification effectuée**:
```typescript
// Dans generateMetadata
export async function generateMetadata(): Promise<Metadata> {
  const seoData = await fetchSEOSettings()

  return {
    // ... existing metadata
    metadataBase: new URL('https://pinnacle-advisors.tech'),
    alternates: {
      canonical: '/',
    },
  }
}
```

**Note**: Architecture one-page scroll - une seule page avec sections (Hero, Services, About, Team, FAQ, Contact)

**Validation**:
- [x] metadataBase configuré
- [x] Canonical URL pour la page d'accueil (/)
- [ ] Format: `<link rel="canonical" href="https://pinnacle-advisors.tech/">` (vérification après déploiement)

---

### 1.5 Implémenter JSON-LD Organization ✅

**Fichier**: `frontend/app/layout.tsx`

**Code implémenté**:
```typescript
// Créer un composant StructuredData
function OrganizationSchema() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'ProfessionalService',
    name: 'Pinnacle Advisors',
    description: 'Cabinet de conseil spécialisé en optimisation et transformation des chaînes d\'approvisionnement',
    url: 'https://pinnacle-advisors.tech',
    logo: 'https://pinnacle-advisors.tech/logo.png',
    sameAs: [
      'https://www.linkedin.com/company/pinnacle-advisors',
      // Ajouter autres réseaux sociaux
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: '+33-X-XX-XX-XX-XX', // À remplir depuis ContactInfo
      contactType: 'customer service',
      availableLanguage: ['fr', 'en'],
    },
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  )
}

// Ajouter dans le body du RootLayout
<body>
  <OrganizationSchema />
  {children}
</body>
```

**Validation**:
- [x] Schema ajouté (composant OrganizationSchema créé et intégré)
- [x] Récupération dynamique depuis ContactInfo API
- [x] Fallback schema en cas d'erreur API
- [ ] Test Rich Results: https://search.google.com/test/rich-results (après déploiement)
- [ ] Aucune erreur détectée (vérification après déploiement)

---

## 🎯 PHASE 2: Métadonnées Avancées 🟡

**Durée estimée**: 1 jour
**Priorité**: P1 - HAUTE
**Impact SEO**: +10 points (70 → 80)

### 2.1 Twitter Cards ❌

**Fichier**: `frontend/app/layout.tsx`

**Modification à apporter**:
```typescript
// Dans generateMetadata
export async function generateMetadata(): Promise<Metadata> {
  const seoData = await fetchSEOSettings()

  return {
    // ... existing metadata
    twitter: {
      card: 'summary_large_image',
      title: seoData.meta_title,
      description: seoData.meta_description,
      images: [seoData.og_image || '/og-default.jpg'],
      creator: '@pinnacleadvisors', // À configurer si compte Twitter existe
    },
  }
}
```

**Validation**:
- [ ] Tags ajoutés
- [ ] Test Twitter Card Validator: https://cards-dev.twitter.com/validator
- [ ] Image correcte (1200x630px recommandé)

---

### 2.2 Extended OpenGraph ❌

**Fichier**: `frontend/app/layout.tsx`

**Modification à apporter**:
```typescript
// Compléter les OpenGraph tags existants
openGraph: {
  type: 'website',
  locale: seoData.og_locale,
  title: seoData.og_title,
  description: seoData.og_description,
  siteName: 'Pinnacle Advisors',
  url: 'https://pinnacle-advisors.tech',
  images: [
    {
      url: seoData.og_image || '/og-default.jpg',
      width: 1200,
      height: 630,
      alt: 'Pinnacle Advisors - Cabinet de Conseil',
    },
  ],
},
```

**Validation**:
- [ ] Tous les champs remplis
- [ ] Test Facebook Debugger: https://developers.facebook.com/tools/debug/
- [ ] Image s'affiche correctement

---

### 2.3 Theme Color ❌

**Fichier**: `frontend/app/layout.tsx`

**Code à ajouter**:
```typescript
// Dans metadata
export const metadata = {
  // ... existing
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#000000' },
  ],
}
```

**Validation**:
- [ ] Tag ajouté
- [ ] Couleur cohérente avec la charte graphique
- [ ] Test sur mobile (barre d'adresse colorée)

---

### 2.4 Métadonnées par page ❌

**Créer layout.tsx pour chaque route**:

**Exemple** `frontend/app/about/layout.tsx`:
```typescript
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'À Propos - Pinnacle Advisors',
  description: 'Découvrez notre équipe d\'experts en supply chain et notre mission de transformation des chaînes d\'approvisionnement.',
  alternates: {
    canonical: '/about',
  },
  openGraph: {
    title: 'À Propos - Pinnacle Advisors',
    description: 'Découvrez notre équipe d\'experts en supply chain',
    url: 'https://pinnacle-advisors.tech/about',
  },
}

export default function AboutLayout({ children }: { children: React.ReactNode }) {
  return children
}
```

**Pages à créer**:
- [ ] `/about/layout.tsx`
- [ ] `/services/layout.tsx`
- [ ] `/team/layout.tsx`
- [ ] `/faq/layout.tsx`
- [ ] `/contact/layout.tsx`

---

## 🎯 PHASE 3: Performance & Images 🟢

**Durée estimée**: 2-3 jours
**Priorité**: P2 - MOYENNE
**Impact SEO**: +5 points (80 → 85)

### 3.1 Convertir images en Next.js Image ❌

**Fichiers à modifier**:
- `frontend/components/sections/Hero.tsx`
- `frontend/components/sections/About.tsx`
- `frontend/components/sections/Team.tsx`

**Exemple de conversion**:
```typescript
// AVANT
<img src={member.photo} alt={member.name} />

// APRÈS
import Image from 'next/image'

<Image
  src={member.photo}
  alt={member.name}
  width={300}
  height={300}
  className="..."
/>
```

**Validation**:
- [ ] Hero section: Background image optimisée
- [ ] About section: Image optimisée
- [ ] Team section: Photos membres optimisées
- [ ] Aucune balise `<img>` directe (sauf logos/icônes SVG)

---

### 3.2 Lazy Loading ❌

**Code à appliquer**:
```typescript
<Image
  src={photo}
  alt={alt}
  width={300}
  height={300}
  loading="lazy" // Pour images below-the-fold
/>
```

**Validation**:
- [ ] Hero: PAS de lazy loading (above-the-fold)
- [ ] Services: Pas d'images (OK)
- [ ] About: Lazy loading si image below-the-fold
- [ ] Team: Lazy loading sur toutes les photos
- [ ] FAQ: Pas d'images (OK)

---

### 3.3 Priority Loading ❌

**Code pour hero image**:
```typescript
<Image
  src={heroBackground}
  alt="Hero background"
  fill
  priority // LCP optimization
  className="object-cover"
/>
```

**Validation**:
- [ ] Hero image a `priority={true}`
- [ ] Lighthouse LCP < 2.5s
- [ ] Aucune autre image n'a priority (uniquement LCP)

---

### 3.4 WebP/AVIF Format ❌

**Fichier**: `frontend/next.config.ts`

**Modification**:
```typescript
const nextConfig: NextConfig = {
  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'api.pinnacle-advisors.tech',
        pathname: '/media/**',
      },
    ],
  },
}
```

**Validation**:
- [ ] Config ajoutée
- [ ] Images servies en AVIF/WebP (vérifier Network DevTools)
- [ ] Fallback JPEG/PNG pour navigateurs anciens

---

### 3.5 Blur Placeholders ❌

**Code à implémenter**:
```typescript
<Image
  src={photo}
  alt={alt}
  width={300}
  height={300}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..." // Généré automatiquement par Next.js
/>
```

**Validation**:
- [ ] Placeholder sur Team photos
- [ ] Effet de blur visible pendant chargement
- [ ] UX améliorée (pas de pop-in brutal)

---

## 🎯 PHASE 4: Structured Data Avancé 🔵

**Durée estimée**: 2-3 jours
**Priorité**: P2 - MOYENNE
**Impact SEO**: +5 points (85 → 90+)

### 4.1 Service Schema ❌

**Fichier**: `frontend/components/sections/Services.tsx`

**Code à implémenter**:
```typescript
function ServiceSchema({ services }: { services: Service[] }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    itemListElement: services.map((service, index) => ({
      '@type': 'Service',
      position: index + 1,
      name: service.title,
      description: service.description,
      provider: {
        '@type': 'Organization',
        name: 'Pinnacle Advisors',
      },
    })),
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  )
}
```

**Validation**:
- [ ] Schema ajouté dans Services section
- [ ] Test Rich Results: Pas d'erreur
- [ ] Tous les services listés

---

### 4.2 FAQPage Schema ❌

**Fichier**: `frontend/components/sections/FAQ.tsx`

**Code à implémenter**:
```typescript
function FAQSchema({ faqs }: { faqs: FAQ[] }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer,
      },
    })),
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  )
}
```

**Validation**:
- [ ] Schema ajouté dans FAQ section
- [ ] Test Rich Results: Éligible pour rich snippet FAQ
- [ ] Toutes les questions listées

---

### 4.3 BreadcrumbList Schema ❌

**Fichier**: Créer `frontend/components/Breadcrumbs.tsx`

**Code**:
```typescript
export function Breadcrumbs({ items }: { items: Array<{ name: string; url: string }> }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: `https://pinnacle-advisors.tech${item.url}`,
    })),
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />
      <nav aria-label="Breadcrumb" className="...">
        {items.map((item, index) => (
          <Link key={index} href={item.url}>
            {item.name}
          </Link>
        ))}
      </nav>
    </>
  )
}
```

**Validation**:
- [ ] Composant créé
- [ ] Ajouté sur toutes les pages (sauf home)
- [ ] Test Rich Results: Breadcrumb visible

---

### 4.4 Person Schema ❌

**Fichier**: `frontend/components/sections/Team.tsx`

**Code à implémenter**:
```typescript
function TeamMemberSchema({ member }: { member: TeamMember }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: member.name,
    jobTitle: member.position,
    description: member.bio,
    image: member.photo,
    email: member.email,
    sameAs: member.linkedin_url ? [member.linkedin_url] : [],
    worksFor: {
      '@type': 'Organization',
      name: 'Pinnacle Advisors',
    },
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  )
}
```

**Validation**:
- [ ] Schema pour chaque membre
- [ ] Test Rich Results: Pas d'erreur
- [ ] LinkedIn links connectés

---

### 4.5 WebPage Schema ❌

**Fichier**: `frontend/app/page.tsx` (et autres pages)

**Code à implémenter**:
```typescript
function WebPageSchema({ page }: { page: { title: string; description: string; url: string } }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: page.title,
    description: page.description,
    url: page.url,
    inLanguage: 'fr-FR',
    isPartOf: {
      '@type': 'WebSite',
      name: 'Pinnacle Advisors',
      url: 'https://pinnacle-advisors.tech',
    },
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  )
}
```

**Validation**:
- [ ] Schema sur page d'accueil
- [ ] Schema sur toutes les pages importantes
- [ ] Test Rich Results: Pas d'erreur

---

## 🚫 Pages à Exclure de l'Indexation

### Cartes Visite Digitales
**Route**: `/card/*`

**Configuration robots.txt**:
```
Disallow: /card/*
```

**Meta tag sur pages card**:
```typescript
// frontend/app/card/[slug]/layout.tsx
export const metadata = {
  robots: {
    index: false,
    follow: false,
  },
}
```

**Raison**: Pages personnelles, pas d'intérêt SEO pour le site principal.

**Validation**:
- [ ] robots.txt bloque /card/*
- [ ] Meta robots noindex sur toutes les pages card
- [ ] Google Search Console ne les indexe pas

---

## ✅ Validation Globale & Outils

### Outils de Test
1. **Google Search Console**: https://search.google.com/search-console
   - [ ] Propriété ajoutée
   - [ ] Sitemap soumis
   - [ ] 0 erreurs d'indexation

2. **Google Rich Results Test**: https://search.google.com/test/rich-results
   - [ ] Organization schema valide
   - [ ] Service schema valide
   - [ ] FAQPage schema valide
   - [ ] Person schema valide

3. **Google PageSpeed Insights**: https://pagespeed.web.dev/
   - [ ] Performance: >90
   - [ ] Accessibility: >90
   - [ ] Best Practices: >90
   - [ ] SEO: >90

4. **Mobile-Friendly Test**: https://search.google.com/test/mobile-friendly
   - [ ] Page is mobile-friendly

5. **Structured Data Testing Tool**
   - [ ] Tous les schemas validés
   - [ ] 0 erreur, 0 warning

### Lighthouse Audit
```bash
# Lancer depuis le terminal
npx lighthouse https://pinnacle-advisors.tech --view
```

**Objectifs**:
- [ ] Performance: >90
- [ ] Accessibility: >90
- [ ] Best Practices: >90
- [ ] SEO: >95+

### Core Web Vitals
- [ ] LCP (Largest Contentful Paint): < 2.5s
- [ ] FID (First Input Delay): < 100ms
- [ ] CLS (Cumulative Layout Shift): < 0.1

---

## 📝 Checklist de Déploiement

**⚠️ IMPORTANT - Commit Git requis:**
À la fin de chaque phase (après toutes les étapes validées), créer un commit Git descriptif:
```bash
git add .
git commit -m "feat(seo): Phase 1 - Fondations critiques SEO (robots.txt, sitemap.xml, viewport, canonical, JSON-LD)"
git push origin main
```
Le push déclenchera un redéploiement automatique sur Vercel.

---

Après chaque phase, vérifier:

### Avant de passer à la phase suivante:
- [ ] Tous les éléments de la phase sont cochés ✅
- [ ] Tests de validation effectués
- [ ] Lighthouse score amélioré
- [ ] Pas de régression sur les pages existantes
- [ ] Commit Git avec message descriptif
- [ ] Push sur GitHub
- [ ] Redéploiement Vercel automatique
- [ ] Vérification en production

### À la fin de toutes les phases:
- [ ] Score SEO global > 90
- [ ] Google Search Console: 0 erreur
- [ ] Rich Results actifs dans Google
- [ ] Core Web Vitals en vert
- [ ] Site indexé correctement (vérifier: `site:pinnacle-advisors.tech`)

---

## 🎯 Objectifs Finaux

```
BEFORE (Actuel):
├─ SEO Score: 45/100
├─ robots.txt: ❌
├─ sitemap.xml: ❌
├─ Structured Data: ❌
├─ Image Optimization: ⚠️ Partiel
└─ Core Web Vitals: ⚠️ Non mesuré

AFTER (Objectif):
├─ SEO Score: 90+/100 ✅
├─ robots.txt: ✅
├─ sitemap.xml: ✅
├─ Structured Data: ✅ (5 schemas)
├─ Image Optimization: ✅ Complet
└─ Core Web Vitals: ✅ Tous en vert
```

---

## 📚 Ressources & Documentation

### Documentation Next.js
- [Metadata API](https://nextjs.org/docs/app/building-your-application/optimizing/metadata)
- [Image Optimization](https://nextjs.org/docs/app/building-your-application/optimizing/images)
- [sitemap.xml](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap)
- [robots.txt](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots)

### Schema.org
- [Organization](https://schema.org/Organization)
- [Service](https://schema.org/Service)
- [FAQPage](https://schema.org/FAQPage)
- [Person](https://schema.org/Person)
- [BreadcrumbList](https://schema.org/BreadcrumbList)

### Google Guidelines
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Structured Data Guidelines](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Core Web Vitals](https://web.dev/vitals/)

---

## 📞 Support & Questions

Si vous rencontrez des problèmes lors de l'implémentation:
1. Vérifier la documentation Next.js officielle
2. Tester avec les outils Google (Rich Results, Search Console)
3. Consulter les logs Vercel pour les erreurs de build
4. Demander de l'aide à Claude Code si blocage

---

**Dernière mise à jour**: 4 novembre 2025
**Statut**: 🟡 EN COURS - Phase 1 à démarrer
**Prochaine étape**: Créer `robots.ts` et `sitemap.ts`
