from django.db import models
from django.utils.translation import gettext_lazy as _


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'année académique'
        verbose_name_plural = 'années académiques'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)


class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='classes')
    order = models.PositiveIntegerField(default=0, help_text='Ordre de progression (CI=1, CP=2, CE1=3, CE2=4, CM1=5, CM2=6)')

    class Meta:
        ordering = ['order']
        verbose_name = 'classe'
        verbose_name_plural = 'classes'

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        return self.students.count()


class Section(models.Model):
    name = models.CharField(max_length=10)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sections')
    capacity = models.PositiveIntegerField(default=40)

    class Meta:
        unique_together = ('name', 'class_obj')
        ordering = ['class_obj', 'name']
        verbose_name = 'section'
        verbose_name_plural = 'sections'

    def __str__(self):
        return f"{self.class_obj.name} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    classes = models.ManyToManyField(Class, blank=True, related_name='subjects')

    class Meta:
        ordering = ['name']
        verbose_name = 'matière'
        verbose_name_plural = 'matières'

    def __str__(self):
        return f"{self.name} ({self.code})"
