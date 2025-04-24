from django import forms
from .models import CLTypeConge

class CLTypeCongeForm(forms.ModelForm):
    class Meta:
        model = CLTypeConge
        fields = ['designation', 'periode_conge', 'mois_debut_autorise']
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Congé annuel'}),
            'periode_conge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Durée en jours'}),
            'mois_debut_autorise': forms.Select(choices=CLTypeConge.MOIS_CHOICES, attrs={'class': 'form-control'}),
        }
        labels = {
            'designation': 'Désignation',
            'periode_conge': 'Durée du congé (en jours)',
            'mois_debut_autorise': 'Mois de début autorisé',
        }
