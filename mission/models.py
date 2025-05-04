from django.db import models
from datetime import timedelta
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
        # Calculer la durée de la mission
        duree = (self.date_fin - self.date_debut).days if self.date_debut and self.date_fin else 0
        return f"{self.objet} - Début: {self.date_debut} ({duree} jours) - {self.lieu_mission}"
