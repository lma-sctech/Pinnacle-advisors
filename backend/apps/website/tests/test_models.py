"""
Tests for Website app models
"""
import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from apps.website.models import (
    HeroSection, Service, AboutSection, TeamMember,
    FAQCategory, FAQ, ContactInfo, ContactSubmission
)


class HeroSectionModelTest(TestCase):
    """Tests for HeroSection model"""

    def setUp(self):
        """Set up test data"""
        self.hero = HeroSection.objects.create(
            title="Test Hero Title",
            subtitle="Test subtitle",
            cta_text="Get Started",
            is_active=True
        )

    def test_hero_creation(self):
        """Test hero section can be created"""
        self.assertIsInstance(self.hero, HeroSection)
        self.assertEqual(self.hero.title, "Test Hero Title")
        self.assertTrue(self.hero.is_active)

    def test_hero_str_method(self):
        """Test string representation"""
        self.assertIn("Test Hero Title", str(self.hero))

    def test_unique_active_hero(self):
        """Test only one hero can be active"""
        # Create second hero
        hero2 = HeroSection.objects.create(
            title="Second Hero",
            subtitle="subtitle",
            cta_text="CTA",
            is_active=True
        )

        # First hero should be deactivated
        self.hero.refresh_from_db()
        self.assertFalse(self.hero.is_active)
        self.assertTrue(hero2.is_active)

    def test_inactive_hero(self):
        """Test inactive hero doesn't affect others"""
        hero2 = HeroSection.objects.create(
            title="Inactive Hero",
            subtitle="subtitle",
            cta_text="CTA",
            is_active=False
        )

        # First hero should still be active
        self.hero.refresh_from_db()
        self.assertTrue(self.hero.is_active)


class ServiceModelTest(TestCase):
    """Tests for Service model"""

    def test_service_creation(self):
        """Test service can be created"""
        service = Service.objects.create(
            title="Test Service",
            description="Test description",
            order=1,
            is_active=True
        )

        self.assertIsInstance(service, Service)
        self.assertEqual(service.title, "Test Service")

    def test_auto_slug_generation(self):
        """Test slug is automatically generated from title"""
        service = Service.objects.create(
            title="Supply Chain Optimization",
            description="Test",
            order=1
        )

        # Slug should be auto-generated
        self.assertIsNotNone(service.slug)
        self.assertEqual(service.slug, "supply-chain-optimization")

    def test_custom_slug(self):
        """Test custom slug is preserved"""
        service = Service.objects.create(
            title="Custom Service",
            slug="my-custom-slug",
            description="Test",
            order=1
        )

        self.assertEqual(service.slug, "my-custom-slug")

    def test_unique_slug(self):
        """Test slugs must be unique"""
        Service.objects.create(
            title="Service 1",
            slug="test-slug",
            description="Test",
            order=1
        )

        with self.assertRaises(IntegrityError):
            Service.objects.create(
                title="Service 2",
                slug="test-slug",  # Duplicate slug
                description="Test",
                order=2
            )

    def test_service_ordering(self):
        """Test services are ordered by 'order' field"""
        s1 = Service.objects.create(title="Service 1", description="Test", order=3)
        s2 = Service.objects.create(title="Service 2", description="Test", order=1)
        s3 = Service.objects.create(title="Service 3", description="Test", order=2)

        services = Service.objects.all()
        self.assertEqual(services[0], s2)  # order=1
        self.assertEqual(services[1], s3)  # order=2
        self.assertEqual(services[2], s1)  # order=3


class AboutSectionModelTest(TestCase):
    """Tests for AboutSection model"""

    def test_about_creation(self):
        """Test about section can be created"""
        about = AboutSection.objects.create(
            title="About Us",
            mission="Our mission",
            vision="Our vision",
            values="Our values",
            experience_years=15,
            clients_count=200,
            projects_count=500
        )

        self.assertIsInstance(about, AboutSection)
        self.assertEqual(about.experience_years, 15)

    def test_unique_active_about(self):
        """Test only one about section can be active"""
        about1 = AboutSection.objects.create(
            title="About 1",
            mission="Mission 1",
            is_active=True
        )

        about2 = AboutSection.objects.create(
            title="About 2",
            mission="Mission 2",
            is_active=True
        )

        # First should be deactivated
        about1.refresh_from_db()
        self.assertFalse(about1.is_active)
        self.assertTrue(about2.is_active)


class TeamMemberModelTest(TestCase):
    """Tests for TeamMember model"""

    def test_team_member_creation(self):
        """Test team member can be created"""
        member = TeamMember.objects.create(
            first_name="John",
            last_name="Doe",
            position="CEO",
            bio="Test bio",
            order=1
        )

        self.assertIsInstance(member, TeamMember)

    def test_full_name_property(self):
        """Test full_name computed property"""
        member = TeamMember.objects.create(
            first_name="Jane",
            last_name="Smith",
            position="CTO",
            bio="Bio",
            order=1
        )

        self.assertEqual(member.full_name, "Jane Smith")

    def test_team_member_ordering(self):
        """Test team members are ordered by 'order'"""
        m1 = TeamMember.objects.create(
            first_name="A", last_name="A", position="P", bio="B", order=3
        )
        m2 = TeamMember.objects.create(
            first_name="B", last_name="B", position="P", bio="B", order=1
        )

        members = TeamMember.objects.all()
        self.assertEqual(members[0], m2)  # order=1


class FAQModelTest(TestCase):
    """Tests for FAQ and FAQCategory models"""

    def setUp(self):
        """Set up test data"""
        self.category = FAQCategory.objects.create(
            name="General",
            order=1
        )

    def test_faq_category_creation(self):
        """Test FAQ category can be created"""
        self.assertIsInstance(self.category, FAQCategory)
        self.assertEqual(self.category.name, "General")

    def test_faq_creation(self):
        """Test FAQ can be created"""
        faq = FAQ.objects.create(
            category=self.category,
            question="Test question?",
            answer="Test answer",
            order=1,
            is_published=True
        )

        self.assertIsInstance(faq, FAQ)
        self.assertEqual(faq.views_count, 0)

    def test_faq_published_filter(self):
        """Test is_published filter works"""
        # Published FAQ
        faq1 = FAQ.objects.create(
            category=self.category,
            question="Published?",
            answer="Yes",
            order=1,
            is_published=True
        )

        # Unpublished FAQ
        FAQ.objects.create(
            category=self.category,
            question="Unpublished?",
            answer="No",
            order=2,
            is_published=False
        )

        published_faqs = FAQ.objects.filter(is_published=True)
        self.assertEqual(published_faqs.count(), 1)
        self.assertEqual(published_faqs[0], faq1)

    def test_faq_views_count_increment(self):
        """Test views_count can be incremented"""
        faq = FAQ.objects.create(
            category=self.category,
            question="Test?",
            answer="Answer",
            order=1
        )

        initial_views = faq.views_count
        faq.views_count += 1
        faq.save()

        self.assertEqual(faq.views_count, initial_views + 1)


class ContactInfoModelTest(TestCase):
    """Tests for ContactInfo model"""

    def test_contact_info_creation(self):
        """Test contact info can be created"""
        contact = ContactInfo.objects.create(
            company_name="Test Company",
            email="test@example.com",
            phone="+33123456789",
            address="123 Test St",
            is_active=True
        )

        self.assertIsInstance(contact, ContactInfo)
        self.assertEqual(contact.email, "test@example.com")

    def test_unique_active_contact(self):
        """Test only one contact info can be active"""
        c1 = ContactInfo.objects.create(
            company_name="Company 1",
            email="c1@example.com",
            is_active=True
        )

        c2 = ContactInfo.objects.create(
            company_name="Company 2",
            email="c2@example.com",
            is_active=True
        )

        c1.refresh_from_db()
        self.assertFalse(c1.is_active)
        self.assertTrue(c2.is_active)


class ContactSubmissionModelTest(TestCase):
    """Tests for ContactSubmission model"""

    def test_contact_submission_creation(self):
        """Test contact submission can be created"""
        submission = ContactSubmission.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="+33123456789",
            company="Test Corp",
            position="CEO",
            need_type="strategy",
            message="I need help with supply chain"
        )

        self.assertIsInstance(submission, ContactSubmission)
        self.assertFalse(submission.is_processed)

    def test_email_validation(self):
        """Test email must be valid"""
        submission = ContactSubmission(
            name="John Doe",
            email="invalid-email",  # Invalid
            message="Test"
        )

        with self.assertRaises(ValidationError):
            submission.full_clean()

    def test_phone_validation(self):
        """Test phone number validation"""
        # Valid phone
        s1 = ContactSubmission.objects.create(
            name="John",
            email="john@example.com",
            phone="+33123456789",  # Valid
            message="Test"
        )
        self.assertIsNotNone(s1)

        # Invalid phone should fail validation
        s2 = ContactSubmission(
            name="Jane",
            email="jane@example.com",
            phone="invalid",  # Invalid
            message="Test"
        )

        with self.assertRaises(ValidationError):
            s2.full_clean()

    def test_submission_timestamps(self):
        """Test created_at is auto-set"""
        submission = ContactSubmission.objects.create(
            name="John Doe",
            email="john@example.com",
            message="Test"
        )

        self.assertIsNotNone(submission.created_at)

    def test_processed_flag(self):
        """Test is_processed flag can be set"""
        submission = ContactSubmission.objects.create(
            name="John Doe",
            email="john@example.com",
            message="Test"
        )

        # Initially not processed
        self.assertFalse(submission.is_processed)

        # Mark as processed
        submission.is_processed = True
        submission.save()

        submission.refresh_from_db()
        self.assertTrue(submission.is_processed)
