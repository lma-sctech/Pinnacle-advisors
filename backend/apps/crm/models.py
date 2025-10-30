from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone


class Lead(models.Model):
    """Leads/Prospects du CRM"""

    QUALIFICATION_CHOICES = (
        ('hot', 'Hot - Priorité haute'),
        ('warm', 'Warm - Priorité moyenne'),
        ('cold', 'Cold - Priorité basse'),
        ('unqualified', 'Non qualifié'),
    )

    STATUS_CHOICES = (
        ('new', 'Nouveau'),
        ('contacted', 'Contacté'),
        ('qualified', 'Qualifié'),
        ('proposal', 'Proposition envoyée'),
        ('negotiation', 'Négociation'),
        ('won', 'Gagné'),
        ('lost', 'Perdu'),
        ('on_hold', 'En attente'),
    )

    SOURCE_CHOICES = (
        ('website', 'Site web'),
        ('referral', 'Recommandation'),
        ('linkedin', 'LinkedIn'),
        ('email', 'Email'),
        ('phone', 'Téléphone'),
        ('event', 'Événement'),
        ('other', 'Autre'),
    )

    COMPANY_SIZE_CHOICES = (
        ('tpe', 'TPE (< 50 employés)'),
        ('pme', 'PME (50-200 employés)'),
        ('eti', 'ETI (200-5000 employés)'),
        ('ge', 'Grande entreprise (> 5000 employés)'),
        ('unknown', 'Inconnu'),
    )

    # Informations de base
    name = models.CharField('Nom complet', max_length=200)
    email = models.EmailField('Email', validators=[EmailValidator()], unique=True)
    phone = models.CharField('Téléphone', max_length=20, blank=True,
                            validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    company = models.CharField('Entreprise', max_length=200, blank=True)
    company_size = models.CharField('Taille entreprise', max_length=20,
                                   choices=COMPANY_SIZE_CHOICES, default='unknown')
    position = models.CharField('Poste', max_length=200, blank=True)

    # Type de besoin
    need_type = models.CharField('Type de besoin', max_length=100)
    message = models.TextField('Message initial')
    budget_mentioned = models.BooleanField('Budget mentionné', default=False)
    estimated_budget = models.DecimalField('Budget estimé (€)', max_digits=10,
                                          decimal_places=2, blank=True, null=True)

    # Qualification et statut
    qualification = models.CharField('Qualification', max_length=20,
                                    choices=QUALIFICATION_CHOICES, default='unqualified')
    status = models.CharField('Statut', max_length=20, choices=STATUS_CHOICES, default='new')
    pipeline = models.ForeignKey('Pipeline', on_delete=models.SET_NULL, null=True,
                                blank=True, related_name='leads', verbose_name='Pipeline')
    score = models.IntegerField('Score de qualification', default=0,
                               help_text='Score calculé automatiquement (0-100)')

    # Source et tracking
    source = models.CharField('Source', max_length=20, choices=SOURCE_CHOICES, default='website')
    ip_address = models.GenericIPAddressField('Adresse IP', blank=True, null=True)
    user_agent = models.TextField('User Agent', blank=True)

    # Gestion
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name='assigned_leads',
                                   verbose_name='Assigné à')
    converted_to_client = models.BooleanField('Converti en client', default=False)
    conversion_date = models.DateTimeField('Date de conversion', blank=True, null=True)
    expected_revenue = models.DecimalField('Revenu attendu (€)', max_digits=10,
                                          decimal_places=2, blank=True, null=True)

    # Dates et métadonnées
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)
    last_contact_date = models.DateTimeField('Dernier contact', blank=True, null=True)
    next_follow_up_date = models.DateTimeField('Prochain suivi', blank=True, null=True)
    internal_notes = models.TextField('Notes internes', blank=True)

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.company} ({self.get_qualification_display()})"

    def save(self, *args, **kwargs):
        if self.qualification == 'unqualified':
            self.auto_qualify()
        super().save(*args, **kwargs)

    def auto_qualify(self):
        """Qualification automatique du lead basée sur des critères"""
        score = 0

        # Taille entreprise (max 30 points)
        size_scores = {'ge': 30, 'eti': 25, 'pme': 15, 'tpe': 5}
        score += size_scores.get(self.company_size, 0)

        # Budget (max 20 points)
        if self.budget_mentioned:
            score += 20
            if self.estimated_budget and self.estimated_budget >= 100000:
                score += 10
            elif self.estimated_budget and self.estimated_budget >= 50000:
                score += 5

        # Mots-clés urgents (max 15 points)
        urgent_keywords = ['urgent', 'rapidement', 'immédiat']
        if any(kw in self.message.lower() for kw in urgent_keywords):
            score += 15

        # Type de besoin (max 15 points)
        strategic_needs = ['transformation', 'optimisation', 'stratégie']
        if any(need in self.need_type.lower() for need in strategic_needs):
            score += 15

        # Longueur message (max 10 points)
        word_count = len(self.message.split())
        score += 10 if word_count > 50 else (5 if word_count > 20 else 0)

        # Infos complètes (max 10 points)
        if self.phone and self.company and self.position:
            score += 10

        self.score = min(score, 100)
        self.qualification = 'hot' if score >= 70 else ('warm' if score >= 40 else 'cold')


class Pipeline(models.Model):
    """Pipelines de vente"""
    name = models.CharField('Nom du pipeline', max_length=200)
    description = models.TextField('Description', blank=True)
    order = models.PositiveIntegerField('Ordre', default=0)
    color = models.CharField('Couleur', max_length=7, default='#3B82F6')
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)

    class Meta:
        verbose_name = 'Pipeline'
        verbose_name_plural = 'Pipelines'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Interaction(models.Model):
    """Interactions avec les leads"""
    TYPE_CHOICES = (
        ('email', 'Email'),
        ('phone', 'Appel'),
        ('meeting', 'Réunion'),
        ('note', 'Note'),
    )

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE,
                            related_name='interactions', verbose_name='Lead')
    type = models.CharField('Type', max_length=20, choices=TYPE_CHOICES)
    subject = models.CharField('Sujet', max_length=300)
    content = models.TextField('Contenu')
    duration_minutes = models.PositiveIntegerField('Durée (min)', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_type_display()} - {self.lead.name}"


class Note(models.Model):
    """Notes sur les leads"""
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE,
                            related_name='notes', verbose_name='Lead')
    content = models.TextField('Contenu')
    is_private = models.BooleanField('Privé', default=False)
    is_important = models.BooleanField('Important', default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['-created_at']

    def __str__(self):
        preview = self.content[:50]
        return f"Note - {self.lead.name}: {preview}"
