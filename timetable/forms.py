from django import forms
from .models import TimetableSlot

class TimetableSlotForm(forms.ModelForm):
    class Meta:
        model = TimetableSlot
        fields = ['class_obj', 'section', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room_number']
        labels = {
            'class_obj': "Classe",
            'section': "Section",
            'subject': "Matière",
            'teacher': "Enseignant",
            'day': "Jour",
            'start_time': "Heure de début",
            'end_time': "Heure de fin",
            'room_number': "Numéro de salle",
        }
        widgets = {
            'class_obj': forms.Select(attrs={'class': 'form-select'}),
            'section': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
