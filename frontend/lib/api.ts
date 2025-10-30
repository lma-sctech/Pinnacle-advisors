import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  HeroSection,
  Service,
  AboutSection,
  TeamMember,
  FAQCategory,
  ContactInfo,
  ContactSubmission,
  BusinessCard,
  Recruitment,
  TeamHeader,
  SEOSettings,
  SiteSettings,
  UserSession,
  PageView,
  AnalyticsEvent,
  ApiResponse,
} from '@/types';

// ============================================================================
// API CLIENT CONFIGURATION
// ============================================================================

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000,
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add any auth tokens here if needed
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // ============================================================================
  // WEBSITE ENDPOINTS
  // ============================================================================

  /**
   * Get active hero section
   */
  async getHero(): Promise<HeroSection> {
    const response = await this.client.get<HeroSection>('/api/website/hero/active/');
    return response.data;
  }

  /**
   * Get all active services
   */
  async getServices(): Promise<Service[]> {
    const response = await this.client.get<ApiResponse<Service>>('/api/website/services/');
    return response.data.results || [];
  }

  /**
   * Get active about section
   */
  async getAbout(): Promise<AboutSection> {
    const response = await this.client.get<AboutSection>('/api/website/about/active/');
    return response.data;
  }

  /**
   * Get all active team members
   */
  async getTeam(): Promise<TeamMember[]> {
    const response = await this.client.get<ApiResponse<TeamMember>>('/api/website/team/');
    return response.data.results || [];
  }

  /**
   * Get FAQ categories with questions
   */
  async getFAQCategories(): Promise<FAQCategory[]> {
    const response = await this.client.get<ApiResponse<FAQCategory>>('/api/website/faq-categories/');
    return response.data.results || [];
  }

  /**
   * Get active contact info
   */
  async getContactInfo(): Promise<ContactInfo> {
    const response = await this.client.get<ContactInfo>('/api/website/contact-info/active/');
    return response.data;
  }

  /**
   * Submit contact form
   */
  async submitContact(data: ContactSubmission): Promise<void> {
    await this.client.post('/api/website/contact/', data);
  }

  /**
   * Get active business card
   */
  async getBusinessCard(): Promise<BusinessCard> {
    const response = await this.client.get<BusinessCard>('/api/website/business-card/active/');
    return response.data;
  }

  /**
   * Get active recruitment section
   */
  async getRecruitment(): Promise<Recruitment | null> {
    try {
      const response = await this.client.get<Recruitment>('/api/website/recruitment/active/');
      return response.data;
    } catch (error) {
      // Si aucune section recrutement active, retourner null au lieu d'une erreur
      return null;
    }
  }

  /**
   * Get active team header
   */
  async getTeamHeader(): Promise<TeamHeader | null> {
    try {
      const response = await this.client.get<TeamHeader>('/api/website/team-header/active/');
      return response.data;
    } catch (error) {
      // Si aucun en-tête actif, retourner null au lieu d'une erreur
      return null;
    }
  }

  /**
   * Get active SEO settings
   */
  async getSEOSettings(): Promise<SEOSettings | null> {
    try {
      const response = await this.client.get<SEOSettings>('/api/website/seo-settings/active/');
      return response.data;
    } catch (error) {
      // Si aucune configuration SEO active, retourner null
      return null;
    }
  }

  /**
   * Get active site settings
   */
  async getSiteSettings(): Promise<SiteSettings | null> {
    try {
      const response = await this.client.get<SiteSettings>('/api/website/site-settings/active/');
      return response.data;
    } catch (error) {
      // Si aucun paramètre de site actif, retourner null
      return null;
    }
  }

  /**
   * Increment business card views
   */
  async incrementBusinessCardViews(id: number): Promise<void> {
    await this.client.post(`/api/website/business-card/${id}/increment_views/`);
  }

  /**
   * Increment business card QR scans
   */
  async incrementQRScans(id: number): Promise<void> {
    await this.client.post(`/api/website/business-card/${id}/increment_qr_scans/`);
  }

  /**
   * Download vCard
   */
  getVCardUrl(id: number): string {
    return `${API_BASE_URL}/api/website/business-card/${id}/vcard/`;
  }

  // ============================================================================
  // ANALYTICS ENDPOINTS (Public tracking)
  // ============================================================================

  /**
   * Track user session
   */
  async trackSession(data: UserSession): Promise<{ session_id: string }> {
    const response = await this.client.post<{ session_id: string }>('/api/analytics/track/session/', data);
    return response.data;
  }

  /**
   * Track page view
   */
  async trackPageView(data: PageView): Promise<void> {
    await this.client.post('/api/analytics/track/pageview/', data);
  }

  /**
   * Track event
   */
  async trackEvent(data: AnalyticsEvent): Promise<void> {
    await this.client.post('/api/analytics/track/event/', data);
  }

  /**
   * Track heatmap data
   */
  async trackHeatmap(data: {
    page_url: string;
    x_position: number;
    y_position: number;
    session?: string;
  }): Promise<void> {
    await this.client.post('/api/analytics/track/heatmap/', data);
  }
}

// ============================================================================
// EXPORT SINGLETON INSTANCE
// ============================================================================

export const api = new ApiClient();

// ============================================================================
// REACT QUERY HELPER FUNCTIONS
// ============================================================================

export const queryKeys = {
  hero: ['hero'] as const,
  services: ['services'] as const,
  about: ['about'] as const,
  team: ['team'] as const,
  faq: ['faq'] as const,
  contactInfo: ['contactInfo'] as const,
  businessCard: ['businessCard'] as const,
  recruitment: ['recruitment'] as const,
  teamHeader: ['teamHeader'] as const,
  seoSettings: ['seoSettings'] as const,
  siteSettings: ['siteSettings'] as const,
};

/**
 * React Query fetch functions
 */
export const fetchHero = () => api.getHero();
export const fetchServices = () => api.getServices();
export const fetchAbout = () => api.getAbout();
export const fetchTeam = () => api.getTeam();
export const fetchFAQ = () => api.getFAQCategories();
export const fetchContactInfo = () => api.getContactInfo();
export const fetchBusinessCard = () => api.getBusinessCard();
export const fetchRecruitment = () => api.getRecruitment();
export const fetchTeamHeader = () => api.getTeamHeader();
export const fetchSEOSettings = () => api.getSEOSettings();
export const fetchSiteSettings = () => api.getSiteSettings();
