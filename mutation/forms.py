from django import forms
from .models import CLMutation


class CLMutationForm(forms.ModelForm):
    class Meta:
        model = CLMutation
        fields = [
            'organizational_unit',
            'employe',
            'responsable',
            'function',
            'date_debut',
            'date_fin',
        ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        employe = cleaned_data.get("employe")
        responsable = cleaned_data.get("responsable")
        organizational_unit = cleaned_data.get("organizational_unit")
        date_debut = cleaned_data.get("date_debut")

        # Vérifier que l'employé n'est pas son propre responsable
        if employe and responsable and employe == responsable:
            raise forms.ValidationError("Un employé ne peut pas être son propre responsable.")

        # Vérifier la validité de la date_debut
        if employe and date_debut:
            # Vérifie que la date de début est postérieure à la date de début de service
            if employe.dsb and date_debut <= employe.dsb:
                raise forms.ValidationError(
                    f"La date de début doit être postérieure à la date de début de service ({employe.dsb}) de l'employé."
                )

            # Vérifie qu'il n'y a pas de chevauchement avec la dernière mutation
            last_mutation = (
                CLMutation.objects
                .filter(employe=employe, organizational_unit=organizational_unit)
                .exclude(date_fin__isnull=True)
                .order_by('-date_fin')
                .first()
            )

            if last_mutation and date_debut <= last_mutation.date_fin:
                raise forms.ValidationError(
                    f"La date de début doit être postérieure à la dernière date de fin ({last_mutation.date_fin}) de mutation pour cette unité organisationnelle."
                )

        return cleaned_data
