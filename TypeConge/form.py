from django import forms
from .models import CLTypeConge
from django.core.exceptions import ValidationError
from datetime import date
from calendar import monthrange

class CLTypeCongeForm(forms.ModelForm):
    class Meta:
        model = CLTypeConge
        fields = ['designation', 'periode_conge', 'mois_debut_autorise']
        widgets = {
            'mois_debut_autorise': forms.Select(choices=CLTypeConge.MOIS_CHOICES),
        }

    def clean(self):
        cleaned_data = super().clean()
        mois_debut = cleaned_data.get('mois_debut_autorise')
        periode_conge = cleaned_data.get('periode_conge')

        if mois_debut and periode_conge:
            # Calculer le mois de fin
            mois_fin = self.calculer_mois_fin(mois_debut, periode_conge)

            # Vérifier que la période de congé est raisonnable (dans l'exemple, on la limite à 12 mois max)
            if mois_fin > 12:
                raise ValidationError("La période de congé dépasse l'année en cours. Veuillez ajuster.")

            # Calculer la date de fin autorisée (juste pour information, selon la période de congé)
            date_debut = date(2022, mois_debut, 1)  # Utiliser une année fictive pour calculer la date
            jours_dans_mois = monthrange(2022, mois_debut)[1]  # Nombre de jours dans le mois de début
            total_jours = periode_conge

            while total_jours > jours_dans_mois:
                total_jours -= jours_dans_mois
                date_debut = date_debut.replace(month=(mois_debut % 12) + 1)  # Passer au mois suivant
                mois_debut = date_debut.month

            date_fin = date_debut.replace(day=total_jours)

            cleaned_data['date_debut_autorisee'] = date_debut
            cleaned_data['date_fin_autorisee'] = date_fin

        return cleaned_data

    def calculer_mois_fin(self, mois_debut, periode_conge):
        """Calculer le mois de fin du congé basé sur le mois de début et la durée"""
        mois_fin = mois_debut
        jours_dans_mois = monthrange(2022, mois_debut)[1]  # Nombre de jours dans le mois de début
        total_jours = periode_conge

        while total_jours > jours_dans_mois:
            total_jours -= jours_dans_mois
            mois_fin += 1
            if mois_fin > 12:
                mois_fin = 1
        return mois_fin
