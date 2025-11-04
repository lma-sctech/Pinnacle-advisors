import { MetadataRoute } from 'next'

/**
 * Génère le sitemap.xml pour le site Pinnacle Advisors
 *
 * Ce sitemap liste toutes les pages publiques du site pour faciliter
 * l'indexation par les moteurs de recherche (Google, Bing, etc.)
 *
 * Architecture: One-page scroll
 * - Page d'accueil (/) contient toutes les sections:
 *   - Hero
 *   - Services (#services)
 *   - À Propos (#about)
 *   - Équipe (#team)
 *   - FAQ (#faq)
 *   - Contact (#contact)
 *
 * Pages exclues:
 * - Cartes visite digitales (/card/*) - Pages personnelles, pas d'intérêt SEO
 * - API endpoints (/api/*) - Non indexables
 *
 * Configuration SEO:
 * - Page d'accueil: priority 1.0, changeFrequency 'weekly'
 *
 * @see https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap
 */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://pinnacle-advisors.tech'

  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 1.0,
    },
  ]
}
