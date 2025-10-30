'use client';

import React from 'react';
import { EnvelopeIcon, PhoneIcon, MapPinIcon } from '@heroicons/react/24/outline';
import { useQuery } from '@tanstack/react-query';
import { fetchContactInfo, fetchSiteSettings, queryKeys } from '@/lib/api';
import { useAnalytics } from '@/lib/analytics';

const quickLinks = [
  { name: 'Accueil', href: '#hero' },
  { name: 'Services', href: '#services' },
  { name: 'À propos', href: '#about' },
  { name: 'Équipe', href: '#team' },
  { name: 'FAQ', href: '#faq' },
  { name: 'Contact', href: '#contact' },
];

const services = [
  'Stratégie Supply Chain',
  'Optimisation Logistique',
  'Transformation Digitale',
  'Excellence Opérationnelle',
];

export const Footer: React.FC = () => {
  const { data: contactInfo } = useQuery({
    queryKey: queryKeys.contactInfo,
    queryFn: fetchContactInfo,
  });

  const { data: siteSettings } = useQuery({
    queryKey: queryKeys.siteSettings,
    queryFn: fetchSiteSettings,
  });

  const analytics = useAnalytics();

  const handleLinkClick = (name: string) => {
    analytics.trackEvent('footer_link_click', { link: name });
  };

  const handleSocialClick = (platform: string, url: string) => {
    analytics.trackEvent('social_click', { platform, url });
  };

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main Footer */}
      <div className="container py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          {/* Company Info */}
          <div>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-success-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">P</span>
              </div>
              <span className="font-bold text-xl">{siteSettings?.company_name || 'Pinnacle Advisors'}</span>
            </div>
            <p className="text-gray-400 mb-6">
              {siteSettings?.company_tagline || 'Cabinet de conseil expert en optimisation et transformation des chaînes d\'approvisionnement.'}
            </p>
            {contactInfo && (
              <div className="space-y-3 text-sm">
                <div className="flex items-start space-x-3">
                  <MapPinIcon className="h-5 w-5 text-primary-400 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-400">
                    {contactInfo.address}, {contactInfo.city}
                  </span>
                </div>
                <div className="flex items-center space-x-3">
                  <PhoneIcon className="h-5 w-5 text-primary-400 flex-shrink-0" />
                  <a
                    href={`tel:${contactInfo.phone}`}
                    className="text-gray-400 hover:text-primary-400 transition-colors"
                    onClick={() => handleLinkClick('phone')}
                  >
                    {contactInfo.phone}
                  </a>
                </div>
                <div className="flex items-center space-x-3">
                  <EnvelopeIcon className="h-5 w-5 text-primary-400 flex-shrink-0" />
                  <a
                    href={`mailto:${contactInfo.email}`}
                    className="text-gray-400 hover:text-primary-400 transition-colors"
                    onClick={() => handleLinkClick('email')}
                  >
                    {contactInfo.email}
                  </a>
                </div>
              </div>
            )}
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-lg mb-6">{siteSettings?.footer_nav_title || 'Navigation'}</h3>
            <ul className="space-y-3">
              {quickLinks.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="text-gray-400 hover:text-primary-400 transition-colors"
                    onClick={(e) => {
                      e.preventDefault();
                      handleLinkClick(link.name);
                      const element = document.querySelector(link.href);
                      if (element) {
                        element.scrollIntoView({ behavior: 'smooth' });
                      }
                    }}
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="font-semibold text-lg mb-6">{siteSettings?.footer_services_title || 'Nos Services'}</h3>
            <ul className="space-y-3">
              {services.map((service) => (
                <li key={service}>
                  <a
                    href="#services"
                    className="text-gray-400 hover:text-primary-400 transition-colors"
                    onClick={(e) => {
                      e.preventDefault();
                      handleLinkClick(service);
                      const element = document.querySelector('#services');
                      if (element) {
                        element.scrollIntoView({ behavior: 'smooth' });
                      }
                    }}
                  >
                    {service}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Social & Hours */}
          <div>
            <h3 className="font-semibold text-lg mb-6">{siteSettings?.footer_follow_title || 'Suivez-nous'}</h3>
            {contactInfo && (
              <>
                <div className="flex space-x-4 mb-6">
                  {contactInfo.linkedin_url && (
                    <a
                      href={contactInfo.linkedin_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-primary-500 transition-all duration-200"
                      onClick={() => handleSocialClick('LinkedIn', contactInfo.linkedin_url!)}
                      aria-label="LinkedIn"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
                      </svg>
                    </a>
                  )}
                  {contactInfo.twitter_url && (
                    <a
                      href={contactInfo.twitter_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-primary-500 transition-all duration-200"
                      onClick={() => handleSocialClick('Twitter', contactInfo.twitter_url!)}
                      aria-label="Twitter"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                      </svg>
                    </a>
                  )}
                </div>
                <div className="text-sm">
                  <p className="text-gray-400 mb-2">{siteSettings?.footer_hours_label || 'Horaires d\'ouverture'}</p>
                  <p className="text-gray-300 font-medium">{contactInfo.working_hours}</p>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800">
        <div className="container py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-gray-400 text-sm">
              {(siteSettings?.footer_copyright_text || '© {year} Pinnacle Advisors. Tous droits réservés.').replace('{year}', new Date().getFullYear().toString())}
            </p>
            <div className="flex space-x-6 text-sm">
              <a
                href="#"
                className="text-gray-400 hover:text-primary-400 transition-colors"
                onClick={(e) => {
                  e.preventDefault();
                  handleLinkClick(siteSettings?.footer_legal_text || 'Mentions légales');
                }}
              >
                {siteSettings?.footer_legal_text || 'Mentions légales'}
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-primary-400 transition-colors"
                onClick={(e) => {
                  e.preventDefault();
                  handleLinkClick(siteSettings?.footer_privacy_text || 'Politique de confidentialité');
                }}
              >
                {siteSettings?.footer_privacy_text || 'Politique de confidentialité'}
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-primary-400 transition-colors"
                onClick={(e) => {
                  e.preventDefault();
                  handleLinkClick(siteSettings?.footer_terms_text || 'CGV');
                }}
              >
                {siteSettings?.footer_terms_text || 'CGV'}
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};
