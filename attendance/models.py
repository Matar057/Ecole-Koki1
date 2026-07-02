from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import datetime


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('late', 'En retard'),
        ('excused', 'Excusé'),
    )

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='attendance_recorded')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date', 'student']
        verbose_name = 'enregistrement de présence'
        verbose_name_plural = 'Enregistrements de présence'

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
