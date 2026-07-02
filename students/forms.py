from django import forms
from django.contrib.auth import get_user_model
from .models import Student, Parent, StudentDocument

User = get_user_model()


class StudentForm(forms.ModelForm):
    # first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}), label="Prénom")
    # last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}), label="Nom")
    # student_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "E-mail de l'étudiant"}), label="E-mail", help_text="Ce sera utilisé pour la connexion")

    parent_full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet du parent/tuteur'}), label="Nom du parent/tuteur")
    parent_phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone du parent'}), label="Téléphone du parent")

    class Meta:
        model = Student
        fields = [
            'date_of_birth', 'gender', 'blood_group', 'photo',
            'class_enrolled', 'section', 'address',
            'emergency_contact', 'medical_notes', 'is_active'
        ]
        labels = {
            'date_of_birth': "Date de naissance",
            'gender': "Genre",
            'blood_group': "Groupe sanguin",
            'photo': "Photo",
            'class_enrolled': "Classe inscrite",
            'section': "Section",
            'address': "Adresse",
            'emergency_contact': "Contact d'urgence",
            'medical_notes': "Notes médicales",
            'is_active': "Actif",
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'class_enrolled': forms.Select(attrs={'class': 'form-select'}),
            'section': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ['title', 'document']
        labels = {
            'title': "Titre",
            'document': "Document",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }
