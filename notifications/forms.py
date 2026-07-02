from django import forms
from .models import Announcement, Notification

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'priority', 'target_audience', 'is_active', 'publish_from', 'publish_to']
        labels = {
            'title': "Titre",
            'content': "Contenu",
            'priority': "Priorité",
            'target_audience': "Public cible",
            'is_active': "Actif",
            'publish_from': "Publier à partir de",
            'publish_to': "Publier jusqu'à",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'target_audience': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'publish_from': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'publish_to': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
