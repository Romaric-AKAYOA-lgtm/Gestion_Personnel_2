# -*- coding: utf-8 -*-
from django import forms
from .models import CLAffectation
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q

class CLAffectationForm(forms.ModelForm):
    class Meta:
        model = CLAffectation
        fields = [
            'employe',
            'organisme_affecte',
            'lieu_affectation',
            'statut',
            'motif_affectation',
            'date_debut',
            'date_fin',
        ]
        widgets = {
            'employe': forms.Select(attrs={'class': 'form-control'}),
            'organisme_affecte': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu_affectation': forms.TextInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'motif_affectation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.now().date()

        # Exclure les employés affectés sauf si c'est celui de l'instance en cours
        if self.instance and self.instance.pk:
            employes_exclus = CLAffectation.objects.filter(
                Q(statut='Définitif') |
                Q(statut='Temporaire', date_fin__lt=today)
            ).exclude(
                employe=self.instance.employe  # Garder l'employé en cours de modification
            ).values_list('employe_id', flat=True)
        else:
            employes_exclus = CLAffectation.objects.filter(
                Q(statut='Définitif') |
                Q(statut='Temporaire', date_fin__lt=today)
            ).values_list('employe_id', flat=True)

        self.fields['employe'].queryset = self.fields['employe'].queryset.exclude(id__in=employes_exclus)

        # Désactiver le champ 'employe' si c'est une modification
        if self.instance and self.instance.pk:
            self.fields['employe'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        statut = cleaned_data.get('statut')
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        employe = cleaned_data.get('employe')
        motif_affectation = cleaned_data.get('motif_affectation')

        # Nettoyer les espaces
        for field in ['organisme_affecte', 'lieu_affectation', 'motif_affectation']:
            if field in cleaned_data and isinstance(cleaned_data[field], str):
                cleaned_data[field] = cleaned_data[field].strip()

        # 1. date_fin obligatoire si Temporaire
        if statut == 'Temporaire' and not date_fin:
            self.add_error('date_fin', "La date de fin est obligatoire pour une affectation temporaire.")

        # 2. date_debut >= dernière affectation (si existante)
        if employe and date_debut:
            last_affectation = (
                CLAffectation.objects
                .filter(employe=employe)
                .exclude(pk=self.instance.pk)
                .order_by('-date_debut')
                .first()
            )
            if last_affectation and last_affectation.date_debut and date_debut < last_affectation.date_debut:
                self.add_error(
                    'date_debut',
                    f"La date de début doit être postérieure ou égale à la dernière date d’affectation ({last_affectation.date_debut})."
                )

        # 3. Vérifie cohérence date_debut <= date_fin
        if date_debut and date_fin and date_debut > date_fin:
            self.add_error('date_fin', "La date de fin doit être postérieure ou égale à la date de début.")

        # 4. Motif obligatoire
        if not motif_affectation:
            self.add_error('motif_affectation', "Le motif d'affectation est obligatoire.")

        return cleaned_data
