from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Exam(models.Model):
    EXAM_TYPE_CHOICES = (
        ('compo_1', 'Composition 1er trimestre'),
        ('compo_2', 'Composition 2e trimestre'),
        ('compo_3', 'Composition 3e trimestre'),
        ('exam_final', 'Examen final'),
        ('other', 'Autre'),
    )

    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE, related_name='exams')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'examen'
        verbose_name_plural = 'examens'

    def __str__(self):
        return self.name


class ExamSubject(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    class_obj = models.ForeignKey('academics.Class', on_delete=models.CASCADE)
    max_marks = models.PositiveIntegerField(default=10, help_text='Note sur 10')
    passing_marks = models.PositiveIntegerField(default=5, help_text='Note de passage sur 10')

    class Meta:
        unique_together = ('exam', 'subject', 'class_obj')
        ordering = ['subject']
        verbose_name = 'matière d\'examen'
        verbose_name_plural = 'matières d\'examen'

    def __str__(self):
        return f"{self.exam} - {self.subject} ({self.class_obj})"


class Mark(models.Model):
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='marks')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, blank=True)
    remarks = models.TextField(blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='marks_entered')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam_subject', 'student')
        ordering = ['student']
        verbose_name = 'note'
        verbose_name_plural = 'notes'

    def __str__(self):
        return f"{self.student} - {self.exam_subject} - {self.marks_obtained}"

    def note_sur_10(self):
        max_marks = self.exam_subject.max_marks
        return round((float(self.marks_obtained) / max_marks) * 10, 2) if max_marks else 0

    def save(self, *args, **kwargs):
        note = self.note_sur_10()
        if note >= 9:
            self.grade = 'TB'
            self.remarks = 'Très bien'
        elif note >= 8:
            self.grade = 'B'
            self.remarks = 'Bien'
        elif note >= 7:
            self.grade = 'AB'
            self.remarks = 'Assez bien'
        elif note >= 6:
            self.grade = 'P'
            self.remarks = 'Passable'
        elif note >= 5:
            self.grade = 'I'
            self.remarks = 'Insuffisant'
        else:
            self.grade = 'N'
            self.remarks = 'Nul'
        super().save(*args, **kwargs)
