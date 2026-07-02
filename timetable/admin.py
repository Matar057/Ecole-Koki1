from django.contrib import admin
from .models import TimetableSlot


@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'section', 'subject', 'teacher', 'day', 'start_time', 'end_time')
    list_filter = ('day', 'class_obj')
