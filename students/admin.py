from django.contrib import admin
from .models import Student, Parent, StudentDocument


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'occupation')
    search_fields = ('user__first_name', 'user__last_name', 'email')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'class_enrolled', 'section', 'gender', 'is_active', 'admission_date')
    list_filter = ('gender', 'is_active', 'class_enrolled', 'section')
    search_fields = ('student_id', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user', 'parent')


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'uploaded_at')
    list_filter = ('uploaded_at',)
