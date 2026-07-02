from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = _('Parent')
        verbose_name_plural = _('Parents')
        ordering = ['user__last_name']

    def __str__(self):
        return self.user.get_full_name()

    @property
    def children(self):
        return self.students.all()


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, blank=True, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ])
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    admission_date = models.DateField(auto_now_add=True)
    class_enrolled = models.ForeignKey(
        'academics.Class', on_delete=models.SET_NULL, null=True, blank=True, related_name='students'
    )
    section = models.ForeignKey(
        'academics.Section', on_delete=models.SET_NULL, null=True, blank=True, related_name='students'
    )
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    medical_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['student_id']
        verbose_name = 'étudiant'
        verbose_name_plural = 'étudiants'

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.student_id:
            last_id = Student.objects.all().order_by('-id').first()
            if last_id:
                try:
                    num = int(last_id.student_id.split('-')[1]) + 1
                except (ValueError, IndexError):
                    num = 1
            else:
                num = 1
            self.student_id = f'STU-{num:04d}'
        super().save(*args, **kwargs)


class StudentDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to='students/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'document étudiant'
        verbose_name_plural = 'documents étudiants'

    def __str__(self):
        return f"{self.student} - {self.title}"
