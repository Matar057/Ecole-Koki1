from django.contrib import admin
from .models import Exam, ExamSubject, Mark


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'academic_year', 'start_date', 'end_date', 'is_published')
    list_filter = ('exam_type', 'is_published', 'academic_year')


@admin.register(ExamSubject)
class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ('exam', 'subject', 'class_obj', 'max_marks', 'passing_marks')
    list_filter = ('exam', 'class_obj')


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam_subject', 'marks_obtained', 'grade')
    list_filter = ('grade', 'exam_subject__exam')
    search_fields = ('student__student_id', 'student__user__first_name')
