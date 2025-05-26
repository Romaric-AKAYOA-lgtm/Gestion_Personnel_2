from django import forms
from Affectation.models import CLAffectation
from .models import CLEmployeMission

class CLEmployeMissionForm(forms.ModelForm):
    class Meta:
        model = CLEmployeMission
        fields = ['mission', 'employe', 'statut']
        widgets = {
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mission = cleaned_data.get('mission')
        employe = cleaned_data.get('employe')
        statut = cleaned_data.get('statut')

        # Vérifier si l'employé est déjà assigné à cette mission
        if CLEmployeMission.objects.filter(
            mission=mission, employe=employe
        ).exclude(pk=self.instance.pk).exists():
            self.add_error('employe', 'Cet employé est déjà affecté à cette mission.')

        # Vérifier l'unicité du chef de mission
        if statut == 'Chef de mission':
            chef_existant = CLEmployeMission.objects.filter(
                mission=mission,
                statut='Chef de mission'
            ).exclude(pk=self.instance.pk).exists()
            if chef_existant:
                self.add_error('statut', 'Cette mission a déjà un chef de mission.')

        # Vérifier les affectations définitives de l'employé
        if employe:
            has_definitive = CLAffectation.objects.filter(
                employe=employe,
                statut='Définitif'
            ).exists()

            if has_definitive:
                raise forms.ValidationError(
                    "Cet employé a déjà une affectation définitive et ne peut pas être modifié/créé."
                )

        return cleaned_data
