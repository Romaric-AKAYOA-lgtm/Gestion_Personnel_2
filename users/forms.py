from django import forms
from django.utils.timezone import now
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import ClUser, Specialite  # Assure-toi d'importer Specialite

class ClUserForm(forms.ModelForm):
    class Meta:
        model = ClUser
        fields = [
            'tnm', 'tpm', 'tsx', 'dns', 'tlns', 'tads', 'teml', 'tphne',
            'dsb', 'ddf', 'observation', 'tstt', 'ttvst', 'img',
            'matricule', 'grade', 'echelon', 'specialite', 'tstt_user'
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

        self.fields['specialite'].required = False  # Champ non obligatoire

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
        if matricule and len(matricule) < 5:
            raise forms.ValidationError("Le matricule doit contenir au moins 5 caractères.")
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
            if delta < timedelta(days=18 * 365):
                self.add_error('dsb', "L'utilisateur doit avoir au moins 18 ans à la date de début.")

    def save(self, commit=True):
        user = super().save(commit=False)

        # ➤ Vérification automatique : si date_retraite atteinte ou dépassée
        date_retraite = getattr(user, 'date_retraite', None)
        today = now().date()

        if date_retraite and date_retraite <= today:
            user.ddf = today             # Mettre à jour la date de départ
            user.tstt_user = False       # Mettre à inactif

        if commit:
            user.save()
            self.save_m2m()

        return user
