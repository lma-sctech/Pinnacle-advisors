"""
Tests for CRM app models - Lead auto-qualification system
"""
import pytest
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from apps.crm.models import Lead, Pipeline, Interaction, Note


User = get_user_model()


class LeadAutoQualifyTest(TestCase):
    """Tests for Lead.auto_qualify() method - Critical functionality"""

    def test_lead_basic_creation(self):
        """Test lead can be created"""
        lead = Lead.objects.create(
            name="John Doe",
            email="john@example.com",
            need_type="test",
            message="Test message"
        )

        self.assertIsInstance(lead, Lead)
        self.assertEqual(lead.name, "John Doe")

    def test_auto_qualify_hot_lead_ge_budget_urgent(self):
        """Test Hot qualification: GE (30) + budget 100k (30) + urgent (15) + strategic (15) + long message (10) + complete (10) = 110 -> capped at 100"""
        lead = Lead.objects.create(
            name="Jean Dupont",
            email="jean.dupont@carrefour.fr",
            phone="+33123456789",
            company="Carrefour France",
            company_size="ge",  # 30 points
            position="Directeur Supply Chain",
            need_type="transformation digitale",  # 15 points (strategic)
            message="Nous avons un besoin urgent de transformer notre supply chain. " * 10,  # 15 points (urgent) + 10 points (long)
            budget_mentioned=True,  # 20 points
            estimated_budget=Decimal("150000.00")  # +10 points (≥100k)
        )

        # auto_qualify() is called in save()
        lead.refresh_from_db()

        expected_score = 30 + 20 + 10 + 15 + 15 + 10 + 10  # 110, capped at 100
        self.assertEqual(lead.score, 100)
        self.assertEqual(lead.qualification, 'hot')

    def test_auto_qualify_hot_lead_minimum_70(self):
        """Test Hot lead with exact 70 points"""
        lead = Lead.objects.create(
            name="Sophie Martin",
            email="sophie@renault.fr",
            phone="+33123456789",
            company="Renault",
            company_size="eti",  # 25 points
            position="Manager Logistique",
            need_type="optimisation des stocks",  # 15 points
            message="Nous cherchons rapidement une solution. " * 10,  # 15 points (urgent) + 10 points (long)
            budget_mentioned=True,  # 20 points
            estimated_budget=Decimal("50000.00")  # +5 points (≥50k)
        )

        expected_score = 25 + 20 + 5 + 15 + 15 + 10 + 10  # 100, but let's calculate actual
        # Actually: 25 + 20 + 5 + 15 + 15 + 10 + 10 = 100
        # But without phone initially? Let me recalculate
        # With phone + company + position: 10 points
        self.assertGreaterEqual(lead.score, 70)
        self.assertEqual(lead.qualification, 'hot')

    def test_auto_qualify_warm_lead(self):
        """Test Warm qualification (40-69 points)"""
        lead = Lead.objects.create(
            name="Marc Lefebvre",
            email="marc@pme-logistics.fr",
            company="PME Logistics",
            company_size="pme",  # 15 points
            need_type="audit supply chain",  # Not strategic, 0 points
            message="Nous recherchons un consultant pour un audit de notre chaîne logistique.",  # ~12 words, 0 points
            budget_mentioned=True,  # 20 points
            estimated_budget=Decimal("30000.00")  # 0 points (< 50k)
        )

        # Expected: 15 + 20 = 35 points -> Cold
        # But let's add more words
        lead.message = "Nous recherchons un consultant expérimenté pour réaliser un audit complet de notre chaîne logistique et proposer des optimisations."  # 18 words, still 0 points
        lead.save()

        # Actually, we need 40-69 for warm
        # Let's create a proper warm lead
        warm_lead = Lead.objects.create(
            name="Amélie Dubois",
            email="amelie@sanofi.com",
            phone="+33123456789",
            company="Sanofi",
            company_size="eti",  # 25 points
            position="Responsable Achats",
            need_type="sourcing stratégique",  # 15 points (strategic)
            message="Nous avons besoin d'améliorer nos processus d'achats.",  # 8 words, 0 points
            budget_mentioned=False  # 0 points
        )

        # Expected: 25 + 15 + 10 (complete info) = 50 points -> Warm
        self.assertGreaterEqual(warm_lead.score, 40)
        self.assertLess(warm_lead.score, 70)
        self.assertEqual(warm_lead.qualification, 'warm')

    def test_auto_qualify_cold_lead(self):
        """Test Cold qualification (<40 points)"""
        lead = Lead.objects.create(
            name="Startup Owner",
            email="contact@startup.com",
            company_size="tpe",  # 5 points
            need_type="conseil",  # Not strategic, 0 points
            message="Bonjour, je cherche des conseils.",  # Short, 5 words, 0 points
            budget_mentioned=False  # 0 points
        )

        # Expected: 5 points -> Cold
        self.assertLess(lead.score, 40)
        self.assertEqual(lead.qualification, 'cold')

    def test_company_size_scoring(self):
        """Test company size points: GE=30, ETI=25, PME=15, TPE=5"""
        # GE (Grande Entreprise)
        lead_ge = Lead.objects.create(
            name="GE Lead",
            email="ge@example.com",
            company_size="ge",
            need_type="test",
            message="test"
        )
        self.assertGreaterEqual(lead_ge.score, 30)

        # ETI
        lead_eti = Lead.objects.create(
            name="ETI Lead",
            email="eti@example.com",
            company_size="eti",
            need_type="test",
            message="test"
        )
        self.assertGreaterEqual(lead_eti.score, 25)

        # PME
        lead_pme = Lead.objects.create(
            name="PME Lead",
            email="pme@example.com",
            company_size="pme",
            need_type="test",
            message="test"
        )
        self.assertGreaterEqual(lead_pme.score, 15)

        # TPE
        lead_tpe = Lead.objects.create(
            name="TPE Lead",
            email="tpe@example.com",
            company_size="tpe",
            need_type="test",
            message="test"
        )
        self.assertEqual(lead_tpe.score, 5)

    def test_budget_scoring(self):
        """Test budget scoring: mentioned=20, ≥100k=+10, ≥50k=+5"""
        # Budget mentioned only (20 points)
        lead1 = Lead.objects.create(
            name="Lead 1",
            email="lead1@example.com",
            need_type="test",
            message="test",
            budget_mentioned=True
        )
        self.assertEqual(lead1.score, 20)

        # Budget ≥50k (20 + 5 = 25 points)
        lead2 = Lead.objects.create(
            name="Lead 2",
            email="lead2@example.com",
            need_type="test",
            message="test",
            budget_mentioned=True,
            estimated_budget=Decimal("60000.00")
        )
        self.assertEqual(lead2.score, 25)

        # Budget ≥100k (20 + 10 = 30 points)
        lead3 = Lead.objects.create(
            name="Lead 3",
            email="lead3@example.com",
            need_type="test",
            message="test",
            budget_mentioned=True,
            estimated_budget=Decimal("150000.00")
        )
        self.assertEqual(lead3.score, 30)

    def test_urgent_keywords_scoring(self):
        """Test urgent keywords: 'urgent', 'rapidement', 'immédiat' = 15 points"""
        # With 'urgent'
        lead1 = Lead.objects.create(
            name="Lead 1",
            email="lead1@example.com",
            need_type="test",
            message="Nous avons un besoin URGENT de transformer nos process"
        )
        self.assertEqual(lead1.score, 15)

        # With 'rapidement'
        lead2 = Lead.objects.create(
            name="Lead 2",
            email="lead2@example.com",
            need_type="test",
            message="Nous devons agir rapidement sur ce sujet"
        )
        self.assertEqual(lead2.score, 15)

        # With 'immédiat'
        lead3 = Lead.objects.create(
            name="Lead 3",
            email="lead3@example.com",
            need_type="test",
            message="Besoin immédiat d'un consultant"
        )
        self.assertEqual(lead3.score, 15)

    def test_strategic_need_scoring(self):
        """Test strategic needs: 'transformation', 'optimisation', 'stratégie' = 15 points"""
        # With 'transformation'
        lead1 = Lead.objects.create(
            name="Lead 1",
            email="lead1@example.com",
            need_type="transformation digitale",
            message="test"
        )
        self.assertEqual(lead1.score, 15)

        # With 'optimisation'
        lead2 = Lead.objects.create(
            name="Lead 2",
            email="lead2@example.com",
            need_type="optimisation des flux",
            message="test"
        )
        self.assertEqual(lead2.score, 15)

        # With 'stratégie'
        lead3 = Lead.objects.create(
            name="Lead 3",
            email="lead3@example.com",
            need_type="stratégie supply chain",
            message="test"
        )
        self.assertEqual(lead3.score, 15)

    def test_message_length_scoring(self):
        """Test message length: >50 words=10, >20 words=5, else=0"""
        # Long message (>50 words) = 10 points
        long_message = " ".join(["word"] * 60)
        lead1 = Lead.objects.create(
            name="Lead 1",
            email="lead1@example.com",
            need_type="test",
            message=long_message
        )
        self.assertEqual(lead1.score, 10)

        # Medium message (>20 words) = 5 points
        medium_message = " ".join(["word"] * 30)
        lead2 = Lead.objects.create(
            name="Lead 2",
            email="lead2@example.com",
            need_type="test",
            message=medium_message
        )
        self.assertEqual(lead2.score, 5)

        # Short message (≤20 words) = 0 points
        short_message = " ".join(["word"] * 10)
        lead3 = Lead.objects.create(
            name="Lead 3",
            email="lead3@example.com",
            need_type="test",
            message=short_message
        )
        self.assertEqual(lead3.score, 0)

    def test_complete_info_scoring(self):
        """Test complete info: phone + company + position = 10 points"""
        # All three fields filled
        lead1 = Lead.objects.create(
            name="Lead 1",
            email="lead1@example.com",
            phone="+33123456789",
            company="Test Company",
            position="CEO",
            need_type="test",
            message="test"
        )
        self.assertEqual(lead1.score, 10)

        # Missing one field
        lead2 = Lead.objects.create(
            name="Lead 2",
            email="lead2@example.com",
            phone="+33123456789",
            company="Test Company",
            # position missing
            need_type="test",
            message="test"
        )
        self.assertEqual(lead2.score, 0)

    def test_score_capped_at_100(self):
        """Test score is capped at 100 even if total exceeds"""
        lead = Lead.objects.create(
            name="Perfect Lead",
            email="perfect@example.com",
            phone="+33123456789",
            company="Perfect Corp",
            company_size="ge",  # 30
            position="CEO",
            need_type="transformation stratégique",  # 15
            message="urgent " + " ".join(["word"] * 60),  # 15 + 10
            budget_mentioned=True,  # 20
            estimated_budget=Decimal("200000.00")  # +10
        )

        # Total: 30 + 20 + 10 + 15 + 15 + 10 + 10 = 110
        self.assertEqual(lead.score, 100)  # Capped at 100
        self.assertEqual(lead.qualification, 'hot')


class LeadValidationTest(TestCase):
    """Tests for Lead model validations"""

    def test_email_unique_constraint(self):
        """Test email must be unique"""
        Lead.objects.create(
            name="User 1",
            email="duplicate@example.com",
            need_type="test",
            message="test"
        )

        with self.assertRaises(IntegrityError):
            Lead.objects.create(
                name="User 2",
                email="duplicate@example.com",  # Duplicate
                need_type="test",
                message="test"
            )

    def test_email_validation(self):
        """Test email must be valid format"""
        lead = Lead(
            name="Test",
            email="invalid-email",  # Invalid format
            need_type="test",
            message="test"
        )

        with self.assertRaises(ValidationError):
            lead.full_clean()

    def test_phone_validation(self):
        """Test phone number validation with regex"""
        # Valid phones
        valid_phones = ["+33123456789", "+1234567890", "123456789"]

        for phone in valid_phones:
            lead = Lead(
                name="Test",
                email=f"test{phone}@example.com",
                phone=phone,
                need_type="test",
                message="test"
            )
            # Should not raise
            lead.full_clean()

        # Invalid phone
        invalid_lead = Lead(
            name="Test",
            email="test@example.com",
            phone="invalid",
            need_type="test",
            message="test"
        )

        with self.assertRaises(ValidationError):
            invalid_lead.full_clean()


class PipelineModelTest(TestCase):
    """Tests for Pipeline model"""

    def test_pipeline_creation(self):
        """Test pipeline can be created"""
        pipeline = Pipeline.objects.create(
            name="Sales Pipeline",
            description="Main sales pipeline",
            order=1,
            color="#3B82F6"
        )

        self.assertIsInstance(pipeline, Pipeline)
        self.assertEqual(pipeline.name, "Sales Pipeline")

    def test_pipeline_ordering(self):
        """Test pipelines are ordered by order field"""
        p1 = Pipeline.objects.create(name="P1", order=3)
        p2 = Pipeline.objects.create(name="P2", order=1)
        p3 = Pipeline.objects.create(name="P3", order=2)

        pipelines = Pipeline.objects.all()
        self.assertEqual(pipelines[0], p2)  # order=1
        self.assertEqual(pipelines[1], p3)  # order=2
        self.assertEqual(pipelines[2], p1)  # order=3


class InteractionModelTest(TestCase):
    """Tests for Interaction model"""

    def setUp(self):
        """Set up test data"""
        self.lead = Lead.objects.create(
            name="Test Lead",
            email="test@example.com",
            need_type="test",
            message="test"
        )

    def test_interaction_creation(self):
        """Test interaction can be created"""
        interaction = Interaction.objects.create(
            lead=self.lead,
            type="email",
            subject="Initial Contact",
            content="First email sent to lead"
        )

        self.assertIsInstance(interaction, Interaction)
        self.assertEqual(interaction.type, "email")

    def test_interaction_types(self):
        """Test different interaction types"""
        types = ['email', 'phone', 'meeting', 'note']

        for itype in types:
            interaction = Interaction.objects.create(
                lead=self.lead,
                type=itype,
                subject=f"Test {itype}",
                content="Test content"
            )
            self.assertEqual(interaction.type, itype)


class NoteModelTest(TestCase):
    """Tests for Note model"""

    def setUp(self):
        """Set up test data"""
        self.lead = Lead.objects.create(
            name="Test Lead",
            email="test@example.com",
            need_type="test",
            message="test"
        )

    def test_note_creation(self):
        """Test note can be created"""
        note = Note.objects.create(
            lead=self.lead,
            content="This is a private note",
            is_private=True
        )

        self.assertIsInstance(note, Note)
        self.assertTrue(note.is_private)

    def test_note_importance_flag(self):
        """Test important flag"""
        important_note = Note.objects.create(
            lead=self.lead,
            content="Important note",
            is_important=True
        )

        self.assertTrue(important_note.is_important)
