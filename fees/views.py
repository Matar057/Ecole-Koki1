from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, Count
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import datetime
from .models import FeeStructure, FeePayment
from .forms import FeeStructureForm, FeePaymentForm
from users.decorators import role_required
from students.models import Student
from django.conf import settings
import os


@login_required
def fee_structure_list(request):
    fees = FeeStructure.objects.select_related('class_obj', 'academic_year').all()
    return render(request, 'fees/fee_structure_list.html', {'fees': fees})


@role_required('admin')
def fee_structure_create(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Structure des frais créée.')
            return redirect('fees:fee_structure_list')
    else:
        form = FeeStructureForm()
    return render(request, 'fees/fee_structure_form.html', {'form': form, 'title': 'Ajouter une structure de frais'})


@role_required('admin')
def fee_structure_edit(request, pk):
    fee = get_object_or_404(FeeStructure, pk=pk)
    if request.method == 'POST':
        form = FeeStructureForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Structure des frais mise à jour.')
            return redirect('fees:fee_structure_list')
    else:
        form = FeeStructureForm(instance=fee)
    return render(request, 'fees/fee_structure_form.html', {'form': form, 'title': 'Modifier la structure de frais'})


@login_required
def payment_list(request):
    payments = FeePayment.objects.select_related('student', 'fee_structure').all()
    status = request.GET.get('status')
    if status:
        payments = payments.filter(status=status)
    return render(request, 'fees/payment_list.html', {'payments': payments})


@role_required('admin')
def payment_create(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.paid_by = request.user
            payment.payment_date = datetime.date.today()
            payment.save()
            messages.success(request, 'Paiement enregistré.')
            return redirect('fees:payment_detail', pk=payment.pk)
    else:
        form = FeePaymentForm()
    return render(request, 'fees/payment_form.html', {'form': form, 'title': 'Enregistrer un paiement'})

@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(FeePayment.objects.select_related('student__user', 'fee_structure', 'paid_by'), pk=pk)
    return render(request, 'fees/payment_detail.html', {'payment': payment})


@role_required('admin')
def payment_receipt(request, pk):
    payment = get_object_or_404(FeePayment, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=receipt_{payment.receipt_number}.pdf'
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph('Système de gestion scolaire', styles['Title']))
    elements.append(Paragraph('Reçu de paiement', styles['h2']))
    elements.append(Spacer(1, 20))
    data = [
        ['Numéro de reçu', payment.receipt_number],
        ['Date', str(payment.payment_date or payment.created_at.date())],
        ['Étudiant', payment.student.user.get_full_name()],
        ['ID Étudiant', payment.student.student_id],
        ['Type de frais', payment.fee_structure.name],
        ['Montant dû', f'${payment.amount_due}'],
        ['Montant payé', f'${payment.amount_paid}'],
        ['Statut', payment.get_status_display()],
        ['Méthode de paiement', payment.get_payment_method_display()],
        ['ID de transaction', payment.transaction_id or 'N/A'],
    ]
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(table)
    doc.build(elements)
    return response


@role_required('admin')
def fee_summary(request):
    total_collected = FeePayment.objects.filter(status__in=['paid', 'partial']).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_pending = FeePayment.objects.filter(status='pending').aggregate(Sum('amount_due'))['amount_due__sum'] or 0
    payments_by_status = FeePayment.objects.values('status').annotate(count=Count('id'))
    return render(request, 'fees/fee_summary.html', {
        'total_collected': total_collected,
        'total_pending': total_pending,
        'payments_by_status': payments_by_status,
    })
