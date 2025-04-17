from .models import CLEmploye
from users.forms import ClUserForm


class ClEmployeForm(ClUserForm):
    class Meta:
        model = CLEmploye    
        fields = ClUserForm.Meta.fields + ['tstt']  # Ajouter le champ tstt
        widgets = ClUserForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        # Appel du constructeur de la classe parente (ClUserForm)
        super().__init__(*args, **kwargs)
        # Initialiser 'tstt' à 'directeur' par défaut si ce n'est pas déjà spécifié
        if not self.instance.pk and not self.instance.tstt:
            self.instance.tstt = 'Employé (e)'