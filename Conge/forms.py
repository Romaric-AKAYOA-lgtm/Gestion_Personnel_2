from django import forms

from Affectation.models import CLAffectation
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

        # ✅ 1. Filtrage des employés actifs
        self.fields['employe'].queryset = self.fields['employe'].queryset.filter(
            tstt_user='actif',
            date_retraite__gt=today
        ).filter(
            Q(ddf__isnull=True) | Q(ddf__gt=today)
        )

        # ✅ 2. Filtrage des types de congé valides
        if not self.instance.pk:
            self.fields['typeconge'].queryset = self.fields['typeconge'].queryset.filter(
                mois_debut_autorise__gte=today.month
            )

            # Préremplissage des dates si un type de congé existe
            typeconges = self.fields['typeconge'].queryset
            if typeconges.exists():
                premier_type = typeconges.first()
                mois_debut = premier_type.mois_debut_autorise
                duree = premier_type.periode_conge

                try:
                    date_debut = datetime(current_year, mois_debut, 1).date()
                    date_retour = date_debut + timedelta(days=duree)

                    self.initial['date_debut_previsionnel'] = date_debut
                    self.initial['date_retour_previsionnel'] = date_retour
                except Exception as e:
                    print(f"Erreur lors de l'initialisation automatique des dates : {e}")

    def clean(self):
        cleaned_data = super().clean()
        typeconge = cleaned_data.get('typeconge')
        date_debut_previsionnel = cleaned_data.get('date_debut_previsionnel')
        date_retour_previsionnel = cleaned_data.get('date_retour_previsionnel')
        date_retour_definitif = cleaned_data.get('date_retour_definitif')
        employe = cleaned_data.get('employe')
        today = now().date()

        # ✅ Auto-complétion des dates manquantes à la soumission
        if not date_debut_previsionnel and typeconge:
            try:
                mois_debut = typeconge.mois_debut_autorise
                date_debut_previsionnel = datetime(today.year, mois_debut, 1).date()
                cleaned_data['date_debut_previsionnel'] = date_debut_previsionnel
            except Exception as e:
                raise ValidationError("Erreur lors de la génération automatique de la date de début.")

        if not date_retour_previsionnel and typeconge and date_debut_previsionnel:
            try:
                duree = typeconge.periode_conge
                date_retour_previsionnel = date_debut_previsionnel + timedelta(days=duree)
                cleaned_data['date_retour_previsionnel'] = date_retour_previsionnel
            except Exception as e:
                raise ValidationError("Erreur lors du calcul de la date de retour prévisionnelle.")

        # ✅ Vérification cohérente des dates
        if date_debut_previsionnel and date_retour_previsionnel:
            if date_debut_previsionnel > date_retour_previsionnel:
                raise ValidationError(
                    f"La date de début doit précéder la date de retour. "
                    f"(Début: {date_debut_previsionnel}, Retour: {date_retour_previsionnel})"
                )

        if date_retour_previsionnel and date_retour_definitif:
            if date_retour_definitif < date_retour_previsionnel:
                raise ValidationError(
                    f"La date de retour définitive doit être après la date de retour prévisionnelle. "
                    f"(Prévisionnel: {date_retour_previsionnel}, Définitif: {date_retour_definitif})"
                )

        if date_debut_previsionnel and date_debut_previsionnel < today:
            raise ValidationError(
                f"La date de début du congé ne peut pas être dans le passé. "
                f"(Choisie: {date_debut_previsionnel})"
            )

        if employe:
            nb_conges = CLConge.objects.filter(employe=employe).count()
            if nb_conges >= 3:
                raise ValidationError(
                    f"L'employé ne peut pas avoir plus de trois congés en cours. (Actuels: {nb_conges})"
                )

        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        employe = self.instance

        # Si c'est une modification (instance pk existe) ou création
        # on vérifie si l'employé a une affectation définitive

        # Récupérer les affectations définitives liées à cet employé
        has_definitive = CLAffectation.objects.filter(
            employe=employe,
            statut='Définitif'
        ).exists()

        if has_definitive:
            raise ValidationError("Cet employé a déjà une affectation définitive et ne peut pas être modifié/créé.")

        return cleaned_data
