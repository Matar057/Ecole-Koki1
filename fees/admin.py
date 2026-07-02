from django.contrib import admin
from .models import FeeStructure, FeePayment


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_obj', 'academic_year', 'amount', 'due_date', 'is_active')
    list_filter = ('is_active', 'academic_year', 'class_obj')


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_structure', 'amount_due', 'amount_paid', 'status', 'payment_date')
    list_filter = ('status', 'payment_method')
    search_fields = ('student__student_id', 'receipt_number')
