// ============================================================================
// WEBSITE TYPES (aligned with Django models)
// ============================================================================

export interface HeroSection {
  id: number;
  title: string;
  subtitle: string;
  cta_text: string;
  cta_link: string;
  background_image?: string;
  video_url?: string;
  is_active: boolean;
  updated_at: string;
}

export interface Service {
  id: number;
  title: string;
  description: string;
  icon: string;
  order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AboutSection {
  id: number;
  title: string;
  description: string;
  mission_statement?: string;
  vision_statement?: string;
  values?: string;
  image?: string;
  show_statistics: boolean;
  years_experience: number;
  clients_count: number;
  projects_count: number;
  is_active: boolean;
  updated_at: string;
}

export interface TeamMember {
  id: number;
  name: string;
  position: string;
  bio: string;
  photo?: string;
  linkedin_url?: string;
  email?: string;
  order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface FAQCategory {
  id: number;
  name: string;
  description?: string;
  order: number;
  is_active: boolean;
  questions: FAQ[];
  created_at: string;
  updated_at: string;
}

export interface FAQ {
  id: number;
  category: number;
  question: string;
  answer: string;
  order: number;
  is_published: boolean;
  is_active: boolean;
  views_count: number;
  created_at: string;
  updated_at: string;
}

export interface ContactInfo {
  id: number;
  company_name: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  country: string;
  linkedin_url?: string;
  twitter_url?: string;
  facebook_url?: string;
  working_hours: string;
  is_active: boolean;
  updated_at: string;
}

export interface ContactSubmission {
  name: string;
  email: string;
  phone?: string;
  company?: string;
  need_type: 'optimization' | 'audit' | 'strategy' | 'digital' | 'training' | 'other';
  message: string;
}

export interface BusinessCard {
  id: number;
  full_name: string;
  job_title: string;
  tagline: string;
  bio: string;
  photo: string;
  email: string;
  phone: string;
  company_name: string;
  company_logo?: string;
  website_url: string;
  linkedin_url: string;
  twitter_url?: string;
  github_url?: string;
  accent_color: string;
  background_gradient_start: string;
  background_gradient_end: string;
}

export interface Recruitment {
  id: number;
  title: string;
  description: string;
  cta_text: string;
  email: string;
}

export interface TeamHeader {
  id: number;
  title_part1: string;
  title_part2: string;
  description?: string;
}

export interface SEOSettings {
  id: number;
  meta_title: string;
  meta_description: string;
  meta_keywords: string;
  author_name: string;
  og_title: string;
  og_description: string;
  og_locale: string;
  og_image?: string;
}

export interface SiteSettings {
  id: number;
  company_name: string;
  company_tagline: string;
  navbar_cta_text: string;
  mobile_menu_cta_text: string;
  footer_nav_title: string;
  footer_services_title: string;
  footer_follow_title: string;
  footer_hours_label: string;
  footer_copyright_text: string;
  footer_legal_text: string;
  footer_privacy_text: string;
  footer_terms_text: string;
}

// ============================================================================
// ANALYTICS TYPES
// ============================================================================

export interface UserSession {
  session_id?: string;
  device_type?: string;
  browser?: string;
  os?: string;
  screen_resolution?: string;
  referrer?: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  ip_address?: string;
  country?: string;
  city?: string;
}

export interface PageView {
  session?: string;
  page_url: string;
  page_title: string;
  time_spent?: number;
  scroll_depth?: number;
}

export interface AnalyticsEvent {
  session_id?: string;
  event_type: string;
  event_action: string;
  element_text?: string;
  x_position?: number;
  y_position?: number;
}

// ============================================================================
// API RESPONSE TYPES
// ============================================================================

export interface ApiResponse<T> {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results?: T[];
  data?: T;
}

export interface ApiError {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
}

// ============================================================================
// FORM TYPES
// ============================================================================

export interface ContactFormData {
  name: string;
  email: string;
  phone: string;
  company: string;
  need_type: 'optimization' | 'audit' | 'strategy' | 'digital' | 'training' | 'other';
  message: string;
}

// ============================================================================
// COMPONENT PROPS TYPES
// ============================================================================

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}
