from django import forms
from .models import CLMission
from django.core.exceptions import ValidationError
from datetime import date

class CLMissionForm(forms.ModelForm):
    class Meta:
        model = CLMission
        fields = [
            'employe_signataire', 
            'objet', 
            'description', 
            'date_debut', 
            'date_fin', 
            'lieu_mission', 
            'organisme',
            'conclusion_mission'  # Added conclusion_mission to the fields list
        ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        today = date.today()

        if date_debut and date_debut < today:
            raise ValidationError("La date de début doit être supérieure ou égale à la date d'aujourd'hui.")

        if date_debut and date_fin and date_fin <= date_debut:
            raise ValidationError("La date de fin doit être strictement supérieure à la date de début.")

        # You can add any validation for conclusion_mission if necessary, but it can be left empty.
        conclusion_mission = cleaned_data.get('conclusion_mission')
        if conclusion_mission and len(conclusion_mission) < 10:  # Example of validation
            self.add_error('conclusion_mission', "La conclusion doit contenir au moins 10 caractères.")

        return cleaned_data
