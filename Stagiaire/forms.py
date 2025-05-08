from django import forms
from django.core.exceptions import ValidationError
from users.forms import ClUserForm
from Stagiaire.models import CLStagiaire
from datetime import date

class ClStagiaireForm(ClUserForm):
    class Meta:
        model = CLStagiaire
        fields = ClUserForm.Meta.fields + [
            'etablissement',
            'theme',
            'filiere',
            'option',
            'responsable',
            'organisationUnit',
            'tstt',
        ]
        widgets = ClUserForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialiser 'tstt' à 'Stagiaire' si c’est une création
        if not self.instance.pk:
            self.fields['tstt'].initial = 'Stagiaire'
            self.fields['tstt'].widget.attrs['readonly'] = True

    def clean_responsable(self):
        """Empêche de sélectionner un responsable déjà retraité (dont la date de retraite est dans le passé)."""
        responsable = self.cleaned_data.get('responsable')

        if responsable and getattr(responsable, 'date_retraite', None):
            # Récupérer la date de retraite et comparer avec la date actuelle
            date_retraite = responsable.date_retraite
            if date_retraite <= date.today():  # Si la date de retraite est dans le passé ou aujourd'hui
                raise ValidationError("Le responsable ne peut pas être un retraité.")
        
        return responsable
