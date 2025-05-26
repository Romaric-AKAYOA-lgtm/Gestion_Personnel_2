from django import forms
from django.db.models import Q
from datetime import date

from mutation.models import CLMutation
from .models import CLParcoursStagiaire

class CLParcoursStagiaireForm(forms.ModelForm):
    class Meta:
        model = CLParcoursStagiaire
        fields = [
            'organizational_unit', 'stagiaire', 'responsable',
            'date_debut', 'date_fin', 'evaluation', 'commentaire', 'competences'
        ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'commentaire': forms.Textarea(attrs={'rows': 3}),
            'competences': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Ex: Python, SQL, Communication'
            }),
        }

    def clean_responsable(self):
        responsable = self.cleaned_data.get('responsable')

        if not responsable:
            raise forms.ValidationError("Veuillez sélectionner un responsable.")

        # 1. Vérification de la date de retraite
        date_retraite = getattr(responsable, 'date_retraite', None)
        if date_retraite and date_retraite <= date.today():
            raise forms.ValidationError("Le responsable sélectionné est déjà à la retraite.")

        # 2. Vérification que le responsable est lié à un utilisateur système
        if not getattr(responsable, 'tstt_user', None):
            raise forms.ValidationError("Le responsable sélectionné n’est associé à aucun utilisateur du système.")


        return responsable

    def clean(self):
        cleaned_data = super().clean()
        stagiaire = cleaned_data.get('stagiaire')
        date_fin = cleaned_data.get('date_fin')

        # Vérification que la date de fin du parcours ne dépasse pas la fin du stage du stagiaire
        if stagiaire and date_fin:
            date_fin_stage = getattr(stagiaire, 'ddf', None)
            if date_fin_stage and date_fin > date_fin_stage:
                self.add_error(
                    'date_fin',
                    f"La date de fin du parcours ne peut pas dépasser la date de fin de stage du stagiaire ({date_fin_stage.strftime('%Y-%m-%d')})."
                )

        return cleaned_data
