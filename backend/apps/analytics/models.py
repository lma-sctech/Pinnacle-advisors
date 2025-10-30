from django.db import models


class UserSession(models.Model):
    """Sessions utilisateur - God View"""
    session_id = models.CharField('ID Session', max_length=100, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField('IP')
    user_agent = models.TextField('User Agent')
    device_type = models.CharField('Appareil', max_length=50, blank=True)
    browser = models.CharField('Navigateur', max_length=100, blank=True)
    screen_resolution = models.CharField('Résolution', max_length=50, blank=True)
    referrer = models.TextField('Référent', blank=True)
    landing_page = models.CharField('Landing Page', max_length=500)
    utm_source = models.CharField('UTM Source', max_length=200, blank=True)
    utm_campaign = models.CharField('UTM Campaign', max_length=200, blank=True)
    start_time = models.DateTimeField('Début', auto_now_add=True)
    end_time = models.DateTimeField('Fin', blank=True, null=True)
    duration_seconds = models.PositiveIntegerField('Durée (sec)', default=0)
    pages_visited = models.PositiveIntegerField('Pages visitées', default=0)
    converted = models.BooleanField('Converti', default=False)

    class Meta:
        verbose_name = 'Session'
        ordering = ['-start_time']

    def __str__(self):
        return f"Session {self.session_id[:8]} - {self.start_time.strftime('%d/%m/%Y')}"


class PageView(models.Model):
    """Vues de pages"""
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='pageviews')
    page_url = models.CharField('URL', max_length=500)
    page_title = models.CharField('Titre', max_length=500, blank=True)
    viewed_at = models.DateTimeField('Vu à', auto_now_add=True)
    time_on_page = models.PositiveIntegerField('Temps (sec)', default=0)
    scroll_depth = models.PositiveIntegerField('Scroll (%)', default=0)

    class Meta:
        verbose_name = 'Vue de page'
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.page_url} - {self.viewed_at.strftime('%d/%m/%Y')}"


class Event(models.Model):
    """Événements trackés"""
    EVENT_TYPES = (
        ('click', 'Clic'),
        ('scroll', 'Scroll'),
        ('form_submit', 'Formulaire'),
        ('download', 'Téléchargement'),
        ('button', 'Bouton'),
    )
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField('Type', max_length=50, choices=EVENT_TYPES)
    event_action = models.CharField('Action', max_length=200)
    element_text = models.TextField('Texte', blank=True)
    x_position = models.IntegerField('X', blank=True, null=True)
    y_position = models.IntegerField('Y', blank=True, null=True)
    timestamp = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        verbose_name = 'Événement'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.event_action}"


class HeatmapData(models.Model):
    """Données Heatmap"""
    page_url = models.CharField('URL', max_length=500, db_index=True)
    x_position = models.PositiveIntegerField('X')
    y_position = models.PositiveIntegerField('Y')
    click_count = models.PositiveIntegerField('Clics', default=1)
    date = models.DateField('Date', auto_now_add=True)

    class Meta:
        verbose_name = 'Heatmap'
        ordering = ['-date']

    def __str__(self):
        return f"{self.page_url} ({self.x_position}, {self.y_position})"


class DailyAnalytics(models.Model):
    """Statistiques quotidiennes"""
    date = models.DateField('Date', unique=True, db_index=True)
    total_sessions = models.PositiveIntegerField('Sessions', default=0)
    unique_visitors = models.PositiveIntegerField('Visiteurs uniques', default=0)
    total_pageviews = models.PositiveIntegerField('Pages vues', default=0)
    avg_session_duration = models.FloatField('Durée moy (min)', default=0)
    bounce_rate = models.FloatField('Taux rebond (%)', default=0)
    conversion_rate = models.FloatField('Taux conversion (%)', default=0)
    top_pages = models.JSONField('Top pages', blank=True, null=True)

    class Meta:
        verbose_name = 'Analytique quotidienne'
        ordering = ['-date']

    def __str__(self):
        return f"Analytics {self.date.strftime('%d/%m/%Y')}"
