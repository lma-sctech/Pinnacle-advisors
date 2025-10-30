"""
Tests for Analytics app models
"""
from django.test import TestCase
from apps.analytics.models import (
    UserSession, PageView, Event, HeatmapData, DailyAnalytics
)


class UserSessionModelTest(TestCase):
    """Tests for UserSession model"""

    def test_user_session_creation(self):
        """Test user session can be created"""
        session = UserSession.objects.create(
            session_id="test-session-123",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0",
            device_type="desktop",
            browser="Chrome",
            landing_page="/"
        )

        self.assertIsInstance(session, UserSession)
        self.assertEqual(session.session_id, "test-session-123")

    def test_session_duration_calculation(self):
        """Test session duration is calculated correctly"""
        session = UserSession.objects.create(
            session_id="test-123",
            ip_address="192.168.1.100",
            user_agent="Test",
            landing_page="/"
        )

        # Initially 0 (default value)
        self.assertEqual(session.duration_seconds, 0)


class PageViewModelTest(TestCase):
    """Tests for PageView model"""

    def setUp(self):
        """Set up test data"""
        self.session = UserSession.objects.create(
            session_id="test-session",
            ip_address="192.168.1.100",
            user_agent="Test",
            landing_page="/"
        )

    def test_pageview_creation(self):
        """Test pageview can be created"""
        pageview = PageView.objects.create(
            session=self.session,
            page_url="/",
            page_title="Home"
        )

        self.assertIsInstance(pageview, PageView)
        self.assertEqual(pageview.page_url, "/")

    def test_scroll_depth_default(self):
        """Test scroll_depth defaults to 0"""
        pageview = PageView.objects.create(
            session=self.session,
            page_url="/test"
        )

        self.assertEqual(pageview.scroll_depth, 0)


class EventModelTest(TestCase):
    """Tests for Event model"""

    def setUp(self):
        """Set up test data"""
        self.session = UserSession.objects.create(
            session_id="test-session",
            ip_address="192.168.1.100",
            user_agent="Test",
            landing_page="/"
        )

    def test_event_creation(self):
        """Test event can be created"""
        event = Event.objects.create(
            session=self.session,
            event_type="click",
            event_action="button_click",
            element_text="Submit Button"
        )

        self.assertIsInstance(event, Event)
        self.assertEqual(event.event_type, "click")

    def test_event_coordinates(self):
        """Test event can store x/y coordinates"""
        event = Event.objects.create(
            session=self.session,
            event_type="click",
            event_action="click",
            x_position=150,
            y_position=300
        )

        self.assertEqual(event.x_position, 150)
        self.assertEqual(event.y_position, 300)


class HeatmapDataModelTest(TestCase):
    """Tests for HeatmapData model"""

    def test_heatmap_data_creation(self):
        """Test heatmap data can be created"""
        heatmap = HeatmapData.objects.create(
            page_url="/contact",
            x_position=250,
            y_position=400,
            click_count=1
        )

        self.assertIsInstance(heatmap, HeatmapData)
        self.assertEqual(heatmap.click_count, 1)

    def test_heatmap_click_increment(self):
        """Test click_count can be incremented"""
        heatmap = HeatmapData.objects.create(
            page_url="/",
            x_position=100,
            y_position=200,
            click_count=1
        )

        heatmap.click_count += 1
        heatmap.save()

        heatmap.refresh_from_db()
        self.assertEqual(heatmap.click_count, 2)


class DailyAnalyticsModelTest(TestCase):
    """Tests for DailyAnalytics model"""

    def test_daily_analytics_creation(self):
        """Test daily analytics can be created"""
        from datetime import date

        analytics = DailyAnalytics.objects.create(
            date=date.today(),
            total_sessions=100,
            unique_visitors=75,
            total_pageviews=350,
            avg_session_duration=180.5,
            bounce_rate=35.2,
            conversion_rate=2.5
        )

        self.assertIsInstance(analytics, DailyAnalytics)
        self.assertEqual(analytics.total_sessions, 100)

    def test_bounce_rate_percentage(self):
        """Test bounce_rate is stored correctly"""
        from datetime import date

        analytics = DailyAnalytics.objects.create(
            date=date.today(),
            total_sessions=100,
            bounce_rate=42.5
        )

        self.assertEqual(analytics.bounce_rate, 42.5)
