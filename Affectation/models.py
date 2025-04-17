from django.db import models
from Employe.models import CLEmploye

class CLAffectation(models.Model):
    STATUT_CHOICES = [
        ('Temporaire', 'Temporaire'),
        ('Définitif', 'Définitif'),
    ]

    employe = models.ForeignKey(CLEmploye, on_delete=models.CASCADE, related_name='affectations')
    organisme_affecte = models.CharField(max_length=50)
    lieu_affectation = models.CharField(max_length=50)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)
    motif_affectation = models.TextField()
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.employe.employe} - {self.organisme_affecte} ({self.statut})"
