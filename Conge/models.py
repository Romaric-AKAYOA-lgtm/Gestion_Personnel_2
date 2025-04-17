from django.db import models
from Employe.models import CLEmploye
from TypeConge.models import CLTypeConge

class CLConge(models.Model):
    employe = models.ForeignKey(CLEmploye, on_delete=models.CASCADE)
    typeconge = models.ForeignKey(CLTypeConge, on_delete=models.CASCADE)

    # Dates prévisionnelles
    date_debut_previsionnel = models.DateField(null=True, blank=True, help_text="Date prévisionnelle de début du congé")
    date_retour_previsionnel = models.DateField(null=True, blank=True, help_text="Date prévisionnelle de retour du congé")

    # Dates définitives
    date_retour_definitif = models.DateField(null=True, blank=True, help_text="Date définitive de retour du congé")

    # Signature de l'employé (champ booléen pour savoir si l'employé a signé)
    employe_signature = models.BooleanField(default=False, help_text="Indique si l'employé a signé le congé")

    def __str__(self):
        return f"{self.employe} - {self.typeconge.designation} ({self.date_debut_previsionnel} - {self.date_retour_previsionnel})"
