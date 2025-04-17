from django import forms
from .models import CLConge
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from calendar import monthrange

class CLCongeForm(forms.ModelForm):
    class Meta:
        model = CLConge
        fields = [
            'employe', 
            'typeconge', 
            'date_debut_previsionnel', 
            'date_retour_previsionnel', 
            'date_retour_definitif', 
            'employe_signature'
        ]
        widgets = {
            'date_debut_previsionnel': forms.DateInput(attrs={'type': 'date'}),
            'date_retour_previsionnel': forms.DateInput(attrs={'type': 'date'}),
            'date_retour_definitif': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CLCongeForm, self).__init__(*args, **kwargs)
        # Calculer la date de début prévisionnelle par défaut en fonction du type de congé sélectionné
        if self.instance and self.instance.typeconge:
            # Prendre l'année actuelle
            current_year = datetime.now().year
            # Extraire le mois de début autorisé du type de congé sélectionné
            mois_debut = self.instance.typeconge.mois_debut_autorise
            # Calculer le premier jour du mois
            self.initial['date_debut_previsionnel'] = datetime(current_year, mois_debut, 1).date()
            # Calculer la date de retour prévisionnelle en ajoutant la période de congé
            periode_conge = self.instance.typeconge.periode_conge
            debut_previsionnel = self.initial['date_debut_previsionnel']
            date_retour_previsionnel = debut_previsionnel + timedelta(days=periode_conge)
            self.initial['date_retour_previsionnel'] = date_retour_previsionnel

    def clean(self):
        cleaned_data = super().clean()
        date_debut_previsionnel = cleaned_data.get('date_debut_previsionnel')
        date_retour_previsionnel = cleaned_data.get('date_retour_previsionnel')
        date_retour_definitif = cleaned_data.get('date_retour_definitif')

        if date_debut_previsionnel and date_retour_previsionnel:
            # Vérifier que la date de début prévisionnelle est avant ou égale à la date de retour prévisionnel
            if date_debut_previsionnel > date_retour_previsionnel:
                raise ValidationError("La date de début prévisionnelle doit être antérieure ou égale à la date de retour prévisionnel.")

        if date_retour_previsionnel and date_retour_definitif:
            # Vérifier que la date de retour prévisionnel est avant ou égale à la date de retour définitive
            if date_retour_previsionnel > date_retour_definitif:
                raise ValidationError("La date de retour prévisionnel doit être antérieure ou égale à la date de retour définitive.")

        return cleaned_data
