'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import {
  ChartBarIcon,
  TruckIcon,
  CpuChipIcon,
  ArchiveBoxIcon,
  ShoppingCartIcon,
  SparklesIcon,
  CogIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline';
import { fetchServices, queryKeys } from '@/lib/api';
import { Card, CardTitle, CardDescription } from '@/components/ui';
import type { Service } from '@/types';

/**
 * Composant JSON-LD pour le Service Schema
 * Améliore le référencement en fournissant des données structurées sur les services
 */
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
        '@type': 'ProfessionalService',
        name: 'Pinnacle Advisors',
      },
    })),
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

// Icon mapping
const iconMap: Record<string, React.ElementType> = {
  'chart-bar': ChartBarIcon,
  'truck': TruckIcon,
  'cpu-chip': CpuChipIcon,
  'archive-box': ArchiveBoxIcon,
  'shopping-cart': ShoppingCartIcon,
  'leaf': SparklesIcon,
  'cog': CogIcon,
  'academic-cap': AcademicCapIcon,
};

export const Services: React.FC = () => {
  const { data: services = [], isLoading } = useQuery({
    queryKey: queryKeys.services,
    queryFn: fetchServices,
  });

  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  if (isLoading) {
    return (
      <section id="services" className="section bg-white">
        <div className="container">
          <div className="animate-pulse grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-64 bg-gray-200 rounded-xl" />
            ))}
          </div>
        </div>
      </section>
    );
  }

  // Ne pas afficher la section si aucun service actif
  if (services.length === 0) return null;

  return (
    <section id="services" className="section bg-gradient-bg">
      <ServiceSchema services={services} />
      <div className="container">
        {/* Section Header */}
        <motion.div
          className="text-center max-w-3xl mx-auto mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="heading-lg mb-6">
            <span className="gradient-text">Nos Services</span> Supply Chain
          </h2>
          <p className="text-xl text-gray-600">
            Une expertise 360° pour transformer votre chaîne d&apos;approvisionnement en avantage compétitif
          </p>
        </motion.div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => {
            const Icon = iconMap[service.icon] || CogIcon;
            const isExpanded = expandedIndex === index;

            return (
              <motion.div
                key={service.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card
                  hover
                  className="h-full flex flex-col cursor-pointer"
                  onClick={() => setExpandedIndex(isExpanded ? null : index)}
                >
                  {/* Icon */}
                  <div className="mb-6">
                    <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary-500 to-success-500 flex items-center justify-center shadow-lg">
                      <Icon className="h-7 w-7 text-white" />
                    </div>
                  </div>

                  {/* Title */}
                  <CardTitle className="mb-4">{service.title}</CardTitle>

                  {/* Description */}
                  <CardDescription
                    className={`flex-grow ${
                      isExpanded ? '' : 'line-clamp-3'
                    }`}
                  >
                    {service.description}
                  </CardDescription>

                  {/* Read More Link */}
                  <button
                    className="mt-4 text-primary-500 hover:text-primary-600 font-medium text-sm flex items-center group"
                    onClick={(e) => {
                      e.stopPropagation();
                      setExpandedIndex(isExpanded ? null : index);
                    }}
                  >
                    {isExpanded ? 'Voir moins' : 'En savoir plus'}
                    <svg
                      className={`ml-2 h-4 w-4 transition-transform ${
                        isExpanded ? 'rotate-90' : ''
                      } group-hover:translate-x-1`}
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </button>
                </Card>
              </motion.div>
            );
          })}
        </div>

        {/* CTA */}
        <motion.div
          className="text-center mt-16"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <p className="text-gray-600 mb-6">
            Besoin d&apos;un conseil personnalisé sur votre projet supply chain ?
          </p>
          <a
            href="#contact"
            onClick={(e) => {
              e.preventDefault();
              const contactSection = document.querySelector('#contact');
              if (contactSection) {
                contactSection.scrollIntoView({ behavior: 'smooth' });
              }
            }}
            className="inline-flex items-center px-8 py-4 bg-primary-500 text-white font-semibold rounded-lg hover:bg-primary-600 transition-all duration-200 shadow-lg shadow-primary-500/30"
          >
            Discutons de votre projet
          </a>
        </motion.div>
      </div>
    </section>
  );
};
