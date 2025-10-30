'use client';

import { useEffect } from 'react';
import { Navbar, Footer } from '@/components/layout';
import { Hero, Services, About, Team, FAQ, Contact } from '@/components/sections';
import { useAnalytics } from '@/lib/analytics';

export default function Home() {
  const analytics = useAnalytics();

  useEffect(() => {
    // Track initial page view
    analytics.trackPageView({
      page_url: '/',
      page_title: 'Accueil - Pinnacle Advisors',
    });

    // Setup intersection observer for section tracking
    const observerOptions = {
      threshold: 0.5,
      rootMargin: '0px',
    };

    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const sectionId = entry.target.id;
          analytics.trackSectionView(sectionId);
        }
      });
    }, observerOptions);

    // Observe all sections
    const sections = document.querySelectorAll('section[id]');
    sections.forEach((section) => sectionObserver.observe(section));

    return () => {
      sections.forEach((section) => sectionObserver.unobserve(section));
    };
  }, [analytics]);

  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <Services />
        <About />
        <Team />
        <FAQ />
        <Contact />
      </main>
      <Footer />
    </>
  );
}
