"""
Tests pour les views/API CRM
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.crm.models import Lead, Pipeline, Interaction, Note


class LeadViewSetTestCase(TestCase):
    """Tests pour LeadViewSet et endpoints API"""

    def setUp(self):
        # Créer utilisateurs (admin et non-admin)
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )

        # Créer un pipeline
        self.pipeline = Pipeline.objects.create(
            name='Test Pipeline',
            description='Test'
        )

        # Créer des leads
        self.lead1 = Lead.objects.create(
            name='Hot Lead',
            email='hot@example.com',
            company='Hot Company',
            company_size='ge',
            need_type='Transformation',
            message='Besoin urgent de transformer notre supply chain',
            qualification='hot',
            score=75,
            source='website'
        )
        self.lead2 = Lead.objects.create(
            name='Cold Lead',
            email='cold@example.com',
            company='Cold Company',
            company_size='tpe',
            need_type='Autre',
            message='Simple question',
            qualification='cold',
            score=20,
            source='email'
        )

        self.client = APIClient()

    def test_list_leads_requires_auth(self):
        """Tester que /api/crm/leads/ requiert authentification admin"""
        # Sans authentification
        response = self.client.get('/api/crm/leads/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Avec user non-admin
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/crm/leads/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Avec admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/crm/leads/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_leads_returns_all_leads(self):
        """Tester que GET /api/crm/leads/ retourne tous les leads"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/crm/leads/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_retrieve_lead(self):
        """Tester GET /api/crm/leads/{id}/"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/crm/leads/{self.lead1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Hot Lead')
        self.assertIn('interactions', response.data)
        self.assertIn('notes', response.data)

    def test_create_lead(self):
        """Tester POST /api/crm/leads/"""
        self.client.force_authenticate(user=self.admin_user)

        data = {
            'name': 'New Lead',
            'email': 'new@example.com',
            'phone': '+33612345678',
            'company': 'New Company',
            'company_size': 'pme',
            'need_type': 'Optimisation',
            'message': 'Message de test',
            'source': 'linkedin'
        }

        response = self.client.post('/api/crm/leads/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 3)

        new_lead = Lead.objects.get(email='new@example.com')
        self.assertEqual(new_lead.name, 'New Lead')
        # Vérifier que l'auto-qualification a été déclenchée
        self.assertIn(new_lead.qualification, ['hot', 'warm', 'cold'])

    def test_update_lead(self):
        """Tester PUT /api/crm/leads/{id}/"""
        self.client.force_authenticate(user=self.admin_user)

        data = {
            'name': 'Updated Name',
            'email': self.lead1.email,
            'company': 'Updated Company',
            'company_size': self.lead1.company_size,
            'need_type': self.lead1.need_type,
            'message': self.lead1.message,
            'status': 'contacted'
        }

        response = self.client.put(
            f'/api/crm/leads/{self.lead1.id}/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lead1.refresh_from_db()
        self.assertEqual(self.lead1.name, 'Updated Name')
        self.assertEqual(self.lead1.status, 'contacted')

    def test_partial_update_lead(self):
        """Tester PATCH /api/crm/leads/{id}/"""
        self.client.force_authenticate(user=self.admin_user)

        data = {'status': 'qualified'}

        response = self.client.patch(
            f'/api/crm/leads/{self.lead1.id}/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lead1.refresh_from_db()
        self.assertEqual(self.lead1.status, 'qualified')

    def test_delete_lead(self):
        """Tester DELETE /api/crm/leads/{id}/"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(f'/api/crm/leads/{self.lead2.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lead.objects.count(), 1)

    def test_requalify_lead_action(self):
        """Tester POST /api/crm/leads/{id}/requalify/"""
        self.client.force_authenticate(user=self.admin_user)

        # Modifier le message pour changer le score
        self.lead1.message = 'Simple question, pas urgent'
        self.lead1.save()

        response = self.client.post(f'/api/crm/leads/{self.lead1.id}/requalify/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('new_score', response.data)
        self.assertIn('new_qualification', response.data)

    def test_assign_lead_action(self):
        """Tester POST /api/crm/leads/{id}/assign/"""
        self.client.force_authenticate(user=self.admin_user)

        data = {'user_id': self.admin_user.id}

        response = self.client.post(
            f'/api/crm/leads/{self.lead1.id}/assign/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lead1.refresh_from_db()
        self.assertEqual(self.lead1.assigned_to, self.admin_user)

    def test_convert_lead_action(self):
        """Tester POST /api/crm/leads/{id}/convert/"""
        self.client.force_authenticate(user=self.admin_user)

        data = {'expected_revenue': 50000}

        response = self.client.post(
            f'/api/crm/leads/{self.lead1.id}/convert/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lead1.refresh_from_db()
        self.assertTrue(self.lead1.converted_to_client)
        self.assertEqual(self.lead1.status, 'won')
        self.assertIsNotNone(self.lead1.conversion_date)

    def test_hot_leads_action(self):
        """Tester GET /api/crm/leads/hot_leads/"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/api/crm/leads/hot_leads/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['qualification'], 'hot')

    def test_stats_action(self):
        """Tester GET /api/crm/leads/stats/"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/api/crm/leads/stats/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_leads', response.data)
        self.assertIn('hot_leads', response.data)
        self.assertIn('warm_leads', response.data)
        self.assertIn('by_status', response.data)
        self.assertIn('by_source', response.data)
        self.assertEqual(response.data['total_leads'], 2)

    def test_filter_leads_by_qualification(self):
        """Tester le filtrage des leads par qualification"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/api/crm/leads/?qualification=hot')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['qualification'], 'hot')

    def test_search_leads(self):
        """Tester la recherche dans les leads"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/api/crm/leads/?search=Hot')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['company'], 'Hot Company')

    def test_ordering_leads(self):
        """Tester le tri des leads"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/api/crm/leads/?ordering=-score')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Le premier devrait être celui avec le score le plus élevé
        self.assertEqual(response.data['results'][0]['score'], 75)


class PipelineViewSetTestCase(TestCase):
    """Tests pour PipelineViewSet"""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        self.pipeline = Pipeline.objects.create(
            name='Sales Pipeline',
            description='Main pipeline',
            order=1,
            is_active=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

    def test_list_pipelines(self):
        """Tester GET /api/crm/pipelines/"""
        response = self.client.get('/api/crm/pipelines/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_pipeline(self):
        """Tester POST /api/crm/pipelines/"""
        data = {
            'name': 'New Pipeline',
            'description': 'New description',
            'order': 2,
            'color': '#10B981',
            'is_active': True
        }

        response = self.client.post('/api/crm/pipelines/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pipeline.objects.count(), 2)

    def test_active_pipelines_action(self):
        """Tester GET /api/crm/pipelines/active/"""
        # Créer un pipeline inactif
        Pipeline.objects.create(
            name='Inactive Pipeline',
            is_active=False
        )

        response = self.client.get('/api/crm/pipelines/active/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]['is_active'])


class InteractionViewSetTestCase(TestCase):
    """Tests pour InteractionViewSet"""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        self.lead = Lead.objects.create(
            name='Test Lead',
            email='lead@example.com',
            company='Test Company',
            need_type='Test',
            message='Test message'
        )
        self.interaction = Interaction.objects.create(
            lead=self.lead,
            type='email',
            subject='Test Subject',
            content='Test content',
            created_by=self.admin_user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

    def test_list_interactions(self):
        """Tester GET /api/crm/interactions/"""
        response = self.client.get('/api/crm/interactions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_interaction(self):
        """Tester POST /api/crm/interactions/"""
        data = {
            'lead': self.lead.id,
            'type': 'phone',
            'subject': 'Phone Call',
            'content': 'Discussed requirements',
            'duration_minutes': 30
        }

        response = self.client.post('/api/crm/interactions/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Interaction.objects.count(), 2)

        # Vérifier que created_by est assigné automatiquement
        new_interaction = Interaction.objects.get(subject='Phone Call')
        self.assertEqual(new_interaction.created_by, self.admin_user)

    def test_filter_interactions_by_lead(self):
        """Tester le filtrage par lead"""
        response = self.client.get(f'/api/crm/interactions/?lead={self.lead.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_by_lead_action(self):
        """Tester GET /api/crm/interactions/by_lead/?lead_id=1"""
        response = self.client.get(f'/api/crm/interactions/by_lead/?lead_id={self.lead.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class NoteViewSetTestCase(TestCase):
    """Tests pour NoteViewSet"""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        self.lead = Lead.objects.create(
            name='Test Lead',
            email='lead@example.com',
            company='Test Company',
            need_type='Test',
            message='Test message'
        )
        self.note = Note.objects.create(
            lead=self.lead,
            content='Test note',
            is_important=True,
            created_by=self.admin_user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

    def test_list_notes(self):
        """Tester GET /api/crm/notes/"""
        response = self.client.get('/api/crm/notes/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_note(self):
        """Tester POST /api/crm/notes/"""
        data = {
            'lead': self.lead.id,
            'content': 'New important note',
            'is_important': True,
            'is_private': False
        }

        response = self.client.post('/api/crm/notes/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)

        # Vérifier que created_by est assigné automatiquement
        new_note = Note.objects.get(content='New important note')
        self.assertEqual(new_note.created_by, self.admin_user)

    def test_important_notes_action(self):
        """Tester GET /api/crm/notes/important/"""
        # Créer une note non importante
        Note.objects.create(
            lead=self.lead,
            content='Regular note',
            is_important=False,
            created_by=self.admin_user
        )

        response = self.client.get('/api/crm/notes/important/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]['is_important'])

    def test_by_lead_action(self):
        """Tester GET /api/crm/notes/by_lead/?lead_id=1"""
        response = self.client.get(f'/api/crm/notes/by_lead/?lead_id={self.lead.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_notes_by_privacy(self):
        """Tester le filtrage des notes par is_private"""
        Note.objects.create(
            lead=self.lead,
            content='Private note',
            is_private=True,
            created_by=self.admin_user
        )

        response = self.client.get('/api/crm/notes/?is_private=true')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(response.data['results'][0]['is_private'])
