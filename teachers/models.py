from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Teacher(models.Model):
    GENDER_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=20, unique=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='teachers/photos/', blank=True, null=True)
    joining_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    subjects = models.ManyToManyField('academics.Subject', blank=True, related_name='teachers')
    classes_assigned = models.ManyToManyField('academics.Class', blank=True, related_name='teachers')

    class Meta:
        ordering = ['teacher_id']
        verbose_name = 'enseignant'
        verbose_name_plural = 'enseignants'

    def __str__(self):
        return f"{self.teacher_id} - {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            last_id = Teacher.objects.all().order_by('-id').first()
            if last_id:
                try:
                    num = int(last_id.teacher_id.split('-')[1]) + 1
                except (ValueError, IndexError):
                    num = 1
            else:
                num = 1
            self.teacher_id = f'TCH-{num:04d}'
        super().save(*args, **kwargs)
