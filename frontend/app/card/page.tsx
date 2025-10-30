'use client';

import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { ArrowLeftIcon, EnvelopeIcon, PhoneIcon } from '@heroicons/react/24/outline';
import { fetchBusinessCard, api, queryKeys } from '@/lib/api';
import Link from 'next/link';
import Image from 'next/image';

export default function BusinessCardPage() {
  const { data: card, isLoading, error } = useQuery({
    queryKey: queryKeys.businessCard,
    queryFn: fetchBusinessCard,
    retry: 2,
  });

  // Increment views on page load
  useEffect(() => {
    if (card?.id) {
      api.incrementBusinessCardViews(card.id).catch(console.error);

      // Check if came from QR code (you can detect this via URL param if needed)
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('source') === 'qr') {
        api.incrementQRScans(card.id).catch(console.error);
      }
    }
  }, [card?.id]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-green-500">
        <div className="text-white text-xl">Chargement...</div>
      </div>
    );
  }

  if (error || !card) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-green-500">
        <div className="text-white text-center">
          <p className="text-xl mb-4">Carte de visite non disponible</p>
          <Link href="/" className="text-white underline">
            Retour au site
          </Link>
        </div>
      </div>
    );
  }

  const handleDownloadVCard = () => {
    const vcardUrl = api.getVCardUrl(card.id);
    window.open(vcardUrl, '_blank');
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden"
      style={{
        background: `linear-gradient(135deg, ${card.background_gradient_start} 0%, ${card.background_gradient_end} 100%)`,
      }}
    >
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-20 w-72 h-72 rounded-full opacity-20"
          style={{ background: card.accent_color }}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.2, 0.3, 0.2],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
        <motion.div
          className="absolute bottom-20 right-20 w-96 h-96 rounded-full opacity-20"
          style={{ background: card.accent_color }}
          animate={{
            scale: [1, 1.3, 1],
            opacity: [0.2, 0.25, 0.2],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: 1,
          }}
        />
      </div>

      {/* Back button */}
      <Link
        href="/"
        className="absolute top-6 left-6 z-50 flex items-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-md rounded-full text-white hover:bg-white/30 transition-all"
      >
        <ArrowLeftIcon className="w-5 h-5" />
        <span className="hidden sm:inline">Retour au site</span>
      </Link>

      {/* Business Card - Glassmorphism */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative z-10 w-full max-w-2xl"
      >
        <div className="bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl overflow-hidden border border-white/20">
          {/* Card Content */}
          <div className="p-8 md:p-12">
            {/* Header with photo and basic info */}
            <div className="flex flex-col md:flex-row items-center md:items-start gap-6 mb-8">
              {/* Photo */}
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: 'spring' }}
                className="relative w-32 h-32 md:w-40 md:h-40 rounded-full overflow-hidden border-4 border-white/30 flex-shrink-0"
              >
                <Image
                  src={card.photo}
                  alt={card.full_name}
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 128px, 160px"
                />
              </motion.div>

              {/* Name and title */}
              <div className="flex-1 text-center md:text-left">
                <motion.h1
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                  className="text-3xl md:text-4xl font-bold text-white mb-2"
                >
                  {card.full_name}
                </motion.h1>
                <motion.p
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4 }}
                  className="text-xl text-white/90 mb-3"
                >
                  {card.job_title}
                </motion.p>
                <motion.p
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 }}
                  className="text-white/80 italic"
                >
                  {card.tagline}
                </motion.p>
              </div>
            </div>

            {/* Company logo and name */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="flex items-center justify-center gap-3 mb-8 pb-8 border-b border-white/20"
            >
              {card.company_logo && (
                <div className="relative w-12 h-12">
                  <Image
                    src={card.company_logo}
                    alt={card.company_name}
                    fill
                    className="object-contain"
                    sizes="48px"
                  />
                </div>
              )}
              <p className="text-xl text-white font-semibold">{card.company_name}</p>
            </motion.div>

            {/* Bio */}
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
              className="text-white/90 text-center md:text-left mb-8 leading-relaxed"
            >
              {card.bio}
            </motion.p>

            {/* Action buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6"
            >
              {/* Email */}
              <a
                href={`mailto:${card.email}`}
                className="flex items-center justify-center gap-3 px-6 py-3 bg-white/20 backdrop-blur-md rounded-xl text-white hover:bg-white/30 transition-all border border-white/30"
              >
                <EnvelopeIcon className="w-5 h-5" />
                <span className="font-medium">Email</span>
              </a>

              {/* Phone */}
              <a
                href={`tel:${card.phone}`}
                className="flex items-center justify-center gap-3 px-6 py-3 bg-white/20 backdrop-blur-md rounded-xl text-white hover:bg-white/30 transition-all border border-white/30"
              >
                <PhoneIcon className="w-5 h-5" />
                <span className="font-medium">Téléphone</span>
              </a>

              {/* LinkedIn */}
              <a
                href={card.linkedin_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-3 px-6 py-3 bg-white/20 backdrop-blur-md rounded-xl text-white hover:bg-white/30 transition-all border border-white/30"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
                <span className="font-medium">LinkedIn</span>
              </a>

              {/* Download vCard */}
              <button
                onClick={handleDownloadVCard}
                className="flex items-center justify-center gap-3 px-6 py-3 bg-white text-gray-900 rounded-xl hover:bg-white/90 transition-all font-semibold shadow-lg"
                style={{ background: card.accent_color, color: 'white' }}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="font-medium">Enregistrer le contact</span>
              </button>
            </motion.div>

            {/* Additional social links */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9 }}
              className="flex items-center justify-center gap-4 pt-6 border-t border-white/20"
            >
              {card.twitter_url && (
                <a
                  href={card.twitter_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-white/70 hover:text-white transition-colors"
                >
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                  </svg>
                </a>
              )}
              {card.github_url && (
                <a
                  href={card.github_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-white/70 hover:text-white transition-colors"
                >
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                  </svg>
                </a>
              )}
              <a
                href={card.website_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-white/70 hover:text-white transition-colors text-sm"
              >
                {card.website_url.replace('https://', '').replace('http://', '')}
              </a>
            </motion.div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
