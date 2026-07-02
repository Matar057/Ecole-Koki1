from django import forms
from .models import Exam, ExamSubject, Mark

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'exam_type', 'academic_year', 'start_date', 'end_date', 'description', 'is_published']
        labels = {
            'name': "Nom",
            'exam_type': "Type d'examen",
            'academic_year': "Année académique",
            'start_date': "Date de début",
            'end_date': "Date de fin",
            'description': "Description",
            'is_published': "Publié",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_type': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ExamSubjectForm(forms.ModelForm):
    class Meta:
        model = ExamSubject
        fields = ['exam', 'subject', 'class_obj', 'max_marks', 'passing_marks']
        labels = {
            'exam': "Examen",
            'subject': "Matière",
            'class_obj': "Classe",
            'max_marks': "Points max",
            'passing_marks': "Note de passage",
        }
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'class_obj': forms.Select(attrs={'class': 'form-select'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['marks_obtained', 'remarks']
        labels = {
            'marks_obtained': "Notes obtenues",
            'remarks': "Remarques",
        }
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ExamSubjectForm(forms.ModelForm):
    class Meta:
        model = ExamSubject
        fields = ['exam', 'subject', 'class_obj', 'max_marks', 'passing_marks']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'class_obj': forms.Select(attrs={'class': 'form-select'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['marks_obtained', 'remarks']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }
