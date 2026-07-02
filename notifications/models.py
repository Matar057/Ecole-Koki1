from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Announcement(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    )

    TARGET_CHOICES = (
        ('all', 'Tous les utilisateurs'),
        ('students', 'Étudiants seulement'),
        ('teachers', 'Enseignants seulement'),
        ('parents', 'Parents seulement'),
        ('admins', 'Administrateurs seulement'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    target_audience = models.CharField(max_length=10, choices=TARGET_CHOICES, default='all')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    publish_from = models.DateTimeField(null=True, blank=True)
    publish_to = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'annonce'
        verbose_name_plural = 'annonces'

    def __str__(self):
        return self.title


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('fee_alert', 'Alerte frais'),
        ('exam_alert', 'Alerte examen'),
        ('attendance_alert', 'Alerte présence'),
        ('announcement', 'Annonce'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'

    def __str__(self):
        return f"{self.user} - {self.title}"
