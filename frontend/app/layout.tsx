import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';
import { api } from '@/lib/api';

const inter = Inter({ subsets: ['latin'] });

// Générer les métadonnées dynamiquement depuis l'API
export async function generateMetadata(): Promise<Metadata> {
  try {
    const seoSettings = await api.getSEOSettings();

    if (seoSettings) {
      return {
        title: seoSettings.meta_title,
        description: seoSettings.meta_description,
        keywords: seoSettings.meta_keywords,
        authors: [{ name: seoSettings.author_name }],
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
    title: 'Pinnacle Advisors - Cabinet de Conseil Expert',
    description: 'Cabinet de conseil spécialisé en optimisation et transformation des chaînes d\'approvisionnement.',
    keywords: 'supply chain, logistique, conseil, optimisation',
    authors: [{ name: 'Pinnacle Advisors' }],
    openGraph: {
      title: 'Pinnacle Advisors - Cabinet de Conseil Expert',
      description: 'Transformez votre supply chain en avantage compétitif',
      type: 'website',
      locale: 'fr_FR',
    },
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className="scroll-smooth">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
