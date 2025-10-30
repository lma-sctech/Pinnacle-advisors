'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useQuery, useMutation } from '@tanstack/react-query';
import {
  EnvelopeIcon,
  PhoneIcon,
  MapPinIcon,
  CheckCircleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { fetchContactInfo, queryKeys, api } from '@/lib/api';
import { Input, Textarea, Select, Button } from '@/components/ui';
import { useAnalytics } from '@/lib/analytics';
import type { ContactFormData } from '@/types';

// Validation Schema with Zod
const contactSchema = z.object({
  name: z.string().min(2, 'Le nom doit contenir au moins 2 caractères'),
  email: z.string().email('Adresse email invalide'),
  phone: z.string().optional(),
  company: z.string().optional(),
  need_type: z.enum(['optimization', 'audit', 'strategy', 'digital', 'training', 'other']),
  message: z.string().min(20, 'Le message doit contenir au moins 20 caractères'),
});

const needTypeOptions = [
  { value: 'optimization', label: 'Optimisation de la supply chain' },
  { value: 'audit', label: 'Audit et diagnostic' },
  { value: 'strategy', label: 'Stratégie logistique' },
  { value: 'digital', label: 'Transformation digitale' },
  { value: 'training', label: 'Formation' },
  { value: 'other', label: 'Autre' },
];

export const Contact: React.FC = () => {
  const { data: contactInfo } = useQuery({
    queryKey: queryKeys.contactInfo,
    queryFn: fetchContactInfo,
  });

  const analytics = useAnalytics();
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
  });

  const mutation = useMutation({
    mutationFn: (data: ContactFormData) => api.submitContact(data),
    onSuccess: () => {
      setSubmitStatus('success');
      analytics.trackFormSubmit('contact', true);
      reset();
      setTimeout(() => setSubmitStatus('idle'), 5000);
    },
    onError: (error) => {
      setSubmitStatus('error');
      analytics.trackFormSubmit('contact', false);
      console.error('Contact form error:', error);
      setTimeout(() => setSubmitStatus('idle'), 5000);
    },
  });

  const onSubmit = (data: ContactFormData) => {
    mutation.mutate(data);
  };

  return (
    <section id="contact" className="section bg-gradient-bg">
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
            <span className="gradient-text">Contactez-nous</span>
          </h2>
          <p className="text-xl text-gray-600">
            Discutons de votre projet supply chain. Notre équipe vous répondra sous 24h.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          {/* Contact Form */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-200">
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {/* Name */}
                <Input
                  label="Nom complet"
                  placeholder="Jean Dupont"
                  required
                  error={errors.name?.message}
                  {...register('name')}
                />

                {/* Email */}
                <Input
                  label="Email"
                  type="email"
                  placeholder="jean.dupont@entreprise.com"
                  required
                  error={errors.email?.message}
                  {...register('email')}
                />

                {/* Phone & Company */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input
                    label="Téléphone"
                    type="tel"
                    placeholder="+33 6 12 34 56 78"
                    error={errors.phone?.message}
                    {...register('phone')}
                  />
                  <Input
                    label="Entreprise"
                    placeholder="Nom de votre entreprise"
                    error={errors.company?.message}
                    {...register('company')}
                  />
                </div>

                {/* Need Type */}
                <Select
                  label="Type de besoin"
                  required
                  options={needTypeOptions}
                  error={errors.need_type?.message}
                  {...register('need_type')}
                />

                {/* Message */}
                <Textarea
                  label="Message"
                  placeholder="Décrivez-nous votre projet, vos enjeux, vos objectifs..."
                  rows={6}
                  required
                  error={errors.message?.message}
                  {...register('message')}
                />

                {/* Submit Button */}
                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  isLoading={mutation.isPending}
                  className="w-full"
                >
                  {mutation.isPending ? 'Envoi en cours...' : 'Envoyer le message'}
                </Button>

                {/* Success/Error Messages */}
                {submitStatus === 'success' && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center space-x-3 p-4 bg-success-50 border border-success-200 rounded-lg text-success-700"
                  >
                    <CheckCircleIcon className="h-5 w-5 flex-shrink-0" />
                    <span className="font-medium">Message envoyé avec succès ! Nous vous recontacterons sous 24h.</span>
                  </motion.div>
                )}

                {submitStatus === 'error' && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center space-x-3 p-4 bg-danger-50 border border-danger-200 rounded-lg text-danger-700"
                  >
                    <XCircleIcon className="h-5 w-5 flex-shrink-0" />
                    <span className="font-medium">Une erreur est survenue. Veuillez réessayer.</span>
                  </motion.div>
                )}
              </form>
            </div>
          </motion.div>

          {/* Contact Info */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="space-y-8">
              {/* Info Cards */}
              {contactInfo && (
                <>
                  <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center flex-shrink-0">
                        <EnvelopeIcon className="h-6 w-6 text-primary-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Email</h3>
                        <a
                          href={`mailto:${contactInfo.email}`}
                          className="text-primary-600 hover:text-primary-700 transition-colors"
                        >
                          {contactInfo.email}
                        </a>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 rounded-lg bg-success-100 flex items-center justify-center flex-shrink-0">
                        <PhoneIcon className="h-6 w-6 text-success-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Téléphone</h3>
                        <a
                          href={`tel:${contactInfo.phone}`}
                          className="text-success-600 hover:text-success-700 transition-colors"
                        >
                          {contactInfo.phone}
                        </a>
                        <p className="text-sm text-gray-500 mt-1">{contactInfo.working_hours}</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 rounded-lg bg-warning-100 flex items-center justify-center flex-shrink-0">
                        <MapPinIcon className="h-6 w-6 text-warning-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Adresse</h3>
                        <p className="text-gray-600">
                          {contactInfo.address}
                          <br />
                          {contactInfo.city}, {contactInfo.country}
                        </p>
                      </div>
                    </div>
                  </div>
                </>
              )}

              {/* Additional Info */}
              <div className="bg-gradient-to-br from-primary-500 to-success-500 p-8 rounded-xl text-white">
                <h3 className="text-xl font-bold mb-4">Pourquoi nous choisir ?</h3>
                <ul className="space-y-3">
                  {[
                    'Expertise supply chain 360°',
                    'ROI garanti sur vos projets',
                    'Équipe d\'experts terrain',
                    'Accompagnement personnalisé',
                  ].map((item, index) => (
                    <li key={index} className="flex items-center space-x-3">
                      <CheckCircleIcon className="h-5 w-5 flex-shrink-0" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};
