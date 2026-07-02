from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status', 'remarks']
        labels = {
            'student': "Étudiant",
            'date': "Date",
            'status': "Statut",
            'remarks': "Remarques",
        }
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BulkAttendanceForm(forms.Form):
    date = forms.DateField(label="Date", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
