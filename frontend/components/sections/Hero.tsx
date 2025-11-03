'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { ChevronDownIcon } from '@heroicons/react/24/outline';
import { useQuery } from '@tanstack/react-query';
import { fetchHero, fetchAbout, queryKeys } from '@/lib/api';
import { Button } from '@/components/ui';
import { useAnalytics } from '@/lib/analytics';

export const Hero: React.FC = () => {
  const { data: hero, isLoading } = useQuery({
    queryKey: queryKeys.hero,
    queryFn: fetchHero,
  });

  // Récupérer les données About pour les statistiques
  const { data: about } = useQuery({
    queryKey: queryKeys.about,
    queryFn: fetchAbout,
  });

  const analytics = useAnalytics();

  const handleCTAClick = () => {
    analytics.trackCTA(hero?.cta_text || 'CTA', 'hero');
    const contactSection = document.querySelector('#contact');
    if (contactSection) {
      contactSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleScrollDown = () => {
    analytics.trackEvent('scroll_down_click', { section: 'hero' });
    const servicesSection = document.querySelector('#services');
    if (servicesSection) {
      servicesSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  if (isLoading) {
    return (
      <section id="hero" className="relative h-screen flex items-center justify-center bg-gradient-bg">
        <div className="animate-pulse">
          <div className="h-12 w-96 bg-gray-300 rounded mb-4"></div>
          <div className="h-8 w-128 bg-gray-200 rounded"></div>
        </div>
      </section>
    );
  }

  if (!hero) return null;

  return (
    <section
      id="hero"
      className="relative min-h-screen flex items-center justify-center overflow-hidden"
    >
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-600 via-primary-500 to-success-500 z-0" />

      {/* Animated Background Pattern */}
      <div className="absolute inset-0 opacity-10 z-0">
        <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      {/* Content */}
      <div className="container relative z-10 py-32">
        <div className="max-w-4xl mx-auto text-center">
          {/* Title */}
          <motion.h1
            className="heading-xl text-white mb-6"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          >
            {hero.title}
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            className="text-xl md:text-2xl text-white/90 mb-12 leading-relaxed"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: 'easeOut' }}
          >
            {hero.subtitle}
          </motion.p>

          {/* CTA Button */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4, ease: 'easeOut' }}
          >
            <Button
              variant="primary"
              size="lg"
              onClick={handleCTAClick}
              className="bg-white text-primary-600 hover:bg-gray-100 shadow-2xl"
            >
              {hero.cta_text}
            </Button>
          </motion.div>

          {/* Stats/Trust Indicators - Afficher seulement si show_statistics est activé */}
          {about?.show_statistics && (
            <motion.div
              className="grid grid-cols-3 gap-8 mt-20 max-w-2xl mx-auto"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1, delay: 0.6 }}
            >
              {[
                about.years_experience > 0 && { value: `${about.years_experience}+`, label: 'Ans d\'expérience' },
                about.clients_count > 0 && { value: `${about.clients_count}+`, label: 'Clients accompagnés' },
                about.projects_count > 0 && { value: `${about.projects_count}+`, label: 'Projets réalisés' },
              ].filter((stat): stat is { value: string; label: string } => Boolean(stat)).map((stat, index) => (
                <motion.div
                  key={index}
                  className="text-white"
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.5, delay: 0.8 + index * 0.1 }}
                >
                  <div className="text-4xl md:text-5xl font-bold mb-2">{stat.value}</div>
                  <div className="text-sm md:text-base text-white/80">{stat.label}</div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </div>
      </div>

      {/* Scroll Down Indicator */}
      <motion.button
        onClick={handleScrollDown}
        className="absolute bottom-10 left-1/2 transform -translate-x-1/2 text-white z-10 flex flex-col items-center space-y-2 group cursor-pointer"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1.2 }}
        aria-label="Scroll down"
      >
        <span className="text-sm font-medium opacity-80 group-hover:opacity-100 transition-opacity">
          Découvrir
        </span>
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
        >
          <ChevronDownIcon className="h-6 w-6" />
        </motion.div>
      </motion.button>
    </section>
  );
};
