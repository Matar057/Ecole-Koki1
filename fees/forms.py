from django import forms
from .models import FeeStructure, FeePayment

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['name', 'class_obj', 'academic_year', 'amount', 'due_date', 'description', 'is_active']
        labels = {
            'name': "Nom",
            'class_obj': "Classe",
            'academic_year': "Année académique",
            'amount': "Montant",
            'due_date': "Date d'échéance",
            'description': "Description",
            'is_active': "Actif",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'class_obj': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'fee_structure', 'amount_due', 'amount_paid', 'payment_method', 'payment_phone', 'transaction_id', 'remarks']
        labels = {
            'student': "Étudiant",
            'fee_structure': "Structure de frais",
            'amount_due': "Montant dû",
            'amount_paid': "Montant payé",
            'payment_method': "Méthode de paiement",
            'payment_phone': "Téléphone du payeur",
            'transaction_id': "ID de transaction",
            'remarks': "Remarques",
        }
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'fee_structure': forms.Select(attrs={'class': 'form-select'}),
            'amount_due': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'payment_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 77 123 45 67'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
