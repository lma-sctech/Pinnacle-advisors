from django.db import models
from django.core.validators import URLValidator, EmailValidator, RegexValidator


class HeroSection(models.Model):
    """Section Hero de la page d'accueil"""
    title = models.CharField('Titre principal', max_length=200)
    subtitle = models.TextField('Sous-titre', max_length=500)
    cta_text = models.CharField('Texte du bouton CTA', max_length=100)
    cta_link = models.CharField('Lien du bouton CTA', max_length=200, default='#contact')
    background_image = models.ImageField('Image de fond', upload_to='hero/', blank=True, null=True)
    video_url = models.URLField('URL de la vidéo (optionnel)', blank=True, null=True, validators=[URLValidator()])
    is_active = models.BooleanField('Actif', default=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Section Hero'
        verbose_name_plural = 'Section Hero'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule section hero active
        if self.is_active:
            HeroSection.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class Service(models.Model):
    """Services supply chain proposés"""
    title = models.CharField('Titre du service', max_length=200)
    description = models.TextField('Description')
    icon = models.CharField('Icône (nom ou code)', max_length=100,
                           help_text='Nom de l\'icône (ex: truck, chart, cog)')
    order = models.PositiveIntegerField('Ordre d\'affichage', default=0)
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class AboutSection(models.Model):
    """Section À propos"""
    title = models.CharField('Titre', max_length=200)
    description = models.TextField('Description')
    mission_statement = models.TextField('Notre mission', blank=True)
    vision_statement = models.TextField('Notre vision', blank=True)
    values = models.TextField('Nos valeurs', blank=True,
                              help_text='Séparer les valeurs par des retours à la ligne')
    image = models.ImageField('Image', upload_to='about/', blank=True, null=True)
    show_statistics = models.BooleanField('Afficher les statistiques', default=True,
                                         help_text='Cochez pour afficher les statistiques (années, clients, projets)')
    years_experience = models.PositiveIntegerField('Années d\'expérience', default=0)
    clients_count = models.PositiveIntegerField('Nombre de clients', default=0)
    projects_count = models.PositiveIntegerField('Nombre de projets', default=0)
    is_active = models.BooleanField('Actif', default=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Section À propos'
        verbose_name_plural = 'Section À propos'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule section about active
        if self.is_active:
            AboutSection.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class TeamMember(models.Model):
    """Membres de l'équipe"""
    name = models.CharField('Nom complet', max_length=200)
    position = models.CharField('Poste', max_length=200)
    bio = models.TextField('Biographie')
    photo = models.ImageField('Photo', upload_to='team/')
    linkedin_url = models.URLField('LinkedIn', blank=True, null=True, validators=[URLValidator()])
    email = models.EmailField('Email', blank=True, validators=[EmailValidator()])
    order = models.PositiveIntegerField('Ordre d\'affichage', default=0)
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField('Date d\'ajout', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Membre de l\'équipe'
        verbose_name_plural = 'Équipe'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.position}"


class FAQCategory(models.Model):
    """Catégories de FAQ"""
    name = models.CharField('Nom de la catégorie', max_length=200)
    description = models.TextField('Description', blank=True)
    order = models.PositiveIntegerField('Ordre d\'affichage', default=0)
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Catégorie FAQ'
        verbose_name_plural = 'Catégories FAQ'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class FAQ(models.Model):
    """Questions fréquentes"""
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE,
                                 related_name='questions', verbose_name='Catégorie')
    question = models.CharField('Question', max_length=500)
    answer = models.TextField('Réponse')
    order = models.PositiveIntegerField('Ordre d\'affichage', default=0)
    is_published = models.BooleanField('Publier sur le site', default=True,
                                      help_text='Cochez pour afficher cette question sur le site')
    is_active = models.BooleanField('Actif', default=True)
    views_count = models.PositiveIntegerField('Nombre de vues', default=0, editable=False)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Question FAQ'
        verbose_name_plural = 'Questions FAQ'
        ordering = ['category__order', 'order', 'question']

    def __str__(self):
        return self.question


class ContactInfo(models.Model):
    """Informations de contact"""
    company_name = models.CharField('Nom de l\'entreprise', max_length=200)
    email = models.EmailField('Email', validators=[EmailValidator()])
    phone = models.CharField('Téléphone', max_length=20,
                            validators=[RegexValidator(r'^\+?1?\d{9,15}$',
                                                      'Entrez un numéro de téléphone valide.')])
    address = models.TextField('Adresse')
    city = models.CharField('Ville', max_length=100)
    country = models.CharField('Pays', max_length=100, default='France')
    linkedin_url = models.URLField('LinkedIn', blank=True, null=True, validators=[URLValidator()])
    twitter_url = models.URLField('Twitter/X', blank=True, null=True, validators=[URLValidator()])
    facebook_url = models.URLField('Facebook', blank=True, null=True, validators=[URLValidator()])
    working_hours = models.CharField('Horaires d\'ouverture', max_length=200,
                                     default='Lun-Ven: 9h-18h')
    is_active = models.BooleanField('Actif', default=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Informations de contact'
        verbose_name_plural = 'Informations de contact'

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule info de contact active
        if self.is_active:
            ContactInfo.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class ContactSubmission(models.Model):
    """Soumissions du formulaire de contact"""
    NEED_TYPES = (
        ('optimization', 'Optimisation de la supply chain'),
        ('audit', 'Audit et diagnostic'),
        ('strategy', 'Stratégie logistique'),
        ('digital', 'Transformation digitale'),
        ('training', 'Formation'),
        ('other', 'Autre'),
    )

    name = models.CharField('Nom complet', max_length=200)
    email = models.EmailField('Email', validators=[EmailValidator()])
    phone = models.CharField('Téléphone', max_length=20, blank=True,
                            validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    company = models.CharField('Entreprise', max_length=200, blank=True)
    need_type = models.CharField('Type de besoin', max_length=50, choices=NEED_TYPES)
    message = models.TextField('Message')

    # Méta-données
    ip_address = models.GenericIPAddressField('Adresse IP', blank=True, null=True)
    user_agent = models.TextField('User Agent', blank=True)
    submitted_at = models.DateTimeField('Date de soumission', auto_now_add=True)
    is_processed = models.BooleanField('Traité', default=False)
    processed_at = models.DateTimeField('Date de traitement', blank=True, null=True)
    notes = models.TextField('Notes internes', blank=True)

    class Meta:
        verbose_name = 'Soumission de contact'
        verbose_name_plural = 'Soumissions de contact'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.company} ({self.submitted_at.strftime('%d/%m/%Y')})"


class BusinessCard(models.Model):
    """Carte de visite digitale (accessible via QR code)"""
    # Informations personnelles
    full_name = models.CharField('Nom complet', max_length=200)
    job_title = models.CharField('Titre/Poste', max_length=200)
    tagline = models.CharField('Tagline/Slogan', max_length=300,
                               help_text='Une phrase accrocheuse qui vous décrit')
    bio = models.TextField('Biographie',
                          help_text='Description complète de votre profil et expertise')
    photo = models.ImageField('Photo de profil', upload_to='business_card/',
                              help_text='Photo professionnelle (format carré recommandé)')

    # Informations de contact
    email = models.EmailField('Email professionnel', validators=[EmailValidator()])
    phone = models.CharField('Téléphone', max_length=20,
                            validators=[RegexValidator(r'^\+?1?\d{9,15}$',
                                                      'Entrez un numéro de téléphone valide.')])

    # Entreprise
    company_name = models.CharField('Nom de l\'entreprise', max_length=200)
    company_logo = models.ImageField('Logo entreprise', upload_to='business_card/logos/',
                                     blank=True, null=True,
                                     help_text='Logo de votre entreprise (format PNG transparent recommandé)')
    website_url = models.URLField('Site web', validators=[URLValidator()],
                                  help_text='URL du site principal')

    # Réseaux sociaux
    linkedin_url = models.URLField('LinkedIn', validators=[URLValidator()],
                                   help_text='URL complète de votre profil LinkedIn')
    twitter_url = models.URLField('Twitter/X', blank=True, null=True, validators=[URLValidator()])
    github_url = models.URLField('GitHub', blank=True, null=True, validators=[URLValidator()])

    # Personnalisation design
    accent_color = models.CharField('Couleur d\'accent', max_length=7, default='#3B82F6',
                                   help_text='Couleur hexadécimale (ex: #3B82F6)')
    background_gradient_start = models.CharField('Couleur dégradé début', max_length=7,
                                                 default='#3B82F6',
                                                 help_text='Couleur de début du fond dégradé')
    background_gradient_end = models.CharField('Couleur dégradé fin', max_length=7,
                                               default='#10B981',
                                               help_text='Couleur de fin du fond dégradé')

    # Méta-données
    is_active = models.BooleanField('Actif', default=True,
                                    help_text='Une seule carte peut être active à la fois')
    views_count = models.PositiveIntegerField('Nombre de vues', default=0, editable=False,
                                              help_text='Nombre de fois que la carte a été consultée')
    qr_scans_count = models.PositiveIntegerField('Scans QR code', default=0, editable=False,
                                                 help_text='Tracking approximatif des scans du QR code')
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Carte de Visite Digitale'
        verbose_name_plural = 'Cartes de Visite Digitales'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.job_title}"

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule carte de visite active
        if self.is_active:
            BusinessCard.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def increment_views(self):
        """Incrémente le compteur de vues"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_qr_scans(self):
        """Incrémente le compteur de scans QR code"""
        self.qr_scans_count += 1
        self.save(update_fields=['qr_scans_count'])


class Recruitment(models.Model):
    """Section Recrutement affichée sur la page équipe"""
    title = models.CharField('Titre', max_length=200, default='Rejoignez notre équipe')
    description = models.TextField('Description', max_length=500,
                                   default='Vous êtes un expert supply chain passionné ? Nous recherchons des talents pour renforcer notre équipe.')
    cta_text = models.CharField('Texte du bouton CTA', max_length=100, default='Voir les opportunités')
    email = models.EmailField('Email de recrutement', default='recrutement@pinnacle-advisors.tech',
                             validators=[EmailValidator()],
                             help_text='Email vers lequel le bouton redirigera')
    is_active = models.BooleanField('Actif', default=True,
                                   help_text='Décochez pour masquer la section recrutement sur le site')
    order = models.PositiveIntegerField('Ordre d\'affichage', default=0,
                                       help_text='Position dans la page (0 = en bas)')
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Section Recrutement'
        verbose_name_plural = 'Section Recrutement'
        ordering = ['order']

    def __str__(self):
        status = "✅ Actif" if self.is_active else "❌ Inactif"
        return f"{self.title} - {status}"

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule section recrutement active
        if self.is_active:
            Recruitment.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class TeamHeader(models.Model):
    """En-tête de la section Team (titre et description)"""
    title_part1 = models.CharField('Première partie du titre', max_length=100, default='Notre Équipe',
                                   help_text='Partie affichée avec gradient (ex: "Notre Équipe")')
    title_part2 = models.CharField('Seconde partie du titre', max_length=100, default='d\'Experts',
                                   help_text='Partie affichée en noir (ex: "d\'Experts")')
    description = models.TextField('Description', max_length=300, blank=True, null=True,
                                  help_text='Description affichée sous le titre (optionnel)')
    is_active = models.BooleanField('Actif', default=True,
                                   help_text='Décochez pour masquer l\'en-tête personnalisé (affiche le texte par défaut)')
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'En-tête Section Équipe'
        verbose_name_plural = 'En-tête Section Équipe'

    def __str__(self):
        status = "✅ Actif" if self.is_active else "❌ Inactif"
        return f"{self.title_part1} {self.title_part2} - {status}"

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'un seul en-tête actif
        if self.is_active:
            TeamHeader.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class SEOSettings(models.Model):
    """Configuration SEO du site (métadonnées, OpenGraph)"""
    # Métadonnées SEO standards
    meta_title = models.CharField('Titre SEO', max_length=200,
                                  default='Pinnacle Advisors - Cabinet de Conseil Expert',
                                  help_text='Titre principal affiché dans les résultats de recherche (60 caractères max recommandé)')
    meta_description = models.TextField('Description SEO', max_length=300,
                                       default='Cabinet de conseil spécialisé en optimisation et transformation des chaînes d\'approvisionnement. Expertise 360° pour faire de votre supply chain un avantage compétitif.',
                                       help_text='Description affichée dans les résultats de recherche (155 caractères max recommandé)')
    meta_keywords = models.CharField('Mots-clés SEO', max_length=500,
                                    default='supply chain, logistique, conseil, optimisation, transformation digitale, WMS, TMS, S&OP',
                                    help_text='Mots-clés séparés par des virgules')
    author_name = models.CharField('Nom de l\'auteur', max_length=100,
                                  default='Pinnacle Advisors',
                                  help_text='Nom de l\'auteur du site (métadonnée author)')

    # OpenGraph (réseaux sociaux)
    og_title = models.CharField('Titre OpenGraph', max_length=200,
                               default='Pinnacle Advisors - Cabinet de Conseil Expert',
                               help_text='Titre affiché lors du partage sur les réseaux sociaux')
    og_description = models.TextField('Description OpenGraph', max_length=300,
                                     default='Transformez votre supply chain en avantage compétitif',
                                     help_text='Description affichée lors du partage sur les réseaux sociaux')
    og_locale = models.CharField('Locale OpenGraph', max_length=10,
                                default='fr_FR',
                                help_text='Langue et région (ex: fr_FR, en_US)')
    og_image = models.ImageField('Image OpenGraph', upload_to='seo/',
                                blank=True, null=True,
                                help_text='Image affichée lors du partage (1200x630px recommandé)')

    # Méta-données
    is_active = models.BooleanField('Actif', default=True,
                                   help_text='Une seule configuration SEO peut être active à la fois')
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Configuration SEO'
        verbose_name_plural = 'Configuration SEO'

    def __str__(self):
        status = "✅ Actif" if self.is_active else "❌ Inactif"
        return f"SEO: {self.meta_title[:50]} - {status}"

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule configuration SEO active
        if self.is_active:
            SEOSettings.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class SiteSettings(models.Model):
    """Paramètres globaux du site (branding, navigation, footer)"""
    # Branding
    company_name = models.CharField('Nom de l\'entreprise', max_length=100,
                                   default='Pinnacle Advisors',
                                   help_text='Nom affiché dans la navbar et le footer')
    company_tagline = models.TextField('Slogan entreprise', max_length=500,
                                      default='Cabinet de conseil expert en optimisation et transformation des chaînes d\'approvisionnement.',
                                      help_text='Description courte affichée dans le footer')

    # Navigation
    navbar_cta_text = models.CharField('Texte CTA Navbar', max_length=50,
                                      default='Demander un devis',
                                      help_text='Texte du bouton d\'appel à l\'action dans la barre de navigation')
    mobile_menu_cta_text = models.CharField('Texte CTA Menu Mobile', max_length=50,
                                           default='Demander un devis',
                                           help_text='Texte du bouton CTA dans le menu mobile')

    # Footer - Titres de sections
    footer_nav_title = models.CharField('Titre Navigation Footer', max_length=50,
                                       default='Navigation',
                                       help_text='Titre de la section navigation dans le footer')
    footer_services_title = models.CharField('Titre Services Footer', max_length=50,
                                            default='Nos Services',
                                            help_text='Titre de la section services dans le footer')
    footer_follow_title = models.CharField('Titre Réseaux Sociaux Footer', max_length=50,
                                          default='Suivez-nous',
                                          help_text='Titre de la section réseaux sociaux dans le footer')
    footer_hours_label = models.CharField('Label Horaires Footer', max_length=50,
                                         default='Horaires d\'ouverture',
                                         help_text='Label affiché avant les horaires d\'ouverture')

    # Footer - Copyright et liens légaux
    footer_copyright_text = models.CharField('Texte Copyright', max_length=200,
                                            default='© {year} Pinnacle Advisors. Tous droits réservés.',
                                            help_text='Texte de copyright ({year} sera remplacé automatiquement)')
    footer_legal_text = models.CharField('Texte Lien Mentions Légales', max_length=50,
                                        default='Mentions légales',
                                        help_text='Texte du lien vers les mentions légales')
    footer_privacy_text = models.CharField('Texte Lien Confidentialité', max_length=50,
                                          default='Politique de confidentialité',
                                          help_text='Texte du lien vers la politique de confidentialité')
    footer_terms_text = models.CharField('Texte Lien CGV', max_length=50,
                                        default='CGV',
                                        help_text='Texte du lien vers les conditions générales de vente')

    # Méta-données
    is_active = models.BooleanField('Actif', default=True,
                                   help_text='Une seule configuration peut être active à la fois')
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière modification', auto_now=True)

    class Meta:
        verbose_name = 'Paramètres du Site'
        verbose_name_plural = 'Paramètres du Site'

    def __str__(self):
        status = "✅ Actif" if self.is_active else "❌ Inactif"
        return f"Site: {self.company_name} - {status}"

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule configuration active
        if self.is_active:
            SiteSettings.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
