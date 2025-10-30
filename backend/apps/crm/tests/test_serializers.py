"""
Tests pour les serializers CRM
"""

from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from apps.crm.models import Lead, Pipeline, Interaction, Note
from apps.crm.serializers import (
    LeadSerializer,
    LeadDetailSerializer,
    LeadCreateSerializer,
    LeadUpdateSerializer,
    LeadListSerializer,
    PipelineSerializer,
    PipelineDetailSerializer,
    InteractionSerializer,
    InteractionCreateSerializer,
    NoteSerializer,
    NoteCreateSerializer,
)


class LeadSerializerTestCase(TestCase):
    """Tests pour LeadSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.pipeline = Pipeline.objects.create(
            name='Sales Pipeline',
            description='Main sales pipeline'
        )
        self.lead = Lead.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='+33612345678',
            company='Test Company',
            company_size='pme',
            position='CEO',
            need_type='Optimisation',
            message='Nous cherchons à optimiser notre supply chain',
            source='website',
            pipeline=self.pipeline,
            assigned_to=self.user
        )

    def test_lead_serializer_fields(self):
        """Tester que LeadSerializer contient tous les champs nécessaires"""
        serializer = LeadSerializer(instance=self.lead)
        data = serializer.data

        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('email', data)
        self.assertIn('qualification', data)
        self.assertIn('qualification_display', data)
        self.assertIn('status_display', data)
        self.assertIn('score', data)
        self.assertIn('assigned_to', data)
        self.assertIn('pipeline', data)

    def test_lead_detail_serializer_includes_relations(self):
        """Tester que LeadDetailSerializer inclut interactions et notes"""
        # Créer une interaction et une note
        Interaction.objects.create(
            lead=self.lead,
            type='email',
            subject='Premier contact',
            content='Email initial',
            created_by=self.user
        )
        Note.objects.create(
            lead=self.lead,
            content='Note importante',
            created_by=self.user
        )

        serializer = LeadDetailSerializer(instance=self.lead)
        data = serializer.data

        self.assertIn('interactions', data)
        self.assertIn('notes', data)
        self.assertIn('interactions_count', data)
        self.assertIn('notes_count', data)
        self.assertEqual(data['interactions_count'], 1)
        self.assertEqual(data['notes_count'], 1)

    def test_lead_list_serializer_lightweight(self):
        """Tester que LeadListSerializer est léger (performances)"""
        serializer = LeadListSerializer(instance=self.lead)
        data = serializer.data

        # Ne devrait pas inclure les relations lourdes
        self.assertNotIn('interactions', data)
        self.assertNotIn('notes', data)
        self.assertNotIn('internal_notes', data)

        # Devrait inclure les infos essentielles
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('qualification', data)
        self.assertIn('score', data)


class LeadCreateSerializerTestCase(TestCase):
    """Tests pour LeadCreateSerializer avec validation"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_lead_valid_data(self):
        """Tester la création d'un lead avec données valides"""
        data = {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'phone': '+33612345678',
            'company': 'New Company',
            'company_size': 'eti',
            'position': 'CTO',
            'need_type': 'Transformation',
            'message': 'Besoin urgent de transformer notre supply chain',
            'source': 'linkedin',
        }

        serializer = LeadCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        lead = serializer.save()
        self.assertEqual(lead.name, 'Jane Smith')
        self.assertEqual(lead.email, 'jane@example.com')
        # Vérifier que l'auto-qualification a été déclenchée
        self.assertNotEqual(lead.score, 0)
        self.assertIn(lead.qualification, ['hot', 'warm', 'cold'])

    def test_create_lead_duplicate_email(self):
        """Tester que la validation empêche les emails en double"""
        # Créer un lead existant
        Lead.objects.create(
            name='Existing Lead',
            email='existing@example.com',
            company='Existing Company',
            need_type='Test',
            message='Test message'
        )

        # Tenter de créer un lead avec le même email
        data = {
            'name': 'New Lead',
            'email': 'existing@example.com',
            'company': 'New Company',
            'need_type': 'Test',
            'message': 'Test message'
        }

        serializer = LeadCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_create_lead_negative_budget_rejected(self):
        """Tester que les budgets négatifs sont rejetés"""
        data = {
            'name': 'Test Lead',
            'email': 'test@example.com',
            'company': 'Test Company',
            'need_type': 'Test',
            'message': 'Test message',
            'estimated_budget': -5000,
        }

        serializer = LeadCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('estimated_budget', serializer.errors)

    def test_create_lead_budget_mentioned_without_amount(self):
        """Tester que budget_mentioned=True requiert un montant"""
        data = {
            'name': 'Test Lead',
            'email': 'test@example.com',
            'company': 'Test Company',
            'need_type': 'Test',
            'message': 'Test message',
            'budget_mentioned': True,
            # Pas de estimated_budget
        }

        serializer = LeadCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('estimated_budget', serializer.errors)


class LeadUpdateSerializerTestCase(TestCase):
    """Tests pour LeadUpdateSerializer"""

    def setUp(self):
        self.lead = Lead.objects.create(
            name='Original Name',
            email='original@example.com',
            company='Original Company',
            need_type='Test',
            message='Test message'
        )

    def test_update_lead_valid_data(self):
        """Tester la mise à jour d'un lead"""
        data = {
            'name': 'Updated Name',
            'company': 'Updated Company',
            'status': 'contacted'
        }

        serializer = LeadUpdateSerializer(instance=self.lead, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

        updated_lead = serializer.save()
        self.assertEqual(updated_lead.name, 'Updated Name')
        self.assertEqual(updated_lead.status, 'contacted')

    def test_update_lead_duplicate_email_rejected(self):
        """Tester qu'on ne peut pas changer l'email vers un email existant"""
        # Créer un autre lead
        Lead.objects.create(
            name='Other Lead',
            email='other@example.com',
            company='Other Company',
            need_type='Test',
            message='Test'
        )

        # Tenter de changer l'email du lead actuel
        data = {'email': 'other@example.com'}
        serializer = LeadUpdateSerializer(instance=self.lead, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


class PipelineSerializerTestCase(TestCase):
    """Tests pour PipelineSerializer"""

    def setUp(self):
        self.pipeline = Pipeline.objects.create(
            name='Test Pipeline',
            description='Test description',
            order=1,
            color='#3B82F6',
            is_active=True
        )

    def test_pipeline_serializer_fields(self):
        """Tester que PipelineSerializer contient tous les champs"""
        serializer = PipelineSerializer(instance=self.pipeline)
        data = serializer.data

        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('description', data)
        self.assertIn('order', data)
        self.assertIn('color', data)
        self.assertIn('is_active', data)
        self.assertIn('leads_count', data)

    def test_pipeline_leads_count(self):
        """Tester que leads_count est calculé correctement"""
        # Créer 3 leads associés à ce pipeline
        for i in range(3):
            Lead.objects.create(
                name=f'Lead {i}',
                email=f'lead{i}@example.com',
                company='Test Company',
                need_type='Test',
                message='Test',
                pipeline=self.pipeline
            )

        serializer = PipelineSerializer(instance=self.pipeline)
        data = serializer.data
        self.assertEqual(data['leads_count'], 3)

    def test_pipeline_detail_serializer_stats(self):
        """Tester que PipelineDetailSerializer inclut les stats"""
        # Créer des leads avec différentes qualifications
        Lead.objects.create(
            name='Hot Lead',
            email='hot@example.com',
            company='Test',
            need_type='Test',
            message='Test',
            pipeline=self.pipeline,
            qualification='hot',
            score=75
        )
        Lead.objects.create(
            name='Warm Lead',
            email='warm@example.com',
            company='Test',
            need_type='Test',
            message='Test',
            pipeline=self.pipeline,
            qualification='warm',
            score=50
        )

        serializer = PipelineDetailSerializer(instance=self.pipeline)
        data = serializer.data

        self.assertIn('hot_leads_count', data)
        self.assertIn('warm_leads_count', data)
        self.assertIn('cold_leads_count', data)
        self.assertEqual(data['hot_leads_count'], 1)
        self.assertEqual(data['warm_leads_count'], 1)


class InteractionSerializerTestCase(TestCase):
    """Tests pour InteractionSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.lead = Lead.objects.create(
            name='Test Lead',
            email='lead@example.com',
            company='Test Company',
            need_type='Test',
            message='Test message'
        )

    def test_interaction_serializer_fields(self):
        """Tester que InteractionSerializer contient tous les champs"""
        interaction = Interaction.objects.create(
            lead=self.lead,
            type='email',
            subject='Test Subject',
            content='Test content',
            created_by=self.user
        )

        serializer = InteractionSerializer(instance=interaction)
        data = serializer.data

        self.assertIn('id', data)
        self.assertIn('lead', data)
        self.assertIn('type', data)
        self.assertIn('type_display', data)
        self.assertIn('subject', data)
        self.assertIn('content', data)
        self.assertIn('created_by', data)
        self.assertEqual(data['type_display'], 'Email')

    def test_interaction_create_auto_assigns_created_by(self):
        """Tester que InteractionCreateSerializer assigne created_by automatiquement"""
        data = {
            'lead': self.lead.id,
            'type': 'phone',
            'subject': 'Appel téléphonique',
            'content': 'Discussion initiale',
            'duration_minutes': 30
        }

        # Simuler un contexte de request
        from rest_framework.test import APIRequestFactory
        from django.contrib.auth.models import AnonymousUser

        factory = APIRequestFactory()
        request = factory.post('/api/crm/interactions/')
        request.user = self.user

        serializer = InteractionCreateSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())

        interaction = serializer.save()
        self.assertEqual(interaction.created_by, self.user)


class NoteSerializerTestCase(TestCase):
    """Tests pour NoteSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.lead = Lead.objects.create(
            name='Test Lead',
            email='lead@example.com',
            company='Test Company',
            need_type='Test',
            message='Test message'
        )

    def test_note_serializer_fields(self):
        """Tester que NoteSerializer contient tous les champs"""
        note = Note.objects.create(
            lead=self.lead,
            content='Test note content',
            is_private=True,
            is_important=True,
            created_by=self.user
        )

        serializer = NoteSerializer(instance=note)
        data = serializer.data

        self.assertIn('id', data)
        self.assertIn('lead', data)
        self.assertIn('content', data)
        self.assertIn('is_private', data)
        self.assertIn('is_important', data)
        self.assertIn('created_by', data)
        self.assertTrue(data['is_private'])
        self.assertTrue(data['is_important'])

    def test_note_create_auto_assigns_created_by(self):
        """Tester que NoteCreateSerializer assigne created_by automatiquement"""
        data = {
            'lead': self.lead.id,
            'content': 'Note importante',
            'is_important': True
        }

        # Simuler un contexte de request
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = factory.post('/api/crm/notes/')
        request.user = self.user

        serializer = NoteCreateSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())

        note = serializer.save()
        self.assertEqual(note.created_by, self.user)
        self.assertEqual(note.content, 'Note importante')
