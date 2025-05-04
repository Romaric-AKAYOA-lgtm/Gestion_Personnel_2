from datetime import date
from django import forms
from .models import CLMission

class CLMissionForm(forms.ModelForm):
    class Meta:
        model = CLMission
        fields = '__all__'
        widgets = {
            'objet': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'organisme': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu_mission': forms.TextInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'conclusion_mission': forms.Textarea(attrs={'class': 'form-control'}),
            'employe_signataire': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        conclusion = cleaned_data.get('conclusion_mission')
        today = date.today()

        # Vérifier que la date de fin est après la date de début
        if date_debut and date_fin and date_fin <= date_debut:
            self.add_error('date_fin', "La date de fin doit être strictement après la date de début.")

        # Vérifier que la conclusion (si présente) est d'au moins 10 caractères
        if conclusion and len(conclusion.strip()) < 10:
            self.add_error('conclusion_mission', "La conclusion doit contenir au moins 10 caractères.")

        return cleaned_data
