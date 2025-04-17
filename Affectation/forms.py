from django import forms
from .models import CLAffectation
from django.core.exceptions import ValidationError

class CLAffectationForm(forms.ModelForm):
    class Meta:
        model = CLAffectation
        fields = [
            'employe',
            'organisme_affecte',
            'lieu_affectation',
            'statut',
            'motif_affectation',  # Include motif_affectation here
            'date_debut',
            'date_fin',
        ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        statut = cleaned_data.get('statut')
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        employe = cleaned_data.get('employe')
        motif_affectation = cleaned_data.get('motif_affectation')  # Include motif_affectation

        # 1. Vérifie que la date_fin est fournie si le statut est Temporaire
        if statut == 'Temporaire' and not date_fin:
            self.add_error('date_fin', "La date de fin est obligatoire pour une affectation temporaire.")

        # 2. Vérifie que date_debut est >= à la dernière date_debut pour le même employé
        if employe and date_debut:
            last_affectation = (
                CLAffectation.objects
                .filter(employe=employe)
                .exclude(pk=self.instance.pk)  # exclure soi-même en cas de mise à jour
                .order_by('-date_debut')
                .first()
            )
            if last_affectation and last_affectation.date_debut and date_debut < last_affectation.date_debut:
                self.add_error('date_debut', "La date de début doit être supérieure ou égale à la dernière date de début d’affectation existante.")
        
        # 3. Vérifie que date_debut <= date_fin si les deux sont fournis
        if date_debut and date_fin and date_debut > date_fin:
            self.add_error('date_fin', "La date de fin doit être postérieure ou égale à la date de début.")
        
        # 4. Vérifie que la date_fin est vide pour un statut Définitif
        if statut == 'Définitif' and date_fin:
            self.add_error('date_fin', "La date de fin ne doit pas être renseignée pour une affectation définitive.")
        
        # 5. Vérifie que le motif d'affectation est fourni
        if not motif_affectation:
            self.add_error('motif_affectation', "Le motif d'affectation est obligatoire.")

        return cleaned_data
