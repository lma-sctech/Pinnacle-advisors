"""
Tests for Website app API ViewSets
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.website.models import (
    HeroSection, Service, AboutSection, TeamMember,
    FAQCategory, FAQ, ContactInfo, ContactSubmission
)


User = get_user_model()


class HeroSectionViewSetTest(TestCase):
    """Tests for HeroSectionViewSet"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.hero = HeroSection.objects.create(
            title="Test Hero",
            subtitle="Subtitle",
            cta_text="CTA",
            is_active=True
        )

    def test_list_hero_sections(self):
        """Test GET /api/website/hero/"""
        url = reverse('website:herosection-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_active_hero_custom_action(self):
        """Test GET /api/website/hero/active/ custom action"""
        url = reverse('website:herosection-active')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Hero')

    def test_permission_allow_any_for_read(self):
        """Test endpoint is accessible without authentication"""
        url = reverse('website:herosection-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ServiceViewSetTest(TestCase):
    """Tests for ServiceViewSet"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.service1 = Service.objects.create(
            name="Service 1",
            short_description="Short",
            full_description="Full",
            order=1,
            is_active=True
        )
        self.service2 = Service.objects.create(
            name="Service 2",
            short_description="Short 2",
            full_description="Full 2",
            order=2,
            is_active=False  # Inactive
        )

    def test_list_services(self):
        """Test GET /api/website/services/"""
        url = reverse('website:service-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should include both active and inactive by default
        self.assertGreaterEqual(len(response.data['results']), 2)

    def test_filter_active_services(self):
        """Test filtering by is_active"""
        url = reverse('website:service-list') + '?is_active=true'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return active services
        for service in response.data['results']:
            self.assertTrue(service['is_active'])

    def test_retrieve_service(self):
        """Test GET /api/website/services/{id}/"""
        url = reverse('website:service-detail', args=[self.service1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Service 1')

    def test_service_ordering(self):
        """Test services are ordered by 'order' field"""
        url = reverse('website:service-list')
        response = self.client.get(url)

        results = response.data['results']
        # First service should have order=1
        self.assertEqual(results[0]['order'], 1)


class TeamMemberViewSetTest(TestCase):
    """Tests for TeamMemberViewSet"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.member = TeamMember.objects.create(
            first_name="John",
            last_name="Doe",
            position="CEO",
            bio="Bio",
            order=1,
            is_active=True
        )

    def test_list_team_members(self):
        """Test GET /api/website/team/"""
        url = reverse('website:teammember-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_full_name_in_response(self):
        """Test full_name computed field is included"""
        url = reverse('website:teammember-list')
        response = self.client.get(url)

        member = response.data['results'][0]
        self.assertEqual(member['full_name'], 'John Doe')


class FAQViewSetTest(TestCase):
    """Tests for FAQViewSet and FAQCategoryViewSet"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.category = FAQCategory.objects.create(
            name="General",
            order=1
        )
        self.faq1 = FAQ.objects.create(
            category=self.category,
            question="Question 1?",
            answer="Answer 1",
            order=1,
            is_published=True
        )
        self.faq2 = FAQ.objects.create(
            category=self.category,
            question="Question 2?",
            answer="Answer 2",
            order=2,
            is_published=False  # Unpublished
        )

    def test_list_faq_categories(self):
        """Test GET /api/website/faq-categories/"""
        url = reverse('website:faqcategory-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_faq_category_includes_questions_count(self):
        """Test category includes questions_count field"""
        url = reverse('website:faqcategory-list')
        response = self.client.get(url)

        category = response.data['results'][0]
        self.assertIn('questions_count', category)
        # Should count only published FAQs
        self.assertEqual(category['questions_count'], 1)

    def test_list_faqs(self):
        """Test GET /api/website/faq/"""
        url = reverse('website:faq-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_published_faqs(self):
        """Test filtering by is_published"""
        url = reverse('website:faq-list') + '?is_published=true'
        response = self.client.get(url)

        # Should only return published FAQs
        for faq in response.data['results']:
            self.assertTrue(faq['is_published'])

    def test_filter_faqs_by_category(self):
        """Test filtering by category"""
        url = reverse('website:faq-list') + f'?category={self.category.id}'
        response = self.client.get(url)

        # All FAQs should be from this category
        for faq in response.data['results']:
            self.assertEqual(faq['category'], self.category.id)

    def test_increment_views_action(self):
        """Test POST /api/website/faq/{id}/increment_views/"""
        initial_views = self.faq1.views_count

        url = reverse('website:faq-increment-views', args=[self.faq1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.faq1.refresh_from_db()
        self.assertEqual(self.faq1.views_count, initial_views + 1)


class ContactInfoViewSetTest(TestCase):
    """Tests for ContactInfoViewSet"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.contact = ContactInfo.objects.create(
            company_name="Pinnacle SC",
            email="contact@pinnacle.com",
            phone="+33123456789",
            address="Paris",
            is_active=True
        )

    def test_active_contact_info(self):
        """Test GET /api/website/contact-info/active/"""
        url = reverse('website:contactinfo-active')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company_name'], 'Pinnacle SC')


class ContactSubmissionViewSetTest(TestCase):
    """Tests for ContactSubmissionViewSet (POST only)"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

    def test_create_contact_submission(self):
        """Test POST /api/website/contact/"""
        url = reverse('website:contactsubmission-list')

        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+33123456789',
            'company': 'Test Corp',
            'position': 'CEO',
            'need_type': 'strategy',
            'message': 'I need help with supply chain strategy'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'John Doe')

        # Check submission was created in database
        submission = ContactSubmission.objects.get(email='john@example.com')
        self.assertEqual(submission.name, 'John Doe')

    def test_create_submission_invalid_email(self):
        """Test POST with invalid email is rejected"""
        url = reverse('website:contactsubmission-list')

        data = {
            'name': 'John Doe',
            'email': 'invalid-email',  # Invalid
            'message': 'Test'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_submission_missing_required_fields(self):
        """Test POST with missing required fields"""
        url = reverse('website:contactsubmission-list')

        data = {
            'name': 'John Doe'
            # Missing email and message
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_submissions_not_allowed(self):
        """Test GET /api/website/contact/ is not allowed"""
        url = reverse('website:contactsubmission-list')
        response = self.client.get(url)

        # Should return 405 Method Not Allowed or similar
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_allow_any_for_submission(self):
        """Test submission endpoint is accessible without authentication"""
        url = reverse('website:contactsubmission-list')

        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test message'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PaginationTest(TestCase):
    """Tests for API pagination"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create multiple services for pagination
        for i in range(15):
            Service.objects.create(
                name=f"Service {i}",
                short_description="Short",
                full_description="Full",
                order=i
            )

    def test_default_pagination(self):
        """Test default pagination is applied"""
        url = reverse('website:service-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 15)

    def test_pagination_page_size(self):
        """Test page size parameter"""
        url = reverse('website:service-list') + '?page_size=5'
        response = self.client.get(url)

        self.assertEqual(len(response.data['results']), 5)
