from django.db import models
from Employe.models import CLEmploye

class CLMission(models.Model):
    employe_signataire = models.ForeignKey(
        CLEmploye, on_delete=models.CASCADE
    )
    objet = models.CharField(max_length=50)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    lieu_mission = models.CharField(max_length=50)
    organisme = models.CharField(max_length=50)
    conclusion_mission = models.TextField(null=True, blank=True)  # Added conclusion_mission field

    def __str__(self):
        return f"{self.objet} ({self.date_debut} à {self.date_fin}) - {self.lieu_mission}"
