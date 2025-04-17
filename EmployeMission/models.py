from django.db import models
from Employe.models import CLEmploye
from mission.models import CLMission

class CLEmployeMission(models.Model):
    STATUT_CHOICES = [
        ('Collaborateur', 'Collaborateur'),
        ('Chef de mission', 'Chef de mission'),
    ]

    mission = models.ForeignKey(CLMission, on_delete=models.CASCADE)
    employe = models.ForeignKey(CLEmploye, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)

    def __str__(self):
        return f"{self.employe} - {self.mission} ({self.statut})"
