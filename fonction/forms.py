from django import forms
from .models import Fonction
from django.core.exceptions import ValidationError
import re

class FonctionForm(forms.ModelForm):
    class Meta:
        model = Fonction
        fields = ['designation', 'parent']  # Inclure le champ 'parent' pour la relation réflexive

    def clean_designation(self):
        designation = self.cleaned_data['designation']
        
        # Vérification que la designation ne contient pas de chiffres ni de caractères spéciaux
        if any(char.isdigit() for char in designation) or not re.match("^[a-zA-Z\s]*$", designation):
            raise ValidationError("La désignation ne doit contenir que des lettres et des espaces, sans chiffres ni caractères spéciaux.")
        
        # Vérification que la designation n'est pas vide
        if not designation:
            raise ValidationError("La désignation est obligatoire.")
        
        return designation

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        
        # Vérifier que la fonction parente ne pointe pas vers elle-même
        if parent and parent == self.instance:
            raise ValidationError("Une fonction ne peut pas être sa propre fonction parente.")
        
        return parent
