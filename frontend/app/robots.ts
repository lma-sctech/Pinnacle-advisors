import { MetadataRoute } from 'next'

/**
 * Génère le fichier robots.txt pour le site Pinnacle Advisors
 *
 * Configuration:
 * - Autorise l'indexation de toutes les pages sauf /card/* (cartes visite digitales)
 * - Exclut /api/* de l'indexation (endpoints API)
 * - Référence le sitemap.xml pour faciliter l'indexation Google
 *
 * @see https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/card/*', '/api/*'], // Exclure cartes visite digitales et API
      },
    ],
    sitemap: 'https://pinnacle-advisors.tech/sitemap.xml',
  }
}
