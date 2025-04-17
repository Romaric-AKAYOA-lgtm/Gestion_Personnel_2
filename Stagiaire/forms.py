from Stagiaire.models import CLStagiaire
from users.forms import ClUserForm
from django.core.exceptions import ValidationError
from django.utils import timezone

class ClStagiaireForm(ClUserForm):
    class Meta:
        model = CLStagiaire
        # Inclure les champs hérités de ClUserForm et les champs spécifiques au modèle CLStagiaire
        fields = ClUserForm.Meta.fields + [
            'etablissement', 'theme', 'filiere', 'option', 'date_debut', 'date_fin', 
            'responsable', 'organisationUnit', 'tstt'
        ]
        widgets = ClUserForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        # Appel du constructeur de la classe parente (ClUserForm)
        super().__init__(*args, **kwargs)

        # Initialiser 'tstt' à 'Stagiaire' par défaut si ce n'est pas déjà spécifié
        if not self.instance.pk and not self.instance.tstt:
            self.instance.tstt = 'Stagiaire'  # Valeur par défaut pour le champ tstt

        # Définir la date de début par défaut à la date système
        if not self.instance.date_debut:
            self.instance.date_debut = timezone.now().date()

    def clean_responsable(self):
        responsable = self.cleaned_data.get('responsable')

        # Vérifier si le responsable est un retraité en vérifiant si la date de retraite est définie
        if responsable and responsable.date_retraite:  # Assurez-vous que vous avez ce champ dans votre modèle ClUser
            raise ValidationError("Le responsable ne peut pas être un retraité.")

        return responsable
