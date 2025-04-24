from django import forms
from .models import OrganizationalUnit, Unite
from django.core.exceptions import ValidationError

class OrganizationalUnitForm(forms.ModelForm):
    class Meta:
        model = OrganizationalUnit
        fields = ['name', 'parent', 'unite', 'designation']

        # Définir des widgets personnalisés si nécessaire
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Nom de l'unité"}),
            'designation': forms.Textarea(attrs={'placeholder': "Désignation de l'unité"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Le nom de l'unité est obligatoire.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')

        # Validation pour s'assurer qu'une unité ne peut pas être son propre parent
        if parent and self.instance.pk and parent.pk == self.instance.pk:
            raise ValidationError("Une unité ne peut pas être son propre parent.")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
