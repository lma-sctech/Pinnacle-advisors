'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { ChevronDownIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { fetchFAQ, queryKeys } from '@/lib/api';
import { cn } from '@/lib/utils';
import type { FAQCategory } from '@/types';

/**
 * Composant JSON-LD pour le FAQPage Schema
 * Améliore le référencement en fournissant des données structurées sur les FAQ
 */
function FAQPageSchema({ categories }: { categories: FAQCategory[] }) {
  const allQuestions = categories.flatMap(cat =>
    (cat.questions || [])
      .filter(q => q.is_published && q.is_active)
      .map(q => ({
        '@type': 'Question',
        name: q.question,
        acceptedAnswer: {
          '@type': 'Answer',
          text: q.answer,
        },
      }))
  );

  if (allQuestions.length === 0) return null;

  const schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: allQuestions,
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

export const FAQ: React.FC = () => {
  const { data: categories = [], isLoading } = useQuery({
    queryKey: queryKeys.faq,
    queryFn: fetchFAQ,
  });

  const [searchQuery, setSearchQuery] = useState('');
  const [expandedItems, setExpandedItems] = useState<Set<number>>(new Set());

  // Filter FAQs based on search
  const filteredCategories = categories
    .map((category) => ({
      ...category,
      questions: (category.questions || []).filter(
        (q) =>
          q.is_published &&
          q.is_active &&
          (q.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
            q.answer.toLowerCase().includes(searchQuery.toLowerCase()))
      ),
    }))
    .filter((category) => category.questions.length > 0);

  const toggleItem = (id: number) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedItems(newExpanded);
  };

  if (isLoading) {
    return (
      <section id="faq" className="section bg-white">
        <div className="container">
          <div className="animate-pulse max-w-3xl mx-auto">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-20 bg-gray-200 rounded-lg mb-4" />
            ))}
          </div>
        </div>
      </section>
    );
  }

  // Ne pas afficher la section si aucune catégorie FAQ active
  if (categories.length === 0) return null;

  return (
    <section id="faq" className="section bg-white">
      <FAQPageSchema categories={categories} />
      <div className="container">
        {/* Section Header */}
        <motion.div
          className="text-center max-w-3xl mx-auto mb-12"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="heading-lg mb-6">
            <span className="gradient-text">Questions</span> Fréquentes
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Trouvez rapidement des réponses à vos questions sur nos services supply chain
          </p>

          {/* Search Bar */}
          <div className="relative max-w-xl mx-auto">
            <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Rechercher une question..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-4 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
          </div>
        </motion.div>

        {/* FAQ by Category */}
        <div className="max-w-4xl mx-auto">
          {filteredCategories.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">
                Aucune question trouvée pour &quot;{searchQuery}&quot;
              </p>
            </div>
          ) : (
            filteredCategories.map((category, categoryIndex) => (
              <motion.div
                key={category.id}
                className="mb-12"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: categoryIndex * 0.1 }}
              >
                {/* Category Header */}
                <div className="mb-6">
                  <h3 className="heading-sm text-gray-900">{category.name}</h3>
                  {category.description && (
                    <p className="text-gray-600 mt-2">{category.description}</p>
                  )}
                </div>

                {/* Questions */}
                <div className="space-y-4">
                  {category.questions.map((faq, index) => {
                    const isExpanded = expandedItems.has(faq.id);

                    return (
                      <motion.div
                        key={faq.id}
                        className="bg-gray-50 rounded-xl border border-gray-200 overflow-hidden hover:border-primary-200 transition-colors"
                        initial={{ opacity: 0, y: 10 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.4, delay: index * 0.05 }}
                      >
                        {/* Question Button */}
                        <button
                          onClick={() => toggleItem(faq.id)}
                          className="w-full px-6 py-5 flex items-start justify-between text-left hover:bg-gray-100 transition-colors"
                        >
                          <span className="font-semibold text-gray-900 pr-8">
                            {faq.question}
                          </span>
                          <ChevronDownIcon
                            className={cn(
                              'h-5 w-5 text-primary-500 flex-shrink-0 transition-transform duration-300',
                              isExpanded && 'transform rotate-180'
                            )}
                          />
                        </button>

                        {/* Answer */}
                        <AnimatePresence>
                          {isExpanded && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: 'auto', opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.3 }}
                              className="overflow-hidden"
                            >
                              <div className="px-6 pb-5 text-gray-700 leading-relaxed whitespace-pre-line">
                                {faq.answer}
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </motion.div>
                    );
                  })}
                </div>
              </motion.div>
            ))
          )}
        </div>

        {/* Still Have Questions CTA */}
        <motion.div
          className="text-center mt-16 p-12 bg-gradient-bg rounded-2xl"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h3 className="heading-md mb-4">Vous avez d&apos;autres questions ?</h3>
          <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
            Notre équipe est à votre disposition pour répondre à toutes vos questions sur vos projets supply chain.
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
            Contactez-nous
          </a>
        </motion.div>
      </div>
    </section>
  );
};
