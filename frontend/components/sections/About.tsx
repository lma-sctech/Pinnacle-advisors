'use client';

import React, { useEffect, useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { CheckCircleIcon } from '@heroicons/react/24/solid';
import { fetchAbout, queryKeys } from '@/lib/api';
import { formatNumber } from '@/lib/utils';

export const About: React.FC = () => {
  const { data: about, isLoading } = useQuery({
    queryKey: queryKeys.about,
    queryFn: fetchAbout,
  });

  if (isLoading) {
    return (
      <section id="about" className="section bg-white">
        <div className="container">
          <div className="animate-pulse">
            <div className="h-12 w-64 bg-gray-300 rounded mb-8 mx-auto" />
            <div className="h-48 bg-gray-200 rounded" />
          </div>
        </div>
      </section>
    );
  }

  if (!about) return null;

  const values = about.values?.split('\n').filter((v) => v.trim()) || [];

  return (
    <section id="about" className="section bg-white">
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
            <span className="gradient-text">{about.title}</span>
          </h2>
          <p className="text-xl text-gray-600 leading-relaxed">
            {about.description}
          </p>
        </motion.div>

        {/* Stats Counter - Afficher seulement si show_statistics est activé */}
        {about.show_statistics && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
            {about.years_experience > 0 && (
              <StatCard
                value={about.years_experience}
                label="Ans d'expérience"
                suffix="+"
                delay={0}
              />
            )}
            {about.clients_count > 0 && (
              <StatCard
                value={about.clients_count}
                label="Clients accompagnés"
                suffix="+"
                delay={0.2}
              />
            )}
            {about.projects_count > 0 && (
              <StatCard
                value={about.projects_count}
                label="Projets réalisés"
                suffix="+"
                delay={0.4}
              />
            )}
          </div>
        )}

        {/* Mission & Vision */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
          {/* Mission */}
          {about.mission_statement && (
            <motion.div
              className="bg-gradient-to-br from-primary-50 to-white p-8 rounded-2xl border border-primary-100"
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <h3 className="heading-sm mb-4 text-primary-600">Notre Mission</h3>
              <p className="text-gray-700 leading-relaxed">{about.mission_statement}</p>
            </motion.div>
          )}

          {/* Vision */}
          {about.vision_statement && (
            <motion.div
              className="bg-gradient-to-br from-success-50 to-white p-8 rounded-2xl border border-success-100"
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <h3 className="heading-sm mb-4 text-success-600">Notre Vision</h3>
              <p className="text-gray-700 leading-relaxed">{about.vision_statement}</p>
            </motion.div>
          )}
        </div>

        {/* Values */}
        {values.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h3 className="heading-md text-center mb-10">Nos Valeurs</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
              {values.map((value, index) => {
                // Parse "Title: Description" format
                const [title, description] = value.includes(':')
                  ? value.split(':').map((s) => s.trim())
                  : [value, ''];

                return (
                  <motion.div
                    key={index}
                    className="flex items-start space-x-4 p-6 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                  >
                    <CheckCircleIcon className="h-6 w-6 text-primary-500 flex-shrink-0 mt-1" />
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-1">{title}</h4>
                      {description && (
                        <p className="text-sm text-gray-600">{description}</p>
                      )}
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        )}
      </div>
    </section>
  );
};

// ============================================================================
// STAT CARD COMPONENT WITH ANIMATED COUNTER
// ============================================================================

interface StatCardProps {
  value: number;
  label: string;
  suffix?: string;
  delay?: number;
}

const StatCard: React.FC<StatCardProps> = ({ value, label, suffix = '', delay = 0 }) => {
  const [count, setCount] = useState(0);
  const [hasAnimated, setHasAnimated] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasAnimated) {
          setHasAnimated(true);
          animateValue(0, value, 2000);
        }
      },
      { threshold: 0.5 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, [value, hasAnimated]);

  const animateValue = (start: number, end: number, duration: number) => {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
      current += increment;
      if (current >= end) {
        setCount(end);
        clearInterval(timer);
      } else {
        setCount(Math.floor(current));
      }
    }, 16);
  };

  return (
    <motion.div
      ref={ref}
      className="text-center p-8 bg-gradient-to-br from-gray-50 to-white rounded-2xl border border-gray-200 shadow-sm"
      initial={{ opacity: 0, scale: 0.9 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
    >
      <div className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-primary-600 to-success-500 bg-clip-text text-transparent mb-3">
        {formatNumber(count)}
        {suffix}
      </div>
      <div className="text-gray-600 font-medium">{label}</div>
    </motion.div>
  );
};
