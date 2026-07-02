from django.db import models
from django.utils.translation import gettext_lazy as _

DAYS_CHOICES = (
    ('monday', 'Lundi'),
    ('tuesday', 'Mardi'),
    ('wednesday', 'Mercredi'),
    ('thursday', 'Jeudi'),
    ('friday', 'Vendredi'),
    ('saturday', 'Samedi'),
)


class TimetableSlot(models.Model):
    class_obj = models.ForeignKey('academics.Class', on_delete=models.CASCADE, related_name='timetable_slots')
    section = models.ForeignKey('academics.Section', on_delete=models.CASCADE, related_name='timetable_slots')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='timetable_slots')
    day = models.CharField(max_length=10, choices=DAYS_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['day', 'start_time']
        verbose_name = 'créneau d\'emploi du temps'
        verbose_name_plural = 'créneaux d\'emploi du temps'

    def __str__(self):
        return f"{self.class_obj} - {self.subject} ({self.day} {self.start_time}-{self.end_time})"
