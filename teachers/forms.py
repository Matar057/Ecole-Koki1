from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'date_of_birth', 'gender', 'phone', 'qualification',
            'specialization', 'experience_years', 'photo', 'joining_date',
            'address', 'is_active', 'subjects', 'classes_assigned'
        ]
        labels = {
            'date_of_birth': "Date de naissance",
            'gender': "Genre",
            'phone': "Téléphone",
            'qualification': "Qualification",
            'specialization': "Spécialisation",
            'experience_years': "Années d'expérience",
            'photo': "Photo",
            'joining_date': "Date de début",
            'address': "Adresse",
            'is_active': "Actif",
            'subjects': "Matières",
            'classes_assigned': "Classes assignées",
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'subjects': forms.CheckboxSelectMultiple(),
            'classes_assigned': forms.CheckboxSelectMultiple(),
        }
