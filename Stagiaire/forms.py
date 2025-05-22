from django import forms
from django.core.exceptions import ValidationError
from Affectation.models import CLAffectation
from users.forms import ClUserForm
from Stagiaire.models import CLStagiaire
from datetime import date

class ClStagiaireForm(ClUserForm):
    class Meta:
        model = CLStagiaire
        fields = ClUserForm.Meta.fields + [
            'etablissement',
            'theme',
            'filiere',
            'option',
            'responsable',
            'organisationUnit',
            'tstt',
            'observation',
        ]
        widgets = ClUserForm.Meta.widgets
        widgets.update({
            'observation': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Saisir une observation du stagiaire',
                'class': 'form-control'
            }),
        })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialiser 'tstt' à 'Stagiaire' si c’est une création
        if not self.instance.pk:
            self.fields['tstt'].initial = 'Stagiaire'
            self.fields['tstt'].widget.attrs['readonly'] = True

        # Filtrer les responsables : date de retraite dépassée + user actif + ddf atteinte
        self.fields['responsable'].queryset = self.fields['responsable'].queryset.filter(
            tstt_user__is_active=True,
            ddf__lte=date.today()
        ).exclude(date_retraite__lte=date.today())

    def clean_responsable(self):
        responsable = self.cleaned_data.get('responsable')

        if responsable:
            date_retraite = getattr(responsable, 'date_retraite', None)
            ddf = getattr(responsable, 'ddf', None)
            tstt_user = getattr(responsable, 'tstt_user', None)

            if date_retraite and date_retraite <= date.today():
                raise ValidationError("Le responsable est déjà à la retraite.")

            if tstt_user and not tstt_user.is_active:
                raise ValidationError("Le responsable sélectionné n'est pas actif.")

            if ddf and ddf > date.today():
                raise ValidationError("Ce responsable n'est pas encore disponible (date de fin non atteinte).")

        return responsable
    
    def clean(self):
        cleaned_data = super().clean()
        responsable = cleaned_data.get('responsable')

        if responsable:
            # Vérifier si le responsable a une affectation définitive
            has_definitive = CLAffectation.objects.filter(
                employe=responsable,
                statut='Définitif'
            ).exists()

            if has_definitive:
                raise ValidationError("Le responsable sélectionné a déjà une affectation définitive.")

        return cleaned_data
