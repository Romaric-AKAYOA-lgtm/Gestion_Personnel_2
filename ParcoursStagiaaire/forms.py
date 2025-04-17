from django import forms
from .models import CLParcoursStagiaire

class CLParcoursStagiaireForm(forms.ModelForm):
    class Meta:
        model = CLParcoursStagiaire
        fields = [
            'organizational_unit', 'stagiaire', 'responsable', 'date_debut', 'date_fin',
            'evaluation', 'commentaire', 'competence'
        ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'commentaire': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation des champs selon les besoins
        # Exemple : Ajouter une valeur par défaut pour l'évaluation ou compétence, si nécessaire
        if not self.instance.pk:
            self.fields['evaluation'].initial = "Évaluation en cours"
            self.fields['competence'].initial = "Aucune compétence spécifiée"

        # Vous pouvez également ajouter des validations supplémentaires si nécessaire
        # Exemple : Vérifier si la date de fin est après la date de début
        if 'date_debut' in self.data and 'date_fin' in self.data:
            date_debut = self.data.get('date_debut')
            date_fin = self.data.get('date_fin')
            if date_fin and date_debut > date_fin:
                raise forms.ValidationError("La date de fin ne peut pas être antérieure à la date de début.")

    def clean_responsable(self):
        responsable = self.cleaned_data.get('responsable')

        # Ajoutez ici toute logique de validation spécifique pour le responsable, si nécessaire
        if responsable and responsable.date_retraite:  # Supposons que `date_retraite` existe sur le modèle CLEmploye
            raise forms.ValidationError("Le responsable ne peut pas être un retraité.")

        return responsable
