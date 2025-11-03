import { api } from './api';
import type { UserSession, PageView, AnalyticsEvent } from '@/types';

// ============================================================================
// ANALYTICS SDK - Client-side tracking for Pinnacle Advisors
// ============================================================================

class Analytics {
  private sessionId: string | null = null;
  private sessionStartTime: number = 0;
  private pageViewStartTime: number = 0;
  private maxScrollDepth: number = 0;
  private isInitialized: boolean = false;

  /**
   * Initialize analytics tracking
   */
  async init(): Promise<void> {
    if (this.isInitialized || typeof window === 'undefined') return;

    try {
      // Get session data
      const sessionData = this.getSessionData();

      // Track session
      const response = await api.trackSession(sessionData);
      this.sessionId = response.session_id;
      this.sessionStartTime = Date.now();

      // Setup event listeners
      this.setupListeners();

      this.isInitialized = true;
      console.log('✅ Analytics initialized with session:', this.sessionId);
    } catch (error) {
      console.error('❌ Analytics init failed:', error);
    }
  }

  /**
   * Get session data from browser
   */
  private getSessionData(): UserSession {
    if (typeof window === 'undefined') return {};

    const urlParams = new URLSearchParams(window.location.search);

    return {
      device_type: this.getDeviceType(),
      browser: this.getBrowser(),
      os: this.getOS(),
      screen_resolution: `${window.screen.width}x${window.screen.height}`,
      referrer: document.referrer || undefined,
      utm_source: urlParams.get('utm_source') || undefined,
      utm_medium: urlParams.get('utm_medium') || undefined,
      utm_campaign: urlParams.get('utm_campaign') || undefined,
    };
  }

  /**
   * Setup event listeners for tracking
   */
  private setupListeners(): void {
    if (typeof window === 'undefined') return;

    // Track scroll depth
    let scrollTimeout: NodeJS.Timeout;
    window.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        const scrollDepth = this.getScrollDepth();
        if (scrollDepth > this.maxScrollDepth) {
          this.maxScrollDepth = scrollDepth;
        }
      }, 150);
    });

    // Track page unload (send time spent)
    window.addEventListener('beforeunload', () => {
      if (this.pageViewStartTime > 0) {
        const timeSpent = Math.floor((Date.now() - this.pageViewStartTime) / 1000);
        this.trackPageView({
          page_url: window.location.pathname,
          page_title: document.title,
          time_spent: timeSpent,
          scroll_depth: this.maxScrollDepth,
        });
      }
    });
  }

  /**
   * Track page view
   */
  async trackPageView(data: Partial<PageView>): Promise<void> {
    if (!this.isInitialized || typeof window === 'undefined') return;

    this.pageViewStartTime = Date.now();
    this.maxScrollDepth = 0;

    const pageViewData: PageView = {
      session: this.sessionId || undefined,
      page_url: data.page_url || window.location.pathname,
      page_title: data.page_title || document.title,
      time_spent: data.time_spent,
      scroll_depth: data.scroll_depth,
    };

    try {
      await api.trackPageView(pageViewData);
    } catch (error) {
      console.error('❌ Page view tracking failed:', error);
    }
  }

  /**
   * Track custom event
   */
  async trackEvent(
    eventType: string,
    eventData?: Record<string, any>,
    element?: HTMLElement
  ): Promise<void> {
    if (!this.isInitialized || typeof window === 'undefined') return;

    // Formater les données pour l'API backend
    const event = {
      session_id: this.sessionId ?? undefined,
      event_type: eventType,
      event_action: eventType, // Utiliser eventType comme action
      element_text: element?.textContent || JSON.stringify(eventData),
      x_position: element ? this.getClickPosition(element).x : undefined,
      y_position: element ? this.getClickPosition(element).y : undefined,
    };

    try {
      await api.trackEvent(event);
    } catch (error) {
      console.error('❌ Event tracking failed:', error);
    }
  }

  private getClickPosition(element: HTMLElement): { x: number; y: number } {
    const rect = element.getBoundingClientRect();
    return {
      x: Math.round(rect.left + rect.width / 2),
      y: Math.round(rect.top + rect.height / 2),
    };
  }

  /**
   * Track click with coordinates (for heatmap)
   */
  async trackClick(x: number, y: number): Promise<void> {
    if (!this.isInitialized || typeof window === 'undefined') return;

    try {
      await api.trackHeatmap({
        page_url: window.location.pathname,
        x_position: x,
        y_position: y,
        session: this.sessionId || undefined,
      });
    } catch (error) {
      console.error('❌ Heatmap tracking failed:', error);
    }
  }

  /**
   * Track CTA click
   */
  trackCTA(ctaName: string, ctaLocation: string): void {
    this.trackEvent('cta_click', {
      cta_name: ctaName,
      cta_location: ctaLocation,
    });
  }

  /**
   * Track form submission
   */
  trackFormSubmit(formName: string, success: boolean): void {
    this.trackEvent('form_submit', {
      form_name: formName,
      success,
    });
  }

  /**
   * Track scroll to section
   */
  trackSectionView(sectionName: string): void {
    this.trackEvent('scroll', {
      section: sectionName,
    });
  }

  // ============================================================================
  // HELPER METHODS
  // ============================================================================

  private getDeviceType(): string {
    if (typeof window === 'undefined') return 'unknown';

    const width = window.innerWidth;
    if (width < 768) return 'mobile';
    if (width < 1024) return 'tablet';
    return 'desktop';
  }

  private getBrowser(): string {
    if (typeof window === 'undefined') return 'unknown';

    const ua = window.navigator.userAgent;
    if (ua.includes('Chrome')) return 'Chrome';
    if (ua.includes('Firefox')) return 'Firefox';
    if (ua.includes('Safari')) return 'Safari';
    if (ua.includes('Edge')) return 'Edge';
    return 'Other';
  }

  private getOS(): string {
    if (typeof window === 'undefined') return 'unknown';

    const ua = window.navigator.userAgent;
    if (ua.includes('Win')) return 'Windows';
    if (ua.includes('Mac')) return 'macOS';
    if (ua.includes('Linux')) return 'Linux';
    if (ua.includes('Android')) return 'Android';
    if (ua.includes('iOS')) return 'iOS';
    return 'Other';
  }

  private getScrollDepth(): number {
    if (typeof window === 'undefined') return 0;

    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    return scrollHeight > 0 ? Math.round((scrollTop / scrollHeight) * 100) : 0;
  }
}

// ============================================================================
// EXPORT SINGLETON
// ============================================================================

export const analytics = new Analytics();

// ============================================================================
// REACT HOOK
// ============================================================================

export function useAnalytics() {
  return analytics;
}
