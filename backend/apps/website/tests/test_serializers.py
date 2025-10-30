"""
Tests for Website app serializers
"""
from django.test import TestCase
from apps.website.models import (
    HeroSection, Service, AboutSection, TeamMember,
    FAQCategory, FAQ, ContactInfo, ContactSubmission
)
from apps.website.serializers import (
    HeroSectionSerializer, ServiceSerializer, TeamMemberSerializer,
    FAQCategorySerializer, FAQSerializer, FAQCategoryDetailSerializer,
    ContactSubmissionCreateSerializer
)


class HeroSectionSerializerTest(TestCase):
    """Tests for HeroSectionSerializer"""

    def setUp(self):
        """Set up test data"""
        self.hero = HeroSection.objects.create(
            title="Test Hero",
            subtitle="Test subtitle",
            cta_text="Get Started",
            is_active=True
        )

    def test_serializer_fields(self):
        """Test serializer contains expected fields"""
        serializer = HeroSectionSerializer(instance=self.hero)
        data = serializer.data

        expected_fields = [
            'id', 'title', 'subtitle', 'cta_text', 'cta_link',
            'background_image', 'video_url', 'is_active', 'updated_at'
        ]

        for field in expected_fields:
            self.assertIn(field, data)

    def test_read_only_fields(self):
        """Test id and updated_at are read-only"""
        data = {
            'id': 999,  # Should be ignored
            'title': 'New Title',
            'subtitle': 'New subtitle',
            'cta_text': 'Click',
            'updated_at': '2020-01-01T00:00:00Z'  # Should be ignored
        }

        serializer = HeroSectionSerializer(instance=self.hero, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.hero.refresh_from_db()
        self.assertNotEqual(self.hero.id, 999)  # ID not changed
        self.assertEqual(self.hero.title, 'New Title')


class ServiceSerializerTest(TestCase):
    """Tests for ServiceSerializer"""

    def test_service_fields(self):
        """Test ServiceSerializer has correct fields"""
        data = {
            'title': 'Supply Chain Strategy',
            'description': 'Full description of the service',
            'icon': 'truck',
            'order': 1
        }

        serializer = ServiceSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        service = serializer.save()

        # Check correct fields
        self.assertEqual(service.title, 'Supply Chain Strategy')
        self.assertEqual(service.description, 'Full description of the service')

    def test_service_serialization(self):
        """Test service is correctly serialized"""
        service = Service.objects.create(
            title="Test Service",
            description="Full description",
            icon="chart",
            order=1
        )

        serializer = ServiceSerializer(instance=service)
        data = serializer.data

        self.assertEqual(data['title'], 'Test Service')
        self.assertEqual(data['description'], 'Full description')
        self.assertIn('id', data)


class TeamMemberSerializerTest(TestCase):
    """Tests for TeamMemberSerializer"""

    def test_team_member_serialization(self):
        """Test TeamMember is correctly serialized"""
        member = TeamMember.objects.create(
            name="John Doe",
            position="CEO",
            bio="Bio",
            photo="team/photo.jpg",
            order=1
        )

        serializer = TeamMemberSerializer(instance=member)
        data = serializer.data

        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['position'], 'CEO')
        self.assertIn('id', data)

    def test_team_member_fields(self):
        """Test TeamMemberSerializer has correct fields"""
        member = TeamMember.objects.create(
            name='Jane Smith',
            position='CTO',
            bio='Experienced CTO',
            photo='team/jane.jpg',
            order=1
        )

        serializer = TeamMemberSerializer(instance=member)
        data = serializer.data

        # Check all expected fields are present
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('position', data)
        self.assertIn('bio', data)
        self.assertIn('photo', data)
        self.assertEqual(data['name'], 'Jane Smith')
        self.assertEqual(data['position'], 'CTO')


class FAQSerializerTest(TestCase):
    """Tests for FAQSerializer and FAQCategorySerializer"""

    def setUp(self):
        """Set up test data"""
        self.category = FAQCategory.objects.create(
            name="General Questions",
            order=1
        )

    def test_faq_category_serializer_method_field(self):
        """Test questions_count SerializerMethodField"""
        # Create multiple FAQs
        FAQ.objects.create(
            category=self.category,
            question="Q1?",
            answer="A1",
            order=1,
            is_published=True
        )
        FAQ.objects.create(
            category=self.category,
            question="Q2?",
            answer="A2",
            order=2,
            is_published=True
        )
        FAQ.objects.create(
            category=self.category,
            question="Q3?",
            answer="A3",
            order=3,
            is_published=False  # Unpublished
        )

        serializer = FAQCategorySerializer(instance=self.category)
        data = serializer.data

        # Should count only published FAQs
        self.assertIn('questions_count', data)
        self.assertEqual(data['questions_count'], 2)

    def test_faq_category_detail_serializer_nested(self):
        """Test FAQCategoryDetailSerializer includes nested questions"""
        FAQ.objects.create(
            category=self.category,
            question="Test question?",
            answer="Test answer",
            order=1,
            is_published=True
        )

        serializer = FAQCategoryDetailSerializer(instance=self.category)
        data = serializer.data

        self.assertIn('questions', data)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['questions'][0]['question'], 'Test question?')


class ContactSubmissionCreateSerializerTest(TestCase):
    """Tests for ContactSubmissionCreateSerializer"""

    def test_valid_contact_submission(self):
        """Test valid contact submission data"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+33123456789',
            'company': 'Test Corp',
            'need_type': 'strategy',
            'message': 'I need help with supply chain strategy'
        }

        serializer = ContactSubmissionCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        submission = serializer.save()
        self.assertEqual(submission.name, 'John Doe')
        self.assertEqual(submission.email, 'john@example.com')

    def test_invalid_email(self):
        """Test invalid email is rejected"""
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',  # Invalid
            'message': 'Test message'
        }

        serializer = ContactSubmissionCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_invalid_phone(self):
        """Test invalid phone is rejected"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': 'abc',  # Invalid
            'message': 'Test'
        }

        serializer = ContactSubmissionCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone', serializer.errors)

    def test_required_fields(self):
        """Test required fields must be present"""
        data = {
            'name': 'John Doe'
            # Missing email and message
        }

        serializer = ContactSubmissionCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('message', serializer.errors)

    def test_optional_fields(self):
        """Test optional fields can be omitted"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Test message',
            'need_type': 'other'  # need_type is required
            # phone and company are optional
        }

        serializer = ContactSubmissionCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        submission = serializer.save()
        self.assertEqual(submission.phone, '')
        self.assertEqual(submission.company, '')
