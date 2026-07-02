from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'user', 'qualification', 'specialization', 'experience_years', 'is_active')
    list_filter = ('is_active', 'subjects', 'classes_assigned')
    search_fields = ('teacher_id', 'user__first_name', 'user__last_name')
    filter_horizontal = ('subjects', 'classes_assigned')
