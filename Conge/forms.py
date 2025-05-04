from django import forms
from .models import CLConge
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.db.models import Q

class CLCongeForm(forms.ModelForm):
    class Meta:
        model = CLConge
        fields = [
            'employe', 
            'typeconge', 
            'date_debut_previsionnel', 
            'date_retour_previsionnel', 
            'date_retour_definitif', 
        ]
        widgets = {
            'date_debut_previsionnel': forms.DateInput(attrs={'type': 'date'}),
            'date_retour_previsionnel': forms.DateInput(attrs={'type': 'date'}),
            'date_retour_definitif': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CLCongeForm, self).__init__(*args, **kwargs)

        today = now().date()
        current_year = today.year

        # ✅ 1. Filtrage des employés
        self.fields['employe'].queryset = self.fields['employe'].queryset.filter(
            tstt_user='actif',
            date_retraite__gt=today
        ).filter(
            Q(ddf__isnull=True) | Q(ddf__gt=today)
        )

        # ✅ 2. Filtrage des types de congé à la création
        if not self.instance.pk:
            self.fields['typeconge'].queryset = self.fields['typeconge'].queryset.filter(
                mois_debut_autorise__gte=today.month
            )

            # ✅ 3. Pré-remplissage automatique des dates
            if 'typeconge' in self.fields:
                typeconges = self.fields['typeconge'].queryset
                if typeconges.exists():
                    premier_type = typeconges.first()
                    mois_debut = premier_type.mois_debut_autorise
                    duree = premier_type.periode_conge

                    date_debut = datetime(current_year, mois_debut, 1).date()
                    date_retour = date_debut + timedelta(days=duree)

                    self.initial['date_debut_previsionnel'] = date_debut
                    self.initial['date_retour_previsionnel'] = date_retour

    def clean(self):
        cleaned_data = super().clean()
        date_debut_previsionnel = cleaned_data.get('date_debut_previsionnel')
        date_retour_previsionnel = cleaned_data.get('date_retour_previsionnel')
        date_retour_definitif = cleaned_data.get('date_retour_definitif')
        employe = cleaned_data.get('employe')
        today = datetime.now().date()

        # Vérification des dates
        if date_debut_previsionnel and date_retour_previsionnel:
            if date_debut_previsionnel > date_retour_previsionnel:
                raise ValidationError(
                    f"La date de début prévisionnelle doit être antérieure ou égale à la date de retour prévisionnelle. "
                    f"(Début: {date_debut_previsionnel}, Retour: {date_retour_previsionnel})"
                )

        if date_retour_previsionnel and date_retour_definitif:
            if date_retour_definitif < date_retour_previsionnel:
                raise ValidationError(
                    f"La date de retour définitive doit être supérieure ou égale à la date de retour prévisionnelle. "
                    f"(Prévisionnel: {date_retour_previsionnel}, Définitif: {date_retour_definitif})"
                )

        if date_debut_previsionnel and date_debut_previsionnel < today:
            raise ValidationError(
                f"La date de début du congé ne peut pas être dans le passé. (Date choisie: {date_debut_previsionnel})"
            )

        if employe:
            nb_conges = CLConge.objects.filter(employe=employe).count()
            if nb_conges >= 3:
                raise ValidationError(
                    f"L'employé ne peut pas avoir plus de trois congés en cours. (Congés actuels: {nb_conges})"
                )

        return cleaned_data
