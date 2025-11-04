'use client';

import React from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { EnvelopeIcon } from '@heroicons/react/24/outline';
import { fetchTeam, fetchRecruitment, fetchTeamHeader, queryKeys } from '@/lib/api';
import { Card } from '@/components/ui';

export const Team: React.FC = () => {
  const { data: team = [], isLoading } = useQuery({
    queryKey: queryKeys.team,
    queryFn: fetchTeam,
  });

  const { data: recruitment } = useQuery({
    queryKey: queryKeys.recruitment,
    queryFn: fetchRecruitment,
  });

  const { data: teamHeader } = useQuery({
    queryKey: queryKeys.teamHeader,
    queryFn: fetchTeamHeader,
  });

  if (isLoading) {
    return (
      <section id="team" className="section bg-gradient-bg">
        <div className="container">
          <div className="animate-pulse grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-96 bg-gray-200 rounded-xl" />
            ))}
          </div>
        </div>
      </section>
    );
  }

  // Ne pas afficher la section si aucun membre actif
  if (team.length === 0) return null;

  return (
    <section id="team" className="section bg-gradient-bg">
      <div className="container">
        {/* Section Header */}
        <motion.div
          className="text-center max-w-3xl mx-auto mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          {teamHeader && (
            <>
              <h2 className="heading-lg mb-6">
                <span className="gradient-text">{teamHeader.title_part1}</span> {teamHeader.title_part2}
              </h2>
              {teamHeader.description && (
                <p className="text-xl text-gray-600">
                  {teamHeader.description}
                </p>
              )}
            </>
          )}
        </motion.div>

        {/* Team Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {team.map((member, index) => (
            <motion.div
              key={member.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card hover padding="none" className="overflow-hidden group h-full flex flex-col">
                {/* Photo (Placeholder) */}
                <div className="relative h-64 bg-gradient-to-br from-primary-400 to-success-400 overflow-hidden">
                  {member.photo ? (
                    <Image
                      src={member.photo}
                      alt={`Photo de ${member.name}, ${member.position}`}
                      fill
                      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                      className="object-cover transition-transform duration-500 group-hover:scale-110"
                      loading="lazy"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <div className="text-8xl font-bold text-white opacity-50">
                        {member.name
                          .split(' ')
                          .map((n) => n[0])
                          .join('')}
                      </div>
                    </div>
                  )}

                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end p-6">
                    <div className="flex space-x-4">
                      {member.linkedin_url && (
                        <a
                          href={member.linkedin_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center hover:bg-primary-500 transition-colors"
                          aria-label={`LinkedIn de ${member.name}`}
                        >
                          <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
                          </svg>
                        </a>
                      )}
                      {member.email && (
                        <a
                          href={`mailto:${member.email}`}
                          className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center hover:bg-primary-500 transition-colors"
                          aria-label={`Email de ${member.name}`}
                        >
                          <EnvelopeIcon className="w-5 h-5 text-white" />
                        </a>
                      )}
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="p-6 flex-grow flex flex-col">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{member.name}</h3>
                  <p className="text-primary-600 font-medium mb-4">{member.position}</p>
                  <p className="text-gray-600 text-sm leading-relaxed line-clamp-4 flex-grow">
                    {member.bio}
                  </p>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Join Team CTA (optional) */}
        {recruitment && (
          <motion.div
            className="text-center mt-16 p-12 bg-white rounded-2xl border border-gray-200"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h3 className="heading-md mb-4">{recruitment.title}</h3>
            <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
              {recruitment.description}
            </p>
            <a
              href={`mailto:${recruitment.email}`}
              className="inline-flex items-center px-8 py-4 bg-success-500 text-white font-semibold rounded-lg hover:bg-success-600 transition-all duration-200 shadow-lg shadow-success-500/30"
            >
              {recruitment.cta_text}
            </a>
          </motion.div>
        )}
      </div>
    </section>
  );
};
