from .models import CLEmploye
from users.forms import ClUserForm

class ClEmployeForm(ClUserForm):
    class Meta:
        model = CLEmploye    
        fields = ClUserForm.Meta.fields + ['tstt']
        widgets = ClUserForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialiser 'tstt' à 'Employé (e)' si c’est une création
        if not self.instance.pk:
            self.fields['tstt'].initial = 'Employé (e)'
            self.fields['tstt'].widget.attrs['readonly'] = True  # Facultatif : pour empêcher la modification manuelle
