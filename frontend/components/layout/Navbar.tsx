'use client';

import React, { useState, useEffect } from 'react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { Button } from '@/components/ui';
import { cn } from '@/lib/utils';
import { useAnalytics } from '@/lib/analytics';
import { useQuery } from '@tanstack/react-query';
import { queryKeys, fetchSiteSettings } from '@/lib/api';

const navigation = [
  { name: 'Accueil', href: '#hero' },
  { name: 'Services', href: '#services' },
  { name: 'À propos', href: '#about' },
  { name: 'Équipe', href: '#team' },
  { name: 'FAQ', href: '#faq' },
  { name: 'Contact', href: '#contact' },
];

export const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const analytics = useAnalytics();

  // Récupérer les paramètres du site depuis l'API
  const { data: siteSettings } = useQuery({
    queryKey: queryKeys.siteSettings,
    queryFn: fetchSiteSettings,
  });

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleNavClick = (name: string, href: string) => {
    analytics.trackEvent('nav_click', { nav_item: name });
    setIsMobileMenuOpen(false);

    // Smooth scroll
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleCTAClick = () => {
    analytics.trackCTA('navbar_contact', 'navbar');
    const contactSection = document.querySelector('#contact');
    if (contactSection) {
      contactSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        isScrolled
          ? 'bg-white/95 backdrop-blur-md shadow-lg'
          : 'bg-transparent'
      )}
    >
      <div className="container">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <div className="flex-shrink-0">
            <a
              href="#hero"
              onClick={(e) => {
                e.preventDefault();
                handleNavClick('Logo', '#hero');
              }}
              className="flex items-center space-x-3"
            >
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-success-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">P</span>
              </div>
              <span
                className={cn(
                  'font-bold text-xl transition-colors',
                  isScrolled ? 'text-gray-900' : 'text-white'
                )}
              >
                {siteSettings?.company_name || 'Pinnacle Advisors'}
              </span>
            </a>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navigation.map((item) => (
              <a
                key={item.name}
                href={item.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleNavClick(item.name, item.href);
                }}
                className={cn(
                  'px-4 py-2 rounded-lg font-medium transition-all duration-200',
                  isScrolled
                    ? 'text-gray-700 hover:text-primary-500 hover:bg-primary-50'
                    : 'text-white/90 hover:text-white hover:bg-white/10'
                )}
              >
                {item.name}
              </a>
            ))}
          </div>

          {/* CTA Button (Desktop) */}
          <div className="hidden md:block">
            <Button
              variant={isScrolled ? 'primary' : 'outline'}
              size="md"
              onClick={handleCTAClick}
              className={!isScrolled ? 'border-white text-white hover:bg-white hover:text-primary-500' : ''}
            >
              {siteSettings?.navbar_cta_text || 'Demander un devis'}
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className={cn(
                'p-2 rounded-lg transition-colors',
                isScrolled
                  ? 'text-gray-700 hover:bg-gray-100'
                  : 'text-white hover:bg-white/10'
              )}
              aria-label="Toggle menu"
            >
              {isMobileMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200 shadow-xl animate-slide-down">
          <div className="container py-4 space-y-2">
            {navigation.map((item) => (
              <a
                key={item.name}
                href={item.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleNavClick(item.name, item.href);
                }}
                className="block px-4 py-3 rounded-lg font-medium text-gray-700 hover:text-primary-500 hover:bg-primary-50 transition-colors"
              >
                {item.name}
              </a>
            ))}
            <div className="pt-2">
              <Button
                variant="primary"
                size="md"
                onClick={handleCTAClick}
                className="w-full"
              >
                {siteSettings?.mobile_menu_cta_text || 'Demander un devis'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};
