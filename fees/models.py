from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import datetime
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


class FeeStructure(models.Model):
    name = models.CharField(max_length=100)
    class_obj = models.ForeignKey('academics.Class', on_delete=models.CASCADE, related_name='fee_structures')
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE, related_name='fee_structures')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['due_date']
        unique_together = ('name', 'class_obj', 'academic_year')
        verbose_name = 'structure de frais'
        verbose_name_plural = 'structures de frais'

    def __str__(self):
        return f"{self.name} - {self.class_obj} ({self.academic_year})"


class FeePayment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('wave', 'Wave'),
        ('orange_money', 'Orange Money'),
    )

    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('partial', 'Partiel'),
        ('overdue', 'En retard'),
        ('waived', 'Exonéré'),
    )

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='payments')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    transaction_id = models.CharField(max_length=50, blank=True)
    payment_phone = models.CharField("Téléphone du payeur", max_length=20, blank=True, help_text="Numéro Wave ou Orange Money utilisé")
    receipt_number = models.CharField(max_length=20, unique=True, blank=True)
    qr_code = models.ImageField("QR Code", upload_to='payment_qrcodes/', blank=True, null=True)
    remarks = models.TextField(blank=True)
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='payments_processed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'paiement de frais'
        verbose_name_plural = 'paiements de frais'

    def __str__(self):
        return f"{self.student} - {self.fee_structure} - {self.status}"

    def generate_qr_code(self):
        qr_data = (
            f"École Élémentaire Koki 1\n"
            f"Reçu: {self.receipt_number}\n"
            f"Élève: {self.student.user.get_full_name()}\n"
            f"Frais: {self.fee_structure.name}\n"
            f"Montant: {self.amount_paid} FC\n"
            f"Méthode: {self.get_payment_method_display()}\n"
            f"Téléphone: {self.payment_phone}\n"
            f"Date: {self.payment_date or ''}"
        )
        qr = qrcode.make(qr_data, box_size=6)
        stream = BytesIO()
        qr.save(stream, format='PNG')
        filename = f'qr_{self.receipt_number}.png'
        self.qr_code.save(filename, ContentFile(stream.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            last_receipt = FeePayment.objects.all().order_by('-id').first()
            if last_receipt and last_receipt.receipt_number:
                try:
                    num = int(last_receipt.receipt_number.split('-')[1]) + 1
                except (ValueError, IndexError):
                    num = 1
            else:
                num = 1
            self.receipt_number = f'RCP-{num:06d}'
        if self.amount_paid >= self.amount_due:
            self.status = 'paid'
        elif self.amount_paid > 0:
            self.status = 'partial'
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)
