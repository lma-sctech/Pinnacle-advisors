import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';
import { api } from '@/lib/api';
import type { ContactInfo } from '@/types';

const inter = Inter({ subsets: ['latin'] });

/**
 * Configuration du viewport pour une indexation mobile-first optimale
 * - width: device-width pour adaptation responsive
 * - initialScale: 1 pour éviter le zoom initial
 * - maximumScale: 5 pour permettre le zoom accessibilité
 */
export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
}

// Générer les métadonnées dynamiquement depuis l'API
export async function generateMetadata(): Promise<Metadata> {
  try {
    const seoSettings = await api.getSEOSettings();

    if (seoSettings) {
      return {
        metadataBase: new URL('https://pinnacle-advisors.tech'),
        title: seoSettings.meta_title,
        description: seoSettings.meta_description,
        keywords: seoSettings.meta_keywords,
        authors: [{ name: seoSettings.author_name }],
        alternates: {
          canonical: '/',
        },
        openGraph: {
          title: seoSettings.og_title,
          description: seoSettings.og_description,
          type: 'website',
          locale: seoSettings.og_locale,
          images: seoSettings.og_image ? [seoSettings.og_image] : undefined,
        },
      };
    }
  } catch (error) {
    console.error('Error fetching SEO settings:', error);
  }

  // Fallback metadata si l'API échoue
  return {
    metadataBase: new URL('https://pinnacle-advisors.tech'),
    title: 'Pinnacle Advisors - Cabinet de Conseil Expert',
    description: 'Cabinet de conseil spécialisé en optimisation et transformation des chaînes d\'approvisionnement.',
    keywords: 'supply chain, logistique, conseil, optimisation',
    authors: [{ name: 'Pinnacle Advisors' }],
    alternates: {
      canonical: '/',
    },
    openGraph: {
      title: 'Pinnacle Advisors - Cabinet de Conseil Expert',
      description: 'Transformez votre supply chain en avantage compétitif',
      type: 'website',
      locale: 'fr_FR',
    },
  };
}

/**
 * Composant JSON-LD pour le structured data Organization
 * Améliore le référencement en fournissant des données structurées à Google
 */
async function OrganizationSchema() {
  try {
    const contactInfo: ContactInfo = await api.getContactInfo();

    const schema = {
      '@context': 'https://schema.org',
      '@type': 'ProfessionalService',
      name: contactInfo.company_name || 'Pinnacle Advisors',
      description: 'Cabinet de conseil spécialisé en optimisation et transformation des chaînes d\'approvisionnement',
      url: 'https://pinnacle-advisors.tech',
      logo: 'https://pinnacle-advisors.tech/logo.png',
      image: 'https://pinnacle-advisors.tech/og-image.png',
      telephone: contactInfo.phone,
      email: contactInfo.email,
      address: {
        '@type': 'PostalAddress',
        streetAddress: contactInfo.address,
        addressLocality: contactInfo.city,
        addressCountry: contactInfo.country,
      },
      contactPoint: {
        '@type': 'ContactPoint',
        telephone: contactInfo.phone,
        email: contactInfo.email,
        contactType: 'customer service',
        availableLanguage: ['fr', 'en'],
      },
      sameAs: [
        contactInfo.linkedin_url,
        contactInfo.twitter_url,
        contactInfo.facebook_url,
      ].filter(Boolean), // Remove null/undefined values
      openingHours: contactInfo.working_hours || 'Mo-Fr 09:00-18:00',
    };

    return (
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />
    );
  } catch (error) {
    console.error('Error loading organization schema:', error);

    // Fallback schema si l'API échoue
    const fallbackSchema = {
      '@context': 'https://schema.org',
      '@type': 'ProfessionalService',
      name: 'Pinnacle Advisors',
      description: 'Cabinet de conseil spécialisé en optimisation et transformation des chaînes d\'approvisionnement',
      url: 'https://pinnacle-advisors.tech',
      logo: 'https://pinnacle-advisors.tech/logo.png',
      contactPoint: {
        '@type': 'ContactPoint',
        contactType: 'customer service',
        availableLanguage: ['fr', 'en'],
      },
    };

    return (
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(fallbackSchema) }}
      />
    );
  }
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className="scroll-smooth">
      <body className={inter.className}>
        <OrganizationSchema />
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
