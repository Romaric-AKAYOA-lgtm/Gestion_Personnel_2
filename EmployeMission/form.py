from django import forms
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

        # Optionnel : éviter qu'un employé soit assigné deux fois à la même mission
        if CLEmployeMission.objects.filter(mission=mission, employe=employe).exclude(pk=self.instance.pk).exists():
            self.add_error('employe', 'Cet employé est déjà affecté à cette mission.')

        return cleaned_data
