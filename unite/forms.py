from django import forms
from .models import Unite
from django.core.exceptions import ValidationError

from django import forms
from .models import Unite

class UniteForm(forms.ModelForm):
    class Meta:
        model = Unite
        fields = ['designation', 'unite_parent']  # Liste des champs à inclure dans le formulaire

    def clean_designation(self):
        designation = self.cleaned_data['designation']
        
        # Vérification que la designation ne contient pas de chiffres ni de caractères spéciaux
        if any(char.isdigit() for char in designation):
            raise ValidationError("La designation ne doit contenir que des lettres, sans chiffres ni caractères spéciaux.")
        
        # Vérification que la designation n'est pas vide
        if not designation:
            raise ValidationError("La designation est obligatoire.")
        
        return designation
