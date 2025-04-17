from django import forms
from django.utils.timezone import now
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import ClUser

class ClUserForm(forms.ModelForm):
    class Meta:
        model = ClUser
        fields = [
            'tnm', 'tpm', 'tsx', 'dns', 'tlns', 'tads', 'teml', 'tphne', 'dsb', 'ddf',
            'tstt', 'ttvst', 'img', 'matricule', 'grade', 'echelon'
        ]
        widgets = {
            'dns': forms.DateInput(attrs={'type': 'date'}),
            'dsb': forms.DateInput(attrs={'type': 'date'}),
            'ddf': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClUserForm, self).__init__(*args, **kwargs)
        if not self.initial.get('dsb'):
            self.fields['dsb'].initial = now().date()

        # Définir les contraintes ici si non présentes dans le modèle
        self.fields['echelon'].validators.extend([
            MinValueValidator(1),
            MaxValueValidator(50),
        ])

    def clean_tnm(self):
        tnm = self.cleaned_data.get('tnm')
        if not tnm:
            raise forms.ValidationError("Le nom ne peut pas être vide.")
        if any(char.isdigit() for char in tnm):
            raise forms.ValidationError("Le nom ne doit pas contenir de chiffres.")
        return tnm

    def clean_tpm(self):
        tpm = self.cleaned_data.get('tpm')
        if tpm and any(char.isdigit() for char in tpm):
            raise forms.ValidationError("Le prénom ne doit pas contenir de chiffres.")
        return tpm

    def clean_matricule(self):
        matricule = self.cleaned_data.get('matricule')
        if not matricule:
            raise forms.ValidationError("Le matricule est requis.")
        if len(matricule) != 7:
            raise forms.ValidationError("Le matricule doit contenir exactement 7 caractères.")
        return matricule

    def clean_echelon(self):
        echelon = self.cleaned_data.get('echelon')
        if echelon is not None and not (1 <= echelon <= 50):
            raise forms.ValidationError("L'échelon doit être compris entre 1 et 50.")
        return echelon

    def clean(self):
        cleaned_data = super().clean()
        dns = cleaned_data.get('dns')
        dsb = cleaned_data.get('dsb')

        if dns and dsb:
            delta = dsb - dns
            if delta < timedelta(days=28 * 365):
                self.add_error('dsb', "L'utilisateur doit avoir au moins 28 ans à la date de début.")
