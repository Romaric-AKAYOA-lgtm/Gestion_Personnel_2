from django.db import models

from Employe.models import CLEmploye
from OrganizationalUnit.models import OrganizationalUnit
from fonction.models import Fonction

# Create your models here.
class CLMutation (models.Model):
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)
    employe = models.ForeignKey(CLEmploye, on_delete=models.CASCADE)
    responsable = models.ForeignKey(
        CLEmploye,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mutation_responsable',  # Nouveau nom pour éviter le conflit
    )
    function = models.ForeignKey(Fonction, on_delete=models.CASCADE)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.employe} - {self.function} à {self.organizational_unit}"
