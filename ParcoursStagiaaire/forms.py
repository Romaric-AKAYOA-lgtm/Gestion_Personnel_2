from django import forms
from .models import CLParcoursStagiaire
from datetime import date

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
        """Empêche de sélectionner un responsable déjà retraité (dont la date de retraite est dans le passé),
        vérifie si l'utilisateur est actif et que la date de fin (ddf) n'est pas encore atteinte."""
        
        responsable = self.cleaned_data.get('responsable')

        if responsable:
            # Vérification de la date de retraite
            date_retraite = getattr(responsable, 'date_retraite', None)
            if date_retraite and date_retraite <= date.today():
                raise forms.ValidationError("Le responsable ne peut pas être un retraité.")

            # Vérification que l'utilisateur est actif (tstt_user actif)
            if not responsable.tstt_user.is_active:
                raise forms.ValidationError("Le responsable doit être un utilisateur actif.")

            # Vérification que la date de fin (ddf) n'est pas encore atteinte
            ddf = getattr(responsable, 'ddf', None)
            if ddf and ddf <= date.today():
                raise forms.ValidationError("La date de fin du responsable est déjà atteinte.")
        
        return responsable
